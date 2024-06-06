import geopandas as gpd
from geopy.point import Point

# Carregar os dados de polígonos de terra
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
land = world(world['geometry'].type == 'Polygon')

def is_on_land(lat, lon):
    point = Point(lon, lat)
    return land.contains(point).any()

def generate_marine_waypoints(start_lat, start_lon, end_lat, end_lon, num_points=10):
    # Gera pontos intermediários automaticamente
    waypoints = []
    lat_diff = (end_lat - start_lat) / num_points
    lon_diff = (end_lon - start_lon) / num_points

    for i in range(1, num_points):
        lat = start_lat + i * lat_diff
        lon = start_lon + i * lon_diff
        # Garantir que os valores estão dentro dos limites válidos
        lat = max(min(lat, 90), -90)
        lon = max(min(lon, 180), -180)
        print(f"Waypoint gerado: lat={lat}, lon={lon}")
        if not is_on_land(lat, lon):
            waypoints.append((lat, lon))
    
    return waypoints

# Coordenadas de Teste
start_lat = 33.7366
start_lon = -118.2626
end_lat = 59.9111
end_lon = 10.7528

waypoints = generate_marine_waypoints(start_lat, start_lon, end_lat, end_lon)
print("Waypoints:", waypoints)
