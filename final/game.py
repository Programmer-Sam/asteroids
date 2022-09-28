import pygame
pygame.init()
clock=pygame.time.Clock()
import math
import random
import numpy as np
import MenuRender

'''---------------------resolution size--------------------------------------'''
'''
from win32api import GetSystemMetrics
maxWidth= GetSystemMetrics(0)
maxHeight= GetSystemMetrics(1)
print(maxWidth,maxHeight)
import ctypes
user32 = ctypes.windll.user32
maxWidth, maxHeight = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


import tkinter
root = tkinter.Tk()
maxWidth = root.winfo_screenwidth()
maxHeight = root.winfo_screenheight()
'''

def main(maxWidth,maxHeight,colour1,colour2,colour3,colour4,NumberOfEnemies,done,canvas,baseHealth,speed,shieldLength,damage):
    '''---------------------objects------------------------------------------'''
    class gameEntities():
        def __init__(self,screenDim,pos,health,colour,degrees, movVector):
            self.canvasSize=screenDim

            self.posVector = pos
            self.movVector = movVector
            self.Health = health
            self.Colour = colour
            self.degrees = degrees  

            self.collisionSurfaces = []
        def move(self):
            self.posVector[0]+=self.movVector[0]
            self.posVector[1]+=self.movVector[1]
            if self.vertices != None:
                for i in range (0, len (self.vertices)):
                    self.vertices[i][0] += self.movVector[0]
                for i in range (0, len (self.vertices)):
                    self.vertices[i][1] += self.movVector[1]
        def wallCollision(self):
            if self.posVector[0]<30:
                self.posVector[0]=30
                self.movVector[0] = 1
            elif self.posVector[0]> self.canvasSize[0]-30:
                self.posVector[0]= self.canvasSize[0]-30
                self.movVector[0] = -1
            if self.posVector[1]<30:
                self.posVector[1]= 30
                self.movVector[1] = 1
            elif self.posVector[1]> self.canvasSize[1]-30:
                self.posVector[1] = self.canvasSize[1]-30
                self.movVector[1] = -1
        def vertexCalc(self, vertexDirection, pixelLength):
            pi = math.pi
            xPoint = (self.posVector[0]+(((math.cos(((self.degrees+vertexDirection)*pi)/180)*pixelLength)))+((math.cos(((self.degrees+vertexDirection)*pi)/180)*pixelLength)))
            yPoint = (self.posVector[1]+(((math.sin(((self.degrees+vertexDirection)*pi)/180)*pixelLength)))+((math.sin(((self.degrees+vertexDirection)*pi)/180)*pixelLength)))
            return [int(xPoint), int(yPoint)]
        def takeDamage(self):
            self.Health -= 1
        def checkDeath(self):
            if self.Health <= 0:
                return True
            else:
                return False
        def returnVariables(self):
            return (int(self.posVector[0]),int(self.posVector[1])),self.Colour,self.degrees
        def getPosition(self):
            return [int(self.posVector[0]),int(self.posVector[1])]
        def getDegrees(self):
            return self.degrees
        def getVertices(self):
            return self.vertices
        def setCollisionSurfaces(self, inpList):
            self.collisionSurfaces = inpList
        def test(self,colour):
            self.Colour = colour
        def setMovementVector(self,inp):
            self.movVector = inp
            
    class player(gameEntities):
        def __init__(self,screenDim,colour,invColour,baseHealth,speed,shieldLength,damage ): #instantiation takes in new level arguements
            startPosition = [screenDim[0]/2,screenDim[1]/2]
            super().__init__(screenDim,startPosition, 5+baseHealth, (colour), 270, [0,0])
            self.vertices = [self.vertexCalc(0,20), self.vertexCalc(135,20), self.vertexCalc(-135,20)]
            self.baseColour = colour#edit
            self.invulnerableColour = invColour
            self.lastHit = 0
            self.invulnerable = False
            self.speedMultiplier = 4 + speed #creates a speed multiplier attribute
            self.shieldCooldown = shieldLength*10

            self.score = 0
            self.projectilesShot = 0
            self.destroyedAsteroids = 0
        def turnLeft(self):
            self.degrees -=5
            if self.degrees < 0:
                self.degrees = 360 - (self.degrees * -1)
            elif self.degrees<=360:
                self.degrees=self.degrees%360
        def turnRight(self):
            self.degrees +=5
            if self.degrees < 0:
                self.degrees = 360 - (self.degrees * -1)
            elif self.degrees<=360:
                self.degrees=self.degrees%360
        def accelerate(self):
            D2R= (math.pi) / 180
            self.movVector[0] += math.cos(D2R*self.degrees)*0.05 * 1.2*(-math.e**(-0.1*self.speedMultiplier)+1)
            self.movVector[1] += math.sin(D2R*self.degrees)*0.05 * 1.2*(-math.e**(-0.1*self.speedMultiplier)+1)
            
        def decelerate(self):
            if self.movVector[0]>0.1:
                self.movVector[0]-=0.05
            elif self.movVector[0]<-0.1:
                self.movVector[0]+=0.05

            if self.movVector[1]>0.1:
                self.movVector[1]-=0.05
            elif self.movVector[1]<-0.1:
                self.movVector[1]+=0.05
        def move(self):
            self.vertices = [self.vertexCalc(0,20), self.vertexCalc(135,20), self.vertexCalc(-135,20)]
            self.posVector[0]+=self.movVector[0]
            self.posVector[1]+=self.movVector[1]
            for i in range (0, len (self.vertices)):
                self.vertices[i][0] += self.movVector[0]
            for i in range (0, len (self.vertices)):
                self.vertices[i][1] += self.movVector[1]
        def renderChar(self, canvas):
            pygame.draw.line(canvas,  self.Colour, self.vertices[0], self.vertices[1],5)
            pygame.draw.line(canvas,  self.Colour, self.vertices[0], self.vertices[2],5)
            pygame.draw.line(canvas,  self.Colour, self.vertices[2], self.vertices[1],5)
            if self.invulnerable:
                pygame.draw.circle(canvas, (self.invulnerableColour), (int(self.posVector[0]),int(self.posVector[1])), 60, 5)
        def invulnerabilityRender(self,tick):
            if (tick - self.lastHit) > 3000+self.shieldCooldown:
                self.invulnerable = False
            if self.invulnerable:
                self.Colour = self.invulnerableColour #edit
            else:
                self.Colour = self.baseColour
        def takeDamage(self, tick):
            if (tick - self.lastHit) > 3000+self.shieldCooldown:
                self.Health -= 1
                self.lastHit = tick
                self.invulnerable = True
        def increaseScore(self,increaseFactor):
            self.score = self.score + increaseFactor
        def incrementProjectile(self):
            self.projectilesShot +=1
        def incrementAsteroids(self):
            self.destroyedAsteroids +=1
    class projectile(gameEntities):
        def __init__(self, screenDim, startPosition, degrees,colour):
            super().__init__(screenDim,startPosition, 1, (colour), degrees, [0,0])
            D2R= (math.pi) / 180
            self.movVector= [math.cos(D2R*self.degrees)*6,math.sin(D2R*self.degrees)*6]
            self.vertices = None
        def renderProj(self, canvas):
            pygame.draw.circle(canvas, (self.Colour), (int(self.posVector[0]),int(self.posVector[1])), 5, 0)
        def wallCollision(self):
            delete = False
            if self.posVector[0]<30:
                delete = True
            elif self.posVector[0]> self.canvasSize[0]-30:
                delete = True
            if self.posVector[1]<30:
                delete = True
            elif self.posVector[1]> self.canvasSize[1]-30:
                delete = True
            return delete
    class meteor(gameEntities):
        def __init__(self,screenDim,colour,player1):
            position, colour2, deg = player1.returnVariables()
            x = random.randint(70,screenDim[0]-70)
            y = random.randint(70,screenDim[1]-70)
            while (position[0]-100< x < position[0]+100) and (position[1]-100< y < position[1]+100):
                x = random.randint(70,screenDim[0]-70)
                y = random.randint(70,screenDim[1]-70)
            startPosition = [x,y]        
            super().__init__(screenDim,startPosition, 4, (colour), 0, [random.randint(-3,3),random.randint(-3,3)])#customise speed
            self.vertices = [self.vertexCalc(0,random.randint(10,40)),
                             self.vertexCalc(60,random.randint(10,40)),
                             self.vertexCalc(120,random.randint(10,40)),
                             self.vertexCalc(180,random.randint(10,40)),
                             self.vertexCalc(240,random.randint(10,40)),
                             self.vertexCalc(300,random.randint(10,40))]
            self.lastHit = 0
        def renderMet(self, canvas):
            pygame.draw.line(canvas, (self.Colour), self.vertices[0], self.vertices[len(self.vertices)-1], 5)
            for i in range (len(self.vertices)-1):
                pygame.draw.line(canvas, self.Colour, self.vertices[i], self.vertices[i+1], 5)

        def wallCollision(self):
            if self.posVector[0]<30:
                self.posVector[0]=30
                self.movVector[0] = self.movVector[0]*-1
            elif self.posVector[0]> self.canvasSize[0]-30:
                self.posVector[0]= self.canvasSize[0]-30
                self.movVector[0] = self.movVector[0]*-1
            if self.posVector[1]<30:
                self.posVector[1]= 30
                self.movVector[1] = self.movVector[1]*-1
            elif self.posVector[1]> self.canvasSize[1]-30:
                self.posVector[1] = self.canvasSize[1]-30
                self.movVector[1] = self.movVector[1]*-1
                
        def enemyCollision(self, collisionVector,movementVector2 , tick, obj2):
            #https://scipython.com/blog/two-dimensional-collisions/
            #https://en.wikipedia.org/wiki/Elastic_collision

            #https://www.youtube.com/watch?v=fdZfddO7YTs
            #https://www.pearsonschoolsandfecolleges.co.uk/secondary/Mathematics/16plus/EdexcelModularMathematicsforASandALevel/Samples/NewSampleChapters/Mechanics4SampleChapter.pdf
            #http://www.sciencecalculators.org/mechanics/collisions/
            
            #Oblique Collision Maths
            temp = tick - self.lastHit
            if temp>=100:
                A = np.array(self.posVector)
                A_v = np.array(self.movVector)
                abs_A = math.sqrt(self.movVector[0]**2 + self.movVector[1]**2)
                B = np.array(collisionVector)
                B_v = np.array(movementVector2)
                abs_B = math.sqrt(movementVector2[0]**2 + movementVector2[1]**2)

                newVector = np.subtract(A_v , (((np.dot((np.subtract(A_v,B_v)),(np.subtract(A,B))))/(np.linalg.norm(A-B)**2))*(np.subtract(A,B))))
                self.movVector = newVector

                newVector2 = np.subtract(B_v , (((np.dot((np.subtract(B_v,A_v)),(np.subtract(B,A))))/(np.linalg.norm(B-A)**2))*(np.subtract(B,A))))
                obj2.setMovementVector(newVector2)
            self.lastHit = tick
            obj2.setlastHit = tick
        def setLastHit(self, inp):
            self.lastHit = inp
    '''---------------------GAME LOGIC----------------------------------------------------------------------------------------------'''
    def projectilesProcedure():
        for i in projectileLinkedList:
            i.move()
            i.renderProj(canvas)
            if i.wallCollision()==True:
                projectileLinkedList.remove(i)
                del i
    def playerProcedure():
        player1.move()
        player1.wallCollision()
        position, colour, deg = player1.returnVariables()
        player1.renderChar(canvas)

    def enemyProcedure():
        enemyVertices = []
        for i in enemyLinkedList:
            i.renderMet(canvas)
            i.move()
            i.wallCollision()
            enemyVertices.append(i.getVertices())

    def enemyCollisionProcedure():
        for count, obj1 in enumerate(enemyLinkedList, 0):
            for j in range (count+1,len(enemyLinkedList)):
                obj2 = enemyLinkedList[j]
                checkFlag= False
                for x in range (len(obj1.getVertices())-1):
                    for y in range (len(obj2.getVertices())-1):
                        segment1 = obj1.getVertices()[x],obj1.getVertices()[x+1]
                        segment2 = obj2.getVertices()[y],obj2.getVertices()[y+1]
                        overlap, intersection = lineOverlap(segment1,segment2)
                        if overlap:
                            checkFlag = True
                if checkFlag:
                    enemyLinkedList[count].enemyCollision(enemyLinkedList[j].getPosition(),enemyLinkedList[j].movVector,pygame.time.get_ticks(),enemyLinkedList[j])
        
    def playerCollisionProcedure():
        check = False
        for i in range (len(playerVertices)-1):
            for x in range (len(enemyVertices)):
                z = lineOverlap([playerVertices[0],playerVertices[2]],[enemyVertices[x][0],enemyVertices[x][5]])
                for j in range(len(enemyVertices[x])-1):
                    line1 = [playerVertices[i],playerVertices[i+1]]
                    line2 = [enemyVertices[x][j],enemyVertices[x][j+1]]
                    overlap, intersection = lineOverlap(line1,line2)
                    if overlap ==True or z==True:
                        check = True
        player1.invulnerabilityRender(pygame.time.get_ticks())
        if check==True:
            player1.takeDamage(pygame.time.get_ticks())
            if player1.checkDeath():
                return True
        
        return False
    def functionGetPositions(inpList):
        outList=[None]*(len(inpList))
        for i in range (len(inpList)):
            if inpList[i].getVertices() == None:
                outList[i] = inpList[i].getPosition()
            else:
                outList[i] = inpList[i].getVertices()
        return outList

    def lineOverlap(lineSeg1, lineSeg2):
        if lineSeg1[0][0] == lineSeg1[1][0]:
            line1_m = 0
        else:
            line1_m=(lineSeg1[0][1]-lineSeg1[1][1])/(lineSeg1[0][0]-lineSeg1[1][0])

        if lineSeg2[0][0] == lineSeg2[1][0]:
            line2_m = 0
        else:
            line2_m=(lineSeg2[0][1]-lineSeg2[1][1])/(lineSeg2[0][0]-lineSeg2[1][0])
            
        line1_c=lineSeg1[0][1]-(line1_m*lineSeg1[0][0])
        line2_c=lineSeg2[0][1]-(line2_m*lineSeg2[0][0])
        #print(f'y={line1_m}x+{line1_c}:')
        #print(f'y={line2_m}x+{line2_c}:')
        if line1_m !=line2_m:
            x=(line2_c-line1_c)/(line1_m-line2_m)
            y=(line1_m*x)+line1_c
            if ((y<=lineSeg1[0][1] and y>=lineSeg1[1][1] ) or (y>=lineSeg1[0][1] and y<=lineSeg1[1][1])) and ((x<=lineSeg1[0][0] and x>=lineSeg1[1][0]) or (x>=lineSeg1[0][0] and x<=lineSeg1[1][0])) and ((y<=lineSeg2[0][1] and y>=lineSeg2[1][1] ) or (y>=lineSeg2[0][1] and y<=lineSeg2[1][1])) and ((x<=lineSeg2[0][0] and x>=lineSeg2[1][0]) or (x>=lineSeg2[0][0] and x<=lineSeg2[1][0])):
                return True, (x,y)
        return False, (0,0)


    def takeEnemyVertices(enemyLinkedList):
        outList= []
        for i in enemyLinkedList:
            outList.append(i.getVertices())
        return outList

    def projectileCollisionProcedure():
        for i in projectileLinkedList:
            deleteItem = False
            j=0
            while j <(len(enemyVertices)) and not deleteItem:
                x=0
                while x <(len(enemyVertices[j])) and not deleteItem:
                    #finding the equation of the line y=mx+c
                    if (enemyVertices[j][x][1]-enemyVertices[j][(x+1)%len(enemyVertices[j])][1])!= 0:
                        m = (enemyVertices[j][x][0]-enemyVertices[j][(x+1)%len(enemyVertices[j])][0])/(enemyVertices[j][x][1]-enemyVertices[j][(x+1)%len(enemyVertices[j])][1])**-1
                        c = i.getPosition()[1]-(m*i.getPosition()[0])
                        arbitraryPoint1 = [(maxWidth), (maxWidth*m+c)]
                        arbitraryPoint2 = [0,(c)]
                        overlap, intersection = lineOverlap([enemyVertices[j][x],enemyVertices[j][(x+1)%len(enemyVertices[j])]],[arbitraryPoint1,arbitraryPoint2])
                        distanceFromLinesegment = math.sqrt((i.getPosition()[0]-intersection[0])**2+(i.getPosition()[1]-intersection[1])**2)
                        if abs(distanceFromLinesegment)<20:
                            projectileLinkedList.remove(i)
                            del i
                            player1.increaseScore(1)
                            deleteItem = True
                            enemyLinkedList[j].takeDamage()
                            if enemyLinkedList[j].checkDeath():
                                player1.increaseScore(10)
                                player1.incrementAsteroids()
                                enemyLinkedList[j] = meteor(screenDim,colour2,player1)
                    x+=1
                j+=1

    '''--------------------GUI-------------------------------------------------------------------------------------'''
    pygame.font.init()
    fontSize = 100

    def initPause(cannvas,screenDim):
        exitButton = MenuRender.buttonInterface((130,(maxHeight-(180+fontSize))),(maxWidth//2,maxHeight//5),canvas)
        restartButton = MenuRender.buttonInterface((160+maxWidth//2,(maxHeight-(180+fontSize))),(maxWidth//2-290,maxHeight//5),canvas)

        return canvas, screenDim, exitButton, restartButton
    def pause(canvas, screenDim, exitButton, restartButton, gameState,player1,enemyLinkedList,inputFlags,projectileLinkedList,projectileLimit,create):
        pause = True
        while pause:
            if gameState:
                player1.renderChar(canvas)
                for i in projectileLinkedList:
                    i.renderProj(canvas)
                for i in enemyLinkedList:
                    i.renderMet(canvas)
                    
                if colour1 == (255,255,255):
                    canvas.fill((200, 200, 200, 1), special_flags=pygame.BLEND_RGB_ADD)
                elif colour1 == (0,0,0):
                    canvas.fill((200, 200, 200, 1), special_flags=pygame.BLEND_RGB_SUB)
                elif colour1 == (51,19,92):
                    canvas.fill((50, 50, 50, 1), special_flags=pygame.BLEND_RGB_SUB)
                elif colour1 == (213,94,0):
                    canvas.fill((50, 50, 50, 1), special_flags=pygame.BLEND_RGB_SUB)
                    
                MenuRender.typeSurface('PAUSED',colour2,(110,110),fontSize,canvas)
                
            pygame.draw.rect(canvas, colour2, (100,100,screenDim[0]-200,screenDim[1]-200), 3)
            exitButton.drawRect(canvas,colour4)
            exitButton.drawText(canvas,'Exit',colour1,100)
            restartButton.drawRect(canvas,colour3)
            restartButton.drawText(canvas,'Restart',colour1,100)
            MenuRender.typeSurface(('Score:'+str(player1.score)), colour2, (130,(maxHeight//2-fontSize*2)), 100, canvas)
            MenuRender.typeSurface(('Projectiles Shot:'+str(player1.projectilesShot)), colour2, (130,(maxHeight//2-fontSize*1)), 100, canvas)
            MenuRender.typeSurface(('Asteroids Destroyed:'+str(player1.destroyedAsteroids)), colour2, (130,(maxHeight//2-fontSize*0)), 100, canvas)

            pygame.display.update()
            for event in pygame.event.get():
                mousePos=pygame.mouse.get_pos()
                button_states=pygame.mouse.get_pressed()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key==pygame.K_RETURN:
                                pause=False
                if button_states[0] == 1:
                    if exitButton.clicked(mousePos)==True:
                        pause=False
                        return True , player1,enemyLinkedList,inputFlags,projectileLinkedList,projectileLimit,create
                    elif restartButton.clicked(mousePos)==True:
                        player1,enemyLinkedList,inputFlags,projectileLinkedList,projectileLimit,create = initialise()
                        pause = False
        return False,player1,enemyLinkedList,inputFlags,projectileLinkedList,projectileLimit,create
    def overlay(canvas,player1):
        MenuRender.typeSurface('Health:'+str(player1.Health),colour2,(30,30),fontSize,canvas)
        MenuRender.typeSurface('Score:'+str(player1.score),colour2,(maxWidth//2,30),fontSize,canvas)

    '''--------------------Game loop---------------------------------------------------------------------------------'''
    screenDim = [maxWidth,maxHeight]
    def initialise():
        player1 = player((screenDim),colour2,colour4,baseHealth,speed,shieldLength,damage)

        enemyLinkedList = []
        for i in range (NumberOfEnemies):
            enemyLinkedList.append(meteor(screenDim,colour2,player1))

        inputFlags=[False,False,False,False]
        projectileLinkedList = []
        projectileLimit = 0
        create= False

        return player1,enemyLinkedList,inputFlags,projectileLinkedList,projectileLimit,create
    player1,enemyLinkedList,inputFlags,projectileLinkedList,projectileLimit,create = initialise()
    while not done:
        projectileLimit +=1
        canvas.fill(colour1)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                done=True
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key==pygame.K_a:
                            inputFlags[0]=True
                if event.key == pygame.K_RIGHT or event.key==pygame.K_d:
                            inputFlags[1]=True
                if event.key==pygame.K_UP or event.key==pygame.K_w:
                            inputFlags[2]=True
                if event.key==pygame.K_SPACE:
                            create=True
                            projectileLimit = 0
                if event.key==pygame.K_ESCAPE or event.key==pygame.K_RETURN:
                            done,player1,enemyLinkedList,inputFlags,projectileLinkedList,projectileLimit,create = pause(*initPause(canvas,screenDim),True,player1,enemyLinkedList,inputFlags,projectileLinkedList,projectileLimit,create) #problem = you can let go of the key and the flag remains true (so we must reset all flags here)
                            inputFlags=[False,False,False,False]
                            
            if event.type == pygame.KEYUP:
                if event.key==pygame.K_LEFT or event.key==pygame.K_a:
                    inputFlags[0]=False
                if event.key==pygame.K_RIGHT or event.key==pygame.K_d:
                    inputFlags[1]=False
                if event.key==pygame.K_UP or event.key==pygame.K_w:
                    inputFlags[2]=False
                if event.key==pygame.K_SPACE:
                            create=False
        if create == True and projectileLimit%15==0:
            projectileLinkedList.append(projectile(screenDim, player1.getPosition(), player1.getDegrees(),colour2))
            player1.incrementProjectile()


        if inputFlags[2]==True:
            player1.accelerate()
        else:
            player1.decelerate()
        if inputFlags[0]==True:
            player1.turnLeft()
        if inputFlags[1]==True:
            player1.turnRight()


        if not done:
            projectilePositions = functionGetPositions(projectileLinkedList)
            enemyVertices = functionGetPositions(enemyLinkedList)
            playerVertices = player1.getVertices()

            playerProcedure()
            projectilesProcedure()
            enemyProcedure()  

            done = playerCollisionProcedure()
            enemyCollisionProcedure()
            projectileCollisionProcedure()

           
            overlay(canvas,player1)
            clock.tick(60)
            pygame.display.update()
            
    pygame.time.delay(1000)
    canvas.fill(colour1)
    MenuRender.centreText(canvas, 'Game Over', (colour2), (0,0), maxWidth, maxHeight, 100)
    pygame.display.update()
    pygame.time.delay(2000)
    canvas.fill(colour1)
    done,player1,enemyLinkedList,inputFlags,projectileLinkedList,projectileLimit,create = pause(*initPause(canvas,screenDim),False,player1,enemyLinkedList,inputFlags,projectileLinkedList,projectileLimit,create)
    return player1.score, player1.destroyedAsteroids, player1.projectilesShot

#main()
