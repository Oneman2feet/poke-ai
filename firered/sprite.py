from PIL import Image

class Sprite:

    def __init__(self):
        # read resource files
        self.trainer = Image.open('./sprites/trainerresize.png').convert('RGBA')
        #r, g, b, a = trainer.getpixel((0, 0))
        #print((r ,g, b, a))
        self.trainerWidth = 16
        self.trainerHeight = 24
        self.trainerUp = (self.trainerHeight * 3, 0)

    def isCharacter(self, ob):
        characterRow = 68
        characterCol = 113
        sames = 0
        for row in range(self.trainerHeight):
            for col in range(self.trainerWidth):
                gameRow = characterRow + row
                gameCol = characterCol + col
                imgRow = self.trainerUp[0] + row
                imgCol = self.trainerUp[1] + col
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
        print("done, %d pixels match out of %d" % (sames, self.trainerWidth * self.trainerHeight))