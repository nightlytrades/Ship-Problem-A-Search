class Node:

    def __init__(self, parent=None, board=None, children=None):
        self.parent = parent
        self.board = board
        self.children = children

        self.g = 0
        self.h = 0
        self.f = 0


    def __eq__(self, other):
        return self.position == other.position

    def set_h(self, h):
        self.h = h
    
    def set_g(self, g):
        self.g = g

    def set_f(self, f):
        self.f = f

    def set_parent(self, parent):
        self.parent = parent

    def set_children(self, children):
        self.children.append(children)

    def set_board(self, board):
        self.board = board

    def get_h(self):
        return self.h

    def get_g(self):
        return self.g

    def get_f(self):
        return self.f

    def get_parent(self):
        return self.parent

    def get_children(self):
        return self.children
    
    def get_board(self):
        return self.board


