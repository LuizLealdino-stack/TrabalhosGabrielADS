from bst import BST
from avl import AVL
from rubro_negra import RedBlackTree

valores = [10, 20, 30, 40, 50, 25]

# ===== BST =====

bst = BST()
for v in valores:
    bst.insert(v)

print("BST altura:", bst.height())
print("BST buscar 25:", bst.search(25) is not None)

# ===== AVL =====

avl = AVL()
for v in valores:
    avl.insert(v)

print("AVL altura:", avl.get_height())
print("AVL buscar 25:", avl.search(25) is not None)

# ===== RUBRO-NEGRA =====

rb = RedBlackTree()
for v in valores:
    rb.insert(v)

print("RB altura:", rb.height())
print("RB buscar 25:", rb.search(25) is not None)
# ===== TSP ===== 
from tsp import tsp_vizinho_mais_proximo

cidades = [(0, 0), (1, 5), (5, 2), (6, 6), (8, 3)]

caminho, distancia_total = tsp_vizinho_mais_proximo(cidades)

print("Caminho TSP:", caminho)
print("Distância total:", distancia_total)
 