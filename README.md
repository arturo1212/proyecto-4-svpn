# proyecto-4-svpn
POMDP
Se desea construir un programa que, dada una instancia del tablero de Russel-Norvig,
genere un archivo en formato Cassandra que pueda ser utilizado por un solver de POMDP
para hallar políticas que mejoren la utilidad del camino seleccionado.

El solver con el que se realizarán las pruebas implementa el algoritmo RTDP-Bel y puede encontrarse en:
https://github.com/bonetblai/gpt-rewards

## Solución
Se construyó un script en python 3.5 que recibe un archivo llamado "generador.py" que permite
especificar las dimensiones de un tablero (NxM), el número de obstáculos (O) y genera K instancias del
tablero con las características dadas. Esto genera un archivo con extensión ".cases" con K+1 lineas,
en donde la primera linea contiene las direcciones del tablero y en cada una de las lineas siguientes se guardan las instancias
Cada instancia consiste en vectores con los valores: 10 (obstáculos) 0, (casillas libres), 1 (recompensa) y 5 (penalización).

Por otro lado, se implementó un script llamado "translator.py" que recibe un archivo de extensión ".cases" y genera
el archivo ".POMDP" para cada una de las instancias.
Esto se logra recorriendo cada posición del tablero y creando las transiciones, observaciones y recompensas con una exhaustividad
de casos para cada posible acción. En este sentido, los casos de las observaciones y las recompensas son inmediatos, mientras que para las transiciones es necesario notar que el
rebote en una pared conlleva a la suma de la probabilidad del desplazamiento al estado inicial.

## Experimentos
En primera instancia se decidió utilizar el solver "pomdp-solve" disponible en: http://www.pomdp.org/
Este solver utiliza el algoritmo de Iteración de valor y al realizar pruebas fue posible notar que el tiempo de ejecución
se incrementaba rápidamente al aumentar el tamaño del tablero, lo cual no ocurría con el solver proporcionado por el
profesor Blai Bonet. Por esto, decidimos descartar el uso de "pomdp-solve"

Adicional a los casos aleatorios generados, se decidió incorporar casos construidos a manos donde la complejidad
del laberinto incrementara agregando los obstáculos de forma estructurada.

DECIR CUALES CASOS 

Todos los experimentos fueron realizados en un equipo con las siguientes especificaciones
-- SPECS DE DAVID --

### Resultados
Los parámetros utilizados para la ejecución del solver fueron:

---------- INSERTAR PARÁMETROS AQUI ------------

El solver devuelve mucha información útil, sin embargo, se hará énfasis en el resultado del Average Reward (AR),
pues representa la utilidad promedio de la política generada por el solver. En este sentido, a lo largo de las ejecuciones se puede notar que
la utilidad obtenida es negativa pero cercana a cero, lo cual tiene sentido debido a que existen dos estados sumideros con valores -1 y 1,
mientras que el resto de los estados tienen un costo de -0.04.

Esto indica que las políticas obtenidas buscan reducir el costo del plan para evitar sufrir penalizaciones altas.
A continuación se presentan los resultados para las instancias seleccionadas:

--- DATOS DE LAS INSTANCIAS ---

