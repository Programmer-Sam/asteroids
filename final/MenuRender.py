
import pygame

class buttonInterface(): #button class
    def __init__(self,aPosition, aSize,canvas): #initialising the button
        self.position = aPosition #x,y coordinate of the top-left corner
        self.size = aSize #length and height of the button
        self.x_range = [aPosition[0],aPosition[0]+aSize[0]] #holds the minimum and maximum x coordinate
        self.y_range = [aPosition[1],aPosition[1]+aSize[1]] #holds the minimum and maximum y coordinate
        self.canvas = canvas #holds the canvas on which the object is drawn on
    def drawText(self,canvas,text,colour,fontSize): #draws text in the button
        surface= ((pygame.font.SysFont('sans serif',fontSize)).render(text, False, colour))#sets font and colour of the text
        self.canvas.blit(surface,(self.position))
    def drawRect(self,canvas,colour): #draw the box for the button
        pygame.draw.rect(self.canvas, colour,(self.position,self.size))
    def clicked(self,mousePos):#takes the x,y coordinates of the cursor as an arguement
        #if the cursor is between the maximum and minimum x/y cordinate of the button
        if self.x_range[0]<mousePos[0]<self.x_range[1] and self.y_range[0]<mousePos[1]<self.y_range[1]:
            return True #return that the button has been pressed
    def drawImg(self,file,scale):
        img = pygame.image.load(file)
        img = pygame.transform.scale(img,scale)
        self.canvas.blit(img, (self.position))
    def drawImgToButton(self,file): #draws an image onto the button (takes the file path as an arguement)
        img = pygame.image.load(file) #loads the file path
        img = pygame.transform.scale(img,self.size) #transforms the resolution of the image
        self.canvas.blit(img, (self.position)) #displays the image with the position of the button
    def indentedText(self,canvas,text,colour,fontSize,x_indent,y_indent):
        surface= ((pygame.font.SysFont('sans serif',fontSize)).render(text, False, colour))#sets font and colour of the text
        self.canvas.blit(surface,(self.position[0]+x_indent,self.position[1]+y_indent))
def typeSurface(text,colour,position,size,canvas):
    surface= ((pygame.font.SysFont('sans serif',size)).render(text, False, colour))
    return canvas.blit(surface,position)
def drawSquare(colour,position,size,canvas):
    return pygame.draw.rect(canvas,colour,(position,size))

def centreText(canvas, text, colour, startPoint, maxWidth, maxHeight, fontSize):#change game
    font = pygame.font.Font(None, fontSize)
    text = font.render(text, True, colour)
    text_rect = text.get_rect(center=(startPoint[0]+maxWidth/2,startPoint[1]+maxHeight/2))
    canvas.blit(text, text_rect)


