Reconocimiento de Cartas de la Baraja Española y Recomendación de Estrategias para el Mus

Este proyecto implementa un sistema de visión por computadora para reconocer cartas de la baraja española y calcular probabilidades estratégicas para el juego de Mus. El sistema utiliza una Raspberry Pi con una cámara, OpenCV y Tesseract OCR para procesar imágenes en tiempo real.

Características del Proyecto

Reconocimiento de Cartas:
Detección y segmentación de cartas utilizando procesamiento de imágenes.
Reconocimiento de los valores de las cartas mediante OCR.
Cálculo de Estrategias:
Simulación de partidas para calcular probabilidades de ganar en las categorías de grande, chica, par y juego.
Visualización en Tiempo Real:
Mostrando FPS, cartas detectadas y probabilidades en la pantalla.
Requisitos

Hardware
Raspberry Pi 4
Cámara compatible (120º FOV recomendado)
Software
Python 3.9+
Bibliotecas:
opencv-python
numpy
pytesseract
imageio
Instrucciones de Uso

Clonar el Repositorio:
git clone https://github.com/tu-usuario/reconocimiento-cartas-mus.git
cd reconocimiento-cartas-mus
Instalar Dependencias:
pip install -r requirements.txt
Ejecutar el Sistema: Asegúrate de que la cámara está conectada a la Raspberry Pi y ejecuta:
python main.py
Estructura del Proyecto

reconocimiento-cartas-mus/
├── calibration/         # Código y datos para calibración de la cámara
├── data/                # Imágenes de entrada
├── data_processed/      # Imágenes procesadas (salidas intermedias)
├── main.py              # Archivo principal para detección en tiempo real
├── README.md            # Este archivo
└── requirements.txt     # Dependencias del proyecto
Calibración de la Cámara

El sistema utiliza un patrón de tablero de ajedrez para calibrar la cámara y corregir distorsiones. Los resultados incluyen:

Matriz intrínseca
Coeficientes de distorsión
RMS (error de reproyección)

Licencia

Este proyecto está licenciado bajo la MIT License.
