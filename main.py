import os

from astar import a_star_search, reconstruir_caminho
from saida import gerar_graphviz, gerar_graphviz_passos, salvar_resultado

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMINHO_GRAFO = os.path.join(BASE_DIR, "dados", "grafo.txt")
CAMINHO_RESULTADO = os.path.join(BASE_DIR, "dados", "resultado.txt")
CAMINHO_DOT = os.path.join(BASE_DIR, "dados", "grafo.dot")
PASTA_PASSOS = os.path.join(BASE_DIR, "dados", "passos")

INICIO = "N0"
DESTINO = "N19"


def ler_grafo(caminho):
    nos = []
    grafo = {}
    coordenadas = {}

    with open(caminho, "r", encoding="utf-8") as f:
        linhas = [linha.strip() for linha in f]

    for linha in linhas:  # ignora linhas vazias/comentarios
        if not linha or linha.startswith("#"):
            continue

        partes = linha.split()

        if len(partes) != 3:
            continue  # linha em formato inesperado, ignora

        primeiro, segundo, terceiro = partes
        eh_linha_de_no = _eh_numero(segundo) and _eh_numero(terceiro)
        # diferencia no (nome x y) de aresta (origem destino custo) vendo se o segundo e numero

        if eh_linha_de_no:
            nome = primeiro
            x, y = float(segundo), float(terceiro)
            nos.append(nome)
            coordenadas[nome] = (x, y)
            grafo.setdefault(nome, [])
        else:
            origem, destino, custo = primeiro, segundo, float(terceiro)
            grafo.setdefault(origem, []).append((destino, custo))
            grafo.setdefault(destino, []).append((origem, custo))  # bidirecional

    return nos, grafo, coordenadas


def _eh_numero(texto):  # true se o texto pode ser convertido p/ float
    try:
        float(texto)
        return True
    except ValueError:
        return False


def main():
    nos, grafo, coordenadas = ler_grafo(CAMINHO_GRAFO)

    print("Nós encontrados:", nos)
    print("\nCoordenadas:")
    for no, (x, y) in coordenadas.items():
        print(f"  {no}: ({x}, {y})")
    print("\nLista de adjacência:")
    for no, vizinhos in grafo.items():
        print(f"  {no}: {vizinhos}")

    # Recebe os 3 retornos da busca, incluindo o histórico para depuração
    veio_de, tabela_hash, historico_passos = a_star_search(
        grafo, coordenadas, INICIO, DESTINO
    )
    caminho = reconstruir_caminho(veio_de, INICIO, DESTINO)

    print(f"\nBusca A* de {INICIO} até {DESTINO}:")
    if caminho:
        print("  Caminho encontrado:", " -> ".join(caminho))
        print("  Custo total:", tabela_hash.get(DESTINO))
    else:
        print("  Nenhum caminho encontrado entre os nós informados.")

    custo_total = tabela_hash.get(DESTINO)
    salvar_resultado(CAMINHO_RESULTADO, caminho, custo_total, INICIO, DESTINO)
    gerar_graphviz(CAMINHO_DOT, grafo, caminho)

    # Gera os arquivos .dot e .png para cada passo do algoritmo
    gerar_graphviz_passos(PASTA_PASSOS, grafo, coordenadas, historico_passos)

    print(f"\nResultado salvo em: {CAMINHO_RESULTADO}")
    print(f"Código Graphviz salvo em: {CAMINHO_DOT}")
    print(f"Passos da depuração salvos na pasta: {PASTA_PASSOS}")


if __name__ == "__main__":
    main()
