import heapq
import itertools
import math


def distancia_euclidiana(coord_a, coord_b):
    xa, ya = coord_a
    xb, yb = coord_b
    return math.sqrt((xa - xb) ** 2 + (ya - yb) ** 2)


def a_star_search(grafo, coordenadas, inicio, destino):
    contador = itertools.count()

    h_inicio = distancia_euclidiana(coordenadas[inicio], coordenadas[destino])
    lista_aberta = [(h_inicio, next(contador), inicio, 0, None)]

    tabela_hash = {}
    veio_de = {}
    historico_passos = []  # Armazena os snapshots de cada iteração

    while lista_aberta:
        f_atual, _, atual, g_atual, pai = heapq.heappop(lista_aberta)

        if atual in tabela_hash:
            continue

        tabela_hash[atual] = g_atual
        veio_de[atual] = pai

        # Captura o estado atual da busca
        abertos = {item[2] for item in lista_aberta if item[2] not in tabela_hash}
        historico_passos.append({
            "passo": len(historico_passos) + 1,
            "atual": atual,
            "abertos": abertos,
            "fechados": set(tabela_hash.keys()),
            "veio_de": dict(veio_de)
        })

        if atual == destino:
            break

        for vizinho, custo_aresta in grafo.get(atual, []):
            if vizinho in tabela_hash:
                continue

            novo_custo = g_atual + custo_aresta
            h_vizinho = distancia_euclidiana(coordenadas[vizinho], coordenadas[destino])
            f_vizinho = novo_custo + h_vizinho

            heapq.heappush(
                lista_aberta, (f_vizinho, next(contador), vizinho, novo_custo, atual)
            )

    return veio_de, tabela_hash, historico_passos


def reconstruir_caminho(veio_de, inicio, destino):
    if destino not in veio_de:
        return []

    caminho = []
    atual = destino
    while atual is not None:
        caminho.append(atual)
        atual = veio_de.get(atual)

    caminho.reverse()

    if not caminho or caminho[0] != inicio:
        return []

    return caminho
