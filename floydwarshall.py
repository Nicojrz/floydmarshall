import math

INF = float('inf')

def leer_grafo_matriz_no_dirigido(nombre_archivo):
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

    matriz = [[INF] * n for _ in range(n)]
    for i in range(n):
        matriz[i][i] = 0

    for u, v, w in aristas:
        i, j = indice[u], indice[v]
        matriz[i][j] = w
        matriz[j][i] = w

    return matriz, vertices, indice

def imprimir_matriz(matriz, vertices):
    print("\nMatriz de adyacencia:")
    print("    ", end="")
    for v in vertices:
        print(f"{v:>4}", end="")
    print()

    for i, fila in enumerate(matriz):
        print(f"{vertices[i]:>4}", end="")
        for val in fila:
            if val == INF:
                print(f"{'∞':>4}", end="")
            else:
                print(f"{val:>4}", end="")
        print()

def floyd_warshall(matriz):
    n = len(matriz)
    dist = [fila[:] for fila in matriz]

    next_node = [[None] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if matriz[i][j] != INF and i != j:
                next_node[i][j] = j

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next_node[i][j] = next_node[i][k]

    return dist, next_node

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

def camino_mas_corto(origen, destino, dist, next_node, indice, vertices):
    if origen == destino:
        print("\nOrigen y destino son el mismo vértice.")
        print("Ruta:", origen)
        print("Costo: 0")
        return

    if origen not in indice or destino not in indice:
        print("\nError: vértice no existente en el grafo.")
        return

    camino = reconstruir_camino(origen, destino, next_node, indice, vertices)
    costo = dist[indice[origen]][indice[destino]]

    if camino is None or costo == INF:
        print(f"\nNo existe camino entre {origen} y {destino}")
    else:
        print(f"\nRuta más corta de {origen} a {destino}:")
        print(" -> ".join(camino))
        print("Costo:", costo)

def main():
    archivo = input("Nombre del archivo del grafo: ")

    try:
        matriz, vertices, indice = leer_grafo_matriz_no_dirigido(archivo)
    except FileNotFoundError:
        print("Error: archivo no encontrado.")
        return

    imprimir_matriz(matriz, vertices)

    dist, next_node = floyd_warshall(matriz)

    origen = input("\nVértice origen: ").strip()
    destino = input("Vértice destino: ").strip()

    camino_mas_corto(origen, destino, dist, next_node, indice, vertices)

if __name__ == "__main__":
    main()