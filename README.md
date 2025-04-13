# Sistema-Transporte-Local
Es un sistema inteligente que a partir de una base de conocimiento escrito en reglas lógicas, gestiona la mejor ruta para moverse desde un punto A a un punto B en el sistema de transporte masivo local

# Requisitos previos
Python 3.8 o superior instalado en tu sistema.
Un entorno virtual de Python para gestionar las dependencias.


# Instalación
Clonar el repositorio:
bash
* git clone <URL-del-repositorio>
* cd <nombre-del-repositorio>


# Crear un entorno virtual:
bash
python -m venv venv
source venv/bin/activate   # En Linux/Mac
venv\Scripts\activate      # En Windows

#Instalar las dependencias:
bash
* pip install --upgrade pip
* pip install geopandas matplotlib shapely networkx

# Comandos para instalar las bibliotecas una a una. 

Pandas: Para manipulación y análisis de datos.
* pip install pandas

NumPy: Para cálculos numéricos.
* pip install numpy

Scikit-learn: Para el modelado predictivo.
* pip install scikit-learn

Matplotlib: Para visualizaciones básicas.
* pip install matplotlib

Seaborn: Para visualizaciones avanzadas.
*pip install seaborn

# Ejecución del proyecto
Ejecutar el programa: Navega al directorio del proyecto y ejecuta el script principal:
bash
* python main.py
Ejemplo de uso: El programa calculará la mejor ruta entre estaciones y mostrará las visualizaciones de las rutas en un mapa interactivo.

# Notas adicionales:
Si tienes problemas instalando geopandas debido a dependencias del sistema, te recomendamos usar el instalador de conda:
bash
* conda install geopandas matplotlib shapely networkx

Puedes modificar el código para agregar estaciones o rutas nuevas y ajustar criterios para encontrar la mejor ruta.
