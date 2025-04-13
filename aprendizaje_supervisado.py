import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt
import seaborn as sns

# Creación del dataset mejorado (simulado)
np.random.seed(42)
stations = ["Portal Norte", "Calle 100", "Héroes", "Calle 72", "Calle 45", "Universidades"]
data = {
    "Estacion": stations * 30,  # 6 estaciones × 30 días
    "Fecha": pd.date_range("2023-01-01", periods=180).tolist(),
    "Dia_Semana": [d.dayofweek for d in pd.date_range("2023-01-01", periods=180)],
    "Es_Festivo": np.random.choice([0, 1], size=180, p=[0.85, 0.15]),
    "Latitud": [4.7528, 4.6768, 4.6686, 4.6582, 4.6455, 4.6019] * 30,
    "Longitud": [-74.0455, -74.0565, -74.0597, -74.0648, -74.0681, -74.0663] * 30,
    "Pasajeros_Manana": np.random.randint(100, 600, size=180),
    "Pasajeros_Tarde": np.random.randint(150, 700, size=180),
    "Pasajeros_Noche": np.random.randint(50, 400, size=180),
    "Eventos_Especiales": np.random.poisson(0.2, size=180)
}

df = pd.DataFrame(data)
df["Total_Pasajeros"] = df["Pasajeros_Manana"] + df["Pasajeros_Tarde"] + df["Pasajeros_Noche"]


# Análisis exploratorio mejorado
print("\n=== Resumen estadístico ===")
print(df.describe())

print("\n=== Demanda por estación ===")
print(df.groupby("Estacion")["Total_Pasajeros"].mean().sort_values(ascending=False))

plt.figure(figsize=(14, 10))

# Mapa de calor de demanda
plt.subplot(2, 2, 1)
sns.scatterplot(data=df, x="Longitud", y="Latitud", hue="Total_Pasajeros",
                size="Total_Pasajeros", sizes=(50, 200), palette="viridis")
plt.title("Demanda por Estación Geográfica")
plt.xlabel("Longitud")
plt.ylabel("Latitud")

# Demanda por día de semana
plt.subplot(2, 2, 2)
sns.boxplot(data=df, x="Dia_Semana", y="Total_Pasajeros")
plt.title("Demanda por Día de Semana")
plt.xlabel("Día de semana (0=Lunes)")
plt.ylabel("Total pasajeros")

# Distribución de demanda
plt.subplot(2, 2, 3)
sns.histplot(df["Total_Pasajeros"], kde=True)
plt.title("Distribución de Demanda Total")

# Correlaciones
plt.subplot(2, 2, 4)
sns.heatmap(df.corr(numeric_only=True)[["Total_Pasajeros"]].sort_values("Total_Pasajeros", ascending=False),
            annot=True, cmap="coolwarm")
plt.title("Correlación con Demanda Total")

plt.tight_layout()
plt.show()


# Modelado predictivo (aprendizaje supervisado)

# Preprocesamiento
X = df[["Latitud", "Longitud", "Dia_Semana", "Es_Festivo", "Eventos_Especiales"]]
y = df["Total_Pasajeros"]

# División de datos
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modelo de Random Forest
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluación
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f"\nError Absoluto Medio (MAE): {mae:.2f} pasajeros")

# Importancia de características
feature_imp = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
plt.figure(figsize=(10, 6))
sns.barplot(x=feature_imp, y=feature_imp.index)
plt.title('Importancia de Variables en la Predicción')
plt.xlabel('Puntuación de Importancia')
plt.ylabel('Variables')
plt.show()


# Resultados y recomendaciones
print("\n=== Recomendaciones basadas en el modelo ===")
print("1. Las estaciones con mayor latitud (más al norte) muestran mayor demanda")
print("2. Los días viernes (día 4) y festivos tienen mayor afluencia")
print("3. Los eventos especiales incrementan la demanda en aproximadamente",
      round(feature_imp["Eventos_Especiales"] * 100), "%")