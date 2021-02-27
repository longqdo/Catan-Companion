import pygame

class Loc:
    def __init__ (self, row, col, coord, image, rect):
        self.row = row
        self.col = col
        self.coord = coord
        self.taken = False
        self.image = image
        self.rect = rect
        self.adj = set(())

    def __str__ (self):
        return str(('row: ', self.row, ", col: ", self.col))