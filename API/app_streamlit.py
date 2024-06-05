import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import folium_static

st.title('Sistema de Navegação Otimizada')

start_lat = st.number_input('Latitude Inicial', value=34.0)
start_lon = st.number_input('Longitude Inicial', value=-118.0)
end_lat = st.number_input('Latitude Final', value=35.0)
end_lon = st.number_input('Longitude Final', value=-120.0)

def predict_current(lat, lon, target_lat, target_lon):
    data = {
        'lat': lat,
        'lon': lon,
        'target_lat': target_lat,
        'target_lon': target_lon,
        'vgs': 0,  # Placeholder values for vgs and ugs
        'ugs': 0
    }
    response = requests.post('http://localhost:5000/predict', json=data)
    return response.json()

if st.button('Otimizar Rota'):
    # Simulação de pontos intermediários para a rota
    waypoints = [(start_lat + (end_lat - start_lat) * i / 10, start_lon + (end_lon - start_lon) * i / 10) for i in range(1, 10)]
    
    route = []
    current_position = (start_lat, start_lon)
    
    for waypoint in waypoints:
        prediction = predict_current(current_position[0], current_position[1], waypoint[0], waypoint[1])
        adjusted_waypoint = (waypoint[0] + prediction['prediction'], waypoint[1] + prediction['prediction'])
        route.append(adjusted_waypoint)
        current_position = adjusted_waypoint

    route.append((end_lat, end_lon))

    st.write('Rota Otimizada:')
    for point in route:
        st.write(f'Latitude: {point[0]}, Longitude: {point[1]}')

    # Criar o mapa
    m = folium.Map(location=[(start_lat + end_lat) / 2, (start_lon + end_lon) / 2], zoom_start=6)

    # Adicionar marcadores para cada ponto na rota
    for point in route:
        folium.Marker(location=point, popup=f'Lat: {point[0]}, Lon: {point[1]}').add_to(m)

    # Adicionar a rota ao mapa
    folium.PolyLine(route, color="blue", weight=2.5, opacity=1).add_to(m)

    # Exibir o mapa
    folium_static(m)