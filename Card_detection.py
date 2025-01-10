import cv2
import numpy as np
import pytesseract
import threading
from statistics import mode
import random
import time

pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'


card_values = [[] for _ in range(4)]  
all_card_sets = []  


fps = 30  
frame_width, frame_height = 1920, 1080  


detected_numbers = []
detected_positions = []


current_probabilities = None


output_filename = "output.mp4"
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
out = cv2.VideoWriter(output_filename, fourcc, fps, (frame_width, frame_height))

def calcular_probabilidades_simulacion(mano, num_simulaciones=10000):

    mano = [10 if carta > 10 else carta for carta in mano]
    conteos = {"Grande": 0, "Chica": 0, "Par": 0, "Juego": 0}

    for _ in range(num_simulaciones):
        mano_rival = [random.randint(1, 12) for _ in range(4)]
        mano_rival = [10 if carta > 10 else carta for carta in mano_rival]

        if sum(mano) > sum(mano_rival):
            conteos["Grande"] += 1
        if sum(mano) < sum(mano_rival):
            conteos["Chica"] += 1
        par_mano = len(set(mano)) < 4
        par_rival = len(set(mano_rival)) < 4
        if par_mano and not par_rival:
            conteos["Par"] += 1
        elif par_mano and par_rival:
            if max([mano.count(c) for c in set(mano)]) > max([mano_rival.count(c) for c in set(mano_rival)]):
                conteos["Par"] += 1
        juego_mano = sum(mano) >= 31
        juego_rival = sum(mano_rival) >= 31
        if juego_mano and not juego_rival:
            conteos["Juego"] += 1
        elif juego_mano and juego_rival:
            if sum(mano) > sum(mano_rival):
                conteos["Juego"] += 1

    probabilidades = {clave: conteos[clave] / num_simulaciones for clave in conteos}
    return probabilidades


def detect_number(roi, index):
    global card_values
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    gray_roi = cv2.GaussianBlur(gray_roi, (5, 5), 0)
    _, binary_roi = cv2.threshold(gray_roi, 150, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    detected_text = pytesseract.image_to_string(binary_roi, config='--psm 6 digits')
    numbers = ''.join(filter(str.isdigit, detected_text))
    
    if numbers:
        card_values[index].append(numbers)


def draw_bounding_box(frame, mask):
    global card_values, all_card_sets, detected_numbers, detected_positions, current_probabilities
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    min_area = 5000
    card_count = 0
    warps = []
    card_positions = []

    for contour in contours:
        if cv2.contourArea(contour) < min_area:
            continue
        
        epsilon = 0.01 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        if len(approx) == 4:
            card_count += 1
            cv2.drawContours(frame, [approx], -1, (0, 255, 0), 2)
            for point in approx:
                cv2.circle(frame, tuple(point[0]), 5, (0, 0, 255), -1)
            
            width, height = 300, 400
            pts1 = np.float32([point[0] for point in approx])
            pts1 = pts1[np.argsort(pts1[:, 1])]
            
            if pts1[0][0] > pts1[1][0]:
                pts1[[0, 1]] = pts1[[1, 0]]
            if pts1[2][0] < pts1[3][0]:
                pts1[[2, 3]] = pts1[[3, 2]]

            pts2 = np.float32([[0, 0], [width, 0], [width, height], [0, height]])
            matrix = cv2.getPerspectiveTransform(pts1, pts2)
            warp = cv2.warpPerspective(frame, matrix, (width, height))
            warps.append(warp)
            card_positions.append(tuple(approx[0][0]))

    detected_values = []

    if card_count == 4:
        threads = []
        for i, warp in enumerate(warps):
            x1, y1, x2, y2 = 27, 23, 60, 45
            roi_corner = warp[y1:y2, x1:x2]
            t = threading.Thread(target=detect_number, args=(roi_corner, i))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        if all(len(vals) >= 3 for vals in card_values):
            final_values = [mode(vals) for vals in card_values]
            detected_values = final_values
            detected_numbers = detected_values
            detected_positions = card_positions
            all_card_sets.append(final_values)
            card_values = [[] for _ in range(4)]
            
            # Calcular probabilidades
            current_probabilities = calcular_probabilidades_simulacion([int(x) for x in final_values])

        if len(all_card_sets) == 5:
            print(f'5 listas de cartas detectadas: {all_card_sets}')
            all_card_sets = []

# Máscara para segmentar las cartas
def mask_cards_threshold(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    return frame, mask

# Captura de video y análisis en vivo
def segment_cards_live():
    global fps, detected_numbers, detected_positions, current_probabilities
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
    
    prev_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        _, mask = mask_cards_threshold(frame)
        draw_bounding_box(frame, mask)
        
        # Mostrar números detectados almacenados
        for pos, num in zip(detected_positions, detected_numbers):
            cv2.putText(frame, num, pos, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Mostrar probabilidades
        if current_probabilities:
            prob_text = "Probabilidades: "
            for key, value in current_probabilities.items():
                prob_text += f"{key}: {value:.2f} "
            cv2.putText(frame, prob_text, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        # Calcular FPS
        curr_time = time.time()
        fps = int(1 / (curr_time - prev_time))
        prev_time = curr_time

        # Mostrar FPS en la esquina superior izquierda
        cv2.putText(frame, f'FPS: {fps}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        
        # Guardar en archivo de salida
        out.write(frame)
        
        cv2.imshow('Detección en Vivo', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    
    cap.release()
    out.release()
    cv2.destroyAllWindows()

segment_cards_live()
