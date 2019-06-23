#  Deals with the making of the board along with the aesthetics of the letters.

import pygame

width = 600
height = 600
screen = pygame.display.set_mode((width, height))


class Letters(pygame.sprite.Sprite):
    def __init__(self, word, board, row, col, xpadding=0, ypadding=0, fol="letters", type="multi", check=False):
        pygame.sprite.Sprite.__init__(self)
        self.word = word
        self.r = 40
        if board == None:
            self.border = width // 4
        else:
            self.border = width//len(board)
        self.cx = self.border//1.5 + col*self.r*2
        self.cy = int(self.border//2 + row*self.r*2)
        self.letter = ""
        self.row = row
        self.col = col
        self.fol = fol
        self.xpadding = xpadding
        self.ypadding = ypadding
        self.board = board
        self.letter, self.fol = self.drawBoard(board, row, col, xpadding, ypadding, fol, self.cx, self.cy)
        r = self.r - 10
        if type == "solo" and check:
            for i in range(len(word)):
                for j in range(len(word[i])):
                    start = (width - (r * 2 * len(word[i]))) // 2 + (j * r * 2)
                    end = start + r * 2
                    pygame.draw.line(screen, (0, 0, 0), (start, 475 + (i*50)), (end - 10, 475 + (i*50)), 5)

        elif type == "multi":
            for i in range(len(word)):
                start = (width - (r * 2 * len(word))) // 2 + (i * r * 2)
                end = start + r * 2
                pygame.draw.line(screen, (0, 0, 0), (start, 550), (end - 10, 550), 5)

    def position(self):
        return self.cx+50, self.cy+40 + self.col*6

    def index(self):
        return self.row, self.col

    def getHashables(self):
        return self.word[0]  # returns a tuple of hashables

    def __hash__(self):  # for sets
        return hash(self.getHashables())

    def __repr__(self):
        return str(self.word)

    @staticmethod
    def drawBoard(boards, row, col, xpadding, ypadding, fol, cx, cy):
        if len(boards) > 4:
            xpadding = 50
            ypadding = 30
            if col > 0:
                xpadding -= 10 * col
            if row > 0:
                ypadding -= 10 * row

        if boards[row][col] != 0:
            scale = 80
            image1 = pygame.image.load("images/" + fol + "/" + str(boards[row][col]) + ".png").convert_alpha()
            if len(boards) > 4:
                scale = 60
            image1 = pygame.transform.scale(image1, (scale, scale))
            rect = image1.get_rect()
            rect.topleft = [cx + xpadding, cy + ypadding]
            screen.blit(image1, rect)
        letter = boards[row][col]
        fol = "letters"
        return letter, fol
