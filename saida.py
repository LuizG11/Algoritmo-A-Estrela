import os
import shutil
import subprocess


def salvar_resultado(caminho_saida, caminho, custo_total, inicio, destino):
    with open(caminho_saida, "w", encoding="utf-8") as f:
        f.write(f"Busca A* de {inicio} até {destino}\n")
        f.write("=" * 40 + "\n\n")

        if caminho:
            f.write("Caminho encontrado:\n")
            f.write(" -> ".join(caminho) + "\n\n")
            f.write(f"Custo total: {custo_total}\n")
        else:
            f.write("Nenhum caminho encontrado entre os nós informados.\n")


def gerar_graphviz(caminho_dot, grafo, caminho):
    arestas_caminho = set()
    for i in range(len(caminho) - 1):
        arestas_caminho.add(frozenset((caminho[i], caminho[i + 1])))

    linhas = ["graph G {", "    rankdir=LR;", "    node [shape=circle];"]
    ja_desenhadas = set()

    for origem, vizinhos in grafo.items():
        for destino_no, custo in vizinhos:
            par = frozenset((origem, destino_no))
            if par in ja_desenhadas:
                continue
            ja_desenhadas.add(par)

            no_caminho = par in arestas_caminho
            cor = (
                'color="red", penwidth=2.5' if no_caminho else 'color="black"'
            )

            linhas.append(
                f'    "{origem}" -- "{destino_no}" [label="{custo}", {cor}];'
            )

    linhas.append("}")

    with open(caminho_dot, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas) + "\n")


def gerar_graphviz_passos(pasta_saida, grafo, coordenadas, historico_passos):
    if os.path.exists(pasta_saida):
        shutil.rmtree(pasta_saida)

    os.makedirs(pasta_saida, exist_ok=True)

    todos_nos = set(grafo.keys())
    for vizinhos in grafo.values():
        for v, _ in vizinhos:
            todos_nos.add(v)

    for passo_info in historico_passos:
        passo_num = passo_info["passo"]
        atual = passo_info["atual"]
        abertos = passo_info["abertos"]
        fechados = passo_info["fechados"]
        veio_de = passo_info["veio_de"]

        # Reconstrói o caminho percorrido especificamente até o nó 'atual' deste passo
        caminho_atual = []
        curr = atual
        while curr is not None:
            caminho_atual.append(curr)
            curr = veio_de.get(curr)

        arestas_caminho_atual = set()
        for i in range(len(caminho_atual) - 1):
            arestas_caminho_atual.add(
                frozenset((caminho_atual[i], caminho_atual[i + 1]))
            )

        caminho_dot = os.path.join(pasta_saida, f"passo_{passo_num:03d}.dot")
        caminho_png = os.path.join(pasta_saida, f"passo_{passo_num:03d}.png")

        linhas = [
            "graph G {",
            "    rankdir=LR;",
            "    node [shape=circle, style=filled];",
        ]

        # 1. Cores dos nós
        for no in sorted(todos_nos):
            if no == atual:
                cor = "#5DADE2"  # Azul (Nó atual em processamento)
            elif no in abertos:
                cor = "#F9E79F"  # Amarelo (Fronteira / Lista Aberta)
            elif no in fechados:
                cor = "#E5E8E8"  # Cinza Claro (Visitados / Lista Fechada)
            else:
                cor = "white"

            linhas.append(f'    "{no}" [fillcolor="{cor}"];')

        # 2. Arestas: destaca em vermelho APENAS o caminho reconstruído até o nó 'atual'
        ja_desenhadas = set()
        for origem, vizinhos in grafo.items():
            for destino_no, custo in vizinhos:
                par = frozenset((origem, destino_no))
                if par in ja_desenhadas:
                    continue
                ja_desenhadas.add(par)

                if par in arestas_caminho_atual:
                    cor_aresta = 'color="red", penwidth=2.5'
                else:
                    cor_aresta = 'color="black"'

                linhas.append(
                    f'    "{origem}" -- "{destino_no}" [label="{custo}", {cor_aresta}];'
                )

        linhas.append("}")

        with open(caminho_dot, "w", encoding="utf-8") as f:
            f.write("\n".join(linhas) + "\n")

        subprocess.run(
            ["dot", "-Tpng", caminho_dot, "-o", caminho_png], check=False
        )
