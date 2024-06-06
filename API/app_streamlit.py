import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import folium_static
from geopy.distance import geodesic, great_circle
from geopy.point import Point
import math

st.title('Sistema de Navegação Otimizada')

# Coordenadas de Teste: EUA e Noruega
start_lat = st.number_input('Latitude Inicial', value=33.7366)
start_lon = st.number_input('Longitude Inicial', value=-118.2626)
end_lat = st.number_input('Latitude Final', value=59.9111)
end_lon = st.number_input('Longitude Final', value=10.7528)
year = st.number_input('Ano', value=2023)
month = st.number_input('Mês', value=6)
day = st.number_input('Dia', value=1)
vgs = st.number_input('Velocidade da Corrente de Superfície (vgs)', value=3.0)
ugs = st.number_input('Velocidade da Corrente Subaquática (ugs)', value=1.5)

def predict_current(lat, lon, target_lat, target_lon, year, month, day, vgs, ugs):
    data = {
        'lat': lat,
        'lon': lon,
        'target_lat': target_lat,
        'target_lon': target_lon,
        'vgs': vgs,
        'ugs': ugs,
        'year': year,
        'month': month,
        'day': day
    }
    response = requests.post('http://localhost:5000/predict', json=data)
    print("Resposta da API:", response.text)  # Log da resposta da API
    
    try:
        response.raise_for_status()  # Levanta uma exceção para códigos de status HTTP 4xx/5xx
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        st.error(f"Error occurred: {err}")
    except ValueError as json_err:
        st.error(f"JSON decode error: {json_err}")
        st.write("Resposta recebida da API:", response.text)  # Mostrar a resposta que causou o erro

def generate_marine_waypoints(start_lat, start_lon, end_lat, end_lon):
    # Definindo pontos de controle intermediários manualmente para garantir que a rota permaneça no mar
    waypoints = [
        (34.0, -119.0),  # Ao norte de Los Angeles
        (40.0, -130.0),  # Oeste da Califórnia
        (45.0, -150.0),  # Sul do Alasca
        (60.0, -170.0),  # Sudeste do Alasca
        (70.0, -160.0),  # Mar de Bering
        (80.0, -10.0),   # Mar de Noruega
    ]
    return waypoints

if st.button('Otimizar Rota'):
    original_route = [(start_lat, start_lon)] + generate_marine_waypoints(start_lat, start_lon, end_lat, end_lon) + [(end_lat, end_lon)]
    optimized_route = []

    current_position = (start_lat, start_lon)
    
    for waypoint in generate_marine_waypoints(start_lat, start_lon, end_lat, end_lon):
        prediction = predict_current(current_position[0], current_position[1], waypoint[0], waypoint[1], year, month, day, vgs, ugs)
        if prediction:
            # Ajustar a previsão de forma realista, sem deslocamentos drásticos
            lat_adjustment = min(max(prediction['prediction'] * 0.01, -0.1), 0.1)
            lon_adjustment = min(max(prediction['prediction'] * 0.01, -0.1), 0.1)
            adjusted_waypoint = (waypoint[0] + lat_adjustment, waypoint[1] + lon_adjustment)
            optimized_route.append(adjusted_waypoint)
            current_position = adjusted_waypoint

    optimized_route.append((end_lat, end_lon))

    st.write('Rota Original:')
    for point in original_route:
        st.write(f'Latitude: {point[0]}, Longitude: {point[1]}')

    st.write('Rota Otimizada:')
    for point in optimized_route:
        st.write(f'Latitude: {point[0]}, Longitude: {point[1]}')

    # Criar o mapa
    m = folium.Map(location=[(start_lat + end_lat) / 2, (start_lon + end_lon) / 2], zoom_start=3)

    # Adicionar marcadores para cada ponto na rota original
    for point in original_route:
        folium.Marker(location=point, popup=f'Lat: {point[0]}, Lon: {point[1]}', icon=folium.Icon(color='red')).add_to(m)

    # Adicionar marcadores para cada ponto na rota otimizada
    for point in optimized_route:
        folium.Marker(location=point, popup=f'Lat: {point[0]}, Lon: {point[1]}', icon=folium.Icon(color='blue')).add_to(m)

    # Adicionar a rota original ao mapa
    folium.PolyLine(original_route, color="red", weight=2.5, opacity=1).add_to(m)

    # Adicionar a rota otimizada ao mapa
    folium.PolyLine(optimized_route, color="blue", weight=2.5, opacity=1).add_to(m)

    # Exibir o mapa
    folium_static(m)
