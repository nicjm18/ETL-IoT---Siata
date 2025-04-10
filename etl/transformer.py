import pandas as pd

def limpiar_datos(df):
    df = df[df['value'] >= 0].copy()
    df.rename(columns={
        'value': 'pm25',
        'date.utc': 'fecha_utc',
        'date.local': 'fecha_local',
        'coordinates.latitude': 'lat',
        'coordinates.longitude': 'lon'
    }, inplace=True)
    return df

def calcular_aqi_pm25(concentracion):
    breakpoints = [
        (0.0, 12.0, 0, 50),
        (12.1, 35.4, 51, 100),
        (35.5, 55.4, 101, 150),
        (55.5, 150.4, 151, 200),
        (150.5, 250.4, 201, 300),
        (250.5, 500.4, 301, 500)
    ]
    
    for C_low, C_high, I_low, I_high in breakpoints:
        if C_low <= concentracion <= C_high:
            aqi = (I_high - I_low) / (C_high - C_low) * (concentracion - C_low) + I_low
            return round(aqi)
    return None  # fuera de rango

def clasificar_riesgo_por_aqi(aqi):
    if aqi <= 50:
        return "Verde", "Aire bueno - Sin recomendaciones"
    elif aqi <= 100:
        return "Amarillo", "Moderado - personas sensibles, precaución"
    elif aqi <= 150:
        return "Naranja", "Dañino para grupos sensibles"
    elif aqi <= 200:
        return "Rojo", "Dañino - Evite exposición prolongada"
    elif aqi <= 300:
        return "Púrpura", "Muy dañino - Alertas de salud"
    else:
        return "Marrón", "Peligroso - Emergencia sanitaria"

def agregar_niveles_de_riesgo(df):
    df['aqi'] = df['pm25'].apply(calcular_aqi_pm25)
    df[['nivel_riesgo', 'accion']] = df['aqi'].apply(lambda x: pd.Series(clasificar_riesgo_por_aqi(x)))
    return df
