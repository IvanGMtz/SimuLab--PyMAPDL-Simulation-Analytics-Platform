<!-- BANNER -->
<div align="center">
  <img src="./static/images/PyMAPDL.png" alt="ParametricFEA Banner" width="80%" />

  <h1>⚙️ ParametricFEA — Análisis Estructural Paramétrico con PyAnsys</h1>

  <p>
    <strong>Simulaciones de elementos finitos accionadas por Python, con interfaz web interactiva.</strong><br/>
    Configura, ejecuta y visualiza análisis estructurales en tiempo real — sin tocar líneas de comando.
  </p>

  <p>
    <a href="#-instalación">Instalación rápida</a> ·
    <a href="#-ejemplo-de-uso">Ver ejemplo</a> ·
    <a href="#-características">Características</a> ·
    <a href="https://docs.pyansys.com/">Documentación PyAnsys</a>
  </p>

  <br/>

  [![pyansys](https://img.shields.io/badge/Py-Ansys-ffc107.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABDklEQVQ4jWNgoDfg5mD8vE7q/3bpVyskbW0sMRUwofHD7Dh5OBkZGBgW7/3W2tZpa2tLQEOyOzeEsfumlK2tbVpaGj4N6jIs1lpsDAwMJ278sveMY2BgCA0NFRISwqkhyQ1q/Nyd3zg4OBgYGNjZ2ePi4rB5loGBhZnhxTLJ/9ulv26Q4uVk1NXV/f///////69du4Zdg78lx//t0v+3S88rFISInD59GqIH2esIJ8G9O2/XVwhjzpw5EAam1xkkBJn/bJX+v1365hxxuCAfH9+3b9/+////48cPuNehNsS7cDEzMTAwMMzb+Q2u4dOnT2vWrMHu9ZtzxP9vl/69RVpCkBlZ3N7enoDXBwEAAA+YYitOilMVAAAAAElFTkSuQmCC)](https://docs.pyansys.com/)
  [![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://www.python.org/)
  [![Flask](https://img.shields.io/badge/Flask-Web%20App-lightgrey?logo=flask)](https://flask.palletsprojects.com/)
  [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
</div>

---

## 🚀 ¿Qué es ParametricFEA?

**ParametricFEA** es una plataforma de análisis estructural que combina la potencia del solver **ANSYS Mechanical APDL** con la flexibilidad de Python y una interfaz web construida con Flask.

Diseñado para ingenieros mecánicos, investigadores y desarrolladores que necesitan:
- Automatizar simulaciones FEA repetitivas con parámetros variables.
- Integrar análisis estructural en flujos de trabajo basados en Python.
- Explorar resultados de forma visual e interactiva desde el navegador.

> **¿Por qué PyMAPDL?** Porque traduce el poder de ANSYS a código Python reutilizable, versionable y fácilmente integrable en pipelines de ingeniería o ciencia de datos.

---

## ✨ Características

| Característica | Descripción |
|---|---|
| 🔁 **Simulación paramétrica** | Define rangos de parámetros (cargas, geometría, material) y ejecuta múltiples análisis automáticamente |
| 🌐 **Interfaz web interactiva** | Formularios web para configurar y lanzar simulaciones sin escribir código |
| 📊 **Postprocesamiento automático** | Visualización de tensiones, deformaciones y factores de seguridad al finalizar cada análisis |
| 🐍 **API Python nativa** | Acceso programático completo a todos los parámetros del modelo via PyMAPDL |
| 📈 **Gráficos exportables** | Resultados exportables como imágenes y datos tabulares (CSV/Excel) via Matplotlib y Pandas |
| ⚡ **Integración DPF** | Postprocesamiento de alta performance con PyDPF para modelos de gran escala |

---

## 📦 Librerías Utilizadas

- **[PyMAPDL](https://mapdl.docs.pyansys.com/)** — Interacción con ANSYS Mechanical APDL: definición de modelo, condiciones de contorno, resolución y extracción de resultados.
- **[PyDPF](https://dpf.docs.pyansys.com/)** — Postprocesamiento y visualización avanzada de resultados de simulación.
- **[Flask](https://flask.palletsprojects.com/)** — Framework web ligero para la interfaz gráfica del usuario.
- **[NumPy](https://numpy.org/)** — Cálculo numérico vectorizado.
- **[Matplotlib](https://matplotlib.org/)** — Generación de gráficos estáticos de resultados.
- **[Pandas](https://pandas.pydata.org/)** — Manipulación y exportación de datos en postprocesamiento.

---

## 🛠️ Instalación

> **Requisito previo:** Tener una licencia activa de ANSYS Mechanical APDL instalada localmente o accesible en red.
```bash
# 1. Clona el repositorio
git clone https://github.com/tu-usuario/parametricfea.git
cd parametricfea

# 2. (Recomendado) Crea un entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instala las dependencias
pip install ansys-mapdl-core ansys-dpf-core flask numpy matplotlib pandas

# 4. Inicia la aplicación
python app.py
```

La aplicación estará disponible en **`http://localhost:5000`** 🎉

---

## 🔬 Ejemplo de Uso

### Análisis de una viga simplemente apoyada bajo carga distribuida variable

Supongamos que queremos estudiar cómo varía la deflexión máxima de una viga de acero al cambiar la magnitud de una carga distribuida entre 1 kN/m y 10 kN/m.

**Desde la interfaz web:**

1. Navega a `http://localhost:5000`
2. Selecciona el tipo de análisis: `Estático Lineal`
3. Ingresa los parámetros de la viga (longitud, sección, material)
4. Define el rango de carga: `q_min = 1000`, `q_max = 10000`, `pasos = 10`
5. Haz clic en **"Ejecutar Simulación"**
6. Visualiza el mapa de deformaciones y la curva carga-deflexión directamente en el navegador

**O directamente desde Python:**
```python
from src.simulation import run_beam_analysis

results = run_beam_analysis(
    length=2.0,          # metros
    load_range=(1000, 10000),  # N/m
    steps=10,
    material="steel"
)

results.plot_deflection()
results.export_csv("resultados_viga.csv")
```

---

## 📁 Estructura del Proyecto
```
parametricfea/
├── app.py                  # Punto de entrada Flask
├── src/
│   ├── simulation.py       # Lógica principal de PyMAPDL
│   ├── postprocessing.py   # Extracción y procesamiento de resultados (DPF)
│   └── utils.py            # Funciones auxiliares
├── static/
│   ├── images/             # Assets visuales
│   └── css/                # Estilos de la interfaz
├── templates/              # Plantillas HTML (Jinja2)
├── tests/                  # Pruebas unitarias
├── requirements.txt
└── README.md
```

> ⚠️ Ajusta los paths según la estructura real de tu proyecto.

---

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si quieres mejorar ParametricFEA:

1. Haz un **fork** del repositorio
2. Crea una rama para tu feature: `git checkout -b feature/nueva-funcionalidad`
3. Realiza tus cambios y haz commit: `git commit -m 'feat: descripción del cambio'`
4. Abre un **Pull Request** describiendo qué cambiaste y por qué

Para bugs o ideas, abre un [Issue](https://github.com/tu-usuario/parametricfea/issues).

---

## 📄 Licencia

Distribuido bajo la licencia **MIT**. Consulta el archivo [LICENSE](LICENSE) para más información.

---

## 🙏 Agradecimientos

- [ANSYS / PyAnsys](https://docs.pyansys.com/) por democratizar el acceso a simulaciones de alto nivel mediante Python.
- La comunidad open-source de ingeniería computacional que hace posible este tipo de herramientas.

---

<div align="center">
  <sub>Construido con 🔩 por ingenieros, para ingenieros.</sub>
</div>
