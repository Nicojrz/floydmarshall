import math

# ---------------------------------------------------
# Crear matriz de adyacencia desde archivo
# ---------------------------------------------------
def leer_grafo_matriz(nombre_archivo):
    vertices = set()
    aristas = []

    with open(nombre_archivo, "r") as f:
        for linea in f:
            u, v, w = linea.split()
            w = int(w)
            vertices.add(u)
            vertices.add(v)
            aristas.append((u, v, w))

    vertices = sorted(vertices)
    n = len(vertices)
    indice = {v: i for i, v in enumerate(vertices)}

    # Inicializar matriz de adyacencia
    matriz = [[math.inf] * n for _ in range(n)]
    for i in range(n):
        matriz[i][i] = 0

    for u, v, w in aristas:
        i, j = indice[u], indice[v]
        matriz[i][j] = w

    return matriz, vertices, indice

def imprimir_matriz(matriz, vertices):
    print("Matriz de adyacencia:")
    print("    ", end="")

    # Encabezado de columnas
    for v in vertices:
        print(f"{v:>4}", end="")
    print()

    # Filas
    for i, fila in enumerate(matriz):
        print(f"{vertices[i]:>4}", end="")
        for valor in fila:
            if valor == float('inf'):
                print(f"{'-':>4}", end="")
            else:
                print(f"{valor:>4}", end="")
        print()

# ---------------------------------------------------
# Floyd-Warshall con matriz de adyacencia
# ---------------------------------------------------
def floyd_warshall(matriz):
    n = len(matriz)
    dist = [fila[:] for fila in matriz]

    next_node = [[None] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if matriz[i][j] != math.inf and i != j:
                next_node[i][j] = j

    # Programación dinámica
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next_node[i][j] = next_node[i][k]

    return dist, next_node


# ---------------------------------------------------
# Reconstrucción del camino (origen -> destino)
# ---------------------------------------------------
def reconstruir_camino(origen, destino, next_node, indice, vertices):
    i = indice[origen]
    j = indice[destino]

    if next_node[i][j] is None:
        return None

    camino = [origen]
    while i != j:
        i = next_node[i][j]
        camino.append(vertices[i])

    return camino


# ---------------------------------------------------
# Función para ejecutar consulta intercambiable
# ---------------------------------------------------
def camino_mas_corto(origen, destino, dist, next_node, indice, vertices):
    camino = reconstruir_camino(origen, destino, next_node, indice, vertices)
    costo = dist[indice[origen]][indice[destino]]

    if camino is None:
        print("No existe camino entre", origen, "y", destino)
    else:
        print(f"Ruta más corta de {origen} a {destino}:")
        print(" -> ".join(camino))
        print("Costo:", costo)


# ---------------------------------------------------
# Programa principal
# ---------------------------------------------------
matriz, vertices, indice = leer_grafo_matriz("grafo.txt")
imprimir_matriz(matriz, vertices)
dist, next_node = floyd_warshall(matriz)

# Se puede intercambiar libremente
camino_mas_corto("A", "E", dist, next_node, indice, vertices)
print()
camino_mas_corto("E", "A", dist, next_node, indice, vertices)
