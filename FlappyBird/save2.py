import pygame
import random
import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

def main():
    global bgPic
    global gameStarted
    global speedOfBg
    global xOfBg
    global xOfBird
    global yOfbird
    global screen
    global score
    global jumpSpeed
    global vertSpeed
    global fallingConst
    global gameOver
    global blockList
    global blockSpeed
    global scoreTime
    global upperPic
    global downerPic
    global gameOverPic
    
    scoreTime = 0
    gameStarted = False
    gameOver = False
    speedOfBg = 3
    xOfBg = 0
    xOfBird = 130
    yOfBird = 400
    score = 0
    jumpSpeed = -10
    vertSpeed = 0
    fallingConst = 0.4
    blockList = []
    blockSpeed = 5

    pygame.init()
    
    size = [1024, 718]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("FlappyBird")

    bgPic = pygame.image.load("bg.png").convert()
    birdPic = pygame.image.load("birdy.png")
    birdPic = pygame.transform.scale2x(birdPic)
    orjBird = birdPic

    upperPic = pygame.image.load("upper.png")
    upperPic =  pygame.transform.scale2x(upperPic)
    downerPic = pygame.image.load("downer.png")
    downerPic =  pygame.transform.scale2x(downerPic)

    gameOverPic = pygame.image.load("gameOver.png")
    gameOverPic = pygame.transform.scale2x(gameOverPic)

    class Block:
        def __init__(self, upper, downer):
            self.xValue = 1300
            self.yValue = random.randrange(200) - 400
            self.upperPic = upper
            self.downerPic =  downer
            self.counted = False
            
        def draw(self, screen):
            screen.blit(self.upperPic, [self.xValue, self.yValue])
            screen.blit(self.downerPic, [self.xValue, self.yValue + 640 + 280])

        def check(self, x, y):
            if (x+70) > self.xValue and x < self.xValue + 100:
                if y < self.yValue + 640 or y > self.yValue + 640 + 280:
                    return True
                elif self.counted == False:
                    self.counted = True
                    return False
    #3 Blocks
    difference = 400
    
    blockList.append(Block(upperPic, downerPic))
    blockList.append(Block(upperPic, downerPic))
    blockList.append(Block(upperPic, downerPic))
    blockList.append(Block(upperPic, downerPic))
    
    blockList[1].xValue = 1300 + difference 
    blockList[2].xValue = 1300 + difference * 2
    blockList[3].xValue = 1300 + difference * 3
    
    done = False
    clock = pygame.time.Clock()
    pygame.time.set_timer(pygame.USEREVENT + 1, 1500)
    
    while not done:
        #Controls
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                if event.key == pygame.K_SPACE:
                    if gameStarted == False and gameOver == False:
                        gameStarted = True
                        vertSpeed = jumpSpeed
                    elif gameStarted and gameOver == False:
                        vertSpeed = jumpSpeed
        
        screen.fill(WHITE)
        
        screen.blit(bgPic, [xOfBg,0])
        screen.blit(bgPic, [xOfBg+401,0])
        screen.blit(bgPic, [xOfBg+802,0])
        screen.blit(bgPic, [xOfBg+1203,0])
        xOfBg -= speedOfBg
        if(xOfBg < -401):
            xOfBg = 0

        birdPic = pygame.transform.rotate(orjBird,math.degrees(math.atan(-vertSpeed/20)))
        screen.blit(birdPic, [xOfBird, yOfBird])

        for block in blockList:
            if gameStarted:
                block.xValue -= blockSpeed
            block.draw(screen)
            if(block.xValue < -300):
                block.xValue = 1300
            if block.check(xOfBird, yOfBird):
                gameStarted = False
                gameOver = True
            else:
                if(scoreTime >= 20):
                    score += 1
                    scoreTime = 0
        scoreTime += 1
        
        if yOfBird > 725:
            gameStarted = False
            gameOver = True
            menuFont = pygame.font.SysFont('Arial', 60, True, False)
            screen.blit(menuFont.render("Score: " + str(score), True, WHITE), [400, 350])
            screen.blit(gameOverPic, [340,250])
            pygame.display.flip()
            pygame.time.delay(5000)
            yOfBird = 400
            xOfBird = 130
            gameOver = False
            blockList = []
            score = 0
            blockList[1].xValue = 1300 + difference 
            blockList[2].xValue = 1300 + difference * 2
            blockList[3].xValue = 1300 + difference * 3
            
        if gameOver:
            xOfBird -= blockSpeed
        
        if(gameStarted) and gameOver == False:
            printScore()
        elif gameStarted == False and gameOver == False:
            printIns()

        pygame.display.flip()

        yOfBird += vertSpeed
        vertSpeed += fallingConst
        if gameStarted == False and yOfBird >= 400 and gameOver == False:
            vertSpeed = jumpSpeed
        clock.tick(60)
    pygame.quit()

def printIns():
    menuFont = pygame.font.SysFont('Arial', 30, True, False)
    screen.blit(menuFont.render("Press SPACE to begin (Also to jump)", True, WHITE), [300, 600])
    menuFont = pygame.font.SysFont('Arial', 15, True, False)
    screen.blit(menuFont.render("Flappy Birdy By Fatih AKTAS", True, WHITE), [450, 640])

def printScore():
    menuFont = pygame.font.SysFont('Arial', 30, True, False)
    screen.blit(menuFont.render("Score: "+ str(score), True, WHITE), [880, 10])
    
if __name__ == "__main__":
    main()
