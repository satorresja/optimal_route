# Optimización de Rutas con Clusterización de Ubicaciones
## Introducción
La optimización de rutas es un problema común en logística y servicios. El objetivo es determinar la secuencia más eficiente para visitar un conjunto de ubicaciones. En este caso, se abordó el problema utilizando un enfoque basado en la clusterización de ubicaciones geográficas.

## Proceso
### Conexión a la Base de Datos:

Se establece una conexión con una base de datos SQL Server utilizando pyodbc.
Se extraen las ubicaciones (latitud y longitud) de los clientes que deben ser visitados.
Por qué se hace: Es esencial obtener datos precisos y actualizados directamente de la base de datos para garantizar que todas las ubicaciones relevantes se incluyan en el proceso de optimización.

### Procesamiento de Datos:

Se cargan los datos en un DataFrame de Pandas.
Se seleccionan solo las columnas relevantes para el proceso (principalmente latitud y longitud).
Por qué se hace: El procesamiento previo de datos es crucial para eliminar cualquier ruido o dato irrelevante y para trabajar con un conjunto de datos limpio y estructurado.

### Clusterización:

Se utiliza el algoritmo DBSCAN para segmentar las ubicaciones en clusters.
Antes de aplicar DBSCAN, se calculan las distancias entre las ubicaciones utilizando la distancia de Haversine, que es adecuada para calcular distancias en la superficie de la Tierra.
Por qué se hace: En una ciudad o región grande, no es práctico que un solo agente visite todas las ubicaciones en un día. La clusterización permite segmentar las ubicaciones en grupos geográficamente cercanos. Cada cluster puede ser asignado a un agente diferente o puede ser visitado en días diferentes.


# Problema del Viajante de Comercio (TSP - Traveling Salesman Problem)
¿Qué es el TSP?
El Problema del Viajante de Comercio (TSP, por sus siglas en inglés) es uno de los problemas más estudiados en optimización combinatoria. En su formulación clásica, se nos da un conjunto de ciudades y las distancias entre cada par de ciudades. El problema es encontrar la ruta más corta que visite cada ciudad exactamente una vez y regrese al punto de partida, es decir, que complete un ciclo hamiltoniano.

¿Por qué es importante?
El TSP tiene aplicaciones prácticas en planificación, logística y fabricación de circuitos. Además, muchas de sus variantes y generalizaciones son aplicables en diversos campos. Dada su naturaleza NP-dura, el TSP también tiene un lugar especial en la teoría de la computación y la investigación de operaciones.

¿Cómo lo aproximamos?
Resolver el TSP de manera exacta para un gran número de ciudades es computacionalmente costoso debido a su complejidad exponencial. Por lo tanto, en muchos casos prácticos, se utilizan métodos heurísticos y aproximados para obtener soluciones "buenas", aunque no necesariamente óptimas, en un tiempo razonable.

En nuestro enfoque:

Uso de Clusterización: Antes de abordar el TSP, se realizó una clusterización de las ubicaciones utilizando DBSCAN. Esto redujo efectivamente la escala del problema al dividirlo en subproblemas más pequeños. En lugar de encontrar una ruta para todas las ubicaciones, encontramos rutas para cada cluster por separado.

Aproximación con tsplib95 y la librería Concorde: tsplib95 es una librería de Python diseñada para leer, generar y manipular instancias del TSP en el formato TSPLIB. Además, se puede utilizar junto con solucionadores externos como Concorde, uno de los solucionadores de TSP más eficientes disponibles. Concorde utiliza una variedad de técnicas, incluidas recortes (cutting-plane), técnicas de ramificación (branch-and-bound) y heurísticas, para encontrar soluciones rápidas a instancias de TSP.

En nuestro caso, después de clusterizar las ubicaciones, utilizamos tsplib95 y Concorde para encontrar rutas óptimas o casi óptimas para cada cluster.

Consideraciones:
Aunque la solución proporcionada por Concorde es óptima o muy cercana al óptimo, es importante tener en cuenta que al dividir el problema mediante clusterización, estamos tomando una decisión que podría no ser óptima en el sentido global. Es decir, la suma de las rutas óptimas de los clusters individuales no necesariamente produce la solución óptima para todas las ubicaciones en conjunto.

El TSP no considera restricciones adicionales, como ventanas de tiempo, capacidades de vehículos, o preferencias específicas. Si tales restricciones son esenciales, se requieren formulaciones más complejas, como el TSP con Ventanas de Tiempo (TSPTW) o el Problema de Rutas de Vehículos (VRP).

### Optimización de Rutas:

Para cada cluster, se determina la secuencia óptima para visitar las ubicaciones utilizando el problema del viajante (TSP).
Por qué se hace: Aunque las ubicaciones en un cluster están geográficamente cercanas entre sí, el orden en que se visitan puede tener un impacto significativo en la distancia total recorrida. La optimización de rutas busca minimizar esta distancia.

### Visualización:

Se visualizan los clusters y las rutas óptimas en un mapa.
Por qué se hace: Una representación visual permite a los usuarios comprender mejor las rutas propuestas y tomar decisiones informadas si es necesario hacer ajustes manuales.

## Consideraciones
Elección del Algoritmo de Clusterización: DBSCAN fue elegido por su capacidad para identificar clusters de forma y tamaño variable. Sin embargo, es sensible a la elección de sus parámetros, especialmente eps, que determina la distancia máxima entre dos puntos para que se consideren en el mismo cluster. Es crucial elegir un valor adecuado para eps basado en el contexto geográfico y las distancias entre ubicaciones.

Complejidad del TSP: El problema del viajante es NP-hard, lo que significa que encontrar la solución óptima exacta es computacionalmente intensivo para un gran número de ubicaciones. En la práctica, se utilizan heurísticas o métodos aproximados para obtener soluciones cercanas al óptimo en un tiempo razonable.

Factores Externos: La optimización se basa únicamente en las coordenadas geográficas. No se tienen en cuenta otros factores como el tráfico, las horas de operación de las ubicaciones o las preferencias de los clientes. Es posible que se requieran ajustes manuales o la integración de datos adicionales para abordar estos aspectos.

Actualización de Datos: Las ubicaciones de los clientes, así como otros detalles, pueden cambiar con el tiempo. Es esencial que el proceso pueda repetirse periódicamente o cuando se requiera para reflejar cambios en los datos.

Seguridad de Datos: Las credenciales de la base de datos y otros detalles sensibles se almacenan en un archivo .env por razones de seguridad. Nunca deben ser expuestos o compartidos inapropiadamente.

Conclusión
La optimización de rutas basada en la clusterización es una herramienta poderosa para mejorar la eficiencia en logística y servicios. Al combinar técnicas de análisis espacial con algoritmos de optimización, es posible proporcionar soluciones prácticas y efectivas a desafíos del mundo real. Sin embargo, como con cualquier herramienta analítica, es esencial comprender sus limitaciones y asegurarse de que las soluciones propuestas sean viables en el contexto operativo.

# Evaluación de Clústeres mediante Métricas
El proceso de clusterización consiste en agrupar puntos de datos en clústeres de tal manera que los puntos en el mismo clúster sean más similares entre sí que con los puntos en otros clústeres. Para evaluar la calidad de estos clústeres, se utilizan diversas métricas. A continuación, te presento una descripción detallada de las métricas que hemos utilizado:

1. Silhouette Score:
Definición: El coeficiente de silueta mide qué tan cerca está cada punto de un clúster a los puntos en los clústeres vecinos. Los valores varían entre -1 y 1. Un valor alto indica que el objeto está bien emparejado con su propio clúster y mal emparejado con los clústeres vecinos.

Interpretación:

Valores cercanos a 1 indican que los puntos están lejos de los clústeres vecinos.
Un valor de 0 indica que los puntos están muy cerca de la decisión de límite entre dos clústeres vecinos.
Valores negativos indican que esos puntos podrían haberse asignado al clúster incorrecto.
Por qué es importante: Ayuda a determinar la distancia entre el clúster resultante y el clúster vecino, es decir, qué tan bien están definidos los clústeres.

2. Calinski Harabasz Score:
Definición: También conocido como el índice de varianza. Es el cociente entre la dispersión entre clústeres y la dispersión dentro del clúster. El score es mayor cuando los clústeres están densos y bien separados.

Interpretación:

Valores más altos indican una mejor definición de clúster.
Por qué es importante: Este score nos da una idea de la densidad y separación de los clústeres formados. Un score más alto es mejor, ya que indica que los clústeres están bien separados entre sí y los puntos dentro de un clúster están cerca entre sí.

3. Davies Bouldin Score:
Definición: Es el promedio de las similitudes entre cada clúster y su clúster más similar, donde la similitud es la relación entre las distancias dentro del clúster y las distancias entre clústeres.

Interpretación:

Valores más bajos indican una mejor separación entre clústeres.
Por qué es importante: El score Davies-Bouldin nos indica la similitud entre un clúster y su clúster más similar. Un valor bajo es deseable, ya que indica que los clústeres están más separados y, por lo tanto, están mejor definidos.

