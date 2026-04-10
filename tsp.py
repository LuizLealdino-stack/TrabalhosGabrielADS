import math

def distancia(c1, c2):
    return math.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)

def tsp_vizinho_mais_proximo(cidades):
    visitadas = [False] * len(cidades)
    caminho = [0]
    visitadas[0] = True

    atual = 0
    total_distancia = 0

    for _ in range(len(cidades) - 1):
        menor_dist = float('inf')
        proxima = -1

        for i in range(len(cidades)):
            if not visitadas[i]:
                d = distancia(cidades[atual], cidades[i])
                if d < menor_dist:
                    menor_dist = d
                    proxima = i

        caminho.append(proxima)
        visitadas[proxima] = True
        total_distancia += menor_dist
        atual = proxima

    # volta para a cidade inicial
    total_distancia += distancia(cidades[atual], cidades[0])
    caminho.append(0)

    return caminho, total_distancia