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
En primera instancia se pretendió utilizar el solver "pomdp-solve" disponible en: http://www.pomdp.org/
Este solver utiliza el algoritmo de Iteración de valor. Sin embargo al realizar pruebas el tiempo de ejecución incrementaba 
exponencialmoente al aumentar el tamaño del tablero. Por lo cual se decidió utilizar el solver proporcionado por el
profesor Blai Bonet que utiliza el algoritmo RTDP-Bel, "gpt", el cual no presentó problema al tratar instancias más grandes. También se decidio usar este solver
pues informaba sobre la utilidad de la politica final encontrada por el solver.

Para todos los tableros existen dos estados sumideros con valores -1(bueno) y 1(malo),
mientras que el resto de los estados tienen un costo de -0.04.

Adicional a los casos aleatorios generados, se decidió incorporar casos construidos a manos donde la complejidad
del laberinto incrementara agregando los obstáculos de forma estructurada. Creemos que al agregar más obstáculos
se incrementa la cantidad de información "leible" por el agente lo que pudiera traducirse en un mayor reward. De 
igual forma, los tableros que sean estructuralmente similares deberían tener un reward cercano o igual.

Tamanho de los laberintos:

- 1x3
- 4x3
- 5x5
- 10x20

Todos los experimentos fueron realizados en una máquina con las siguientes especificaciones

i7-7700HQ 16GB RAM

### Resultados
Los parámetros utilizados para la ejecución del solver fueron:

  pims [8,2000,500]

  Los demás parámetros son los que utiliza el solver por defecto 

El solver devuelve mucha información útil, sin embargo, se hará énfasis en el resultado del Average Reward (rewardAvg),
pues representa la utilidad promedio de la política generada por el solver. 

En este sentido, a lo largo de las ejecuciones se puede notar que:

* En los tableros donde encontrar el goal positivo se dificulta o imposibilita, el reward siempre es negativo.
* En los tableros donde encontrar cualquiera de los dos goals se dificulta o se hace extenso, el reward es un número negativo muy pequeño.
Esto tiene sentido pues todos los demás movimientos tienen valor -0.04 y el solver trata de minimizar la pérdida.
* En los tableros grandes el reward suele ser negativo independientemente de la dificultad del laberinto pues
se acumulan movimeintos de valor -0.04. **Se sugiere utilizar un esquema de valor de acorde al tamaño del tablero para medir el desempeño**
* En tableros equivalentes (casos 3 y 4 de 1x3, casos 1 y 2 de 2x2) el reward es igual, como era esperado.
* En la mayoria de os tableros estructurados se percibe un reward mayor que en aquellos generados aleatoriamente.
Con la excepción del caso 4 de 10x20 donde, a pesar de que son estructurados, la naturaleza del laberinto 
difuclta que una política encuentre el + en la mayoría de los casos para 4. Puede notarse que en el caso 5 de 10x20
se tiene que el reward es similar al de los demás casos para ese tamaño de mapa donde el goal + es "facilmente" alcanzable

NOTA: TODOS LOS MAPAS ESTAN DIBUJADOS EN LOS POMDP

