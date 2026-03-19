## 1. Transformación y limpieza de datos del dataset 'bank-additional.csv'

1.1 Carga del conjunto de datos

Se carga el archivo bank-additional.csv utilizando la biblioteca Pandas en Python. Para ello se utilizó la función read_csv() para poder leer el archivo csv y convertirlo en un DataFrame que posibilite su análisis y manipulación.

1.2 Exploración y limpieza de datos

Para comprobar que los datos se habían importado correctamente se visualizaron las primeras filas del DataFrame utilizando la función head() y se revisaron los nombres de las columnas del dataset utilizando bank.columns y se detectó una columna llamada "Unnamed: 0", la cual fue eliminada con la función 'drop' para evitar tener datos que no contienen información y perjudican el análisis.
Para verificar el tamaño del dataset se utilizó el comando 'shape' y se comprobó que se compone aproximadamente de 43000 registros y 23 variables.
Se analizó el tipo de datos que componen el conjunto de datos con el comando 'info' y se comprobó el tipo de dato de cada variable y el número de valores no nulos por columna. Posteriormente se ejecuta el código print(bank.isnull().sum()) para comprobar si hay valores nulos en el dataset. Esto nos permite detectar que hay varias columnas que contienen valores nulos que se tendrán que tratar en el proceso de limpieza de datos.
Se verifica que id_ no tenga duplicados con la función duplicated().sum(). Nos devuelve 0 así que no hay duplicados.

1.3 Transformación de las variables numéricas

Tratamos las variables que tienen valores nulos para evitar problemas en nuestro análisis. Para ello decidimos sustituir los valores nulos de las variables numéricas (age, cons.price.idx y euribor3m) por su mediana (de esta manera se evitan problemas con los valores extremos de las variables) en vez de eliminarlos, dado que perderíamos muchos datos y podrían ser relevantes para nuestro análisis.
Al realizar este paso con la función median() nos da error en las variables cons.price.idx y euribor3m porque sus valores son tipo texto debido a que están expresados los decimales de sus valores en comas en vez de puntos. Por ello, primero reemplazamos las comas por puntos y luego convertimos dichas variables a numéricas con la función pandas.to_numeric(). Además añadimos la función errors="coerce" para convertir valores que no sean números en Nan y así no dar error al calcular la mediana.

1.4 Transformación de las variables binarias

Se decide sustituir los valores nulos de las variables 'default', 'housing' y 'loan' por -1 para crear una categoría nueva que recoja dichos valores y evite los sesgos que supondría clasificarlos como 1 o 0. Para ello utilizamos la función fillna(-1).

1.5 Transformación de las variables categóricas

Decidimos sustituir los valores nulos de las variables 'job', 'marital' y 'education' por una nueva categoría "unknown" utilizando fillna("unknown").

1.6 Transformación de las variable 'date'

Decidimos sustituir los valores nulos de la variable 'date' por el valor "unknown" utilizando fillna("unknown"). De esta manera los mantenemos en el dataset y nos permitirá identificar los casos en los que no se dispone de información temporal.

NOTA: al analizar la variable 'pdays' vemos que el 96% de las veces se muestra el valor '999'. Es muy probable que represente un valor especial y al ser un porcentaje tan alto lo dejamos tal cual para evitar perjudicar el análisis.

## 2. Transformación y limpieza de datos del dataset 'customer-details.xlsx'

2.1 Carga del conjunto de datos

Se carga el archivo customer-details.xlsx utilizando la biblioteca Pandas en Python. Para ello se utilizó la función read_excel() para poder leer el archivo Excel y convertirlo en un DataFrame que posibilite su análisis y manipulación.

2.2 Exploración y limpieza de datos

Para comprobar que los datos se habían importado correctamente se visualizaron las primeras filas del DataFrame utilizando la función head() y se revisaron los nombres de las columnas del dataset utilizando customers.columns y se detectó una columna llamada "Unnamed: 0", la cual fue eliminada con la función 'drop' para evitar tener datos que no contienen información y perjudican el análisis.
Para verificar el tamaño del dataset se utilizó el comando 'shape' y se comprobó que se compone de 20115 filas y 6 columnas.
Se analizó el tipo de datos que componen el conjunto de datos con el comando 'info' y se comprobó el tipo de dato de cada variable y el número de valores no nulos por columna. Posteriormente se ejecuta el código print(customers.isnull().sum()) para analizar si hay datos faltantes. Comprobamos que no existen valores nulos en ninguna de las variables.
Se verifica que ID no tenga duplicados con la función duplicated().sum(). Nos devuelve 0 así que no hay duplicados.

2.3 Transformación de variables

Vemos que únicamente es necesario renombrar la variable ID para que al fusionarla con el dataset de bank no haya problemas. Para ello la renombramos a id_ con la función customers.rename().

## 3. Fusión de ambos datasets

Usamos el código bank.merge(customers, on="id_", how="left") para realizar un left join entre el dataset de bank y el de customers. De esta manera lo que buscamos es que se muestre toda la información del dataset de bank, con independencia o no de que exista correspondencia con la información de customers.
Posteriormente buscamos nulos en el nuevo dataset fusionado y vemos que de las 43000 filas que tiene el dataset de bank no se ha encontrado información en 'customers' para 22982 registros y solo hay correspondencia para 20018 registros entre ambos datasets.
A partir de esta fusión podemos usar el dataset fusionado (bank) para estudiar variables de ambos datasets.

## 4. Análisis descriptivo de datos

4.1 Variables numéricas

4.1.1 Identificación de variables numéricas

Averiguamos qué variables son numéricas utilizando la función select_dtypes(include="number"). Confirmamos que 'age', 'duration', 'campaign', 'pdays','previous', 'emp.var.rate', 'cons.price.idx', 'euribor3m', 'latitude', 'longitude', 'Income', 'Kidhome', 'Teenhome' y 'NumWebVisitsMonth' son variables numéricas.

4.1.2 Distribución de las variables numéricas

Se analiza la distribución de las variables numéricas utilizando la función describe(). Se obtienen así la media, desviación estándar, mínimo y máximo y percentiles. Esto nos permite además detectar valores extremos o atípicos. Explicamos los hallazgos más significativos:

a) Dataset 'Bank'

Duration: la media de duración de las llamadas es de 258 segundos pero hay llamadas muy cortas y otras muy largas (ej. 4918 segundos).

Campaign: los clientes son contactados 2.5 veces de media y el 75% de los mismos son contactados menos de 3 veces, por lo que en general no se contacta demasiadas veces a los clientes. Sin embargo, vemos que el máximo es 56 contactos, lo cual debe ser un valor extremo.

Previous: los percentiles muestran valor 0, lo cual significa que la mayoría de clientes no habían sido contactados previamente.

Pdays: como vimos anteriormente, la mayoría de veces esta variable tiene el valor 999, dado el resultado del punto anterior entendemos que ese valor seguramente es un código que se le da a la variable para indicar que nunca se ha contactado al cliente.

Age: la media de edad de los clientes es de 40 años. El 75% de los mismos tiene 46 años o menos, por tanto podemos confirmar que se trata de un público de mediana edad en su mayoría. La edad mínima es 17 y la máxima 98, por lo que hay clientes de grupos de edad variados.

b) Dataset 'Customers'

Income: los ingresos medios de los clientes son 93071. La desviación estándar es elevada (50615), lo cual indica que hay una gran dispersión entre los niveles de ingresos. Esto se refleja por ejemplo en la gran diferencia entre el mínimo (5852) y el máximo (180791).

Kidhome: los valores de clientes con hijos oscilan entre 0 y 2, lo cual significa que no hay clientes con más de dos hijos. El promedio de hijos en casa es aproximadamente 1. Hay varios clientes que no tienen ningún hijo.

Teenhome: los valores de clientes con hijos adolescentes en casa oscilan entre 0 y 2. La media de hijos adolescentes en casa se sitúa en 1. La mediana también es 1, lo que sugiere que parte importante de los clientes tienen un adolescente en casa, aunque también hay clientes sin adolescentes.

NumWebVisitsMonth: la media de visitas de los clientes a la web del banco es de 16 veces al mes. El número de visitas al mes oscila entre 1 y 32, por lo que todos los clientes la han visitado por lo menos una vez.

4.2 Variable Objetivo

Se analiza la distribución de la variable objetivo 'y' utilizando la función value_counts().
Vemos que 38156 clientes no suscribieron el depósito a plazo bancario y 4844 sí lo hicieron. Por tanto, podemos decir que la mayoría de clientes no suscribieron el depósito.

4.3 Variables Categóricas

Se analiza la distribución de las variables categóricas usando la función value_counts():

Job: vemos que los empleos más frecuentes son admin., blue-collar y technician. Por el contrario, housemaid, unemployed y student son las menos frecuentes. Hay muy pocos empleos con categoría "unknown" lo cual significa que tenemos información de la mayoría de ellos.

Marital: observamos que la mayoría de los clientes están casados, seguidos del estado civil "soltero". Hay pocos divorciados y un escaso número de casos para los cuales no hay información sobre el estado civil.

Education: el nivel educativo del cliente más frecuente es university degree, seguidos de high school. Los analfabetos son prácticamente inexistentes y hay muy pocos registros "unknown".

4.4 Relación entre variables categóricas y la variable objetivo 'y'

Job <--> y: los empleos que mayor proporción de aceptación del depósito tienen son los jubilados y los estudiantes. Los empleos con menor aceptación del depósito son blue-collar o services. Por tanto, parece que el empleo y la aceptación del depósito están relacionados.

Marital <--> y: vemos que los solteros son el grupo que acepta el depósito en mayor proporción que el resto de estados civiles. Por tanto, también podemos confirmar que existe una relación entre estado civil y aceptación del depósito bancario.

Education <--> y: se observa que los clientes de niveles educativos superiores (university degree o high school) tienen una aceptación mayor del depósito que los clientes de niveles educativos básicos. Podemos decir entonces que existe relación entre ambas variables.

Poutcome <--> y: se observa muy claramente que cuando la campaña anterior de marketing tuvo éxito, la probabilidad de que los clientes acepten el depósito es mucho mayor (65%). Confirmamos relación positiva entre las variables.

4.5 Relación entre variables numéricas y la variable objetivo 'y'

Vemos que resultaría complejo y sin sentido analizar cada uno de los distintos valores de la variable 'age'por lo que realizamos un paso previo: creamos nueva variable que agrupe las edades en distintos tramos de edad (age_group): 18-30,31-40,41-50,51-60,61-70,71-100 utilizando la funcion pandas.cut().
Analizamos posteriormente la proporción de aceptación del depósito de 'age_group', 'previous', 'pdays', 'Kidhome' y 'Teenhome' con la función crosstab().

Age_group <--> y: observamos que en los dos últimos grupos de edad (edades entre 61-100 años) más del 40% de los clientes aceptan el depósito bancario mientras que para el resto de grupos de edad dicha aceptación no llega ni al 15%.

Previous y Pdays <--> y: observamos que generalmente cuando el cliente ha sido contactado previamente tiene mayor probabilidad de aceptar el depósito. Mientras que cuando se contacta al cliente por primera vez la probabilidad de que lo acepte baja mucho (<9%).

Kidhome y Teenhome: vemos valores muy similares al analizar las proporciones de aceptación del depósito de dichas variables. Por lo que no se observan diferencias relevantes en la aceptación del depósito según estas variables.

Analizamos además la distribución de las variables 'duration', 'campaign', 'Income' y 'NumWebVisitsMonth' en función de la aceptación del depósito con la función groupby().describe.

Duration <--> y: como esperado, si las llamadas son más largas la proporción de aceptación del depósito bancario es mayor.

Campaign <--> y: la media de contactos realizados a los clientes que acaban aceptando el depósito es de 2, mientras que la media de los que no lo aceptan es de casi 3. Además, en su mayoría el nº de contactos necesarios para que el cliente acabe aceptando es de 2, mientras que es 3 para aquellos que acabaron rechazando. Esto sugiere una posible relación negativa entre el número de contactos y la aceptación del depósito.

Income y NumWebVisitsMonth: observamos que la distribución de dichas variables es muy similar acepten o no el depósito. Por lo que no se observan diferencias relevantes en la aceptación del depósito según estas variables.

4.6 Relación entre variables binarias y la variable objetivo 'y'

Default <--> y: dado que el número de clientes con historial de incumplimiento de pagos es muy bajo (3) no podemos estudiar correctamente la relación entre esta variable y la probabilidad de aceptación del depósito bancario.

Housing <--> y: el porcentaje de clientes con hipoteca que acepta el depósito es de 11.6% y 10.9% si no la tiene, por tanto las diferencias son mínimas y no podemos confirmar que exista relación entre ambas variables.

Loan <--> y: el porcentaje de clientes que tienen algún préstamo y acepta el depósito es de 10,9% y 11,3% si no lo tienen, por tanto las diferencias son mínimas y no podemos confirmar que exista relación entre ambas variables.

4.7 Correlación entre variables numéricas

Al analizar los tipos de variables con la función 'dtypes' vemos que hay varias variables que están en formato texto (duration, emp.var.rate, cons.conf.idx y nr.employed) y las necesitaríamos en formato numérico para poderlas analizar correctamente. Para ello las convertimos a formato numérico usando la función to_numeric () y con la función errors=coerce hacemos que cualquier valor que no sea convertible a número se convierta en Nan para evitar que dé error.
Calculamos posteriormente la matriz de correlación de Pearson entre las diferentes variables numéricas con la función corr() y nos damos cuenta de que nr.employed aparece como NaN en la matriz. Al analizarla por separado con la función describe() vemos que su valor es siempre 5191 y su desviación típica es 0, lo cual indica que no muestra variabilidad, por ello la vamos a ignorar en nuestro análisis de la correlación. Posteriormente interpretaremos los resultados ayudándonos de un mapa de calor.

## 5. Visualización de datos

5.1 Mapa de Calor de Correlación

Para poder ver más claramente la correlación entre las variables numéricas anteriores, generamos un mapa de calor utilizando las librerías Matplotlib y Seaborn.

Tamaño del gráfico: ejecutamos el código plt.figure(figsize=(10,8)) para indicar el tamaño que queremos que tenga el gráfico.

Eliminación de variables no informativas: eliminamos del gráfico las variables que no aportan información relevante en la matriz de correlación (como nr.employed) con la función dropna() para que quede más limpio.

Formato del gráfico: ejecutamos el código:

sns.heatmap(
    correlation_matrix,
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

Con el mismo queremos que cada valor se muestre en una celda diferente (annot=True), que los colores sean divergentes, rojo para correlación positiva y azul para correlación negativa (cmap="coolwarm") y que los números mostrados tengan máximo dos decimales (fmt=".2f").

Título del gráfico: usamos el código plt.title("Mapa de Calor de Correlación") para darle un título.

Ajuste del gráfico: usamos el código plt.tight_layout() para que todos los parámetros incluidos en el mismo (títulos, valores, etiquetas, etc.) quepa bien y el gráfico se visualice bien, sin solapes ni márgenes estrechos.

Guardar la imagen del gráfico: usamos el código plt.savefig("Gráficos/mapa_calor_correlacion.png") para que se guarde el mapa de calor como archivo png en nuestra carpeta del proyecto.

Mostrar el gráfico: usamos el código plt.show() para que nos muestre el mapa de calor.

5.2 Histograma de Ingresos de los clientes

Para poder analizar y visualizar bien la distribución de la variable 'Income' creamos un histograma usando las librerías Matplotlib y Seaborn.

Tamaño del gráfico: ejecutamos el código plt.figure(figsize=(8,5)) para indicar el tamaño que queremos que tenga el gráfico.

Intervalos de datos: usamos el código sns.histplot(bank["Income"], bins=20) para crear el histograma de la variable 'Income' y agrupar los valores en 20 intervalos diferentes de ingresos. De esta manera, cada intervalo representará un barra diferente del histograma.

Título del gráfico: usamos el código plt.title("Histograma Ingresos de los clientes") para crear el título del gráfico.

Ejes del gráfico: usamos el código plt.xlabel("Ingresos") plt.ylabel("Número de clientes") para indicar que el eje X corresponde a los ingresos e Y al número de clientes.

Ajuste, guardado y visualización del gráfico: usamos los mismos códigos vistos en el punto anterior (mapa de calor).

5.3 Boxplot: comparativa duración vs aceptación depósito bancario

Queremos visualizar si hay diferencias en la distribución de la duración de las llamadas en función de si aceptan o no el depósito. Para ello creamos un gráfico Boxplot usando las librerías Matplotlib y Seaborn. Utilizamos las mismas funciones que el punto anterior, cambiando únicamente el tipo de gráfico por boxplot con la siguiente función sns.boxplot(x=bank["y"], y=bank["duration"]). En este caso en el eje X se mostrará la aceptación o no del depósito y en el Y se mostrará la duración.

5.4 Gráfico de barras: tasa de suscripción del depósito según grupo de edad

Para visualizar mejor la tasa de aceptación del depósito bancario en función del grupo de edad creamos un gráfico de barras usando las funciones de visualización de Pandas (basadas en Matplotlib).

Cálculo de tasa de suscripción según grupo de edad: usamos el código:

age_subscription = pandas.crosstab(
    bank["age_group"],
    bank["y"],
    normalize="index"
)

para calcular qué proporción de los clientes aceptan o no el depósito en función del grupo de edad.

Creación del gráfico de barras: usamos el código age_subscription.plot(kind="bar")

Título y ejes: usamos la función 'title' para indicar el título del gráfico (Tasa de suscripción del depósito por grupo de edad), la función 'xlabel' para indicar el eje X (Grupo de edad) e Y (Proporción de clientes).

Ajuste, guardado y visualización del gráfico: usamos las funciones tight_layout(), savefig() y show() como en puntos anteriores.
Vemos que se generan dos barras por cada grupo de edad. La azul muestra la proporción de clientes que no suscriben el depósito y la naranja muestra la proporción de los que sí lo suscriben.

5.5 Gráfico de violín: distribución de la edad según aceptación del depósito

Queremos ver cómo se distribuyen las edades de los clientes en función de si aceptan o no el depósito. Para ello construimos un gráfico de violín usando la libreria Seaborn.

Creación del gráfico de violín: usamos el código sns.violinplot(x=bank["y"], y=bank["age"])

Título y ejes: usamos las mismas funciones que el punto anterior.

Ajuste, guardado y visualización del gráfico: usamos las funciones tight_layout(), savefig() y show() como en puntos anteriores.

5.6 Gráfico circular: tasa de suscripción del depósito bancario

Analizamos la tasa de aceptación del depósito bancario a través de un gráfico circular usando la librería Matplotlib.

Creación del gráfico circular: usamos el código:

bank["y"].value_counts().plot(
    kind="pie",
    autopct="%1.1f%%",
    explode=(0,0.1)
)

Formato: aplicamos el código autopct="%1.1f%%" para indicar que queremos que los valores solo tengan un decimal y el código explode=(0,0.1) para separar uno de los segmentos del gráfico y así destacarlo visualmente. 

Título: usamos las mismas funciones que el punto anterior.

## 6. Informe explicativo del análisis

A partir del análisis realizado sobre los datasets de bank-additional y customer-details, así como su posterior fusión, se han identificado varios factores relevantes en relación con la suscripción de depósitos bancarios.
En primer lugar, se observa que la tasa de aceptación del depósito bancario es baja, ya que la mayoría de clientes no lo suscriben (89%).

6.1 Perfil del cliente

Edad: media en torno a los 40 años.

Nivel educativo: grado universitario frecuente, seguido de educación secundaria.

Estado civil: mayoritariamente casados.

Nº de hijos: suelen tener pocos hijos (entre ninguno y 2 máximo) y media cercana a 1.

Ingresos: se observa una gran dispersión, lo que indica que existen perfiles muy distintos de clientes en términos de ingresos.

6.2 Variables significativas

6.2.1 Edad

La variable edad muestra una relación clara con la aceptación del depósito.
Los clientes de mayor edad (especialmente mayores de 60 años) presentan una mayor tasa de suscripción del depósito bancario.
Los grupos más jóvenes presentan tasas significativamente más bajas.
Esto sugiere que la edad es un factor relevante en la toma de decisión.

6.2.2 Duración de la llamada

Es una de las variables más influyentes:
A mayor duración de la llamada, mayor probabilidad de aceptación y viceversa.
Esto puede indicar que una mayor interacción mejora la conversión.

6.2.3 Campaña (número de contactos)

Se observa una relación negativa:
Los clientes que aceptan suelen necesitar menos contactos (≈2).
Los que no aceptan reciben más contactos (≈3 o más).
Esto sugiere que insistir más no mejora los resultados, sino que puede ser contraproducente.

6.2.4 Resultados de campañas anteriores (poutcome)

Existe una relación muy clara:
Si la campaña anterior fue exitosa → alta probabilidad de aceptación.
Si no → probabilidad muy baja.

6.3 Variables poco significativas

Las variables procedentes del dataset de customers muestran un impacto mucho menor:

Income

Kidhome

Teenhome

NumWebVisitsMonth

En todos los casos, no se observan diferencias relevantes entre clientes que aceptan y los que no.
Esto sugiere que estas variables no son determinantes en la decisión.

6.4 Correlación entre variables

Observamos a través de la matriz de correlación de Pearson una fuerte relación entre variables como emp.var.rate y euribor3m, pero en general no se observan correlaciones fuertes entre la mayoría de variables. Sin embargo, sí se identifican algunas relaciones destacables:
Existe una correlación positiva alta entre emp.var.rate y euribor3m, lo que sugiere que ambas variables están relacionadas con el contexto económico y tienden a moverse en la misma dirección.
También se observa relación entre emp.var.rate y cons.price.idx, lo cual sugiere de nuevo que estas variables están influenciadas por factores macroeconómicos comunes.
Por otro lado, las variables procedentes del dataset de customers (Income, Kidhome, Teenhome, NumWebVisitsMonth) no presentan correlaciones relevantes ni entre ellas ni con el resto de variables, lo que indica que seguramente no afecten demasiado a la aceptación del depósito.
Finalmente, se detecta que la variable nr.employed no presenta variabilidad (valor=5191), por lo que no aporta información útil en el análisis de correlación y se ha excluido de la interpretación.

6.5 Visualización de datos

Las visualizaciones han permitido reforzar los resultados obtenidos:

Mapa de calor de correlación: como visto al realizar la matriz de correlación, podemos observar fuertes correlaciones positivas (en rojo) entre la tasa de variación del empleo y el índice de precio al consumo (IPC). Esto se debe a que cuando crece el empleo, crece también el consumo y a su vez los precios ante el aumento de demanda.
Vemos también fuerte relación positiva entre la tasa de variación del empleo y el tipo de interés de refencia a 3 meses. Esto seguramente se deba a que el aumento de empleo suele provocar aumento de precios, por ello suben también los intereses para tratar de paliar ese aumento de inflación.

Histograma ingresos: muestra la dispersión del nivel de ingresos de los clientes. Se pueden observa grandes diferencias, desde los que ingresan menos de 25000 hasta los que ingresan más de 175000.

Boxplot duración vs aceptación del depósito: evidencia de forma clara la relación entre la duración de la llamada y la aceptación del depósito, mostrando una mayor aceptación del mismo cuando las llamadas son más largas.

Gráfico de barras por grupos de edad: visualizamos muy claramente como los grupos de edad mayores de 60 años son los más propensos a aceptar el depósito bancario con una tasa de aceptación mayor al 40%. Sin embargo, los clientes de los grupos de edad más jóvenes (menores de 60 años) tienden a tener una tasa de aceptación menor al 20%.

Gráfico de violin: observamos que a pesar de que la mediana de edad tanto en el grupo de los clientes que sí aceptan el depósito, como en los que no lo aceptan es muy similar (cercana a los 40 años), la distribución de los clientes que sí aceptan el depósito está más centrada en las edades más elevadas (más de 60 años). Mientras que la de los clientes que no aceptan es más amplia y con mayor presencia en el público joven. Refuerza por tanto la relación positiva entre edad y probabilidad de suscripción del depósito, a mayor edad, mayor probabilidad de aceptación del mismo.

Gráfico circular: confirma la baja tasa de aceptación general del depósito bancario, siendo tan solo 11,3% de los clientes los que suscriben el mismo.

6.6 Conclusión final

Los factores más relevantes en la aceptación del depósito son:

* Edad: a mayor edad, mayor es la probabilidad de contratación del depósito.

* Duración de la llamada: llamadas más largas acaban más probablemente en la suscripción del depósito bancario.

* Número de contactos: a mayor nº de contactos realizados al cliente, menor probabilidad de que acabe suscribiendo el depósito.

* Resultado de campañas anteriores: si las campañas anteriores fueran exitosas es más probable que se suscriba el depósito.

Por el contrario, las variables del dataset de customers tienen un impacto bastante limitado en la variabilidad de la tasa de aceptación del depósito bancario.
