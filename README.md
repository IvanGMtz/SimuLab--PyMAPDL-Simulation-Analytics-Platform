# Análisis de Estructuras con PyMAPDL

<img src="./static/images/PyMAPDL.png" alt="iconName" width="70%" />

Este proyecto demuestra el uso de PyAnsys para analizar estructuras específicas mediante simulaciones de elementos finitos. Utilizamos PyMAPDL para configurar y resolver problemas de análisis estructural.

## Librerías Utilizadas

- **PyMAPDL**: Para la interacción con ANSYS Mechanical APDL, configuración de simulaciones, y ejecución de análisis de elementos finitos.
- **PyDPF**: Para el postprocesamiento y visualización de los resultados de las simulaciones.
- **Flask**: Para crear una aplicación web que permite interactuar con las simulaciones de PyMAPDL de forma gráfica.
- **NumPy**: Para el manejo de cálculos numéricos.
- **Matplotlib**: Para la generación de gráficos estáticos de los resultados.
- **Pandas**: Utilizado ocasionalmente para manipulación de datos en el postprocesamiento.

## Instalación

Para instalar este proyecto, sigue los siguientes pasos:

1. Clona este repositorio en tu máquina local.

2. Asegúrate de tener Python instalado. Este proyecto es compatible con Python 3.8+.

3. Instala las dependencias ejecutando:

   ```bash
   pip install ansys-mapdl-core flask numpy matplotlib pandas
   ```

4. Navega al directorio del proyecto y ejecuta la aplicación Flask con:

   ```bash
   python app.py
   ```

Esto levantará el servidor local y la aplicación estará disponible en `http://localhost:5000`.

## Ejecución

Una vez instalado y ejecutando el servidor Flask, puedes acceder a la aplicación web desde un navegador para ejecutar simulaciones y ver resultados. La interfaz web proporciona formularios para ingresar los parámetros de las simulaciones y visualizar los resultados directamente en el navegador.

## Agradecimientos

Agradecemos a [ANSYS](https://docs.pyansys.com/) por proporcionar las herramientas que hacen posible este análisis, y especialmente por su biblioteca PyAnsys que facilita la interacción con software de simulación de alto nivel a través de Python.

[![pyansys](https://img.shields.io/badge/Py-Ansys-ffc107.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABDklEQVQ4jWNgoDfg5mD8vE7q/3bpVyskbW0sMRUwofHD7Dh5OBkZGBgW7/3W2tZpa2tLQEOyOzeEsfumlK2tbVpaGj4N6jIs1lpsDAwMJ278sveMY2BgCA0NFRISwqkhyQ1q/Nyd3zg4OBgYGNjZ2ePi4rB5loGBhZnhxTLJ/9ulv26Q4uVk1NXV/f///////69du4Zdg78lx//t0v+3S88rFISInD59GqIH2esIJ8G9O2/XVwhjzpw5EAam1xkkBJn/bJX+v1365hxxuCAfH9+3b9/+////48cPuNehNsS7cDEzMTAwMMzb+Q2u4dOnT2vWrMHu9ZtzxP9vl/69RVpCkBlZ3N7enoDXBwEAAA+YYitOilMVAAAAAElFTkSuQmCC)](https://docs.pyansys.com/)