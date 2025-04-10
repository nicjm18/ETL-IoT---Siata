import streamlit as st
import folium
from streamlit_folium import folium_static
from etl.extractor import extraer_datos
from etl.transformer import limpiar_datos, agregar_niveles_de_riesgo, clasificar_riesgo_por_aqi
from etl.interpolator import interpolar_en_punto, generar_heatmap_data
from PIL import Image
from folium.plugins import HeatMap


URL = "https://siata.gov.co/EntregaData1/Datos_SIATA_Aire_AQ_pm25_Last.json"
LAT_U, LON_U = 6.241257, -75.590577  # Coordenadas de la universidad

st.set_page_config(page_title="Dashboard SIATA", layout="wide")

st.title("Sistema de Monitoreo Ambiental - SIATA")

with st.spinner("Cargando datos..."):
    df = extraer_datos(URL)
    df = limpiar_datos(df)
    df = agregar_niveles_de_riesgo(df)

# Mostrar resultados interpolados
aqi_u = interpolar_en_punto(df, LAT_U, LON_U)
nivel, accion = clasificar_riesgo_por_aqi(aqi_u)

st.subheader("🧠 Toma de decisión estimada para universidad UPB:")
st.metric(label="AQI estimado", value=f"{aqi_u}", help="Interpolado con vecinos más cercanos")
st.markdown(f"**Nivel de riesgo:** {nivel}")
st.markdown(f"**Recomendación:** {accion}")


st.subheader("📍 Mapa de estaciones SIATA")
m = folium.Map(location=[LAT_U, LON_U], zoom_start=11)

color_dict = {
    "Verde": "green",
    "Amarillo": "yellow",
    "Naranja": "orange",
    "Rojo": "red",
    "Púrpura": "purple",
    "Marrón": "maroon"
}

for _, row in df.iterrows():
    color = color_dict.get(row['nivel_riesgo'], 'gray')
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=7,
        popup=f"{row['location']}<br>AQI: {row['aqi']}<br>PM2.5: {row['pm25']}",
        color=color,
        fill=True
    ).add_to(m)

folium_static(m)

# Mapa de calor interpolado
st.subheader("🌡️ Mapa de calor interpolado de AQI en Medellín")

heat_data = generar_heatmap_data(df, grid_res=100)

m2 = folium.Map(location=[LAT_U, LON_U], zoom_start=11)

folium.plugins.HeatMap(
    heat_data,
    radius=12,
    blur=18,
    max_zoom=13,
    min_opacity=0.4
).add_to(m2)

folium_static(m2)


st.subheader("📊 Tabla de referencia AQI y PM2.5")
image = Image.open("cuadro-pm2.5.webp")
st.image(image, caption="Fuente: https://www.purioperu.com/como-se-miden-los-niveles-de-pm-2-5/", width=800)


