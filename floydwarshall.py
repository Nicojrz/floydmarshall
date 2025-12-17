INF = float('inf')

def leer_matriz_W(nombre_archivo):
    matriz = []

    with open(nombre_archivo, "r") as archivo:
        for linea in archivo:
            fila = []
            elementos = linea.split()

            for valor in elementos:
                if valor.upper() == "INF":
                    fila.append(INF)
                else:
                    fila.append(int(valor))

            matriz.append(fila)

    return matriz

# ---------------------------------------------------
def imprimir_matriz(matriz, titulo):
    print("\n" + titulo)
    for fila in matriz:
        for valor in fila:
            if valor == INF:
                print(f"{'∞':>4}", end=" ")
            else:
                print(f"{valor:>4}", end=" ")
        print()


# ---------------------------------------------------
def floyd_warshall(W):
    n = len(W)

    dist = [[INF for _ in range(n)] for _ in range(n)]
    succ = [[-1 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(n):
            dist[i][j] = W[i][j]

            if W[i][j] != INF and i != j:
                succ[i][j] = j

        dist[i][i] = 0
        succ[i][i] = i
        
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    succ[i][j] = succ[i][k]

    return dist, succ


# ---------------------------------------------------
def construir_camino(succ, origen, destino):
    if succ[origen][destino] == -1:
        return []

    camino = []
    actual = origen

    while actual != destino:
        camino.append(actual)
        actual = succ[actual][destino]

    camino.append(destino)
    return camino

# ---------------------------------------------------
def imprimir_camino(camino):
    if not camino:
        print("No existe camino entre los vértices.")
        return

    print("Camino más corto:")
    for i in range(len(camino)):
        if i != len(camino) - 1:
            print(camino[i], "->", end=" ")
        else:
            print(camino[i])

# main ---------------------------------------------------
def main():
    nombre_archivo = input("Nombre del archivo con la matriz W: ")

    W = leer_matriz_W(nombre_archivo)

    imprimir_matriz(W, "Matriz de adyacencia W:")

    dist, succ = floyd_warshall(W)

    imprimir_matriz(dist, "Matriz de distancias mínimas:")
    imprimir_matriz(succ, "Matriz de sucesores:")

    origen = int(input("\nVértice origen (índice): "))
    destino = int(input("Vértice destino (índice): "))

    camino = construir_camino(succ, origen, destino)
    imprimir_camino(camino)

    if camino:
        print("Costo total:", dist[origen][destino])

if __name__ == "__main__":
    main()