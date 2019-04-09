from graphviz import Digraph


CHAR_EMPTY = chr(1)
CHAR_ENDMARK = '#'
available_chars = 'abcdefghijklmnopqrstuvwxyz'
operands = '()*|.+'
position = 1


class Tree:
    """
    Узел дерева
    """

    def __init__(self, cargo):
        self.childs = list()
        self.cargo = cargo

    def __str__(self):
        return str(self.cargo)


def visualize_tree_node(root, fa_graph, level = 0, head_name = None):
    """
    :type root: Tree
    """
    root_str = f'{root}_{level}' if head_name is None else f'({head_name})_{root}_{level}'
    fa_graph.node(name=root_str, label=str(root))
    for child in root.childs:
        left_str = f'{child}_{level + 1}'
        fa_graph.edge(root_str, left_str)
        visualize_tree_node(child, fa_graph, level + 1)


def visualize_tree(root):
    fa_graph = Digraph('finite_state_machine')
    visualize_tree_node(root, fa_graph)
    fa_graph.view('tree')
