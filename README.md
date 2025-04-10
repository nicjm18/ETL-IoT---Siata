# 🛰️ ETL IoT - SIATA Air Quality Dashboard

Este proyecto corresponde al desarrollo de un sistema ETL con visualización georreferenciada para datos de calidad del aire, como parte del curso **Internet de las Cosas (IoT)**. Se construyó un dashboard usando **Python, Streamlit, Docker y datos abiertos del SIATA**, y fue desplegado en una instancia EC2 de AWS.

---

## 🧠 Descripción del proyecto

El sistema realiza:

- 📥 **Extracción** de datos JSON desde SIATA (PM2.5).
- 🧼 **Transformación**: limpieza de datos, cálculo del índice **AQI**.
- 📊 **Carga y visualización**:
  - Mapa de estaciones con niveles AQI por zona.
  - Interpolación de AQI en zonas de interés.
  - Mapa de calor interpolado sobre Medellín.
  - Recomendaciones según el nivel de riesgo.

---

## 📌 Tecnologías utilizadas

- **Python 3.10**
- **Streamlit**
- **Folium + Streamlit-Folium**
- **NumPy / Pandas / SciPy / Scikit-learn**
- **Docker**
- **AWS EC2 (Ubuntu 22.04)**

---

## 🚀 Cómo ejecutar el proyecto

### 🔧 Requisitos

- Python 3.10+
- Docker (opcional para contenerización)

### 🛠️ Instalación local

```bash
git clone https://github.com/nicjm18/ETL-IoT---Siata.git
cd ETL-IoT---Siata

python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

pip install -r requirements.txt
streamlit run app.py

```

### 🚀 Ejecución del Proyecto Usando Docker

Este proyecto ha sido contenerizado completamente usando Docker

---

## 🐳 Paso 1: Clonar el repositorio

```bash
git clone https://github.com/nicjm18/ETL-IoT---Siata.git
cd ETL-IoT---Siata

docker build -t siata-dashboard .
docker run -d -p 8501:8501 siata-dashboard

