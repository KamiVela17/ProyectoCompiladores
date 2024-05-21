class Node:
    def __init__(self, data):
        self._data = data
        self._children = []

    def get_data(self):
        return self._data

    def get_children(self):
        return self._children

    def add(self, node):
        self._children.append(node)

    def print_node(self, prefix):
        print('  ' * prefix, '+', self._data)
        for child in self._children:
            child.print_node(prefix + 1)
