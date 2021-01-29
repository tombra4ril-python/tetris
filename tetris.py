"This Game was coded by Tombra and it is titled: TETRIS"
###
    #global variables are
    #_font - Indicates the font of all the text
    #status - Indicates the status of the game, either paused or started
###

#import dependencies
import pygame
import random

#create global variables
#This is the width and height of the entire game
_displayWidth = 600
_displayHeight = 605
#This is the width and height of the main part(play area) of the game
#It should be noted that the height is always double the width
_gameWidth = 300
_gameHeight = 600
#set the block size
_blockSize = 30
#set the top left x and y position of the game width and height, so it is easy to calculate its position
_topLeftX = 5
_topLeftY = 5
#set the row and column for the grid
_gridRow = 20
_gridColumn = 10

#status of the game, whether paused or started
STATUS_TEXT = "STARTED"
#Game dispaly area
_display = None
#position on the grid occupied by the blocks
_filledPositions = {}
#occupied positions
_lockedPositions = {}
_firstPiece = True
#grid
grid = None
#global flag to start another tetrimonone
_reset = False

# create the shapes, notice that the shapes is a grid of 5 x 5
# and the first 2 rows, last row, first column and last column are empty
# shapes rotation
_s = [
        [
            '0000000000',
            '0000000000', 
            '0000110000',
            '0001100000',
            '0000000000'
        ],
        [
            '0000000000',
            '0000100000',
            '0000110000',
            '0000010000',
            '0000000000'
        ]
]

_z = [
        [
            '0000000000',
            '0000000000',
            '0001100000',
            '0000110000',
            '0000000000'
        ],
        [
            '0000000000',
            '0000100000',
            '0001100000',
            '0001000000',
            '0000000000'
        ]
]

_i = [
        [
            '0000100000',
            '0000100000',
            '0000100000',
            '0000100000',
            '0000000000'
        ],
        [
            '0000000000',
            '0011110000',
            '0000000000',
            '0000000000',
            '0000000000'
        ]
]

_o = [
        [
            '0000000000',
            '0000000000',
            '0000110000',
            '0000110000',
            '0000000000'
        ]
]

_mL = [
        [
            '0000000000',
            '0001000000',
            '0001110000',
            '0000000000',
            '0000000000'
        ],
        [
            '0000000000',
            '0000110000',
            '0000100000',
            '0000100000',
            '0000000000'
        ],
        [
            '0000000000',
            '0000000000',
            '0001110000',
            '0000010000',
            '0000000000'
        ],
        [
            '0000000000',
            '0000100000',
            '0000100000',
            '0001100000',
            '0000000000'
        ]
]

_l = [
        [
            '0000000000',
            '0000010000',
            '0001110000',
            '0000000000',
            '0000000000'
        ],
        [
            '0000000000',
            '0000100000',
            '0000100000',
            '0000110000',
            '0000000000'
        ],
        [
            '0000000000',
            '0000000000',
            '0001110000',
            '0001000000',
            '0000000000'
        ],
        [
            '0000000000',
            '0001100000',
            '0000100000',
            '0000100000',
            '0000000000'
        ]
]

_t = [
        [
            '0000000000',
            '0000100000',
            '0001110000',
            '0000000000',
            '0000000000'
        ],
        [
            '0000000000',
            '0000100000',
            '0000110000',
            '0000100000',
            '0000000000'
        ],
        [
            '0000000000',
            '0000000000',
            '0001110000',
            '0000100000',
            '0000000000'
        ],
        [
            '0000000000',
            '0000100000',
            '0001100000',
            '0000100000',
            '0000000000'
        ]
]
#shapes array
_shapes = [_s, _z, _i, _o, _mL, _l, _t]
#shapes colours
_shapesColours = [
    (151, 151, 151),
    (1, 1, 255),
    (1, 255, 255),
    (255, 1, 1),
    (255, 1, 255),
    (255, 255, 1),
    (255, 255, 255)
]
_shapesWidth = [3, 3, 1, 2, 3, 3, 3]

#creating classes to handle each independent feature
class Block(object):
    def __init__(self, shape):
        self.xMin = 0 #closest point from the left wall of the game area
        self.xMax = 0 #closest point from the left wall of the game area
        self.y = 0 #closest point from the bottom of the game area
        self.shape = shape #current shape
        self.colour = _shapesColours[_shapes.index(shape)] #colour of shape
        self.rotation = 0 #current shape item in the shape list
        self.pos = -1 #how many times the tetrimone has move down
        self.width = _shapesWidth[_shapes.index(shape)] #the width of the shape in blocks

def getShape():
    "This returns a random shape"
    return random.choice(_shapes)

#This function is used to convert the shapes variable to real shapes block
def shapeToBlock(piece):
    "Converts string of 0's and 1's to a block of tetrimone"
    shape = piece.shape[piece.rotation % len(piece.shape)]



def logger(message, flag = "verbose"):
    "This class is used for logging out verbose"
    
    if(flag == "verbose"):
        print(message)
    elif(flag == "error"):
        print("Error Message-- ", message)
    
    return

#This function is used to draw all what is needed on the screen
def drawWindow(surface, block, reset = False):
    "Draws the entire window"
    global STATUS_TEXT #This indicates whether the game is paused or not
    #draw the grid for the game
    drawGrid(surface, block, reset)

    #draw a window to envelop other items to be used in the game
    width = _displayWidth - _topLeftX - _gameWidth
    height = _displayHeight - _topLeftY
    x = _topLeftX + _gameWidth + 5
    y = _topLeftY
    pygame.draw.rect(surface, (211, 211, 211), (x, y, width, height))

    #draw the start button
    #draw the pause button
    #draw scores
    colour = (211, 11, 11)
    status = _font.render("Status: " + STATUS_TEXT, 1, colour)
    scoreLabel = _font.render("Scores: ", 1, colour)
    highScoreLabel = _font.render("Highscore: ", 1, colour)
    #get the x and y positions of the status
    statusX = x + 5
    statusY = y + 5
    height = 31
    #get the x and y positions for the score label
    scoreY = statusY + 2 * height
    #get the x and y positions for the high score label
    hScoreY = scoreY + 2 * height
    #draw status
    surface.blit(status, (statusX, statusY))
    #draw scores
    surface.blit(scoreLabel, (statusX, scoreY))
    #draw high scores
    surface.blit(highScoreLabel, (statusX, hScoreY))

    return

#Draws a tetrimone on the screen
def drawTetrimones(block):
    "Draws the tetrimone on the screen"
    global _filledPositions
    global _lockedPositions
    global _gridRow
    global grid
    _filledPositions = {}

    #contains x and y values used to check the distance of the block from the walls of the game area
    # xValues, yValues = [], [] 

    # for row, item in enumerate(block.shape[block.rotation]):
    # for row, _ in enumerate(block.shpae[block.rotation]):
    #     test = True
    #     for col, value in enumerate(list(_)):
    #         if value == "1":
    #             if(test):
    #                 block.pos += 1
    #                 test = False

    #             xValues.append(col)
    #             yValues.append(row)

    #             #fill space
    #             grid[block.pos][col] = block.colour
    #             _filledPositions[(row, col)] = block.colour
    block.pos += 1
    columns = []
    count = -1 #used to increment the rows of the list in the for the column
    #get the columns of the block
    for row, _ in enumerate(block.shape[block.rotation]):
        test = True
        l = []
        for col, value in enumerate(list(_)):
            if value == "1":
                if(test):
                    count += 1
                    test = False
                l.append(col)
        # columns[row][col] = col #Only the columns are needed
        if(len(l) >= 1):
            columns.append(l) #Only the columns are needed
    
    #get min and max
    minX = []
    maxX = []
    for item in columns:
        minX.append(min(item))
        maxX.append(max(item))

    #set the min and max x values of the block
    block.xMin = min(minX)
    block.xMax = max(maxX)

    if block.pos == 0:
        lCol = columns.pop()
        for _, element in enumerate(lCol):
            grid[block.pos][element] = block.colour
            _filledPositions[(block.pos, element)] = block.colour
        # print("Grid now is: ", grid)
    elif block.pos > 0 and block.pos < _gridRow:
        last = block.pos
        for row in range(len(columns)):
            lCol = columns.pop()
            for _, element in enumerate(lCol):
                grid[last][element] = block.colour
                _filledPositions[(last, element)] = block.colour
            last -= 1
        # print("Grid now is: ", grid)
        print("Filled is: ", _filledPositions)
    else:
        pass
        # quit()

    

    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if(row, col) in _lockedPositions:
                grid[row][col] = _lockedPositions[(row, col)]

    # #find the x and y values
    # if(row < _gridRow): #do this only when the bottom of the tetrimones is above the bottom of the grid
    #     block.xMin = sorted(xValues)[0]
    #     block.xMax = sorted(xValues).pop()
    #     block.y = sorted(yValues)[0]
    return

#This function is used to check the position of the tetrimone if it is valid
def checkValidSpaceHorizontal(block, value):
    "Checks whether it is okay to move left"
    global _gridColumn
    passed = True

    if block.xMin + value < 0 or block.xMax + value >= _gridColumn:
        passed = False

    return passed

#pads the sides tetrimones with 0's
def padSideBlock(block, value):
    if(value == 1): #moved right, pad the left
        for row, item in enumerate(block.shape):
            for col, value in enumerate(item):
                nShape = list(value)
                nShape.pop()

                nString = ""
                for i in nShape:
                    nString += i

                block.shape[row][col] = "0" + nString

    elif(value == -1): #move left, pad the right
        for row, item in enumerate(block.shape):
            for col, value in enumerate(item):
                nShape = list(value)
                nShape.pop(0)

                nString = ""
                for i in nShape:
                    nString += i

                block.shape[row][col] = nString + "0"

#pads the top of the tetrimones with 0's
def padTopBlock(block):
    global _gridColumn
    insert = ""
    for _ in range(_gridColumn):
        insert += "0"

    for index, item in enumerate(block.shape):
            item.insert(0, insert)
            block.shape[index] = item

#This function is used to draw the grid for the game
def drawGrid(surface, block, reset):
    "Draws the grid on the surface"
    global _filledPositions #bring in the global _filledPositions
    global grid
    surface.fill((1, 1, 1)) #This fills the surface with black colour

    #reset the filledposition if necessary
    if reset == True:
        _filledPositions = {}

    createGrid(_filledPositions, reset)
    drawTetrimones(block)
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            pygame.draw.rect(surface, grid[row][col], (_topLeftX + col * _blockSize, _topLeftY + row * _blockSize, _blockSize, _blockSize), 0)
            pygame.draw.rect(surface, (255, 255, 255), (_topLeftX + col * _blockSize, _topLeftY + row * _blockSize, _blockSize, _blockSize), 1)

    #draw a border for the game
    pygame.draw.rect(surface, (151, 211, 251), (_topLeftX, _topLeftY, _gameWidth, _gameHeight), 2)

#This function is used to create the grid on the game area
def createGrid(filledPositions = {}, reset = False):
    global grid
    "This function is used to create the grid in the display area"
    grid = [[(1, 1, 1) for _ in range(_gridColumn)] for _ in range(_gridRow)]
    
    # #find the filled position in the grid
    # for row in range(len(grid)):
    #     for col in range(len(grid[row])):
    #         if(row, col) in filledPositions:
    #             grid[row][col] = filledPositions[(row, col)]
        
    #return value is the grid

#This function is used to rotate a piece
def rotatePiece(block):
    block.rotation = (block.rotation + 1) % len(block.shape)
    pass

def getIntercept():
    #increment filledkeys to that you get the positions it is just above the locked positions
    tempFilledKeys = _filledPositions.keys() #holds a copy of the filledkeys
    tupleList = [] #this will hold the modified tuples
    for element in tempFilledKeys:
        first = True
        tupleToJoin = []
        for row in element:
            if first:
                row += 1
                first = False
                # print("Row: ", row)

            tupleToJoin.append(row) #append the row with the column to a list
        
        #convert the list to a tuple and append it to the tuple list
        tupleList.append(tuple(tupleToJoin))
    print("Tuplelist: ", tupleList)
    # quit()

    return tupleList

#checks which row is completely filled
def filledRows():
    global _lockedPositions #get the locked position into this scope
    global _gridColumn #get the gridCol into this scope
    global _gridRow #get the gridRow into this scope

    tempFilledKeys = _lockedPositions.keys() #holds a copy of the locked positions
    tupleList = [] #this will hold the modified tuples
    clearList = [] #holds the rows to clear
    for row in range(_gridRow):
        count = 0
        for col in range(_gridColumn):
            if (row, col) in tempFilledKeys:
                count += 1 #increment the count of the columns found

        #check if the columns in each row is filled
        if count == _gridColumn:
            clearList.append(row)
    
    if(len(clearList) > 0):
        clearRow(clearList)

#clears a completely filled row
def clearRow(value):
    global _lockedPositions #get the locked position into this scope
    global _gridColumn #get the gridCol into this scope

    newLockedPositions = {} #set the new locked positions
    tempFilledKeys = _lockedPositions.keys() #holds a copy of the locked positions
    value = sorted(value)
    # value.reverse() #sort the list of rows in descending order
    # for row in range(0, _gridRow): #from the bottom of the grid
    for i in value: #from the bottom of the grid
        #set all the grid values above it by bringing one row down
        for row in range(i):
            for col in range(_gridColumn): #all the columns
                #bring down all the rows above it
                nRow = row + 1 #bring down the row by 1 grid row
                if((row, col) in _lockedPositions):
                    cellColour = _lockedPositions[(row, col)] #cell colour of the previous column
                    newLockedPositions[(nRow, col)] = cellColour
        print("Set new locked positions: ", newLockedPositions)
        #set all the grid values below 
        for row in range(i, _gridRow):
            print("Rows below clear point: ", row)
            continue
            for col in range(_gridColumn): #all the columns
                cellColour = _lockedPositions[(row, col)] #cell colour of the previous column
                newLockedPositions[(row, col)] = cellColour
        print("Set new locked positions: ", newLockedPositions)
        quit()

    #assign the new locked positions to the old one
    print("locked positions: ", _lockedPositions)
    print("New locked positions: ", newLockedPositions)
    # quit()
    _lockedPositions = newLockedPositions

#This is the main part of the game
def start():
    pygame.init() #Initialize game
    pygame.font.init() #This initializes the font for writing
    global _font
    global STATUS_TEXT
    global _gridRow
    global _reset
    global _lockedPositions
    global _filledPositions
    global _firstPiece

    _font = pygame.font.SysFont("times new roman", 31)
    display = pygame.display.set_mode((_displayWidth, _displayHeight)) #set width and height
    pygame.display.set_caption("Tetris") #set caption or title of game

    clock = pygame.time.Clock() #get the clock of the game
    fallTime = 0 #time in millisec
    gravity = 0.2

    #blocks
    shape = getShape()#generates a random shape
    currentBlock = Block(shape)
    
    crashed = False

    #update the status
    x1 = _topLeftX + _gameWidth + 5
    y1 = _topLeftY
    x = x1 + 5
    y = y1 + 5
    height = 31
    width = _displayWidth - x
    stutusRect = pygame.Rect(x, y, width, height)

    #for changing the shape of the current piece
    reset = False

    # drawWindow(display, currentBlock, reset) #draws all that is needed in the game
    # #display the game
    # pygame.display.update()

    #game loop
    while not crashed:
        #change the value of reset on every loop
        reset = False

        for event in pygame.event.get():
            pygame.display.update()
            if event.type == pygame.QUIT:
                crashed = True
                break
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        #change the status of the game
                        STATUS_TEXT = "STARTED" if STATUS_TEXT == "PAUSED" else "PAUSED"
                        logger("Space bar pressed, STATUS_TEXT: " +  STATUS_TEXT, "verbose")
                    elif STATUS_TEXT == "STARTED":
                        if event.key == pygame.K_q:
                            _filledPositions = {}
                            reset = True
                            currentBlock = Block(getShape())
                        elif event.key == pygame.K_UP:
                            rotatePiece(currentBlock)
                            logger("UP KEY PRESSED", "verbose")
                        elif event.key == pygame.K_DOWN:
                            logger("DOWN KEY PRESSED", "verbose")

                        elif event.key == pygame.K_RIGHT:
                            logger("RIGHT KEY PRESSED", "verbose")
                            #increase the step to the right by one
                            if currentBlock.xMax < _gridColumn:
                                if checkValidSpaceHorizontal(currentBlock, 1):
                                    padSideBlock(currentBlock, 1)

                        elif event.key == pygame.K_LEFT:
                            logger("LEFT KEY PRESSED", "verbose")
                            #increase the step to the left by one
                            if currentBlock.xMin > 0:
                                if checkValidSpaceHorizontal(currentBlock, -1):
                                    padSideBlock(currentBlock, -1)

        if STATUS_TEXT == "STARTED":
            fallTime += clock.get_rawtime() #get how long it took to get here
            clock.tick()


            #check when to drop the tetrimones
            if(fallTime / 1000 > gravity):
                fallTime = 0
                drawWindow(display, currentBlock, reset)

            if _firstPiece:
                if(currentBlock.pos >= _gridRow - 1):
                    currentBlock = Block(getShape())
                    _lockedPositions = _filledPositions
                    _firstPiece = False
            else:
                tupleList = getIntercept()
                lockedKeys = _lockedPositions.keys()

                #check whether the falling block is just above the blocks locked
                for element in lockedKeys:
                    # if element in filledKeys:
                    if element in tupleList:
                        print("Hit`")
                        # STATUS_TEXT = "PAUSED"
                        #start a new block
                        _lockedPositions = dict(list(_lockedPositions.items()) + list(_filledPositions.items()))
                        currentBlock = Block(getShape())
                        _filledPositions = {}
                        break #do not continue because one square in on top another
                
                #else if the block is at the bottom, then it did not intercept the one before it
                if(currentBlock.pos >= _gridRow - 1):
                    currentBlock = Block(getShape())
                    _lockedPositions = dict(list(_lockedPositions.items()) + list(_filledPositions.items()))


            # padTopBlock(currentBlock)
    
            #end of game loop
            # crashed = True
            pygame.display.update()
            
            #clear the locked positions that are complete
            filledRows()
            print("Locked: ", _lockedPositions)

    #finalize anything and close the window
    pygame.quit()
    quit()

#start the game
if (__name__ == "__main__"):
    start()