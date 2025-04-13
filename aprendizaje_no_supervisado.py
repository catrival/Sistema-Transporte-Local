import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D  # Necesario para gráficos 3D

class VisualizadorClusters:
    def __init__(self):
        # Definición de las estaciones con coordenadas
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
        self._realizar_clustering()

    def _realizar_clustering(self):
        # Usamos KMeans para agrupar las estaciones
        coords = self.gdf_estaciones[["Latitud", "Longitud"]].values
        self.kmeans = KMeans(n_clusters=3, random_state=42)  # Tres clusters como ejemplo
        self.gdf_estaciones["Cluster"] = self.kmeans.fit_predict(coords)

    def graficar_clusters_basico(self):
        # Gráfica básica de clusters
        plt.figure(figsize=(10, 6))
        for cluster_id in self.gdf_estaciones["Cluster"].unique():
            cluster = self.gdf_estaciones[self.gdf_estaciones["Cluster"] == cluster_id]
            plt.scatter(cluster["Longitud"], cluster["Latitud"], label=f'Cluster {cluster_id}', s=100)
        plt.title("Clusters de Estaciones (Básico)")
        plt.xlabel("Longitud")
        plt.ylabel("Latitud")
        plt.legend()
        plt.show()

    def graficar_con_mapa(self):
        # Gráfica sobre mapa
        fig, ax = plt.subplots(figsize=(12, 8))
        self.gdf_estaciones.plot(ax=ax, column="Cluster", cmap="Set1", markersize=50, legend=True)
        plt.title("Clusters en el Mapa")
        plt.show()

    def graficar_scatter3d(self):
        # Gráfico 3D con Latitud, Longitud y Cluster
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')

        # Iterar sobre los clusters únicos
        clusters_unicos = self.gdf_estaciones["Cluster"].unique()
        for cluster_id in clusters_unicos:
            datos_cluster = self.gdf_estaciones[self.gdf_estaciones["Cluster"] == cluster_id]
            ax.scatter(
                datos_cluster["Longitud"],
                datos_cluster["Latitud"],
                zs=cluster_id,  # Usamos el ID del cluster como la tercera dimensión
                label=f"Cluster {cluster_id}",
                s=100
            )

        # Configuración del gráfico
        ax.set_title("Visualización 3D de Clusters", fontsize=16)
        ax.set_xlabel("Longitud", fontsize=12)
        ax.set_ylabel("Latitud", fontsize=12)
        ax.set_zlabel("Cluster", fontsize=12)
        ax.legend(title="Cluster", fontsize=10)
        plt.show()

# Ejecución del código y generación de gráficas
if __name__ == "__main__":
    visualizador = VisualizadorClusters()
    visualizador.graficar_clusters_basico()   # Gráfica 1
    visualizador.graficar_con_mapa()          # Gráfica 2
    visualizador.graficar_scatter3d()         # Gráfica 3 (Nueva)
