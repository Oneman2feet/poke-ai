from PIL import Image

class Sprite:

    def __init__(self):
        # read resource files
        self.trainer = Image.open('./sprites/trainer.png').convert('RGBA')
        #r, g, b, a = trainer.getpixel((0, 0))
        #print((r ,g, b, a))

    def isCharacter(self, ob):
        characterRow = 68
        characterCol = 113
        spriteRow = 76
        spriteCol = 1
        trainerHeight = 18
        trainerWidth = 14
        row = 8
        col = 0
        sames = 0
        for row in range(trainerHeight):
            for col in range(trainerWidth):
                gameRow = characterRow + row
                gameCol = characterCol + col
                imgRow = spriteRow + row
                imgCol = spriteCol + col
                gamePixel = ob[gameRow][gameCol]
                imgPixel = self.trainer.getpixel((imgCol, imgRow))
                print((gameRow, gameCol))
                print(gamePixel)
                print((imgRow, imgCol))
                print(imgPixel)
                same = False
                if (imgPixel[3]==0):
                    same = True
                elif (gamePixel[0]==imgPixel[0] and gamePixel[1]==imgPixel[1] and gamePixel[2]==imgPixel[2]):
                    same = True
                print(same)
                if same:
                    sames+=1
        print("done, %d pixels match out of %d" % (sames, trainerWidth * trainerHeight))