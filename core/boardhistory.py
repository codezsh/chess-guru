class MoveNode:
    def __init__(self, move=None, parent=None):
        self.move = move  # Dict with from/to/piece/capture/etc.
        self.parent = parent
        self.children = []  # All variation continuations
        self.selected_child = 0  # Index of mainline


class MoveTree:
    def __init__(self):
        self.root = MoveNode()  # Root node, empty move
        self.current = self.root

    def add_move(self, move_dict):
        new_node = MoveNode(move=move_dict, parent=self.current)
        self.current.children.append(new_node)
        self.current.selected_child = len(self.current.children) - 1
        self.current = new_node

    def undo(self):
        if self.current.parent:
            self.current = self.current.parent

    def redo(self):
        if self.current.children:
            self.current = self.current.children[self.current.selected_child]

    def jump_to(self, node):
        self.current = node
