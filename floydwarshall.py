import math

# ---------------------------------------------------
# Lectura del grafo desde archivo
# ---------------------------------------------------
def leer_grafo(nombre_archivo):
    vertices = set()
    aristas = []

    with open(nombre_archivo, "r") as f:
        for linea in f:
            u, v, w = linea.split()
            w = int(w)
            vertices.add(u)
            vertices.add(v)
            aristas.append((u, v, w))

    return list(vertices), aristas


# ---------------------------------------------------
# Floyd-Warshall con reconstrucción de camino
# ---------------------------------------------------
def floyd_warshall(vertices, aristas):
    n = len(vertices)
    indice = {v: i for i, v in enumerate(vertices)}

    # Inicialización DP
    dist = [[math.inf] * n for _ in range(n)]
    next_node = [[None] * n for _ in range(n)]

    for i in range(n):
        dist[i][i] = 0

    for u, v, w in aristas:
        i, j = indice[u], indice[v]
        dist[i][j] = w
        next_node[i][j] = j

    # Programación dinámica
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next_node[i][j] = next_node[i][k]

    return dist, next_node, indice


# ---------------------------------------------------
# Reconstrucción del camino más corto
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
# Ejecución principal
# ---------------------------------------------------
vertices, aristas = leer_grafo("grafo.txt")
dist, next_node, indice = floyd_warshall(vertices, aristas)

origen = "A"
destino = "E"

camino = reconstruir_camino(origen, destino, next_node, indice, vertices)
costo = dist[indice[origen]][indice[destino]]

print("Ruta más corta:", " -> ".join(camino))
print("Costo total:", costo)
