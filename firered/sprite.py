from PIL import Image

class Sprite:

    def __init__(self):
        # read resource files
        self.trainer = Image.open('./sprites/trainer.png').convert('RGBA')
        #r, g, b, a = trainer.getpixel((0, 0))
        #print((r ,g, b, a))
        self.trainerRow = 64 # position of sprite in game (centered)
        self.trainerCol = 112 # position of sprite in game (centered)
        self.trainerWidth = 16
        self.trainerHeight = 24
        self.trainerDownRow = 0
        self.trainerLeftRow = self.trainerHeight * 1
        self.trainerRightRow = self.trainerHeight * 2
        self.trainerUpRow = self.trainerHeight * 3

    def matchesSprite(self, ob, startRow, startCol, im, spriteRow, spriteCol, spriteWidth, spriteHeight):
        score = 0
        for row in range(spriteHeight):
            for col in range(spriteWidth):
                gameRow = startRow + row
                gameCol = startCol + col
                imgRow = spriteRow + row
                imgCol = spriteCol + col
                gamePixel = ob[gameRow][gameCol]
                imgPixel = im.getpixel((imgCol, imgRow))
                if (imgPixel[3]!=0):
                    if (gamePixel[0]==imgPixel[0] \
                        and gamePixel[1]==imgPixel[1] \
                        and gamePixel[2]==imgPixel[2]):
                        score += 1
        return score

    def isCharacterDown(self, ob):
        for col in range(1):
            score = self.matchesSprite(ob, self.trainerRow, self.trainerCol, self.trainer, self.trainerDownRow, col * self.trainerWidth, self.trainerWidth, self.trainerHeight)
            if (score > 170):
                return True
            return False

    def isCharacterLeft(self, ob):
        for col in range(1):
            score = self.matchesSprite(ob, self.trainerRow, self.trainerCol, self.trainer, self.trainerLeftRow, col * self.trainerWidth, self.trainerWidth, self.trainerHeight)
            if (score > 170):
                return True
            return False
    
    def isCharacterRight(self, ob):
        for col in range(1):
            score = self.matchesSprite(ob, self.trainerRow, self.trainerCol, self.trainer, self.trainerRightRow, col * self.trainerWidth, self.trainerWidth, self.trainerHeight)
            if (score > 170):
                return True
            return False

    def isCharacterUp(self, ob):
        for col in range(1):
            score = self.matchesSprite(ob, self.trainerRow, self.trainerCol, self.trainer, self.trainerUpRow, col * self.trainerWidth, self.trainerWidth, self.trainerHeight)
            if (score > 170):
                return True
            return False

    def characterDirection(self, ob):
        if (self.isCharacterDown(ob)):
            return 1
        elif (self.isCharacterLeft(ob)):
            return 2
        elif (self.isCharacterRight(ob)):
            return 0
        elif (self.isCharacterUp(ob)):
            return 3
        else:
            return -1