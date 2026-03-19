# ============================================================
# LIBRERÍAS
# ============================================================

import pandas
import numpy
import matplotlib.pyplot as plt
import seaborn as sns


# ============================================================
# 1. TRANSFORMACIÓN Y LIMPIEZA DE DATOS DEL DATASET
# 'bank-additional.csv'
# ============================================================

# ------------------------------------------------------------
# 1.1 Carga del conjunto de datos
# ------------------------------------------------------------

bank = pandas.read_csv("Datos/Bruto/bank-additional.csv")

# ------------------------------------------------------------
# 1.2 Exploración y limpieza inicial de datos
# ------------------------------------------------------------

print(bank.head())
print(bank.columns)

bank = bank.drop(columns=["Unnamed: 0"])

print(bank.columns)
print(bank.shape)
print(bank.info())
print(bank.isnull().sum())
print(bank["id_"].duplicated().sum())


# ------------------------------------------------------------
# 1.3 Exploración inicial de variables categóricas y objetivo
# ------------------------------------------------------------

print(bank["job"].value_counts())
print(bank["marital"].value_counts())
print(bank["education"].value_counts())
print(bank["housing"].value_counts())
print(bank["loan"].value_counts())
print(bank["contact"].value_counts())
print(bank["y"].value_counts())


# ------------------------------------------------------------
# 1.4 Exploración inicial de variables numéricas
# ------------------------------------------------------------

print(bank.describe())
print(bank["age"].describe())


# ------------------------------------------------------------
# 1.5 Transformación de variables numéricas
# ------------------------------------------------------------

# Sustitución de valores nulos de age por la mediana
bank["age"] = bank["age"].fillna(bank["age"].median())

# Conversión de variables con comas decimales a formato numérico
bank["cons.price.idx"] = bank["cons.price.idx"].str.replace(",", ".")
bank["euribor3m"] = bank["euribor3m"].str.replace(",", ".")

bank["cons.price.idx"] = pandas.to_numeric(bank["cons.price.idx"], errors="coerce")
bank["euribor3m"] = pandas.to_numeric(bank["euribor3m"], errors="coerce")

# Sustitución de valores nulos por la mediana
bank["cons.price.idx"] = bank["cons.price.idx"].fillna(bank["cons.price.idx"].median())
bank["euribor3m"] = bank["euribor3m"].fillna(bank["euribor3m"].median())

print(bank["cons.price.idx"].isnull().sum())
print(bank["euribor3m"].isnull().sum())


# ------------------------------------------------------------
# 1.6 Exploración de valores faltantes en variables categóricas
# ------------------------------------------------------------

print(bank["job"].value_counts(dropna=False))
print(bank["marital"].value_counts(dropna=False))
print(bank["education"].value_counts(dropna=False))
print(bank["default"].value_counts(dropna=False))
print(bank["housing"].value_counts(dropna=False))
print(bank["loan"].value_counts(dropna=False))
print(bank["date"].value_counts(dropna=False))


# ------------------------------------------------------------
# 1.7 Transformación de variables binarias, categóricas y fecha
# ------------------------------------------------------------

# Variables binarias
bank["default"] = bank["default"].fillna(-1)
bank["housing"] = bank["housing"].fillna(-1)
bank["loan"] = bank["loan"].fillna(-1)

# Variables categóricas
bank["job"] = bank["job"].fillna("unknown")
bank["marital"] = bank["marital"].fillna("unknown")
bank["education"] = bank["education"].fillna("unknown")

# Variable de fecha
bank["date"] = bank["date"].fillna("unknown")

print(bank.isnull().sum())
print(bank[["cons.price.idx", "euribor3m"]].info())
print(bank["pdays"].value_counts())


# ============================================================
# 2. TRANSFORMACIÓN Y LIMPIEZA DE DATOS DEL DATASET
# 'customer-details.xlsx'
# ============================================================

# ------------------------------------------------------------
# 2.1 Carga del conjunto de datos
# ------------------------------------------------------------
customers = pandas.read_excel("Datos/Bruto/customer-details.xlsx")

# ------------------------------------------------------------
# 2.2 Exploración y limpieza inicial de datos
# ------------------------------------------------------------

print(customers.head())
print(customers.columns)

customers = customers.drop(columns=["Unnamed: 0"])

print(customers.columns)
print(customers.shape)
print(customers.info())
print(customers.isnull().sum())
print(customers["ID"].duplicated().sum())


# ------------------------------------------------------------
# 2.3 Transformación de variables
# ------------------------------------------------------------

customers = customers.rename(columns={"ID": "id_"})

print(customers.info())
print(customers.isnull().sum())
print(customers.head())


# ============================================================
# 3. FUSIÓN DE AMBOS DATASETS
# ============================================================

bank = bank.merge(customers, on="id_", how="left")

print(bank.shape)
print(bank.isnull().sum())


# ============================================================
# 4. ANÁLISIS DESCRIPTIVO DE DATOS
# ============================================================

# ------------------------------------------------------------
# 4.1 Variables numéricas
# ------------------------------------------------------------

print(bank.select_dtypes(include="number").columns)
print(bank.describe())

# Variables numéricas del dataset bank
print(bank["duration"].describe())
print(bank["campaign"].describe())
print(bank["previous"].describe())
print(bank["pdays"].describe())
print(bank["age"].describe())

# Variables numéricas procedentes del dataset customers
print(bank["Income"].describe())
print(bank["Kidhome"].describe())
print(bank["Teenhome"].describe())
print(bank["NumWebVisitsMonth"].describe())


# ------------------------------------------------------------
# 4.2 Variable objetivo
# ------------------------------------------------------------

print(bank["y"].value_counts())


# ------------------------------------------------------------
# 4.3 Variables categóricas
# ------------------------------------------------------------

print(bank["job"].value_counts())
print(bank["marital"].value_counts())
print(bank["education"].value_counts())


# ------------------------------------------------------------
# 4.4 Relación entre variables categóricas y variable objetivo
# ------------------------------------------------------------

print(pandas.crosstab(bank["job"], bank["y"]))
print(pandas.crosstab(bank["marital"], bank["y"]))
print(pandas.crosstab(bank["education"], bank["y"]))
print(pandas.crosstab(bank["poutcome"], bank["y"]))


# ------------------------------------------------------------
# 4.5 Relación entre variables numéricas y variable objetivo
# ------------------------------------------------------------

# Agrupación de la edad en tramos
bank["age_group"] = pandas.cut(bank["age"], bins=[17, 30, 40, 50, 60, 70, 100])

# Crosstab para variables discretas / agrupadas
print(pandas.crosstab(bank["age_group"], bank["y"]))
print(pandas.crosstab(bank["previous"], bank["y"]))
print(pandas.crosstab(bank["pdays"], bank["y"]))
print(pandas.crosstab(bank["Kidhome"], bank["y"]))
print(pandas.crosstab(bank["Teenhome"], bank["y"]))

# Groupby para variables numéricas continuas
print(bank.groupby("y")["duration"].describe())
print(bank.groupby("y")["campaign"].describe())
print(bank.groupby("y")["Income"].describe())
print(bank.groupby("y")["NumWebVisitsMonth"].describe())


# ------------------------------------------------------------
# 4.6 Relación entre variables binarias y variable objetivo
# ------------------------------------------------------------

print(pandas.crosstab(bank["default"], bank["y"]))
print(pandas.crosstab(bank["housing"], bank["y"]))
print(pandas.crosstab(bank["loan"], bank["y"]))


# ------------------------------------------------------------
# 4.7 Correlación entre variables numéricas
# ------------------------------------------------------------

print(bank.dtypes)

bank["duration"] = pandas.to_numeric(bank["duration"], errors="coerce")
bank["emp.var.rate"] = pandas.to_numeric(bank["emp.var.rate"], errors="coerce")
bank["cons.conf.idx"] = pandas.to_numeric(bank["cons.conf.idx"], errors="coerce")
bank["nr.employed"] = pandas.to_numeric(bank["nr.employed"], errors="coerce")

print(bank.dtypes)

numerical_variables = bank.select_dtypes(include="number")
correlation_matrix = numerical_variables.corr()

print(correlation_matrix)
print(bank["nr.employed"].describe())


# ============================================================
# 5. VISUALIZACIÓN DE DATOS
# ============================================================

# ------------------------------------------------------------
# 5.1 Mapa de calor de correlación
# ------------------------------------------------------------

plt.figure(figsize=(10, 8))

# Eliminamos variables no informativas en la matriz de correlación
correlation_matrix = correlation_matrix.dropna(axis=0, how="all")
correlation_matrix = correlation_matrix.dropna(axis=1, how="all")

sns.heatmap(
    correlation_matrix,
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

plt.title("Mapa de Calor de Correlación")
plt.tight_layout()
plt.savefig("Gráficos/mapa_calor_correlacion.png")
plt.show()


# ------------------------------------------------------------
# 5.2 Histograma de ingresos de los clientes
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

sns.histplot(bank["Income"], bins=20)

plt.title("Histograma de Ingresos de los Clientes")
plt.xlabel("Ingresos")
plt.ylabel("Número de clientes")

plt.tight_layout()
plt.savefig("Gráficos/histograma_ingresos.png")
plt.show()


# ------------------------------------------------------------
# 5.3 Boxplot: duración de llamada vs suscripción al depósito
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

sns.boxplot(x=bank["y"], y=bank["duration"])

plt.title("Duración de la Llamada según Suscripción del Depósito")
plt.xlabel("Suscripción al depósito")
plt.ylabel("Duración")

plt.tight_layout()
plt.savefig("Gráficos/boxplot_duracion_suscripcion.png")
plt.show()


# ------------------------------------------------------------
# 5.4 Gráfico de barras: tasa de suscripción según grupo de edad
# ------------------------------------------------------------

age_subscription = pandas.crosstab(
    bank["age_group"],
    bank["y"],
    normalize="index"
)

age_subscription.plot(kind="bar")

plt.title("Tasa de Suscripción del Depósito por Grupo de Edad")
plt.xlabel("Grupo de edad")
plt.ylabel("Proporción de clientes")

plt.tight_layout()
plt.savefig("Gráficos/bar_grupo_edad_suscripcion.png")
plt.show()


# ------------------------------------------------------------
# 5.5 Gráfico de violín: distribución de la edad según suscripción
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

sns.violinplot(x=bank["y"], y=bank["age"])

plt.title("Distribución de la Edad según Suscripción del Depósito")
plt.xlabel("Suscripción")
plt.ylabel("Edad")

plt.tight_layout()
plt.savefig("Gráficos/violin_suscripcion_edad.png")
plt.show()


# ------------------------------------------------------------
# 5.6 Gráfico circular: tasa de suscripción del depósito bancario
# ------------------------------------------------------------

bank["y"].value_counts().plot(
    kind="pie",
    autopct="%1.1f%%",
    explode=(0, 0.1)
)

plt.title("Tasa de Suscripción del Depósito Bancario")
plt.ylabel("")

plt.tight_layout()
plt.savefig("Gráficos/circular_suscripcion.png")
plt.show()

# Guardado del dataset transformado
bank.to_csv("Datos/Transformados/bank_transformado.csv", index=False)
