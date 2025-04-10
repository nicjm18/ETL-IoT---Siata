from geopy.distance import geodesic
import numpy as np
from scipy.interpolate import griddata

def interpolar_en_punto(df, lat_u, lon_u, k=3):
    df['distancia_km'] = df.apply(lambda row: geodesic((lat_u, lon_u), (row['lat'], row['lon'])).km, axis=1)
    vecinos = df.nsmallest(k, 'distancia_km')
    pesos = 1 / vecinos['distancia_km']
    pm25_interp = np.sum(vecinos['pm25'] * pesos) / np.sum(pesos)
    return round(pm25_interp)

def generar_heatmap_data(df, grid_res=100):
    # Área aproximada de Medellín
    lat_min, lat_max = 6.15, 6.38
    lon_min, lon_max = -75.65, -75.45

    lats = np.linspace(lat_min, lat_max, grid_res)
    lons = np.linspace(lon_min, lon_max, grid_res)
    lon_grid, lat_grid = np.meshgrid(lons, lats)

    # Interpolación usando coordenadas y AQI
    points = df[['lat', 'lon']].values
    values = df['aqi'].values
    aqi_grid = griddata(points, values, (lat_grid, lon_grid), method='cubic')

    # Convertir a formato para folium HeatMap
    heat_data = []
    for i in range(len(lats)):
        for j in range(len(lons)):
            if not np.isnan(aqi_grid[i][j]):
                heat_data.append([lats[i], lons[j], float(aqi_grid[i][j])])
    
    return heat_data
