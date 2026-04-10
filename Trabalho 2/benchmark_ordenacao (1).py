"""
PROJETO III – Benchmark de Ordenação
Algoritmos: Bubble Sort e Quick Sort
Análise: Melhor caso, Caso Médio e Pior Caso
"""

import time
import random
import statistics
import math

# ─────────────────────────────────────────────
#  ALGORITMOS
# ─────────────────────────────────────────────

def bubble_sort(arr):
    comparacoes = 0
    trocas = 0
    n = len(arr)
    arr = arr[:]
    for i in range(n):
        trocado = False
        for j in range(0, n - i - 1):
            comparacoes += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                trocas += 1
                trocado = True
        if not trocado:
            break
    return arr, comparacoes, trocas


def quick_sort(arr):
    comparacoes = [0]
    trocas = [0]
    arr = arr[:]

    def particionar(a, baixo, alto):
        pivo = a[alto]
        i = baixo - 1
        for j in range(baixo, alto):
            comparacoes[0] += 1
            if a[j] <= pivo:
                i += 1
                a[i], a[j] = a[j], a[i]
                trocas[0] += 1
        a[i + 1], a[alto] = a[alto], a[i + 1]
        trocas[0] += 1
        return i + 1

    def _quick(a, baixo, alto):
        if baixo < alto:
            pi = particionar(a, baixo, alto)
            _quick(a, baixo, pi - 1)
            _quick(a, pi + 1, alto)

    import sys
    sys.setrecursionlimit(100_000)
    _quick(arr, 0, len(arr) - 1)
    return arr, comparacoes[0], trocas[0]


# ─────────────────────────────────────────────
#  GERACAO DE ARRAYS
# ─────────────────────────────────────────────

def gerar_melhor_caso(n, algoritmo):
    if algoritmo == "bubble":
        return list(range(n))
    else:
        return list(range(n // 2, n)) + list(range(n // 2))


def gerar_caso_medio(n, _=None):
    arr = list(range(n))
    random.shuffle(arr)
    return arr


def gerar_pior_caso(n, algoritmo):
    if algoritmo == "bubble":
        return list(range(n, 0, -1))
    else:
        return list(range(n))


# ─────────────────────────────────────────────
#  BENCHMARK
# ─────────────────────────────────────────────

TAMANHOS   = [100, 500, 1_000, 2_000, 5_000]
REPETICOES = 10


def medir(func, arr):
    inicio = time.perf_counter()
    _, comp, troc = func(arr)
    fim = time.perf_counter()
    return fim - inicio, comp, troc


def executar_benchmark():
    resultados = {}
    algoritmos = {
        "Bubble Sort": (bubble_sort, "bubble"),
        "Quick Sort" : (quick_sort,  "quick"),
    }
    casos = {
        "Melhor Caso": gerar_melhor_caso,
        "Caso Medio" : gerar_caso_medio,
        "Pior Caso"  : gerar_pior_caso,
    }

    total = len(algoritmos) * len(casos) * len(TAMANHOS) * REPETICOES
    atual = 0

    for nome_alg, (func, tag) in algoritmos.items():
        resultados[nome_alg] = {}
        for nome_caso, gerar in casos.items():
            resultados[nome_alg][nome_caso] = {
                "tamanhos"      : TAMANHOS,
                "tempos_media"  : [],
                "tempos_desvio" : [],
                "tempos_min"    : [],
                "tempos_max"    : [],
                "comp_media"    : [],
                "trocas_media"  : [],
            }
            for n in TAMANHOS:
                tempos, comps, trocs = [], [], []
                for _ in range(REPETICOES):
                    arr = gerar(n, tag)
                    t, c, tr = medir(func, arr)
                    tempos.append(t)
                    comps.append(c)
                    trocs.append(tr)
                    atual += 1
                    print(f"  [{atual}/{total}] {nome_alg} | {nome_caso} | n={n}", end="\r")

                r = resultados[nome_alg][nome_caso]
                r["tempos_media"].append(statistics.mean(tempos))
                r["tempos_desvio"].append(statistics.stdev(tempos) if len(tempos) > 1 else 0)
                r["tempos_min"].append(min(tempos))
                r["tempos_max"].append(max(tempos))
                r["comp_media"].append(statistics.mean(comps))
                r["trocas_media"].append(statistics.mean(trocs))

    print("\nBenchmark concluido!\n")
    return resultados


# ─────────────────────────────────────────────
#  COMPLEXIDADE TEORICA
# ─────────────────────────────────────────────

def complexidade_teorica(n, caso, algoritmo):
    if algoritmo == "Bubble Sort":
        return n - 1 if caso == "Melhor Caso" else n * (n - 1) / 2
    else:
        return n * (n - 1) / 2 if caso == "Pior Caso" else n * math.log2(n) if n > 1 else 1


# ─────────────────────────────────────────────
#  TABELA DE RESULTADOS
# ─────────────────────────────────────────────

def imprimir_tabela(resultados):
    print("=" * 95)
    print(f"{'ANALISE ESTATISTICA - BENCHMARK DE ORDENACAO':^95}")
    print("=" * 95)

    for nome_alg, casos in resultados.items():
        print(f"\n{'─' * 95}")
        print(f"  Algoritmo: {nome_alg}")
        print(f"{'─' * 95}")
        print(f"  {'Caso':<13} {'n':>6}  {'Media(ms)':>10} {'Desvio(ms)':>11} "
              f"{'Min(ms)':>9} {'Max(ms)':>9} {'Comparacoes':>13} {'Trocas':>11} {'CV%':>7}")
        print(f"  {'─' * 88}")
        for nome_caso, d in casos.items():
            for i, n in enumerate(d["tamanhos"]):
                media  = d["tempos_media"][i]  * 1000
                desvio = d["tempos_desvio"][i] * 1000
                mn     = d["tempos_min"][i]    * 1000
                mx     = d["tempos_max"][i]    * 1000
                comp   = int(d["comp_media"][i])
                troc   = int(d["trocas_media"][i])
                cv     = (desvio / media * 100) if media > 0 else 0
                print(f"  {nome_caso:<13} {n:>6}  {media:>10.4f} {desvio:>11.4f} "
                      f"{mn:>9.4f} {mx:>9.4f} {comp:>13,} {troc:>11,} {cv:>6.1f}%")
            print()

    print(f"{'─' * 95}")
    print("  CORRELACAO TEORIA x PRATICA  (comparacoes, n = 5000)")
    print(f"  {'─' * 88}")
    print(f"  {'Algoritmo':<13} {'Caso':<13} {'Teorico':>16} {'Pratico':>16} {'Razao':>10}")
    for nome_alg, casos in resultados.items():
        for nome_caso, d in casos.items():
            n     = d["tamanhos"][-1]
            prat  = d["comp_media"][-1]
            teor  = complexidade_teorica(n, nome_caso, nome_alg)
            razao = prat / teor if teor else float("inf")
            print(f"  {nome_alg:<13} {nome_caso:<13} {int(teor):>16,} {int(prat):>16,} {razao:>9.4f}x")
    print()


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("   PROJETO III - Benchmark de Ordenacao")
    print("   Algoritmos : Bubble Sort x Quick Sort")
    print("   Repeticoes :", REPETICOES)
    print("   Tamanhos   :", TAMANHOS)
    print("=" * 60 + "\n")

    resultados = executar_benchmark()
    imprimir_tabela(resultados)
