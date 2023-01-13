#-----------------------------------------------------------------------------
# Name:        Jamie's Casino (assignment.py)
# Purpose:     My project is a casino game where the user can play slots and blackjack, with a betting system. 
#
# Author:      Mr. Brooks
# Created:     13-March-2021
# Updated:     2-April-2021
#-----------------------------------------------------------------------------
#I think this project deserves a level 4+ because while meeting all my goals and satisfying almost all of the program requirements, \
#I managed to execute this challenging project in an efficient manner. I also had several extra features including the microbit, reading and
#writing for remembering account balances, and creating a friendly UI for the user to have an easy and fun time utilizing the program.
#
#Features Added:
#I used the microbit to play ("spin") my slots game, and to bet/hit/stand/replay in my blackjack game
#I used reading and writing to store the account balances for different users. The player can choose from the different accounts to play on.
#I used sound effects to make the game much more engaging.
#I had a replay feature in my games, where the user could play again without having to stop and start the code again
#I had a betting system implemented, where the user could bet different amounts.
#-----------------------------------------------------------------------------
#Thing to Note:
#There is a specific set of cards (1 of them being an ace), where the computer cannot seem to recognize that the user/player is over 21 as it
#gets confused about if the ace can become a 1. This does not happen often, and most times the aces function perfectly fine (properly switching
#from an 11 to a 1, or even simply staying an 11, or even when there are multiple aces) 
#If you happen to run out of money on all the accounts, you can simply change the money values in the text file.
#-----------------------------------------------------------------------------
'''Code to be run on the microbit:

from microbit import *
import time

while True:
    gesture = accelerometer.current_gesture()
    if gesture == "shake":
        #display.show(Image.HAPPY)
        print("shakeYes")
    elif gesture != "shake":
        #display.show(Image.ANGRY)
        print("shakeNo")
    
    if button_a.is_pressed():
        print("buttonAPressed")
        display.show(Image.ANGRY)
    if not button_a.is_pressed():
        print("buttonANotPressed")
        display.show(Image.HAPPY)
    if button_b.is_pressed():
        print("buttonBPressed")
        display.show(Image.ANGRY)
    if not button_b.is_pressed():
        print("buttonBNotPressed")
        display.show(Image.HAPPY)
    time.sleep(0.5)
'''
#-----------------------------------------------------------------------------

import pygame
import random
import time
import serial
import serial.tools.list_ports as list_ports

#-----------------------------------------------------------------------------------------------------------------------

class Card():
    
    def __init__(self, cardNumber, cardSuit):
        self.cardNumber = cardNumber
        self.cardSuit = cardSuit
        '''
        intializes the init method, 
        
        Creates attributes to help organize the Card. This is entirely for the shell. It doesn't change anything in the pygame variable.

        Parameters (Attributes)
        ----------
        self: 
            used to represent the instance of the class
        cardNumber:
            the number of the card
        cardSuit:
            the suit of the card
  
        Returns
        -------
        None
        '''
    
    def __repr__(self):  
        '''
        converts instances to proper strings
        
        Without this the instances look something like "0v3xxxxd0". It takes these, converts them to proper words.

        Parameters (Attributes)
        ----------
        self: 
            used to represent the instance of the class
  
        Returns
        -------
        "% s of % s":
            returns the proper word of the instance.
        '''
        return "% s of % s" % (self.cardNumber, self.cardSuit)
        
#-----------------------------------------------------------------------------------------------------------------------

class Button():
    
    def __init__(self, rectIn, colorIn, valueIn=False ):
        '''
        intializes the init method
        
        Creates attributes for the button

        Parameters (Attributes)
        ----------
        self: 
            used to represent the instance of the class
        rectIn:
            Size of the button
        colorIn:
            Colour of the button
        valueIn:
            States that mouse isn't over the button
  
        Returns
        -------
        None
        '''
        self.rect = rectIn
        self.displayColor = colorIn
        self.baseColor = colorIn
        self.hoverColor = pygame.Color(0,0,0)
        #if mouse is hovering button, decrease each rgb value by 50
        if self.baseColor.r > 50:
            self.hoverColor.r = self.baseColor.r - 50
            
        if self.baseColor.g > 50:
            self.hoverColor.g = self.baseColor.g - 50
            
        if self.baseColor.b > 50:
            self.hoverColor.b = self.baseColor.b - 50
        
        self.value = valueIn
        
        
    def draw(self, surfaceIn):
        '''
        This method draws a button in accordance to the given values

        Parameters
        ----------
        self: 
            used to represent the instance of the class
        surfaceIn:
            Describe what layer to draw the button on
  
        Returns
        -------
        None
        '''
        #blits image to the screen
        pygame.draw.rect(surfaceIn, self.displayColor, self.rect, border_radius = 5)
        
    def update(self):
        '''
        updates if mouse is hovering over button
        
        is called on and checks to see if user mouse is hovering over button

        Parameters
        ----------
        self: 
            used to represent the instance of the class
  
        Returns
        -------
        None
        '''
        #if mouse is hovering over button
        if self.collidePoint(pygame.mouse.get_pos()):
          
            self.displayColor = self.hoverColor
        else:
            self.displayColor = self.baseColor   
   
    def collidePoint(self, pointIn):
        '''
        This method checks if mouse is over the button
        
        It compares the x and y values with the mouse curser to see if the mouse is inside the button

        Parameters
        ----------
        pointIn: 
            takes the point of the mouse cursor
  
        Returns
        -------
        Returns True if mouse is over button
        Returns False if mouse is not over button
        '''
        #checks iof mouse is above button
        if (pointIn[0] > self.rect[0] and pointIn[0] < self.rect[0] + self.rect[2] and pointIn[1] > self.rect[1] and pointIn[1] < self.rect[1] + self.rect[3]):
            return True
        else:
            return False
        
#-----------------------------------------------------------------------------------------------------------------------

class PlayingCard():
    
    def __init__(self, imageIn, posIn, imageRectIn):
        '''
        This method creates attributes and draws the blank playing cards

        Parameters
        ----------
        self: 
            used to represent the instance of the class
        imageIn:
            takes the coordinates (size) of the card
        posIn: 
            where the card is located
        imageRectIn:
            the pixels of the shark image
            
        Returns
        -------
        None
        '''
        self.image = imageIn
        self.imageRect = imageRectIn
        self.pos = posIn
        
        
    def draw(self, surfaceIn):
        '''
        This method draws the card to the screen when called on

        Parameters
        ----------
        self: 
            used to represent the instance of the class
        surfaceIn:
            Describe what layer to draw the card on
  
        Returns
        -------
        None
        '''
        #blits image to the screen
        surfaceIn.blit(self.image, self.pos, self.imageRect)

#-----------------------------------------------------------------------------------------------------------------------

class Suit():
    
    def __init__(self, imageIn, posIn, imageRectIn):
        '''
        This is for the photos of the different suits printed
        
        I need this as I'm using blank playing cards to show cards on the screen,
        and I'm seperately printing the card numbers and suits. In this class I print
        the different suits

        Parameters
        ----------
        self: 
            used to represent the instance of the class
        imageIn:
            takes the coordinates (size) of the obstacles
        posIn: 
            where the card is to be located on the screen
        imageRectIn:
            the pixels of the corresponding suit
            
        Returns
        -------
        None
        '''
        self.image = imageIn
        self.imageRect = imageRectIn
        self.pos = posIn
        
        
    def draw(self, surfaceIn):
        '''
        This method draws the corresponding suit to the screen

        Parameters
        ----------
        self: 
            used to represent the instance of the class
        surfaceIn:
            Describe what layer to draw the card suit on
  
        Returns
        -------
        None
        '''
        #blits image to the screen
        surfaceIn.blit(self.image, self.pos, self.imageRect)
        
#-----------------------------------------------------------------------------------------------------------------------

def findMicrobitComPort(pid=516, vid=3368, baud=115200):
    '''
    This function finds a device connected to usb by it's PID and VID and returns a serial connection
    Parameters
    ----------
    pid - Product id of device to search for
    vid - Vendor id of device to search for
    baud - Baud rate to open the serial connection at
    Returns
    -------
    Serial - If a device is found a serial connection for the device is configured and returned
    References
    ----------
    Mr. Brook's microbit code
    '''
    #Required information about the microbit so it can be found
    #PID_MICROBIT = 516
    #VID_MICROBIT = 3368
    TIMEOUT = 0.1
    
    #Create the serial object
    serPort = serial.Serial(timeout=TIMEOUT)
    serPort.baudrate = baud
    
    #Search for device on open ports and return connection if found
    ports = list(list_ports.comports())
    print('scanning ports')
    for p in ports:
        print('port: {}'.format(p))
        try:
            print('pid: {} vid: {}'.format(p.pid, p.vid))
        except AttributeError:
            continue
        if (p.pid == pid) and (p.vid == vid):
            print('found target device pid: {} vid: {} port: {}'.format(
                p.pid, p.vid, p.device))
            serPort.port = str(p.device)
            return serPort
    
    #If nothing found then return None
    return None

#-----------------------------------------------------------------------------------------------------------------------

def signIn(userNumber):
    '''
    This function reads the data of the text file and sets out the available balances / users to the player to pick from.
    Depending on what user profile the user chooses, it will set the balance of the player to the associated profile
    Parameters
    ----------
    userNumber - used to determine which account the user chose (to see which balance we should take from the text document)
    Returns
    -------
    int(fileContents[i-1]) - Returns an integer value of what balance the player should have in accordance to the account they chose.
    '''
    #opens, copies, closes the text file
    file = open("FPTUsers.txt", "r")   # Open the file
    fileContents = file.readlines()
    file.close()
    
    #picks the appropriate value, then returns it
    for i in range(1, 4, 1):
        if userNumber == i:
            return int(fileContents[i-1])

#-----------------------------------------------------------------------------------------------------------------------

def signOut(money, accountNumber):
    '''
    This function reads and copies the data of the text file, then it writes it, replacing the old balance of the user to the new balance.
    (The new balance being the money they had when they signed out)
    Parameters
    ----------
    money - this is the "new" player balance (the new player balance to replace the old balance)
    accountNumber - used to determine the proper account balance to change and replace (within the text document)
    Returns 
    -------
    none
    Hazards 
    -------
    Although I did not come across this issue, there is a chance that if there is a space then an error message will pop up and the code will not run
    '''
    
    file = open("FPTUsers.txt", "r")   
    fileContents = file.readlines()
    file.close()
    
    file = open("FPTUsers.txt", "w")
    
    #print(len(fileContents))
    for i in range(1, 4, 1):
        #print(fileContents[i-1])
        #print(i)
            
        if i == accountNumber:
            file.write(str(money))
        
        if i != accountNumber:
            file.write(str(fileContents[i-1]))
        
        if i == 1 and accountNumber == 1 and accountNumber != 2:
            file.write("\n")
        
        if accountNumber == 2 and i != 1:
            file.write("\n")
        
    file.close()
        
#-----------------------------------------------------------------------------------------------------------------------

def startingAccountBalances():
    '''
    This function reads the data of the text file and returns the different balances of each account, so that the user can see
    how much money is in each account
    Parameters
    ----------
    none
    Returns
    -------
    balances - Returns the integer values of the different account balances
    '''
    file = open("FPTUsers.txt", "r")   # Open the file
    fileContents = file.readlines()
    file.close()
    
    balances = []
    #print(len(fileContents))
    for i in range(1, 4, 1):
        balances.append(int(fileContents[i-1]))
    return balances
#-----------------------------------------------------------------------------------------------------------------------

def main():
    '''
    The main function here holds all my variables, gamestates, and logic of code.
    Parameters
    ----------
    none
    Returns
    -------
    none
    '''
    
    #Prepares the pygame module for use
    pygame.init()
    
    #Forces frame rate to be slower
    clock = pygame.time.Clock() 

    #Creating surface of (width, height), and its window.
    mainSurface = pygame.display.set_mode((1000, 600))
    
#     #The microbit checking for microbit
#     print('looking for microbit')
#     microbit = findMicrobitComPort()
#     if not microbit:
#         print('microbit not found')
#         return
#     print('opening and monitoring microbit port')
#     microbit.open()
    
    
    #all the photos used in my program
    cardPhoto = pygame.image.load("images//blankPlayingCard.png")
    cardPhoto = pygame.transform.scale(cardPhoto,(222,327))
    suitPhoto = pygame.image.load("images//allSuits.png")
    suitPhoto = pygame.transform.scale(suitPhoto, (250, 100))
    backOfCardPhoto = pygame.image.load("images//playingCardback.png")
    backOfCardPhoto = pygame.transform.scale(backOfCardPhoto, (170,230))
    slotMachine = pygame.image.load("images//slotMachine.png")
    blackjackPhoto = pygame.image.load("images//blackjackPhoto.jpg")
    blackjackPhoto = pygame.transform.scale(blackjackPhoto, (350,170))
    slotMachinePhoto = pygame.image.load("images//slotMachinePhoto.jpg")
    slotMachinePhoto = pygame.transform.scale(slotMachinePhoto, (350, 170))
    roulettePhoto = pygame.image.load("images//roulettePhoto.jpg")
    roulettePhoto = pygame.transform.scale(roulettePhoto, (350, 170))
    fiveCardPokerPhoto = pygame.image.load("images//5CardPokerPhoto.jpg")
    fiveCardPokerPhoto = pygame.transform.scale(fiveCardPokerPhoto, (350,170))
    comingSoon = pygame.image.load("images//comingSoon.png")
    comingSoon = pygame.transform.scale(comingSoon, (350, 170))
    beachPhoto = pygame.image.load("images//beachPhoto.jpg")
    beachPhoto = pygame.transform.scale(beachPhoto, (540, 300))
    casinoPhoto = pygame.image.load("images//casinoPhoto.jpg")
    
    
    #My Lists:
    #the list of all 52 cards in order
    allCards = []
    #a list of all 52  cards in random order (to be used in the game) 
    playCardList = []
    #a list of only the values of the 52 cards
    allCardListOfValues = []
    #a list of only the values of the 52, in the same random order as playCardList
    playCardListOfValues = []
    #to represent the displayed values
    displayCards = []
    #a list of 52 cards' suits
    displaySuitsBefore = []
    #to represnt the displayed suits (in a randomized order)
    displaySuits = []

    #creating instances for the 52 different cards
    #creating instances (cards) for all hearts
    for i in range(1, 14, 1):
        #appends each heart-suited card to the list of all cards and suits
        allCards.append(Card(i, "hearts"))
        allCardListOfValues.append(i)
        displaySuitsBefore.append("hearts")#You could do this with only one for loop
    
    #for i in range(1, 14, 1):
        #appends each diamond-suited card to the list of all cards and suits
        allCards.append(Card(i, "diamonds"))
        allCardListOfValues.append(i)
        displaySuitsBefore.append("diamonds")
    
    #for i in range(1, 14, 1):
        #appends each club-suited card to the list of all cards and suits
        allCards.append(Card(i, "clubs"))
        allCardListOfValues.append(i)
        displaySuitsBefore.append("clubs")
    
    #for i in range(1, 14, 1):
        #appends each spade-suited card to the list of all cards and suits
        allCards.append(Card(i, "spades"))
        allCardListOfValues.append(i)
        displaySuitsBefore.append("spades")
    
    print(allCardListOfValues)
    #the different fonts I'll be using
    titleFont = pygame.font.SysFont("comicsansms", 60)
    bigFont = pygame.font.SysFont("comicsansms", 30)
    hugeFont = pygame.font.SysFont("impact", 140)
    
    
    #setting up variables 
    gameState = "welcome"
    playerCardSum = 0
    playerNumberOfCards = 1
    robotCardSum = 0
    robotNumberOfCards = 1
    nextDecision = "none"
    comparisonTime = False
    playerAceAmount = 0
    robotAceAmount = 0
    playerBalance = 1000
    answer = set()
    sampleSize = 51
    answerSize = 0
    step = 0
    frameCount = 0
    runOnce = True
    displayInsufficiency = False
    moneyChangeWin = 3
    order = 0
    frameCountSlots = 0
    profitPrinter = 0
    shaking = False
    buttonAPressed = False
    buttonBPressed = False
    theAccount = 0
    timeToClose = 0
    playSound = True
    skipper = True
    #my different sound effects
    jackpotSound = pygame.mixer.Sound("soundEffects//slotsJackpot.mp3") #source: https://www.youtube.com/watch?v=9nvwUwqo6O8
    cardSound = pygame.mixer.Sound("soundEffects//cardSound.mp3") #source: me
    
    #my different buttons
    blackjackBet50Button = Button([40,220,125,35], pygame.Color(200,255,0))
    blackjackBet100Button = Button([40,260,125,35], pygame.Color(255,105,180))
    blackjackBet200Button = Button([40,340,125,35], pygame.Color(255,10,10))
    blackjackBet500Button = Button([40,380,125,35], pygame.Color(100,25,200))
    blackjackBet1000Button = Button([40,420,125,35], pygame.Color(50,105,180))
    blackjackHitButton = Button([900,190,125,35], pygame.Color(10,105,180))
    blackjackStandButton = Button([900,270,125,35], pygame.Color(255,105,130))
    blackjackReplayButton = Button([40,320,125,35], pygame.Color(100,150,255))   
    slotsBet50Button = Button([40,220,125,35], pygame.Color(200,255,0))
    slotsBet100Button = Button([40,260,125,35], pygame.Color(255,105,180))
    slotsBet200Button = Button([40,300,125,35], pygame.Color(255,10,10))
    slotsBet500Button = Button([40,340,125,35], pygame.Color(100,25,200))
    slotsBet1000Button = Button([40,380,125,35], pygame.Color(50,105,180))
    toBlackjackButton = Button([200,105,140,35], pygame.Color(0,255,0))
    toSlotsButton = Button([650,105,125,35], pygame.Color(255,125,150))
    toFiveCardPokerButton = Button([170,355,200,35], pygame.Color(255,45,45))
    toRouletteButton = Button([645,355,135,35], pygame.Color(80,80,240))
    returnFromBlackjackButton = Button([40,520,125,35], pygame.Color(165,230,180))
    returnFromSlotsButton = Button([40,520,125,35], pygame.Color(255,230,180))
    toSignInScreenButton = Button([365,520,250,65], pygame.Color(255,255,255))
    toBlackjackInstructionsButton = Button([770,520,200,35], pygame.Color(0,255,255))
    fromBlackjackInstructionsButton = Button([40,539,125,35], pygame.Color(100,255,180))
    toSlotsInstructionsButton = Button([635,560,360,35], pygame.Color(50,255,50))
    fromSlotsInstructionsButton = Button([40,539,125,35], pygame.Color(100,255,180))
    user1Button = Button([20,200,170,35], pygame.Color(0,255,0))
    user2Button = Button([20,280,170,35], pygame.Color(0,255,0))
    user3Button = Button([20,360,170,35], pygame.Color(0,255,0))
    signOutButton = Button([850,10,140,35], pygame.Color(10,105,180))
    
    print("\n"*2)
    
    #while loop to constantly cycle through code
    while True:
        
#         #checking incoming data from microbit
#         if (microbit.inWaiting()>0):
#         
#             data = microbit.readlines()  #Read lines into a list, one line per list entry
#                   
#             for i in range(len(data)): #Convert each entry in list from binary to a readable text format
#                 data[i] = data[i].decode('utf-8').strip()
#                 
#                 #checking for shaking
#                 if data[i] == "shakeNo":
#                     shaking = False
#                 if data[i] == "shakeYes":
#                     shaking = True
#                 #checking for the different buttons being pressed
#                 if data[i] == "buttonAPressed":
#                     buttonAPressed = True
#                 if data[i] == "buttonANotPressed":
#                     buttonAPressed = False
#                 if data[i] == "buttonBPressed":
#                     buttonBPressed = True
#                 if data[i] == "buttonBNotPressed":
#                     buttonBPressed = False
        
        #checks for events
        ev = pygame.event.poll()
        #For when window close button is clicked, it closes
        if ev.type == pygame.QUIT:  
            break
        
        #if the user opens up blackjack
        if gameState == "blackjack":
            #if mouse button is pressed
            if ev.type == pygame.MOUSEBUTTONDOWN:
                #brings player to instructions
                if toBlackjackInstructionsButton.collidePoint(pygame.mouse.get_pos()) and step == 0:
                    gameState = "blackjackInstructions"
                #if player bets x amount
                if blackjackBet50Button.collidePoint(pygame.mouse.get_pos()) and playerBalance >= 50:
                    betAmount = 50
                    nextDecision = "hit"
                #if player tries to bet x amount, but doesn't have enough money
                elif blackjackBet50Button.collidePoint(pygame.mouse.get_pos()) and playerBalance < 50:
                    displayInsufficiency = True
                if blackjackBet100Button.collidePoint(pygame.mouse.get_pos()) and step == 0 and playerBalance >= 100:
                    nextDecision = "hit"
                    betAmount = 100
                elif blackjackBet100Button.collidePoint(pygame.mouse.get_pos()) and playerBalance < 100:
                    displayInsufficiency = True                
                if blackjackBet200Button.collidePoint(pygame.mouse.get_pos()) and step == 0 and playerBalance >= 200:
                    nextDecision = "hit"
                    betAmount = 200
                elif blackjackBet200Button.collidePoint(pygame.mouse.get_pos()) and playerBalance < 200:
                    displayInsufficiency = True                    
                if blackjackBet500Button.collidePoint(pygame.mouse.get_pos()) and step == 0 and playerBalance >= 500:
                    nextDecision = "hit"
                    betAmount = 500
                elif blackjackBet500Button.collidePoint(pygame.mouse.get_pos()) and playerBalance < 500:
                    displayInsufficiency = True                    
                if blackjackBet1000Button.collidePoint(pygame.mouse.get_pos()) and step == 0 and playerBalance >= 1000:
                    nextDecision = "hit"
                    betAmount = 1000
                elif blackjackBet1000Button.collidePoint(pygame.mouse.get_pos()) and playerBalance < 1000:
                    displayInsufficiency = True
                #if they decide to hit for a new card
                elif blackjackHitButton.collidePoint(pygame.mouse.get_pos()) and step == 1 and nextDecision == "none":
                    nextDecision = "hit"
                #if they decide to stand and not take a new card
                elif blackjackStandButton.collidePoint(pygame.mouse.get_pos()) and step == 1 and nextDecision == "none":
                    nextDecision = "stand"
                #if they want to replay the game, sets variables back 
                elif blackjackReplayButton.collidePoint(pygame.mouse.get_pos()) and step == 2:
                    step = 0
                    playCardList = []
                    playCardListOfValues = []
                    playerCardSum = 0
                    displaySuits = []
                    displayCards = []
                    blankRobotCards = []
                    runOnce = True
                    robotCardSum = 0
                    moneyChangeWin = 3
                    skipper = True
                #if they want to go to selectionScreen
                if returnFromBlackjackButton.collidePoint(pygame.mouse.get_pos()) and step == 0:
                    gameState = "selectionScreen"
            
            #checking for if different buttons have been pressed
            #for if user hits
            if buttonAPressed == True and step == 1 and nextDecision == "none":
                nextDecision = "hit"
                buttonAPressed = False
            #for if stand
            if buttonBPressed == True and step == 1 and nextDecision == "none":
                nextDecision = "stand"
                buttonBPressed = False
            #resets
            if (buttonAPressed == True and buttonBPressed == True) and step == 2:
                step = 0
                playCardList = []
                playCardListOfValues = []
                playerCardSum = 0
                displaySuits = []
                displayCards = []
                blankRobotCards = []
                runOnce = True
                robotCardSum = 0
                moneyChangeWin = 3
                skipper = True
            if shaking == True and step == 0 and playerBalance >= 100:
                nextDecision = "hit"
                betAmount = 100
            if shaking == True and step == 0 and playerBalance < 100:#use elif when possible!
                displayInsufficiency = True
            
            #setting up the dealer's first card
            if runOnce == True:
                blankRobotCards = []
                blankRobotCards.append(PlayingCard(cardPhoto,[50,-150],[0,0,296,400])) 
                runOnce = False
            
            #fills screen a "table" -like colour
            mainSurface.fill((111,195,145))
            #a counter variable for delays
            frameCount += 1
            
            #for if the player tries to bet but doesn't have enough money
            if displayInsufficiency == True:
                renderedText11 = bigFont.render("Player balace not sufficient", 1, (255, 0, 0))         
                mainSurface.blit(renderedText11, (270,320))
                #once 2 seconds pass, stop showing the text
                if frameCount >= 120:
                    displayInsufficiency = False 
                    frameCount = 0
                          
            #THE LOGIC FOR THE BLACKJACK
            #if player hits
            if nextDecision == "hit":
                step = 1
                frameCount = 0
                showBackOfCard = True
                
                cardSound.play()
                
                #plays again, for if it's the first card (since you start with 2 cards)
                if skipper == True:
                    time.sleep(0.2)
                    cardSound.play()
                    skipper = False
                    
            
                #sets a new set of randomized cards, suits, card values
                while answerSize < sampleSize:
                    randomValue = random.randint(0,51)
                    #print(randomValue)
                    if randomValue not in answer:
                        answerSize += 1
                        answer.add(randomValue)
                        playCardList.append(allCards[randomValue])
                        playCardListOfValues.append(allCardListOfValues[randomValue])
                        displayCards.append(allCardListOfValues[randomValue])
                        displaySuits.append(displaySuitsBefore[randomValue])
                
                #sets cards to their appropriate values
                for i in range(51):
                    #sets kings, queens, and jacks to 10
                    if playCardListOfValues[i] > 10 and playCardListOfValues[i] != 1:
                        playCardListOfValues[i] = 10
                    
                
                #sets the nextdecision to none so that the code does not "hit" again automatically
                nextDecision = "none"
    
                playerNumberOfCards += 1
                
                blankCards = []
                suitToPrint = []
                robotSuitToPrint = []
                #cycles through each player card, and checking the suit
                for i in range(playerNumberOfCards):
                    #appends a blank card to the list
                    blankCards.append(PlayingCard(cardPhoto,[(50 + (i*50)),450],[0,0,296,400]))
                    #prints the appropriate suit photo
                    if displaySuits[i] == "spades":
                        suitToPrint.append(Suit(suitPhoto, [(50 + (i*50)),500],[0,0,76,94]))
                    if displaySuits[i] == "hearts":#elif
                        suitToPrint.append(Suit(suitPhoto, [(67 + (i*50)),500],[68,0,50,94]))
                    if displaySuits[i] == "clubs":
                        suitToPrint.append(Suit(suitPhoto, [(80 + (i*50)),500],[130,0,50,94]))
                    if displaySuits[i] == "diamonds":
                        suitToPrint.append(Suit(suitPhoto, [(70 + (i*50)),500],[170,0,76,94]))
                
                #indentifies the first card's suit for the dealer, and appends it to the list
                if displaySuits[25] == "spades":
                    robotSuitToPrint.append(Suit(suitPhoto, [50 ,70],[0,0,76,94]))
                if displaySuits[25] == "hearts":
                    robotSuitToPrint.append(Suit(suitPhoto, [67,70],[68,0,50,94]))
                if displaySuits[25] == "clubs":
                    robotSuitToPrint.append(Suit(suitPhoto, [80 ,70],[130,0,50,94]))
                if displaySuits[25] == "diamonds":
                    robotSuitToPrint.append(Suit(suitPhoto, [70,70],[170,0,76,94]))
              
                #print(blankCards)
                playerCardSum = 0
                print("")
                
                
                print(f"dealer's first Card is {playCardList[25]}")
                print("")
                #cycles through the player's cards, adding to it by the appropriate values
                for j in range(playerNumberOfCards):
                    print(f"Your cards are the {playCardList[j]}")
                    if playCardListOfValues[j] == 1:
                        playerCardSum += 11
                        playerAceAmount += 1
                        #adds it every turn since you have a one
                    elif playCardListOfValues[j] > 1:
                        playerCardSum += playCardListOfValues[j]
                    #if player goes over 
                    if playerCardSum > 21:
                        #if they do have an ace
                        if playerAceAmount > 0:
                            print("hello, we do have an ace! I set you back down so you don't go over")
                            playerCardSum -= 10
                            playerAceAmount -= 1
                        #if they don't have an ace
                        else:
                            print("You busted :(")
                            nextDecision = "done"
                            frameCount = 0
                    #if the player's card sum is 21
                    if playerCardSum == 21:
                        nextDecision = "done"
                        frameCount = 0
                          
                print(playerCardSum)
            
            
            #if the player stands
            elif nextDecision == "stand":
                print("you stand")
                nextDecision = "done"
                frameCount = 0
            
            #Robot/dealer's logic
            #waits a bit of time, to prevent timing issues
            if nextDecision == "done" and frameCount > 30:
                #if the player has a blackjack, and if the dealer doesn't have a blackjack, then it skips all the robot card calculations
                if playerCardSum == 21 and robotCardSum != 21 and playerNumberOfCards <= 2 and robotNumberOfCards <= 2:
                    comparisonTime = True
                    nextDecision = "something else"
                
                #constantly gives the dealer / robot a card until they reach 17 or higher
                #(Blackjack's rules has it so that the dealer must hit on 16 and lower)
                if robotCardSum <= 16 and step == 1:
                    robotNumberOfCards += 1
                    robotCardSum = 0
                    robotSuitToPrint = []
                    blankRobotCards = []
                    showBackOfCard = False
                    
                    #cycles through the robot's cards
                    for k in range(robotNumberOfCards):
                        print(f"Robot cards are the {playCardList[k+25]}")
                        time.sleep(0.2)
                        frameCount = 0
                        #appends blank cards to a list
                        blankRobotCards.append(PlayingCard(cardPhoto,[(50 + (k*50)),-150],[0,0,296,400]))
                        #appends a proper suit photo to a list
                        if displaySuits[k+25] == "spades":
                            robotSuitToPrint.append(Suit(suitPhoto, [(50 + (k*50)),70],[0,0,76,94]))
                        if displaySuits[k+25] == "hearts":
                            robotSuitToPrint.append(Suit(suitPhoto, [(67 + (k*50)),70],[68,0,50,94]))
                        if displaySuits[k+25] == "clubs":
                            robotSuitToPrint.append(Suit(suitPhoto, [(80 + (k*50)),70],[130,0,50,94]))
                        if displaySuits[k+25] == "diamonds":
                            robotSuitToPrint.append(Suit(suitPhoto, [(70 + (k*50)),70],[170,0,76,94]))
                        
                        #print(blankRobotCards)
                        #if the robot's card is an ace
                        if playCardListOfValues[k+25] == 1:
                            robotCardSum += 11
                            robotAceAmount += 1
                            #if the robot goes over
                            if robotCardSum > 21 and robotAceAmount > 0:
                                print("dealer has an ace! Goes down 10 so he doesn't go over")
                                robotCardSum -= 10
                                robotAceAmount -= 1
                                #if robot goes over 16, goes to the card comparison stage
                                if robotCardSum > 16:
                                    comparisonTime = True
                                    
                        #if the robot's card is not a 1
                        elif playCardListOfValues[k+25] > 1:
                            #adds it by the proper value
                            robotCardSum += playCardListOfValues[k+25]
                            #checks for an ace
                            if robotCardSum > 21 and robotAceAmount > 0:
                                print("dealer has an ace! Goes down 10 so he doesn't go over")
                                robotCardSum -= 10
                                robotAceAmount -= 1
                                #if robot goes over 16, goes to the card comparison stage
                                if robotCardSum > 16:
                                    comparisonTime = True
                                    
                    cardSound.play()
                    print(robotCardSum)
                #if the robot goes over 16, goes to the card comparison stage
                if robotCardSum > 16:
                    comparisonTime = True
            
            
            #final comparison of two cards
            if comparisonTime == True:
                renderedText12 = bigFont.render("Player Wins!", 1, (0, 0, 0))         
                renderedText13 = bigFont.render("Dealer Wins :/", 1, (0, 0, 0))         
                
                if robotCardSum == playerCardSum and robotCardSum <= 21:
                    #print("Push time!!")
                    renderedText14 = bigFont.render("Push (Tie)", 1, (0, 0, 0))         
                    mainSurface.blit(renderedText14, (300,320))
                    
                elif robotCardSum == playerCardSum and robotCardSum <= 21 and robotNumberOfCards == 2 and playerNumberOfCards == 2:
                    renderedText15 = bigFont.render("Double Blackjack, push (Tie)", 1, (0, 0, 0))         
                    mainSurface.blit(renderedText15, (300,320))
                    #print("double blackjack, push")
                    
                #if dealer gets a blackjack and the player doesn't
                elif robotCardSum == 21 and playerCardSum != 21 and robotNumberOfCards <= 2:
                    #print("BLACKJACK FOR THE DEALER")
                    renderedText16 = bigFont.render("Blackjack for the dealer!", 1, (0, 0, 0))         
                    mainSurface.blit(renderedText16, (300,320))
                    #playerBalance -= betAmount
                    moneyChangeWin = 0
                    
                #if player gets a blackjack and the player doesn't
                elif playerCardSum == 21 and robotCardSum != 21 and playerNumberOfCards <= 2:
                    renderedText17 = bigFont.render("You got blackjack!", 1, (0, 0, 0))         
                    mainSurface.blit(renderedText17, (300,320))
                    #print("BLACKJACK FOR THE PLAYER")
                    #playerBalance += betAmount*1.5
                    moneyChangeWin = 2
                    
                     
                #if the dealer had a bigger total than the player, and didn't go over 21
                elif robotCardSum > playerCardSum and robotCardSum <= 21:
                    #print("dealer wins without going over 21")
                    renderedText13 = bigFont.render("Dealer Wins :/", 1, (0, 0, 0)) 
                    mainSurface.blit(renderedText13, (300,320))
                    #playerBalance -= betAmount
                    moneyChangeWin = 0
                    
                    
                #if the player had a bigger total than the dealer, and didn't go over 21
                elif playerCardSum > robotCardSum and playerCardSum <= 21:
                    #print("my guy didn't go over 21 but still won")
                    renderedText12 = bigFont.render("Player Wins!", 1, (0, 0, 0))
                    mainSurface.blit(renderedText12, (300,320))
                    #playerBalance += betAmount
                    moneyChangeWin = 1
                    
                #if both the player and the dealer is over
                elif robotCardSum > 21 and playerCardSum > 21:
                    #print("dealer wins (you both busted)!!")
                    renderedText13 = bigFont.render("Dealer Wins :/", 1, (0, 0, 0)) 
                    mainSurface.blit(renderedText13, (300,320))
                    #playerBalance -= betAmount
                    moneyChangeWin = 0
                    
                #if the dealer busts, and the player didn't go over
                elif robotCardSum > 21 and playerCardSum <= 21:
                    #print("MY BOIIII WON, dealer busted and you didnt")
                    renderedText12 = bigFont.render("Player Wins!", 1, (0, 0, 0))
                    mainSurface.blit(renderedText12, (300,320))
                    #playerBalance += betAmount
                    moneyChangeWin = 1
                
                #if the player busts, and the dealer didn't go over
                elif playerCardSum > 21 and robotCardSum <= 21:
                    #print("dealer wins, you went over but he didn't")
                    renderedText13 = bigFont.render("Dealer Wins :/", 1, (0, 0, 0)) 
                    mainSurface.blit(renderedText13, (300,320))
                    #playerBalance -= betAmount
                    moneyChangeWin = 0
                
                #once 1.5 seconds passes, stops displaying who won, and resets
                if frameCount >= 90:  
                    frameCount = 0
                    #resets all values to play again
                    comparisonTime = False
                    playerNumberOfCards = 1
                    robotNumberOfCards = 1
                    playerAceAmount = 0
                    robotAceAmount = 0
                    answer = set()
                    answerSize = 0
                    step = 2
                    nextDecision = "none"
                    #changes the players balance in accordance to if they won/lost
                    if moneyChangeWin == 1:
                        playerBalance += betAmount
                    if moneyChangeWin == 2:
                        playerBalance += betAmount*1.5
                    if moneyChangeWin == 0:
                        playerBalance -= betAmount
                    
                    print(f"you now have ${playerBalance}")

            #prints player balance for 2 seconds
            if frameCount <= 120 and step == 2:
                renderedText18 = bigFont.render(f"You now have ${playerBalance}", 1, (0, 0, 0))         
                mainSurface.blit(renderedText18, (10,200))
                
            #asks if player wants to hit or stand
            if nextDecision == "none" and step == 1:
                renderedText34 = bigFont.render("Hit or Stand?", 1, (0, 0, 0))         
                mainSurface.blit(renderedText34, (300,350))
            
            #prints buttons and text if the step varaible(a sequence controlling variable) is 0
            if step == 0:
                blackjackBet50Button.update()
                blackjackBet50Button.draw(mainSurface)
                blackjackBet100Button.update()
                blackjackBet100Button.draw(mainSurface)
                blackjackBet200Button.update()
                blackjackBet200Button.draw(mainSurface)
                blackjackBet500Button.update()
                blackjackBet500Button.draw(mainSurface)
                blackjackBet1000Button.update()
                blackjackBet1000Button.draw(mainSurface)
                renderedText0 = bigFont.render("Bet Amount:", 1, (0, 0, 0))         
                mainSurface.blit(renderedText0, (20,170))
                renderedText28 = bigFont.render("50", 1, (0, 0, 0))         
                mainSurface.blit(renderedText28, (79,215))
                renderedText6 = bigFont.render("100", 1, (0, 0, 0))         
                mainSurface.blit(renderedText6, (75,255))
                renderedText40 = bigFont.render("200", 1, (0, 0, 0))         
                mainSurface.blit(renderedText40, (75,335))
                renderedText41 = bigFont.render("500", 1, (0, 0, 0))         
                mainSurface.blit(renderedText41, (75,375))
                renderedText42 = bigFont.render("1000", 1, (0, 0, 0))         
                mainSurface.blit(renderedText42, (70,415))
                returnFromBlackjackButton.update()
                returnFromBlackjackButton.draw(mainSurface)
                renderedText27 = bigFont.render("Return", 1, (0, 0, 0))         
                mainSurface.blit(renderedText27, (50,515))
                toBlackjackInstructionsButton.draw(mainSurface)
                toBlackjackInstructionsButton.update()
                renderedText27 = bigFont.render("How To Play?", 1, (0, 0, 0))         
                mainSurface.blit(renderedText27, (780,515))
                renderedText32 = bigFont.render(f"Your Balance: ${playerBalance}", 1, (0, 0, 0))         
                mainSurface.blit(renderedText32, (20,100))
                renderedText31 = bigFont.render("Shake to Bet $100", 1, (0, 0, 0))         
                mainSurface.blit(renderedText31, (5,295))
                
            #prints different text and buttons if the step varaible(a sequence controlling variable) is 1
            if step == 1:
                blackjackHitButton.update()
                blackjackHitButton.draw(mainSurface)
                blackjackStandButton.update()
                blackjackStandButton.draw(mainSurface)
                renderedText1 = bigFont.render("Hit", 1, (0, 0, 0))         
                mainSurface.blit(renderedText1, (900,185))
                renderedText2 = bigFont.render("Stand", 1, (0, 0, 0))         
                mainSurface.blit(renderedText2, (900,265))
                renderedText3 = bigFont.render("Button A to Hit", 1, (0, 0, 0))         
                mainSurface.blit(renderedText3, (774,310))
                renderedText4 = bigFont.render("Button B to Stand", 1, (0, 0, 0))         
                mainSurface.blit(renderedText4, (740,360))
            
            #prints different text and buttons if the step varaible(a sequence controlling variable) is 2 
            if step == 2:
                blackjackReplayButton.update()
                blackjackReplayButton.draw(mainSurface)
                renderedText5 = bigFont.render("Replay", 1, (0, 0, 0))         
                mainSurface.blit(renderedText5, (50,315))
                renderedText6 = bigFont.render("Press A and B at the same time to Replay", 1, (0, 0, 0))         
                mainSurface.blit(renderedText6, (45,355))
            
            #text that always prints (meant to engraved be on the blackjack table)
            renderedText8 = bigFont.render("Dealer must draw to 16,", 1, (255, 50, 50))         
            mainSurface.blit(renderedText8, (300,170))
            renderedText9 = bigFont.render("and stand on anything higher", 1, (255, 50, 50))         
            mainSurface.blit(renderedText9, (300,200))
            renderedText10 = bigFont.render("Blackjack pays 3 to 2", 1, (255, 50, 50))         
            mainSurface.blit(renderedText10, (300,270))
            
            #prints player card total when playing
            if step > 0:
                renderedText3 = bigFont.render(f"Your Card Total: {playerCardSum}", 1, (0, 0, 0))         
                mainSurface.blit(renderedText3, (75,430))
                
                #changes values to face cards and aces (for printing)
                for i in range(len(displayCards)):
                    if displayCards[i] == 1:
                        displayCards[i] = "A"
                    if displayCards[i] == 11:
                        displayCards[i] = "J"
                    if displayCards[i] == 12:
                        displayCards[i] = "Q"
                    if displayCards[i] == 13:
                        displayCards[i] = "K"
                
                #cycles through the number of blank cards
                for i in range(len(blankCards)):
                    
                    #drawing suits and cards
                    blankCards[i].draw(mainSurface)
                    suitToPrint[i].draw(mainSurface)

                    #makes text red if suit is hearts or diamonds
                    if displaySuits[i] == "hearts" or displaySuits[i] == "diamonds":
                        renderedText4 = bigFont.render(str(displayCards[i]), 1, (255, 0, 0))
                    #makes text black if suit is spades or clubs
                    if displaySuits[i] == "spades" or displaySuits[i] == "clubs":
                        renderedText4 = bigFont.render(str(displayCards[i]), 1, (0, 0, 0))
                    mainSurface.blit(renderedText4, (90 + i*50,490))
                    
                    #print(blankCards)
                    
                
                #printing the blank cards
                for i in range(len(blankRobotCards)):
                    blankRobotCards[i].draw(mainSurface)
                #the letter values to print by colours
                for i in range(len(blankRobotCards)):
                    if displaySuits[i+25] == "hearts" or displaySuits[i+25] == "diamonds":
                        renderedText7 = bigFont.render(str(displayCards[i+25]), 1, (255, 0, 0))
                    #makes text black if suit is spades or clubs
                    if displaySuits[i+25] == "spades" or displaySuits[i+25] == "clubs":
                        renderedText7 = bigFont.render(str(displayCards[i+25]), 1, (0, 0, 0))
                    mainSurface.blit(renderedText7, (90 + i*50,50))
                    #displaySuits[i+25].draw(mainSurface)
                
                #printing the different suits
                for i in range(len(robotSuitToPrint)):
                    robotSuitToPrint[i].draw(mainSurface)
                #prints the back of the dealer's second card
                if step == 1 and showBackOfCard == True:
                    mainSurface.blit(backOfCardPhoto,[120,-66])
                #prints dealer card sum
                if nextDecision == "done":
                    renderedText7 = bigFont.render(f"Dealer Card Total: {robotCardSum}", 1, (0, 0, 0))         
                    mainSurface.blit(renderedText7, (600,100))
                #prints how much the player is betting
                if step != 2:
                    renderedText19 = bigFont.render(f"Your bet: ${betAmount}", 1, (255, 0, 255))         
                    mainSurface.blit(renderedText19, (10,350))
                    
        #-----------------------------------------------------------------------------------------------------------------------
        #the selection screen for all the games
        if gameState == "selectionScreen":
            if ev.type == pygame.MOUSEBUTTONDOWN:
                #if player signs out
                if signOutButton.collidePoint(pygame.mouse.get_pos()):
                    gameState = "signOutScreen"
                #if player goes to blackjack
                if toBlackjackButton.collidePoint(pygame.mouse.get_pos()):
                    gameState = "blackjack"
                #if player goes to slots game
                if toSlotsButton.collidePoint(pygame.mouse.get_pos()):
                    gameState = "slots"
            mainSurface.fill((255,255,0))
            
            #prints buttons and text
            toBlackjackButton.update()
            toBlackjackButton.draw(mainSurface)
            toSlotsButton.update()
            toSlotsButton.draw(mainSurface)
            toFiveCardPokerButton.update()
            toFiveCardPokerButton.draw(mainSurface)
            toRouletteButton.update()
            toRouletteButton.draw(mainSurface)
            signOutButton.update()
            signOutButton.draw(mainSurface)
            mainSurface.blit(blackjackPhoto,[100,150])
            mainSurface.blit(slotMachinePhoto,[550,150])
            mainSurface.blit(fiveCardPokerPhoto,[100,400])
            mainSurface.blit(roulettePhoto,[550,400])
            mainSurface.blit(comingSoon,[100,400])
            mainSurface.blit(comingSoon,[550,400])
            renderedText22 = bigFont.render("Blackjack", 1, (0, 0, 0))         
            mainSurface.blit(renderedText22, (205,100))
            renderedText23 = bigFont.render("Slots", 1, (0, 0, 0))         
            mainSurface.blit(renderedText23, (675,100))
            renderedText24 = bigFont.render("5 Card Poker", 1, (0, 0, 0))         
            mainSurface.blit(renderedText24, (185,350))
            renderedText25 = bigFont.render("Roulette", 1, (0, 0, 0))         
            mainSurface.blit(renderedText25, (655,350))
            renderedText26 = bigFont.render("Select Your Game:", 1, (0, 0, 0))         
            mainSurface.blit(renderedText26, (360,25))
            renderedText0 = bigFont.render("Sign Out", 1, (0, 0, 0))         
            mainSurface.blit(renderedText0, (855,6))
            
        
        #-----------------------------------------------------------------------------------------------------------------------
        
        #if gamestate is sets to the slots game
        if gameState == "slots":
            mainSurface.fill((111,255,255))
            if ev.type == pygame.MOUSEBUTTONDOWN:
                #if the player wants to return back to the game selection screen
                if returnFromSlotsButton.collidePoint(pygame.mouse.get_pos()) and order == 0:
                    gameState = "selectionScreen"
                #bets x amount depending on bet amount button clicked
                if (slotsBet50Button.collidePoint(pygame.mouse.get_pos())) and order == 0 and playerBalance >= 50:
                    order = 1
                    betAmount = 50
                #if the player tries to bet x amount but does not have enough money
                elif slotsBet50Button.collidePoint(pygame.mouse.get_pos()) and playerBalance < 50:
                    displayInsufficiency = True
                if (slotsBet100Button.collidePoint(pygame.mouse.get_pos())) and order == 0 and playerBalance >= 100:
                    order = 1
                    betAmount = 100
                elif slotsBet100Button.collidePoint(pygame.mouse.get_pos()) and playerBalance < 100:
                    displayInsufficiency = True      
                if (slotsBet200Button.collidePoint(pygame.mouse.get_pos())) and order == 0 and playerBalance >= 200:
                    order = 1
                    betAmount = 200
                elif slotsBet200Button.collidePoint(pygame.mouse.get_pos()) and playerBalance < 200:
                    displayInsufficiency = True
                if (slotsBet500Button.collidePoint(pygame.mouse.get_pos())) and order == 0 and playerBalance >= 500:
                    order = 1
                    betAmount = 500
                elif slotsBet500Button.collidePoint(pygame.mouse.get_pos()) and playerBalance < 500:
                    displayInsufficiency = True
                if (slotsBet1000Button.collidePoint(pygame.mouse.get_pos())) and order == 0 and playerBalance >= 1000:
                    order = 1
                    betAmount = 1000
                elif slotsBet1000Button.collidePoint(pygame.mouse.get_pos()) and playerBalance < 1000:
                    displayInsufficiency = True
                #if the player wants to head to the instructions screen
                if toSlotsInstructionsButton.collidePoint(pygame.mouse.get_pos()) and order == 0:
                    gameState = "slotsInstructionsScreen"
                    
            #tick counting system
            frameCountSlots += 1
            
            #if they shake microbit, spins slot machine
            if (shaking == True) and order == 1 and playerBalance >= 100:
                order = 2
                frameCountSlots = 0
            #if the player does not have enough money for their bet, prints blank amount
            if displayInsufficiency == True:
                renderedText11 = bigFont.render("Player balace not sufficient", 1, (255, 0, 0))         
                mainSurface.blit(renderedText11, (20,20))
                #once 2 seconds pass, stop displaying 
                if frameCountSlots >= 120:
                    displayInsufficiency = False 
                    frameCountSlots = 0
            #prints my photos
            mainSurface.blit(beachPhoto,[355,255])
            mainSurface.blit(slotMachine,[350,50])
            #first step in the code
            if order == 0:
                
                #sets random numbers
                slot1 = random.randint(1,7)
                slot2 = random.randint(1,7)
                slot3 = random.randint(1,7)
                
                #draws text and buttons
                #print(f"{slot1} {slot2} {slot3}")
                slotsBet50Button.update()
                slotsBet50Button.draw(mainSurface)
                slotsBet100Button.update()
                slotsBet100Button.draw(mainSurface)
                slotsBet200Button.update()
                slotsBet200Button.draw(mainSurface)
                slotsBet500Button.update()
                slotsBet500Button.draw(mainSurface)
                slotsBet1000Button.update()
                slotsBet1000Button.draw(mainSurface)
                renderedText0 = bigFont.render("Bet Amount:", 1, (0, 0, 0))         
                mainSurface.blit(renderedText0, (20,170))
                renderedText28 = bigFont.render("50", 1, (0, 0, 0))         
                mainSurface.blit(renderedText28, (79,215))
                renderedText6 = bigFont.render("100", 1, (0, 0, 0))         
                mainSurface.blit(renderedText6, (75,255))
                renderedText40 = bigFont.render("200", 1, (0, 0, 0))         
                mainSurface.blit(renderedText40, (75,295))
                renderedText41 = bigFont.render("500", 1, (0, 0, 0))         
                mainSurface.blit(renderedText41, (75,335))
                renderedText42 = bigFont.render("1000", 1, (0, 0, 0))         
                mainSurface.blit(renderedText42, (70,375))
                returnFromSlotsButton.draw(mainSurface)
                returnFromSlotsButton.update()
                renderedText5 = bigFont.render("Return", 1, (0, 0, 0))         
                mainSurface.blit(renderedText5, (50,515))
                renderedText31 = bigFont.render(f"Your Balance: ${playerBalance}", 1, (0, 0, 0))         
                mainSurface.blit(renderedText31, (20,100))
                toSlotsInstructionsButton.draw(mainSurface)
                toSlotsInstructionsButton.update()
                renderedText32 = bigFont.render("Instructions and Payouts", 1, (0, 0, 0))         
                mainSurface.blit(renderedText32, (640,557))
            
            #prints bet amount
            if order > 0:
                renderedText19 = bigFont.render(f"Your bet: ${betAmount}", 1, (255, 0, 255))         
                mainSurface.blit(renderedText19, (10,150))
            
            #tells player to spin, prints balance
            if order == 1:
                renderedText31 = bigFont.render(f"Your Balance: ${playerBalance}", 1, (0, 0, 0))         
                mainSurface.blit(renderedText31, (20,100))
                renderedText33 = bigFont.render("Now Shake to Spin!", 1, (0, 0, 0))         
                mainSurface.blit(renderedText33, (20,20))
            
            #creates an animation for the numbers to seem like they are cycling randomly
            if order == 2:
                #runs for some time
                if frameCountSlots < 90: 
                    animeSlot1 = random.randint(1,7)
                    renderedText20 = hugeFont.render(f"{animeSlot1}", 1, (0,255,0))         
                    mainSurface.blit(renderedText20, (420,320))
                #run for more time
                if frameCountSlots < 160:
                    animeSlot2 = random.randint(1,7)
                    renderedText20 = hugeFont.render(f"{animeSlot2}", 1, (0,255,0))         
                    mainSurface.blit(renderedText20, (590,320))
                #runs for the most time
                if frameCountSlots < 230:
                    animeSlot3 = random.randint(1,7)
                    renderedText20 = hugeFont.render(f"{animeSlot3}", 1, (0,255,0))         
                    mainSurface.blit(renderedText20, (760,320))
                #once all numbers have been printed, waits a little then runs the code below
                if frameCountSlots >= 290:
                    #if the player got 3 7's
                    if slot1 == 7 and slot2 == 7 and slot3 == 7:
                        print("you got three 7's, money multiplied by 10!")
                        playerBalance += betAmount*10
                        profitPrinter = 3
                    #if the player got 2 7's 
                    elif (slot1 == 7 and slot2 == 7) or (slot1 == 7 and slot3 == 7) or (slot2 == 7 and slot3 == 7):
                        print("you got two 7's, money multipled by 4!")
                        playerBalance += betAmount*4
                        profitPrinter = 2
                    #if the player got 1 7's  
                    elif slot1 == 7 or slot2 == 7 or slot3 == 7:
                        print("you got one 7, money multiplied by 2!")
                        playerBalance += betAmount*2
                        profitPrinter = 1
                    #if the player got 0 7's
                    else:
                        print("Nothing, you lose your bet")
                        playerBalance -= betAmount
                        profitPrinter = 0
                    #after runs through all the code, setings order to 3 to print results
                    print(f"now you have ${playerBalance}")
                    order = 3
            #prints the results of the slots       
            if order == 3:
                #if they got 3 7's
                if profitPrinter == 3:
                    renderedText30 = bigFont.render("Three 7's! 10x Your Bet", 1, (255, 0, 255))         
                    mainSurface.blit(renderedText30, (10,50))
                #if they got 2 7's
                if profitPrinter == 2:
                    renderedText30 = bigFont.render("Two 7's! 4x Your Bet", 1, (255, 0, 255))         
                    mainSurface.blit(renderedText30, (10,50))
                #if they got 1 7's
                if profitPrinter == 1:
                    renderedText29 = bigFont.render("One 7! 2x Your Bet", 1, (255, 0, 255))         
                    mainSurface.blit(renderedText29, (10,50))
                #if the player won in any way
                if profitPrinter > 0 and playSound == True:
                    jackpotSound.play()
                    playSound = False
                #if the player didn't get any 7's
                if profitPrinter == 0:
                    renderedText30 = bigFont.render("No 7's :(", 1, (255, 0, 255))         
                    mainSurface.blit(renderedText30, (10,50))
                #prints the player's balance
                renderedText29 = bigFont.render(f"You now have ${playerBalance}", 1, (255, 0, 255))         
                mainSurface.blit(renderedText29, (10,10))
                #once 6.5 seconds pass (since the beginning)
                if frameCountSlots > 400:
                    order = 0
                    playSound = True
                    
            #prints the final results to the screen
            if frameCountSlots >= 90 and order >= 2:
                renderedText21 = hugeFont.render(f"{slot1}", 1, (0,255,0))         
                mainSurface.blit(renderedText21, (420,320))
            if frameCountSlots >= 160 and order >= 2:
                renderedText21 = hugeFont.render(f"{slot2}", 1, (0,255,0))         
                mainSurface.blit(renderedText21, (590,320))
            if frameCountSlots >= 230 and order >= 2:
                renderedText21 = hugeFont.render(f"{slot3}", 1, (0,255,0))         
                mainSurface.blit(renderedText21, (760,320))
                #print to offset
        #-----------------------------------------------------------------------------------------------------------------------
        
        if gameState == "slotsInstructionsScreen":
            if ev.type == pygame.MOUSEBUTTONDOWN:
                #if player wants to return back to slots game
                if fromSlotsInstructionsButton.collidePoint(pygame.mouse.get_pos()):
                    gameState = "slots"
            mainSurface.fill((50,140,255))    
            
            #prints return button, and other text
            fromSlotsInstructionsButton.draw(mainSurface)
            fromSlotsInstructionsButton.update()
            renderedText0 = bigFont.render("Return", 1, (0, 0, 0))         
            mainSurface.blit(renderedText0, (50,535))
            renderedText1 = bigFont.render("Bet how much you'd like, by clicking the corresponding button", 1, (0, 0, 0))         
            mainSurface.blit(renderedText1, (20,15))
            renderedText2 = bigFont.render("Then, shake the MicroBit", 1, (0, 0, 0))         
            mainSurface.blit(renderedText2, (20,55))
            renderedText3 = bigFont.render("One 7 pays 2x your bet", 1, (0, 0, 0))         
            mainSurface.blit(renderedText3, (20,135))
            renderedText6 = bigFont.render("Two 7's pays 4x your bet", 1, (0, 0, 0))         
            mainSurface.blit(renderedText6, (20,175))
            renderedText7 = bigFont.render("Three 7's pays 10x your bet", 1, (0, 0, 0))         
            mainSurface.blit(renderedText7, (20,215))
                
                
        #-----------------------------------------------------------------------------------------------------------------------
        
        if gameState == "welcome":
            if ev.type == pygame.MOUSEBUTTONDOWN:
                #if the user wants to go to the sign in screen
                if toSignInScreenButton.collidePoint(pygame.mouse.get_pos()):
                    gameState = "signInScreen"
            
            #prints text and photos
            mainSurface.blit(casinoPhoto,[0,0])
            renderedText0 = bigFont.render("Welcome To:", 1, (255, 255, 255))         
            mainSurface.blit(renderedText0, (10,10))
            renderedText1 = hugeFont.render("Jamie's Casino", 1, (255, 255, 255))         
            mainSurface.blit(renderedText1, (10,50))
            toSignInScreenButton.draw(mainSurface)
            toSignInScreenButton.update()
            renderedText2 = titleFont.render("Continue", 1, (0, 0, 0))         
            mainSurface.blit(renderedText2, (368,510))
            
        #-----------------------------------------------------------------------------------------------------------------------
        
        if gameState == "blackjackInstructions":
            mainSurface.fill((111,195,145))
            if ev.type == pygame.MOUSEBUTTONDOWN:
                #if player wants to go back to the blackjack game
                if fromBlackjackInstructionsButton.collidePoint(pygame.mouse.get_pos()):
                    gameState = "blackjack"
            #prints text and buttons
            fromBlackjackInstructionsButton.draw(mainSurface)
            fromBlackjackInstructionsButton.update()
            renderedText0 = bigFont.render("Return", 1, (0, 0, 0))         
            mainSurface.blit(renderedText0, (50,535))
            renderedText1 = bigFont.render("The goal is to have the sum of your cards get as close to 21", 1, (0, 0, 0))         
            mainSurface.blit(renderedText1, (20,15))
            renderedText2 = bigFont.render("Press 'Hit' to take a new card", 1, (255, 255, 255))         
            mainSurface.blit(renderedText2, (20,55))
            renderedText3 = bigFont.render("Press 'Stand' to not take any more cards, if you think you'll go over", 1, (0, 0, 0))         
            mainSurface.blit(renderedText3, (20,95))
            renderedText6 = bigFont.render("If you go over 21, you lose", 1, (255, 255, 255))         
            mainSurface.blit(renderedText6, (20,135))
            renderedText7 = bigFont.render("If the dealer is closer to 21 than you, you lose", 1, (0, 0, 0))         
            mainSurface.blit(renderedText7, (20,175))
            renderedText8 = bigFont.render("If both you and the dealer's card sum is under 21 but the same,", 1, (255, 255, 255))         
            mainSurface.blit(renderedText8, (20,215))
            renderedText9 = bigFont.render("you tie and don't lose any money. (Called a push)", 1, (255, 255, 255))         
            mainSurface.blit(renderedText9, (20,245))
            renderedText10 = bigFont.render("Otherwise, you win", 1, (0, 0, 0))         
            mainSurface.blit(renderedText10, (20,285))
            renderedText10 = bigFont.render("A blackjack is when you have an Ace + a 10 value card (To make 21)", 1, (255, 255, 255))         
            mainSurface.blit(renderedText10, (20,435))
            renderedText4 = bigFont.render("Face Cards (Jack, Queen, King) are worth 10", 1, (255, 255, 255))         
            mainSurface.blit(renderedText4, (20,355))
            renderedText5 = bigFont.render("Aces are worth 1 or 11", 1, (0, 0, 0))         
            mainSurface.blit(renderedText5, (20,395))
            renderedText11 = bigFont.render("You can also use a MicroBit to hit/stand/restart/bet", 1, (0, 0, 0))         
            mainSurface.blit(renderedText11, (20,475))
            
        #-----------------------------------------------------------------------------------------------------------------------
        
        if gameState == "signInScreen":
            
            if ev.type == pygame.MOUSEBUTTONDOWN:
                #if player chooses to choose user 1
                if user1Button.collidePoint(pygame.mouse.get_pos()):
                    playerBalance = signIn(1)
                    theAccount = 1
                    gameState = "selectionScreen"
                #if player chooses to choose user 2
                if user2Button.collidePoint(pygame.mouse.get_pos()):
                    playerBalance = signIn(2)
                    theAccount = 2
                    gameState = "selectionScreen"
                #if player chooses to choose user 3
                if user3Button.collidePoint(pygame.mouse.get_pos()):
                    playerBalance = signIn(3)
                    theAccount = 3
                    gameState = "selectionScreen"
                #the reason I couldn't simply put 1 line setting gameState to the selection
                #screen was because the previous click was also affecting this
            
            #calls on account balance function for printing account balances
            accountBalances = startingAccountBalances()
            mainSurface.fill((255,105,180))
            #prints text
            renderedText0 = titleFont.render("Choose Your Account:", 1, (0, 0, 0))         
            mainSurface.blit(renderedText0, (10,50))
            renderedText1 = bigFont.render(f"Account Balance: ${accountBalances[0]}", 1, (0, 0, 0))         
            mainSurface.blit(renderedText1, (200,197))
            renderedText2 = bigFont.render(f"Account Balance: ${accountBalances[1]}", 1, (0, 0, 0))         
            mainSurface.blit(renderedText2, (200,277))
            renderedText3 = bigFont.render(f"Account Balance: ${accountBalances[2]}", 1, (0, 0, 0))         
            mainSurface.blit(renderedText3, (200,354))
            
            #draws buttons
            user1Button.draw(mainSurface)
            user1Button.update()
            user2Button.draw(mainSurface)
            user2Button.update()
            user3Button.draw(mainSurface)
            user3Button.update()
            
            #prints text over buttons
            renderedText4 = bigFont.render("User 1", 1, (0, 0, 0))         
            mainSurface.blit(renderedText4, (50,195))
            renderedText5 = bigFont.render("User 2", 1, (0, 0, 0))         
            mainSurface.blit(renderedText5, (50,275))
            renderedText6 = bigFont.render("User 3", 1, (0, 0, 0))         
            mainSurface.blit(renderedText6, (50,355))
        
        #-----------------------------------------------------------------------------------------------------------------------
        
        if gameState == "signOutScreen":
            
            #timer
            timeToClose += 1
            mainSurface.fill((160,0,160))
            #text
            renderedText0 = titleFont.render("Thanks For Playing!", 1, (0, 255, 255))         
            mainSurface.blit(renderedText0, (10,50))
            #once half a second passes, sets gamestate to quit
            if timeToClose > 30:
                gameState = "quit"
        #-----------------------------------------------------------------------------------------------------------------------
        
        if gameState == "quit":
            #writes the new player balance to the text file, and also tells the function which account was accessed
            signOut(playerBalance, theAccount)
            #quits loop
            break
        
        #-----------------------------------------------------------------------------------------------------------------------    
            
        #Displaying the surface
        pygame.display.flip()
        
        #Forces frame rate to be slower
        clock.tick(60) 

    #Quit program once loop is left
    pygame.quit()     
                      
main()