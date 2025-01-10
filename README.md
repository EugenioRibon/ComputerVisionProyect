# **Reconocimiento de Cartas de la Baraja Española y Recomendación de Estrategias para el Mus**

Este proyecto implementa un sistema de visión por computadora para reconocer cartas de la baraja española y calcular probabilidades estratégicas para el juego de Mus. El sistema utiliza una Raspberry Pi con una cámara, OpenCV y Tesseract OCR para procesar imágenes en tiempo real.

---

## **Características del Proyecto**

- **Reconocimiento de Cartas:**
  - Detección y segmentación de cartas utilizando procesamiento de imágenes.
  - Reconocimiento de los valores de las cartas mediante OCR.
- **Cálculo de Estrategias:**
  - Simulación de partidas para calcular probabilidades de ganar en las categorías de grande, chica, par y juego.
- **Visualización en Tiempo Real:**
  - Mostrando FPS, cartas detectadas y probabilidades en la pantalla.

---

## **Requisitos**

### **Hardware**
- Raspberry Pi 4
- Cámara compatible (120º FOV recomendado)

### **Software**
- Python 3.9+
- Bibliotecas:
  - `opencv-python`
  - `numpy`
  - `pytesseract`
  - `imageio`

---

## **Instrucciones de Uso**

1. **Clonar el Repositorio:**
   ```bash
   git clone https://github.com/tu-usuario/reconocimiento-cartas-mus.git
   cd reconocimiento-cartas-mus

