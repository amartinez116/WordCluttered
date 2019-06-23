
#  Created the board that allows multiplayers and to use the board to play the game

import socket
import threading
from queue import Queue


def handleServerMsg(server, serverMsg):
    server.setblocking(1)
    msg = ""
    command = ""
    while True:
        msg += server.recv(10).decode("UTF-8")
        command = msg.split("\n")
        while (len(command) > 1):
            readyMsg = command[0]
            msg = "\n".join(command[1:])
            serverMsg.put(readyMsg)
            command = msg.split("\n")

import wordCluttered
import random
import string
import pygame

width = 600
height = 600
screen = pygame.display.set_mode((width, height))
server1 = None
serverMsg1 = None
otherStrangers = dict()


class Board(object):
    def __init__(self, word, hint):
        self.otherStrangers = dict()
        self.word = word
        self.hint = hint
        if len(self.word) > 7:
            self.level = "Medium"
        else:
            self.level = "Easy"
        self.board()
        pygame.draw.rect(screen, (206, 185, 177), (0, 515, 600, 40))

    def board(self):
        word = self.word
        if self.level == "Easy":  # Easy:5x5, medium:6x6
            length = 3
        else:
            length = 4
        boards = [[0 for x in range(length)] for y in range(length)]
        x = random.randint(0, length-1)
        y = random.randint(0, length-1)

        board = self.makepuzzle(boards, word, x, y)
        wordCluttered.main(word, board, self.hint, "multi")

        return board

    @staticmethod
    def isFull(board):  # Complete board with no 0's
        for rows in range(len(board)):
            for cols in range(len(board)):
                if board[rows][cols] == 0:
                    return False
        return True

    def makepuzzle(self, board, word, x, y, index=0):
        while index < len(word):
            rows = random.randint(0, len(board) - 1)
            cols = random.randint(0, len(board) - 1)
            if board[rows][cols] == 0:
                if self.oneAway(x, y, rows, cols):  # guess & check:
                    board[rows][cols] = word[index]
                    solution = self.makepuzzle(board, word, rows, cols, index + 1)
                    if solution is not None:  # Guess worked!

                        return solution

        for row in range(len(board)):
            for col in range(len(board[0])):
                if board[row][col] == 0:
                    board[row][col] = random.choice(string.ascii_lowercase)

        return board

    @staticmethod
    def oneAway(row, col, rows, cols):
        if (abs(rows - row) == 1 or rows - row == 0) and (abs(cols - col) == 1 or cols - col == 0):

            return True
        return False


class Player(object):
    def __init__(self, word, hint, msg="",  new=False, serverMsg="", server=""):
        self.word = word
        self.hint = hint
        if serverMsg == "":
            global serverMsg1, server1
            serverMsg = serverMsg1
            server = server1

        self.server = server
        self.serverMsg = serverMsg
        if new:
            self.me = Board(self.word, self.hint)

        self.run(msg, self.serverMsg, self.server)
        self.msg = msg

    @staticmethod
    def run(msg1="", serverMsg=None, server=None):

        if serverMsg == None:
            global serverMsg1, server1
            serverMsg = serverMsg1
            server = server1
        # sends message to other player
        if msg1 != "":
            print("sending: ", msg1)
            server.send(msg1.encode())

        while serverMsg.qsize() > 0:
            msg = serverMsg.get(False)

            try:
                print("received: ", msg, msg1, "\n")
                msg = msg.split()
                command = msg[0]

                if (command == "myIDis"):
                    myPID = msg[1]
                    #self.me.changePID(myPID)

                elif (command == "newPlayer"):
                    newPID = msg[1]
                    x = width / 2
                    y = height / 2
                    print("New player entered!!")
                    #otherStrangers[newPID] = Board(self.word, self.hint)

            except:
                print("failed")
            serverMsg.task_done()


def start(check=True):
    if check:
        HOST = "" # put your IP address here if playing on multiple computers
        PORT = 50003

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server.connect((HOST, PORT))
        print("connected to server")
        global otherStrangers
        #otherStrangers

        serverMsg = Queue(100)
        threading.Thread(target=handleServerMsg, args=(server, serverMsg)).start()
        global server1, serverMsg1
        server1 = server
        serverMsg1 = serverMsg
        server1.send("yes".encode())
    try:
        word, hint = wordCluttered.game()
    except:
        start()
    Player(word, hint, "", True, serverMsg1, server1)


if __name__ == "__main__":
    start()

