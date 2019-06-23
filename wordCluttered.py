# Adriana Martinez, amartin1

#  Main file that runs the entire game

from letters import Letters
import screen
from datamuse import Datamuse
import scripts
from random_words import RandomWords
import pygame
from wordnik import*

pygame.init()
width = 600
height = 600
screen1 = pygame.display.set_mode((width, height))
pygame.display.update()
myfont = pygame.font.SysFont("serif", 50)
guess = []

pygame.draw.rect(screen1, (59, 103, 191), (0, 515, 600, 40))

score = 0
numHints = 0
minutes = 0
seconds = 0
milliseconds = 0
check = True


def sologame():
    global guess
    guess = []
    #  from https://pypi.python.org/pypi/RandomWords/0.1.5
    rw = RandomWords()
    hint = rw.random_word()

    #  from https://www.datamuse.com/api/
    api = Datamuse()

    foo_complete = api.words(ml=hint, max=4)
    foo_df = scripts.dm_to_df(foo_complete)

    loo = api.words(rel_par=hint, max=1)
    loo_df = scripts.dm_to_df(loo)

    maybe = api.words(rel_trg=hint, max=1)
    maybe_df = scripts.dm_to_df(maybe)

    values = foo_df['word'].values
    val = loo_df['word'].values
    v = maybe_df['word'].values
    wordList = set()

    level = 0
    if score > 5:
        level = 2

    for i in values:
        if 3+level < len(i) < 7+level and i.isalpha():
            wordList.add(i)
    for i in val:
        if 3+level < len(i) < 7+level and i.isalpha():
            wordList.add(i)
    for i in v:
        if 3+level < len(i) < 7+level and i.isalpha():
            pass
            wordList.add(i)

    wordList = list(wordList)
    if len(wordList) < 2:
        sologame()
    while len(wordList) > 3:
        wordList.pop()

    soloB = screen.Solo.game(wordList)
    try:
        main(wordList, soloB, hint, "solo")
    except:
        sologame()


def game():
    rw = RandomWords()
    hint = rw.random_word()

    api = Datamuse()

    foo_complete = api.words(ml=hint, max=3)
    foo_df = scripts.dm_to_df(foo_complete)

    loo = api.words(rel_par=hint, max=1)
    loo_df = scripts.dm_to_df(loo)

    maybe = api.words(rel_trg=hint, max=1)
    maybe_df = scripts.dm_to_df(maybe)

    values = foo_df['word'].values
    val = loo_df['word'].values
    v = maybe_df['word'].values

    words = set()

    for i in values:
        if 3 < len(i) < 8 and i.isalpha():
            words.add(i)
    for i in val:
        if 3 < len(i) < 8 and i.isalpha():
            words.add(i)
    for i in v:
        if 3 < len(i) < 8 and i.isalpha():
            pass
            words.add(i)

    words = list(words)
    if len(words) < 1:
        game()

    global guess
    guess = []
    try:
        return words[0], hint
    except:
        game()


def colorboard(board, word, affected, type, check=False):
    count = -1
    circleList = []
    ypadding = 0
    for row in range(len(board)):
        xpadding = 0
        ypadding += 8

        for col in range(len(board[0])):
            count += 1
            xpadding += 8
            if count in affected:
                fol = "green"
            else:
                fol = "letters"
            circle = Letters(word, board, row, col, xpadding, ypadding, fol, type, check)
            circleList.append(circle)

    return circleList


def main(word, board, hint, type):
    pygame.display.set_caption("Word Cluttered")
    background = pygame.Surface(screen1.get_size())
    screen1.blit(background, (0, 0))

    pygame.display.flip()

    global guess
    guess = []
    circle = Letters("", board, 0, 0, 0, 0, "letters", type, True)
    Letters.__init__(circle, word, board, 0, 0, 0, 0, "letters", type, True)
    allSprites = pygame.sprite.Group(circle)
    keepGoing = True
    print(str(circle))

    screen1.fill((206, 185, 177))

    allSprites.clear(screen1, background)

    tempX = 0
    tempY = 0

    used = [True for x in range(len(board)**2)]
    affected = []
    circleList = colorboard(board, word, affected, type, True)

    clock = pygame.time.Clock()

    soloCount = 0
    totalCount = len(word)
    popWords = []
    msg = ""

    while keepGoing:
        global score
        if type == "multi":
            global milliseconds
            global seconds
            global minutes

            if milliseconds > 1000:
                seconds += 1
                milliseconds -= 1000
            if seconds > 60:
                minutes += 1
                seconds -= 60

            if minutes > 1:
                screen.Multi.timesUp(score)

            timer(minutes, seconds)
            milliseconds += clock.tick_busy_loop(60)
        totalScore()
        theme(hint)

        image = pygame.image.load("images/mm.png").convert_alpha()
        rect = image.get_rect()
        image = pygame.transform.scale(image, (175, 50))
        rect.center = [180, 50]
        screen1.blit(image, rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            pressed1, pressed2, pressed3 = pygame.mouse.get_pressed()
            currentLetters = -1

            if pressed1:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                #  inspired from https://stackoverflow.com/questions/43641282/how-would-i-go-about-making-clickable-
                # text-in-pygame
                tx = width//2 - (len(hint)//2 * 20)
                if x in range(tx, tx+100) and y in range(30, 60):
                    define(hint)
                    pass
                if x < 175 and y < 37:
                    screen.Multi.mainMenu((175, 50), 180, 50)

                for circle in circleList:
                    currentLetters += 1
                    circleX, circleY = circle.position()
                    x = pygame.mouse.get_pos()[0]
                    y = pygame.mouse.get_pos()[1]
                    r = 40

                    if circleX + r >= x >= circleX - r and circleY + r >= y >= circleY - r and used[currentLetters]:
                        if len(guess) == 0 and circle.letter != 0:
                            guess.append(circle.letter)
                            prevX = circle.index()[0]
                            prevY = circle.index()[1]
                            used[currentLetters] = False
                            affected.append(currentLetters)

                        elif len(guess) > 0 and legal(circle.index()[0], circle.index()[1], prevX, prevY) and circle.letter != 0:
                            tempX = prevX  # for when the user deletes their answer choice
                            tempY = prevY
                            guess.append(circle.letter)
                            prevX = circle.index()[0]
                            prevY = circle.index()[1]
                            used[currentLetters] = False

                            affected.append(currentLetters)
                        if type == "solo":
                            soloAnswer(guess, word, popWords)
                        else:
                            answer(guess, word)
                        colorboard(board, word, affected, type)
            global numHints
            if event.type == pygame.KEYDOWN and pygame.key.name(event.key) == 'space':
                print("space")
                numHints = 0
                guess = []
                used = [True for x in range(len(board)**2)]

                for i in range(len(popWords)):
                    word.insert(0, popWords[i])
                    score -= 1

                popWords = []
                affected = []
                soloCount = 0
                colorboard(board, word, affected, type)
                soloAnswer(guess, word, popWords)

            if event.type == pygame.KEYDOWN and pygame.key.name(event.key) == 'h' and numHints < 5:
                i = 0
                next = ""
                size = 30
                for j in range(len(word[i])):
                    if j < len(guess) and guess[j] == (word[i])[j]:
                        next = (word[i])[j+1]
                    elif j < len(guess) and guess[j] != (word[i])[j]:
                        next = "Wrong Guess"

                if next == "":
                    next = word[i][0]

                myfont = pygame.font.SysFont("serif", 30)
                pygame.draw.rect(screen1, (206, 185, 177), (500, 40, 140, 80))
                label = myfont.render("Hint: ", 1, (0, 0, 0))
                screen1.blit(label, (520, 40))

                if next == "Wrong Guess":
                    myfont = pygame.font.SysFont("serif", 25)
                    label2 = myfont.render("Wrong", 1, (0, 0, 0))
                    label3 = myfont.render("Guess", 1, (0, 0, 0))
                    screen1.blit(label2, (520, 60))
                    screen1.blit(label3, (520, 80))
                else:
                    myfont = pygame.font.SysFont("serif", 40)
                    label2 = myfont.render(next.upper(), 1, (0, 0, 0))
                    screen1.blit(label2, (530, 65))
                    numHints += 1

            if len(guess) > 0 and event.type == pygame.KEYDOWN and pygame.key.name(event.key) == 'backspace':
                prevX = tempX
                prevY = tempY

                index = affected.pop()
                used[index] = True
                guess.pop()
                if type == "solo":
                    soloAnswer(guess, word, popWords)
                else:
                    answer(guess, word)
                colorboard(board, word, affected, type)

            if type == "solo":
                for i in range(len(word)):
                    if yesWon(guess, word[i]):
                        popWords.append(word.pop(0))
                        guess = []
                        soloCount += 1
                        score += 1
                        break
            if soloCount == totalCount:
                screen1.fill((0, 0, 0))
                pygame.display.update()
                print("winner! Score: ", score)
                sologame()

            elif won(guess, word, type):
                print("winner! Score: ", score)

                screen1.fill((0, 0, 0))
                pygame.display.update()
                guess = []
                score += 1
                msg = "point"

                from board import Player
                Player(word, hint, msg)

                if type == "multi":
                    import board
                    board.start(False)
                else:
                    sologame()

        pygame.display.flip()
        clock.tick(200)
    pygame.mouse.set_visible(True)
    pygame.quit()


def legal(row, col, rows, cols):
    if (abs(rows - row) == 1 or rows - row == 0) and (abs(cols - col) == 1 or cols - col == 0):
        return True
    return False


def yesWon(guess, word):
    temp = ""
    for i in range(len(guess)):
        temp += str(guess[i])
    if temp == word:
        return True
    return False


def won(guess, word, type):
    temp = ""
    for i in range(len(guess)):
        temp += str(guess[i])
    xword = ""

    for i in range(len(word)):
        xword += word[i]
    if type == "solo":
        if temp == xword:
            return True
    else:
        if temp == word:
            return True
    return False


def soloAnswer(guess, word, used):
    r = 30
    y = 475

    startY = 445
    for i in range(len(word) + len(used)):  # draws blue bars indicating correct word
        pygame.draw.rect(screen1, (206, 185, 177), (0, startY, 600, 40))
        startY += 50

    startY = 445
    for j in range(len(used)):  # draws the solid lines once a word has been guessed
        pygame.draw.rect(screen1, (1, 150, 119), (0, startY, 600, 40))
        x = (width - (r * 2 * len(used[j]))) // 2
        tempword = used[j]
        for i in range(len(tempword)):
            start = (width - (r * 2 * len(tempword))) // 2 + (i * r * 2)
            end = start + r * 2
            pygame.draw.line(screen1, (0, 0, 0), (start, y + (j * 50)), (end - 10, y + (j * 50)), 5)
            myfont = pygame.font.SysFont("serif", 50)
            # render text
            label = myfont.render(str(tempword[i]).upper(), True, (0, 0, 0))
            screen1.blit(label, (x + 15, y - 30 + (50*j)))
            x += 60
        startY += 50

    y = 475
    y += len(used) * 50
    for j in range(len(word)):
        for i in range(len(word[j])):
            start = (width - (r * 2 * len(word[j]))) // 2 + (i * r * 2)
            end = start + r * 2
            pygame.draw.line(screen1, (0, 0, 0), (start, y + (j * 50)), (end - 10, y + (j * 50)), 5)
    xword = ""
    for j in range(len(word)):
        xword += word[j] + " "
    myfont = ""
    count = 0
    x = (width - (r * 2 * len(word[count]))) // 2
    for i in range(len(guess)):
        if xword[i] == " ":
            count += 1
            if count <= len(word):
                x = (width - (r * 2 * len(word[count]))) // 2

        myfont = pygame.font.SysFont("serif", 50)
        label = myfont.render(str(guess[i]).upper(), True, (0, 0, 0))
        screen1.blit(label, (x + 15, y - 30 + (count * 50)))
        x += 60


def answer(guess, word):
    r = 30
    pygame.draw.rect(screen1, (206, 185, 177), (0, 515, 600, 40))
    for i in range(len(word)):
        start = (width - (r*2*len(word)))//2 + (i * r * 2)
        end = start + r * 2
        pygame.draw.line(screen1, (0, 0, 0), (start, 550), (end - 10, 550), 5)

    x = (width - (r*2*len(word)))//2

    myfont = ""
    for i in range(len(guess)):
        myfont = pygame.font.SysFont("serif", 50)
        # render text
        label = myfont.render(str(guess[i]).upper(), True, (0, 0, 0))
        screen1.blit(label, (x+15, 520))
        x += 60


def timer(minutes, seconds):
    myfont = pygame.font.SysFont("serif", 50)
    pygame.draw.rect(screen1, (206, 185, 177), (500, 0, 600, 50))
    label = myfont.render(str(minutes) + ":" + str(seconds), 1, (0, 0, 0))
    screen1.blit(label, (520, 10))


def define(hint):
    myfont = pygame.font.SysFont("serif", 20)
    try:
        apiUrl = 'http://api.wordnik.com/v4'
        apiKey = '43625d7af7960f15b71363a1061a2cfa12a7988465f44dd39'
        client = client = swagger.ApiClient(apiKey, apiUrl)
        wordApi = WordApi.WordApi(client)
        d = wordApi.getDefinitions(hint, sourceDictionaries='all', limit=1, useCanonical=True)
        pygame.draw.rect(screen1, (1, 150, 119), (180, 0, 410, 40))
        text = d[0].text
        y = 5
        for i in range(0, len(text), 62):
            label = myfont.render(text[i:i+62], 1, (0, 0, 0))
            screen1.blit(label, (190, y))
            y += 12
    except:
        pass


def totalScore():
    myfont = pygame.font.SysFont("serif", 30)
    pygame.draw.rect(screen1, (206, 185, 177), (0, 40, 100, 40))
    label = myfont.render("Score: " + str(score), 1, (0, 0, 0))
    screen1.blit(label, (10, 55))


def theme(hint):
    myfont = pygame.font.SysFont("serif", 40)
    label = myfont.render(hint, 1, (0, 0, 0))
    screen1.blit(label, (width//2 - (len(hint)//2 * 20), 40))


def run():
    global score, minutes, seconds, milliseconds
    score = 0
    minutes = 0
    seconds = 0
    milliseconds = 0
    pygame.event.clear(pygame.KEYDOWN)
    pygame.event.clear(pygame.KEYUP)
    pygame.event.clear(pygame.MOUSEBUTTONDOWN)
    pygame.event.clear()

    screens = screen.Screen()
    instructions = screen.Instruct()
    allSprites1 = pygame.sprite.Group(instructions)
    multiplayer = screen.Multi()
    allSprites2 = pygame.sprite.Group(multiplayer)
    solo = screen.Solo()
    allSprites3 = pygame.sprite.Group(solo)
    keepGoing = True
    while keepGoing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False

            pressed1, pressed2, pressed3 = pygame.mouse.get_pressed()

            if pressed1:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]

                for sprite in allSprites1:
                    if sprite.rect.collidepoint(x, y):
                        screens.instruction()

                        print("Instructions Clicked")

                for sprite in allSprites2:
                    if sprite.rect.collidepoint(x, y):
                        print("Multi Clicked")

                        try:
                            global check
                            import board
                            pygame.draw.rect(screen1, (1, 150, 119), (0, 515, 600, 40))
                            board.start(check)
                            check = False
                        except:
                            print("Need Sockets")
                            background = pygame.Surface(screen1.get_size())
                            screen1.blit(background, (0, 0))

                            myfont = pygame.font.SysFont("serif", 50)
                            # render text
                            label = myfont.render("Need Sockets", True, (255, 255, 255))
                            screen1.blit(label, (200, 200))

                for sprite in allSprites3:
                    if sprite.rect.collidepoint(x, y):
                        print("Solo Clicked")
                        screens.soloMode()
                        sologame()

        pygame.display.flip()
    pygame.mouse.set_visible(True)
    pygame.quit()


if __name__ == "__main__":
    run()

