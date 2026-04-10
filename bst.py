class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None


# INSERÇÃO
    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if node is None:
            return Node(key)

        if key < node.key:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)

        return node

    # BUSCA
    def search(self, key):
        return self._search(self.root, key)

    def _search(self, node, key):
        if node is None or node.key == key:
            return node

        if key < node.key:
            return self._search(node.left, key)

        return self._search(node.right, key)

    # ALTURA
    def height(self):
        return self._height(self.root)

    def _height(self, node):
        if node is None:
            return -1
        return 1 + max(self._height(node.left), self._height(node.right))

    # REMOÇÃO
    def remove(self, key):
        self.root = self._remove(self.root, key)

    def _remove(self, node, key):
        if node is None:
            return None

        if key < node.key:
            node.left = self._remove(node.left, key)

        elif key > node.key:
            node.right = self._remove(node.right, key)

        else:
            # Caso 1: sem filhos
            if node.left is None and node.right is None:
                return None

            # Caso 2: um filho
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left

            # Caso 3: dois filhos
            temp = self._min_value(node.right)
            node.key = temp.key
            node.right = self._remove(node.right, temp.key)

        return node

    def _min_value(self, node):
        while node.left:
            node = node.left
        return node

