
#  Creates the different screens along with calling other classes to handle all the modes in the game
#  A lot of style is involved in making sure the screens look right and function when an even is triggered

import wordCluttered
import pygame, math, random


width = 600
height = 600
screen = pygame.display.set_mode((width, height))


class Screen(pygame.sprite.Sprite):  # Switch between pages
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.mainScreen()

    def mainScreen(self):
        pygame.init()
        pygame.display.update()
        pygame.display.set_caption("Main Menu")
        background = pygame.Surface(screen.get_size())
        background.fill((1, 150, 119))
        screen.blit(background, (0, 0))
        image1 = pygame.image.load("images/logo.png").convert_alpha()
        image1 = pygame.transform.scale(image1, (500, 200))
        rect = pygame.draw.rect(screen, (1, 150, 119), (200, 400, 400, 600))
        rect.center = [250, 110]
        screen.blit(image1, rect)

    @staticmethod
    def instruction():
        background = pygame.Surface(screen.get_size())
        background.fill((1, 150, 119))
        screen.blit(background, (0, 0))
        pygame.display.set_caption("Instruction")
        myfont = pygame.font.SysFont("serif", 20)
        # render text

        image1 = pygame.image.load("images/IN.png").convert_alpha()
        #image1 = pygame.transform.scale(image1,(50,50))
        rect = pygame.draw.rect(screen, (1, 150, 119), (200, 400, 400, 600))
        rect.center = [225, 110]
        screen.blit(image1, rect)
        Multi.mainMenu((375, 100), 300, 500)

    @staticmethod
    def soloMode():
        background = pygame.Surface(screen.get_size())
        background.fill((1, 150, 119))
        screen.blit(background, (0, 0))
        pygame.display.set_caption("Solo Mode")


class Instruct(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/instructions.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (350, 100))
        self.instruct()

    def instruct(self):
        self.rect.center = [300, 300]
        screen.blit(self.image, self.rect)


class Multi(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image1 = pygame.image.load("images/multiplayer.png").convert_alpha()
        self.rect = self.image1.get_rect()
        self.image1 = pygame.transform.scale(self.image1, (350, 100))
        self.multi()

    def multi(self):
        self.rect.center = [300, 420]
        screen.blit(self.image1, self.rect)

    @staticmethod
    def timesUp(score):
        background = pygame.Surface(screen.get_size())
        background.fill((1, 150, 119))
        screen.blit(background, (0, 0))

        pygame.display.set_caption("Time is up!")
        myfont = pygame.font.SysFont("serif", 50)
        # render text
        label = myfont.render("Final Score %d" % score, True, (0, 0, 0))
        screen.blit(label, (200, 200))

        Multi.mainMenu((375, 100), 300, 420)

    @staticmethod
    def mainMenu(size, x, y):
        image = pygame.image.load("images/mm.png").convert_alpha()
        rect = image.get_rect()
        image = pygame.transform.scale(image, size)
        rect.center = [x, y]
        screen.blit(image, rect)
        pygame.display.update()
        keep = True

        while keep:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    keep = False

            pressed1, pressed2, pressed3 = pygame.mouse.get_pressed()
            if pressed1:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                if rect.collidepoint(x, y):
                    wordCluttered.run()
                    keep = False
                    break

            pygame.display.flip()
        pygame.mouse.set_visible(True)
        pygame.quit()


class Solo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image2 = pygame.image.load("images/solo.png").convert_alpha()
        self.rect = self.image2.get_rect()
        self.image2 = pygame.transform.scale(self.image2, (350, 100))
        self.solo()

    def solo(self):
        self.rect.center = [300, 540]
        screen.blit(self.image2, self.rect)


    @staticmethod
    def game(wordList):

        boardLength = 0
        for i in range(len(wordList)):
            boardLength += len(wordList[i])

        boardLength = math.ceil(boardLength**0.5)
        board = [[0 for x in range(boardLength)] for y in range(boardLength)]
        for i in range(len(wordList)):
            board = Solo.game1(wordList[i], board)
            if board == None:
                Solo.game(wordList)
                return board

        return board

    @staticmethod
    def game1(word, board, error=0):
        tempBoard = [[0 for x in range(len(board))] for y in range(len(board))]
        for row in range(len(board)):
            for col in range(len(board[0])):
                tempBoard[row][col] = board[row][col]
        rows, cols = Solo.findZero(board)

        if rows is not None:
            try:
                board = Solo.makepuzzle(board, word, rows, cols, 0)
            except:
                if error > 5:
                    return None
                board = Solo.game1(word,  tempBoard, error+1)
        return board

    @staticmethod
    def makepuzzle(board, word, x, y, index):
        while index < len(word):

            pos = Solo.findAdjacent(board, x, y)
            rows, cols = pos[random.randint(0, len(pos)-1)]

            board[rows][cols] = word[index]
            index += 1
            x = rows
            y = cols

        return board

    @staticmethod
    def findAdjacent(board, x, y):
        pos = []
        for row in range(len(board)):
            for col in range(len(board[0])):
                if board[row][col] == 0 and abs(row-x) <= 1 and abs(col-y) <= 1:
                    pos.append((row, col))

        return pos

    @staticmethod
    def findZero(board):
        found = False
        while not found:
            rows = random.randint(0, len(board) - 1)
            cols = random.randint(0, len(board) - 1)
            if board[rows][cols] == 0:
                return rows, cols
            elif Solo.isFull(board):
                return None, None

    @staticmethod
    def isFull(board):
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 0:
                    return False
        return True

    @staticmethod
    def oneAway(row, col, rows, cols):
        if (abs(rows - row) == 1 or rows - row == 0) and (abs(cols - col) == 1 or cols - col == 0):
            return True
        return False

# Taken from 112 website notes
def maxItemLength(a):
    maxLen = 0
    rows = len(a)
    cols = len(a[0])
    for row in range(rows):
        for col in range(cols):
            maxLen = max(maxLen, len(str(a[row][col])))
    return maxLen


# Taken from 112 website notes
def print2dList(a):
    if (a == []):
        # So we don't crash accessing a[0]
        print([])
        return
    rows = len(a)
    cols = len(a[0])
    fieldWidth = maxItemLength(a)
    print("[ ", end="")
    for row in range(rows):
        if (row > 0): print("\n  ", end="")
        print("[ ", end="")
        for col in range(cols):
            if (col > 0): print(", ", end="")
            # The next 2 lines print a[row][col] with the given fieldWidth
            formatSpec = "%" + str(fieldWidth) + "s"
            print(formatSpec % str(a[row][col]), end="")
        print(" ]", end="")
    print("]")

