import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, LineString
import networkx as nx

class SistemaTransporte:
    def __init__(self):
        self.grafo = nx.Graph()
        self.estaciones = {
            "Nombre": ["Portal Norte", "Calle 100", "Héroes", "Calle 72", "Calle 45", "Universidades",
                       "Portal Sur", "General Santander", "Venecia", "Banderas", "Kennedy", "Américas"],
            "Latitud": [4.7528, 4.6768, 4.6686, 4.6582, 4.6455, 4.6019,
                        4.5953, 4.6097, 4.6164, 4.6265, 4.6333, 4.6354],
            "Longitud": [-74.0455, -74.0565, -74.0597, -74.0648, -74.0681, -74.0663,
                         -74.1362, -74.1257, -74.1228, -74.1135, -74.1066, -74.0977]
        }
        self.gdf_estaciones = gpd.GeoDataFrame(
            self.estaciones,
            geometry=gpd.points_from_xy(self.estaciones["Longitud"], self.estaciones["Latitud"]),
            crs="EPSG:4326"
        )
        self._definir_conexiones()

    def _definir_conexiones(self):
        rutas = [
            ["Portal Norte", "Calle 100", "Héroes", "Calle 72", "Calle 45", "Universidades"],
            ["Portal Sur", "General Santander", "Venecia", "Banderas", "Kennedy", "Américas"]
        ]
        for ruta in rutas:
            for i in range(len(ruta)-1):
                estacion_a = ruta[i]
                estacion_b = ruta[i+1]
                coord_a = self._obtener_coordenadas(estacion_a)
                coord_b = self._obtener_coordenadas(estacion_b)
                distancia = self._calcular_distancia(coord_a, coord_b)
                self.grafo.add_edge(
                    estacion_a,
                    estacion_b,
                    distancia=distancia,
                    tiempo=distancia*1.5,
                    linea=ruta[0]
                )
        estacion_a = "Américas"
        estacion_b = "Calle 45"
        coord_a = self._obtener_coordenadas(estacion_a)
        coord_b = self._obtener_coordenadas(estacion_b)
        distancia = self._calcular_distancia(coord_a, coord_b)
        self.grafo.add_edge(
            estacion_a,
            estacion_b,
            distancia=distancia,
            tiempo=distancia*2.0,
            linea="Interconexión"
        )

    def _obtener_coordenadas(self, nombre_estacion):
        idx = self.estaciones["Nombre"].index(nombre_estacion)
        return (self.estaciones["Longitud"][idx], self.estaciones["Latitud"][idx])

    def _calcular_distancia(self, coord_a, coord_b):
        return ((coord_a[0]-coord_b[0])**2 + (coord_a[1]-coord_b[1])**2)**0.5

    def encontrar_mejor_ruta(self, inicio, fin, criterio="tiempo"):
        if criterio == "tiempo":
            return nx.shortest_path(self.grafo, inicio, fin, weight="tiempo")
        elif criterio == "distancia":
            return nx.shortest_path(self.grafo, inicio, fin, weight="distancia")
        elif criterio == "trasbordos":
            return nx.shortest_path(self.grafo, inicio, fin)
        else:
            raise ValueError("Criterio no válido")

    def visualizar_ruta(self, ruta):
        geometrias = []
        for estacion in ruta:
            idx = self.estaciones["Nombre"].index(estacion)
            punto = Point(self.estaciones["Longitud"][idx], self.estaciones["Latitud"][idx])
            geometrias.append(punto)
        linea_ruta = LineString(geometrias)
        rutas_general = [
            LineString(self.gdf_estaciones.iloc[0:6].geometry),
            LineString(self.gdf_estaciones.iloc[6:].geometry),
            LineString([
                self.gdf_estaciones.iloc[11].geometry,
                self.gdf_estaciones.iloc[4].geometry
            ])
        ]
        gdf_rutas = gpd.GeoDataFrame(
            {
                "Nombre": ["Ruta Norte", "Ruta Sur", "Interconexión"],
                "geometry": rutas_general
            },
            crs="EPSG:4326"
        )
        gdf_ruta_especifica = gpd.GeoDataFrame(
            {"Nombre": ["Ruta Encontrada"], "geometry": [linea_ruta]},
            crs="EPSG:4326"
        )
        fig, ax = plt.subplots(figsize=(12, 8))
        gdf_rutas[gdf_rutas["Nombre"] == "Ruta Norte"].plot(
            ax=ax, color="blue", linewidth=2, label="Ruta Norte")
        gdf_rutas[gdf_rutas["Nombre"] == "Ruta Sur"].plot(
            ax=ax, color="red", linewidth=2, label="Ruta Sur")
        gdf_rutas[gdf_rutas["Nombre"] == "Interconexión"].plot(
            ax=ax, color="purple", linewidth=2, linestyle="--", label="Interconexión")
        gdf_ruta_especifica.plot(ax=ax, color="green", linewidth=3, label="Ruta Encontrada")
        self.gdf_estaciones.plot(ax=ax, color="orange", markersize=50, label="Estaciones")
        for x, y, label in zip(self.gdf_estaciones.geometry.x, self.gdf_estaciones.geometry.y, self.gdf_estaciones["Nombre"]):
            ax.text(x, y, label, fontsize=8, ha="right")
        plt.title(f"Ruta de {ruta[0]} a {ruta[-1]} en TransMilenio")
        plt.legend()
        plt.show()

if __name__ == "__main__":
    sistema = SistemaTransporte()

    # Ejemplo 1: Ruta basada en tiempo
    ruta_optima_tiempo = sistema.encontrar_mejor_ruta("Portal Norte", "Calle 45", criterio="tiempo")
    print(f"Mejor ruta basada en tiempo: {ruta_optima_tiempo}")
    sistema.visualizar_ruta(ruta_optima_tiempo)

    # Ejemplo 2: Ruta basada en distancia
    ruta_optima_distancia = sistema.encontrar_mejor_ruta("Portal Norte", "Universidades", criterio="distancia")
    print(f"Mejor ruta basada en distancia: {ruta_optima_distancia}")
    sistema.visualizar_ruta(ruta_optima_distancia)

    # Ejemplo 3: Ruta basada en trasbordos
    ruta_optima_trasbordos = sistema.encontrar_mejor_ruta("Portal Sur", "Américas", criterio="trasbordos")
    print(f"Mejor ruta basada en trasbordos: {ruta_optima_trasbordos}")
    sistema.visualizar_ruta(ruta_optima_trasbordos)
