Word Cluttered is a game that allows the user to come up with words that are related to the given theme.

-	To obtain themes I used the random_words module that allows me to filter through words that are popular and that fit my requirements in the program.
-	Used Datamuse API to obtain words from the internet based of the given theme. It is constantly updating and picks words related to, synonymous, compared to, and so on. It follows my algorithms in choosing words that make the most sense. 
-	Levels generate themselves and get difficult as the player’s score increases by length in word and in how common it appears.
-	I used Wordnik to obtain the definition of the words through a series of 
-	I used sockets to enable multiplayer locally and allows you to play with a different user in competing to reach the highest score! 	


Main files are:
wordCluttered.py
screen.py
letters.py
board.py
dots_server.py (originally by Rohan Varma)

The rest of the files are used to run the API's and libraries used in my game and not own by me. All which are included to run the game.

To run: 
Run wordCluttered.py and you're ready do play!
If playing with Multiplayers then use sockets! First run the dots_server.py file.
Next run wordCluttered.py on two separate terminals in order to connect to the sockets. That should enable connection and should allow two player games!