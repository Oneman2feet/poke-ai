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
        self.trainerUp = (self.trainerHeight * 3, 0)

    def matchesSprite(self, ob, startRow, startCol, im, spriteRow, spriteCol, spriteWidth, spriteHeight):
        for row in range(spriteHeight):
            for col in range(spriteWidth):
                gameRow = startRow + row
                gameCol = startCol + col
                imgRow = spriteRow + row
                imgCol = spriteCol + col
                gamePixel = ob[gameRow][gameCol]
                imgPixel = im.getpixel((imgCol, imgRow))
                if (imgPixel[3]!=0 and (gamePixel[0]!=imgPixel[0] or gamePixel[1]!=imgPixel[1] or gamePixel[2]!=imgPixel[2])):
                    return False
        return True

    def isCharacterUp(self, ob):
        return self.matchesSprite(ob, self.trainerRow, self.trainerCol, self.trainer, self.trainerUp[0], self.trainerUp[1], self.trainerWidth, self.trainerHeight)