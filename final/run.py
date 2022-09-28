import pygame
import MenuRender
import saveFile
import tkinter
pygame.init()
pygame.font.init()

'''--------------------CSV replacements---------------------------------------------------'''
clock=pygame.time.Clock()



from ast import literal_eval #helps convert string values from save files into arrays and tuples

importSettings = saveFile.readSettings('accounts/settings.csv',1) #calling the data saved within the CSV files and saving it as an array
def getResolution(importSettings):
    if importSettings[2]=='FULLSCREEN': #if the resolution is set to full screen
        #the tkinter module is called to find the native resolution of the display and initialises teh window(canvas) object with these dimensions
        root = tkinter.Tk()

        maxWidth = root.winfo_screenwidth()
        maxHeight = root.winfo_screenheight()
        canvas=pygame.display.set_mode((maxWidth,maxHeight), pygame.FULLSCREEN)#initialises the window in fullscreen mode
        root.destroy()
    else: #else, the value in importSettings[2] holds an array with the required screen dimensions
        #function literal_eval (from the ast module) turns a string into an array with integer values
        maxWidth = literal_eval(importSettings[2])[0] #sets the x-dimension of the window size
        maxHeight = literal_eval(importSettings[2])[1] #sets the y-dimension of the window size
        canvas=pygame.display.set_mode((maxWidth,maxHeight)) #initialises a "windowed" menu screen
    return maxWidth,maxHeight,canvas #returns the size of the window and the window object (canvas)

maxWidth,maxHeight,canvas = getResolution(importSettings)
#colours

def colourScheme(importSettings): #takes the settings array from the CSV as an input
    #holds the hard-coded colour combinations of the menu screen
    colourScheme1 = [(0,0,0),(255,255,255),(0,0,255),(255,0,0)]
    colourScheme2 = [(255,255,255),(0,0,0),(0,0,255),(255,0,0)]
    colourScheme3 = [(51,19,92),(101,46,199),(222,56,200),(255,211,0)]
    colourScheme4 = [(213,94,0),(0,114,178),(0,158,115),(204,121,157)]

    if importSettings[3] =='1': #sets the colour combination to colour scheme 1
        baseColour = colourScheme1[0]
        contrastColour = colourScheme1[1]
        secondaryColour = colourScheme1[2]
        tertiaryColour = colourScheme1[3]
    elif importSettings[3] =='2':#sets the colour combination to colour scheme 2
        baseColour = colourScheme2[0]
        contrastColour = colourScheme2[1]
        secondaryColour = colourScheme2[2]
        tertiaryColour = colourScheme2[3]
    elif importSettings[3] =='3':#sets the colour combination to colour scheme 3
        baseColour = colourScheme3[0]
        contrastColour = colourScheme3[1]
        secondaryColour = colourScheme3[2]
        tertiaryColour = colourScheme3[3]
    elif importSettings[3] =='4':#sets the colour combination to colour scheme 4
        baseColour = colourScheme4[0]
        contrastColour = colourScheme4[1]
        secondaryColour = colourScheme4[2]
        tertiaryColour = colourScheme4[3]
    return baseColour,contrastColour,secondaryColour,tertiaryColour#returns the colours to the main programme

baseColour,contrastColour,secondaryColour,tertiaryColour = colourScheme(importSettings) #initialises the colour schemes

#geometric positions
TitleFontSize= 300
ButtonDimension_Y= (maxHeight-TitleFontSize)/4
ButtonDimension_X= maxWidth-500

'''-----------------main menu-------------------------'''
def initMenuobj(ButtonDimension_X,ButtonDimension_Y): #initialise the button objects for the main menu
    #initiates the 4 buttons with their x,y coordinates and sizes
    ButtonDimension_Y= (maxHeight-TitleFontSize)/4 #height of each button scaled to the screen dimension size
    ButtonDimension_X= maxWidth-500 #width of each button scaled to the screen dimension size
    playButton = MenuRender.buttonInterface((30,maxHeight-(ButtonDimension_Y+20)*4),(ButtonDimension_X,ButtonDimension_Y),canvas)
    shopButton = MenuRender.buttonInterface((30,maxHeight-(ButtonDimension_Y+20)*3),(ButtonDimension_X,ButtonDimension_Y),canvas)
    controlButton = MenuRender.buttonInterface((30,maxHeight-(ButtonDimension_Y+20)*2),(ButtonDimension_X,ButtonDimension_Y),canvas)
    exitButton = MenuRender.buttonInterface((30,(maxHeight-(ButtonDimension_Y+20)*1)),(ButtonDimension_X,ButtonDimension_Y),canvas)

    settingsButton = MenuRender.buttonInterface((maxWidth-110,310),(100,100),canvas)
    profileButton = MenuRender.buttonInterface((maxWidth-110,420),(100,100),canvas)

    return playButton, shopButton, controlButton, exitButton, settingsButton, profileButton

def displayMenu(playButton, shopButton, controlButton, exitButton, settingsButton, profileButton, canvas): #displays the menu screen

    MenuRender.typeSurface('Asteroids',contrastColour,(30,30),TitleFontSize,canvas) #draws the title onto the game screen

    #draws each button and the corresponding text for the user
    playButton.drawRect(canvas,contrastColour)
    playButton.drawText(canvas,'Play',baseColour,100)

    shopButton.drawRect(canvas,contrastColour)
    shopButton.drawText(canvas,'Shop',baseColour,100)
    
    controlButton.drawRect(canvas,contrastColour)
    controlButton.drawText(canvas,'Controls',baseColour,100)
    
    exitButton.drawRect(canvas,tertiaryColour)
    exitButton.drawText(canvas,'Exit',baseColour,100)

    settingsButton.drawRect(canvas,contrastColour)
    settingsButton.drawImg('external/settings.jpg',(100,100))
    profileButton.drawRect(canvas,contrastColour)
    profileButton.drawImg('external/profileSymbol.png',(100,100))
    
    if button_states[0]==1: #if the mouse has been clicked
            if playButton.clicked(mousePos)==True: #check if the mouse cursor is on top of the play button
                button[0]=True #toggles the play menu
                del playButton, shopButton, controlButton, exitButton, settingsButton,profileButton #deletes the button objects in the main menu
            elif shopButton.clicked(mousePos)==True: #check if the mouse cursor is on top of the shop button
                button[1]=True #toggles the shop menu
                del playButton, shopButton, controlButton, exitButton, settingsButton,profileButton
            elif controlButton.clicked(mousePos)==True: #check if the mouse cursor is on top of the Controls button
                button[2]=True #toggles the controls menu
                del playButton, shopButton, controlButton, exitButton, settingsButton,profileButton
            elif settingsButton.clicked(mousePos)==True:
                button[3]=True #toggles the settings menu
                del playButton, shopButton, controlButton, exitButton, settingsButton,profileButton
            elif profileButton.clicked(mousePos)==True:
                button[4]=True #toggles the profile menu
                del playButton, shopButton, controlButton, exitButton, settingsButton,profileButton
            elif exitButton.clicked(mousePos)==True: #check if the mouse cursor is on top of the Exit button
                done=True #exits out of the main game loop
                pygame.quit()#terminates the pygame window


'''--------------------------------------test screen-----------------------'''
returnButton = MenuRender.buttonInterface(((maxWidth-110),20),(100,50),canvas) #initiates the return button
def baseScreen(): #renders a return button (takes the user back to the home screen)
    returnButton = MenuRender.buttonInterface(((maxWidth-110),20),(100,50),canvas)
    returnButton.drawRect(canvas,contrastColour) #draws the button on the window
    returnButton.drawText(canvas,'Return',baseColour,40) #draws the text on the button
    if button_states[0]==1:
            if returnButton.clicked(mousePos)==True: #if user clicked the return button then
                for i in range (0, len(button)-1):
                    button[i]=False #resets the menu button flags to False so that the base screen 

'''--------------------------------------Play Screen-----------------------'''

import game #imports the game file
def initPlayMenuObj(lastState):
    gameButton = MenuRender.buttonInterface((50,50),(maxWidth-300,maxHeight-100),canvas)

    return gameButton, lastState
def playMenu(gameButton,lastState):
    gameButton.drawRect(canvas,(contrastColour))
    gameButton.drawImg('external/spaceship.png',(maxWidth-300, maxHeight-100))
    gameButton.drawText(canvas,"PLAY", (baseColour), 300)
    
    if button_states[0]==1 and lastState==0: #detects the first time the mouse is clicked
            if gameButton.clicked(mousePos)==True:
                upgrades = saveFile.readFrom("accounts/levels.csv", 1)
                score,kills,shot = game.main(maxWidth,maxHeight, baseColour, contrastColour,secondaryColour, tertiaryColour,7,False,canvas,int(upgrades[3]),int(upgrades[2]),int(upgrades[4]),int(upgrades[5]))
                #after returning from the game, the new player statistics must be calculated and stored
                name,killNumber,gameNumber,highScore,points = profileStats() #stores the data from the profile statistics
                if score >int(highScore): #if the score the user just obtained is higher than the one stored in the CSV
                    highScore = score #new highest score is updated with score of the last game played
                killNumber = int(killNumber)+kills #adds the number of kills to the kill counter
                gameNumber = int(gameNumber)+1 #increments the number of games played by 1
                newPoints = int(points) + score//100 #a spendable point is added for every 100 in-game points that the player obtained
                saveFile.saveProfile("accounts/profile.csv",[1,name,killNumber,gameNumber,highScore,newPoints]) #updates the CSV with the new profile statistics
    return button_states[0]


'''---------------------------------Shop Screen-----------------------'''
def updateAccount(shoppingStack): #takes the stack of items in the shopping cart
    List = saveFile.readFrom("accounts/levels.csv",1) #reads the current stored levels from the CSV file
    for i in (shoppingStack): #increments the levels to the corresponding items on the shopping stack
        if i=="acceleration":
            List[2] = int(List[2])+1
        elif i=="health":
            List[3] = int(List[3])+1
        elif i=="damage":
            List[4] = int(List[4])+1
        elif i=="shield":
            List[5] = int(List[5])+1
    saveFile.writeTo("accounts/levels.csv",([List[0],List[1],str(List[2]),str(List[3]),str(List[4]),str(List[5])])) #saves the new levels of the player to the CSV file
       

def initShopMenuObj(lastState): #initialises the menu buttons for the shop menu
    Size_Y = (maxHeight-TitleFontSize-30)//4
    Size_X = maxWidth//6
    upgradeSize_X = maxWidth//2
    shipUpgrades = MenuRender.buttonInterface((30,TitleFontSize-50),(upgradeSize_X,maxHeight-TitleFontSize+40),canvas)

    upgradeOutlinePos=(upgradeSize_X-(upgradeSize_X-60)//5,TitleFontSize+100) #geometric positions for the buttons
    upgradeOutlineDim= ((upgradeSize_X-60)//5,(maxHeight-TitleFontSize-150)//4) #geometric size for the buttons
    
    #intialises the buttons for the upgrades for the ship
    upgrade1 = MenuRender.buttonInterface((upgradeOutlinePos[0], upgradeOutlinePos[1]+(upgradeOutlineDim[1]+10)*0),(upgradeOutlineDim),canvas)
    upgrade2 = MenuRender.buttonInterface((upgradeOutlinePos[0], upgradeOutlinePos[1]+(upgradeOutlineDim[1]+10)*1),(upgradeOutlineDim),canvas)
    upgrade3 = MenuRender.buttonInterface((upgradeOutlinePos[0], upgradeOutlinePos[1]+(upgradeOutlineDim[1]+10)*2),(upgradeOutlineDim),canvas)
    upgrade4 = MenuRender.buttonInterface((upgradeOutlinePos[0], upgradeOutlinePos[1]+(upgradeOutlineDim[1]+10)*3),(upgradeOutlineDim),canvas)
    arrayUpgrades = [upgrade1,upgrade2,upgrade3,upgrade4] #stores the buttons into an array (easier to store and manipulate)
    
    shoppingCartPos=(80+upgradeSize_X,TitleFontSize) #geometric positions for the shopping cart
    shoppingCartDim= (maxWidth -(Size_X)-(upgradeSize_X),maxHeight-TitleFontSize-80) #geometric size for the shopping cart

    #initialising the shopping cart, purchase button and dequeue button
    shoppingCart = MenuRender.buttonInterface((shoppingCartPos),(shoppingCartDim),canvas)
    purchaseButton = MenuRender.buttonInterface((shoppingCartPos[0],shoppingCartPos[1]+shoppingCartDim[1]+10),((shoppingCartDim[0]//6)*4,70),canvas)
    cartRemoval = MenuRender.buttonInterface((shoppingCartPos[0]+(shoppingCartDim[0]//6)*4+ 10,shoppingCartPos[1]+shoppingCartDim[1]+10),((shoppingCartDim[0]//6)*2-10,70),canvas)

    name,killNumber,gameNumber,highScore,points = profileStats()
    return shipUpgrades, shoppingCart, purchaseButton, cartRemoval, saveFile.readFrom("accounts/levels.csv",1),arrayUpgrades,lastState,points #returns all the initialised objects
def shopMenu(shipUpgrades, shoppingCart, purchaseButton, cartRemoval, saveFile, arrayUpgrades,lastState,points): #procedure to render the shop menu using the iniitialised objects
    global shoppingStack
    points = int(points)
    MenuRender.typeSurface('Item Shop',contrastColour,(30,30),TitleFontSize,canvas) #displays the title
    MenuRender.typeSurface('Spendable Points:'+str(points),contrastColour,(maxWidth-300,250),30,canvas)
    shipUpgrades.drawRect(canvas,(contrastColour))
    MenuRender.centreText(canvas, 'Ship Upgrades', (baseColour), (shipUpgrades.position), shipUpgrades.size[0], 100, 100)

    MenuRender.typeSurface("Acceleration", (baseColour), (50,arrayUpgrades[0].position[1]), arrayUpgrades[0].size[1],canvas)
    MenuRender.typeSurface("Health", (baseColour), (50,arrayUpgrades[1].position[1]), arrayUpgrades[1].size[1],canvas)
    MenuRender.typeSurface("Damage", (baseColour), (50,arrayUpgrades[2].position[1]), arrayUpgrades[2].size[1],canvas)
    MenuRender.typeSurface("Shield", (baseColour), (50,arrayUpgrades[3].position[1]), arrayUpgrades[3].size[1],canvas)
    for i in arrayUpgrades: #renders all the upgrade buttons with the symbol "+"
        i.drawRect(canvas,(baseColour))
        MenuRender.centreText(canvas, "+", (contrastColour), i.position, i.size[0], i.size[1],200)

    #draws the shopping cart and buttons corresponding to buying the items  
    shoppingCart.drawRect(canvas,(contrastColour))                        
    purchaseButton.drawRect(canvas,(tertiaryColour))
    purchaseButton.drawText(canvas, "PURCHASE", (baseColour), 60)
    cartRemoval.drawRect(canvas,(contrastColour))
    cartRemoval.drawText(canvas, "  -", (baseColour),80)


    shoppingCartPos=(shoppingCart.position)#variables to help calculate the position at which the text should be dynamically rendered onto
    shoppingCartDim= (shoppingCart.size)
    for count,text in enumerate(shoppingStack): #iterates through the stack and returns the text and index that it was placed in
        #Y poision is calculated by dividing the shopping list size into 10 sectors and displayed on the corresponding index in the list
        MenuRender.typeSurface(text.upper()+' Level +1',(baseColour), (shoppingCartPos[0]+30 ,shoppingCartPos[1]+(shoppingCartDim[1]//10)*(count)), 40,canvas) #displays the item
        
    if button_states[0]==1 and lastState==0: #if the mouse is clicked once
        for count,obj in enumerate(arrayUpgrades): #for every upgrade button check if it has been clicked
            if obj.clicked(mousePos) == True and len(shoppingStack)<10 and points>0: #and check if the shopping cart has exceeded its limit (10 items)
                #pushes the corresponding upgrade level onto the shopping stack
                if count == 0:
                    shoppingStack.append("acceleration")
                elif count == 1:
                    shoppingStack.append("health")
                elif count == 2:
                    shoppingStack.append("damage")
                elif count == 3:
                    shoppingStack.append("shield")
                profileChangePoints(-1)
        if purchaseButton.clicked(mousePos) == True: #checks if the upgrade button has been clicked
            #function to increase the levels of the player's account
            updateAccount(shoppingStack)
            shoppingStack = []
        elif cartRemoval.clicked(mousePos) == True and len(shoppingStack)>0: #checks if the remove from cart button has been clicked
            shoppingStack.pop() #removes the last item from the stack
            profileChangePoints(1)

    del shipUpgrades, shoppingCart, purchaseButton, cartRemoval, saveFile, arrayUpgrades,lastState
    return button_states[0]

'''---------------------------------Control Screen-----------------------'''
def initControlMenuObj():
    controlImg = MenuRender.buttonInterface((10,10),(maxWidth-300,maxHeight-300),canvas)

    return controlImg

def initControlScreenObj(controlImg):
    controlImg.drawImg('external/controls.png',(maxWidth-300, maxHeight-300))


'''---------------------------------Settings Screen-----------------------'''
def initSettingsMenuObj():
    resolutionBox = MenuRender.buttonInterface((30,280),(maxWidth//4,maxHeight-300),canvas)

    resolutionPos = resolutionBox.position
    resolutionDim = resolutionBox.size
    #array of the reolution size buttons
    resolutionSizes = [MenuRender.buttonInterface((resolutionPos),(resolutionDim[0] ,(resolutionDim[1]//5)-5),canvas),
                       MenuRender.buttonInterface((resolutionPos[0],resolutionPos[1]+(resolutionDim[1]//5)*1),(resolutionDim[0] ,(resolutionDim[1]//5)-5),canvas),
                       MenuRender.buttonInterface((resolutionPos[0],resolutionPos[1]+(resolutionDim[1]//5)*2),(resolutionDim[0] ,(resolutionDim[1]//5)-5),canvas),
                       MenuRender.buttonInterface((resolutionPos[0],resolutionPos[1]+(resolutionDim[1]//5)*3),(resolutionDim[0] ,(resolutionDim[1]//5)-5),canvas),
                       MenuRender.buttonInterface((resolutionPos[0],resolutionPos[1]+(resolutionDim[1]//5)*4),(resolutionDim[0] ,(resolutionDim[1]//5)-5),canvas)]

    colourBoxPos = [resolutionBox.position[0]+ resolutionBox.size[0]+30,resolutionBox.position[1]]
    colourBoxDim = [maxWidth-resolutionBox.size[0]-resolutionBox.position[0]-360,maxHeight-300]
    colourChangeBox = MenuRender.buttonInterface((colourBoxPos),(colourBoxDim),canvas)

    #array of the different colour schemes that can be selected in the game
    colourChanges = [MenuRender.buttonInterface((colourBoxPos),(colourBoxDim[0]//2-3,colourBoxDim[1]//2-3),canvas),
                     MenuRender.buttonInterface((colourBoxPos[0]+colourBoxDim[0]//2,colourBoxPos[1]),(colourBoxDim[0]//2-3,colourBoxDim[1]//2-3),canvas),
                     MenuRender.buttonInterface((colourBoxPos[0],colourBoxPos[1]+colourBoxDim[1]//2),(colourBoxDim[0]//2-3,colourBoxDim[1]//2-3),canvas),
                     MenuRender.buttonInterface((colourBoxPos[0]+colourBoxDim[0]//2,colourBoxPos[1]+colourBoxDim[1]//2),(colourBoxDim[0]//2-3,colourBoxDim[1]//2-3),canvas)]


        
    updateButton =  MenuRender.buttonInterface((maxWidth-310,maxHeight-110),(300,100),canvas) #instantiates the button

    

    return resolutionBox,resolutionSizes,updateButton,colourChangeBox,colourChanges
def settingsScreen(resolutionBox,resolutionSizes,updateButton,colourChangeBox,colourChanges):
    global canvas, maxWidth, maxHeight, baseColour,contrastColour,secondaryColour,tertiaryColour

    MenuRender.typeSurface('Settings',contrastColour,(30,30),TitleFontSize,canvas) #renders the title of the settings screen

    #accesses the array for the resolution options
    resolutionBox.drawRect(canvas,(contrastColour))
    updateButton.drawRect(canvas,(tertiaryColour))
    updateButton.drawText(canvas,"update",baseColour,100)

    resolutions = ['Resolution Size', '[1280, 720]', '[1366, 768]', '[1920, 1080]','FULLSCREEN'] #holds the text to be rendered onto the selectable button options
    for i in range(len(resolutionSizes)): #iterates between all buttons concerning the resolution size
        resolutionSizes[i].indentedText(canvas,resolutions[i],baseColour,50,20,5) #prints the corresponding text to each button
        if resolutions[i] == importSettings[2]: #if the current resolution matches the corresponding button for the resolution size...
            #draws a box around the current resolution so the user knows what  the current settings are
            pygame.draw.rect(canvas, secondaryColour, (resolutionSizes[i].position[0],resolutionSizes[i].position[1],resolutionSizes[i].size[0],resolutionSizes[i].size[1]), 10)


    colourChangeBox.drawRect(canvas,(contrastColour))
    colourChanges[0].drawImg('external/Scheme1.png',(colourChanges[0].size))
    colourChanges[1].drawImg('external/Scheme2.png',(colourChanges[1].size))
    colourChanges[2].drawImg('external/Scheme3.png',(colourChanges[2].size))
    colourChanges[3].drawImg('external/Scheme4.png',(colourChanges[3].size))
    
    if importSettings[3] =='1':
        pygame.draw.rect(canvas, secondaryColour, (colourChanges[0].position[0],colourChanges[0].position[1],colourChanges[0].size[0],colourChanges[0].size[1]),10)
    elif importSettings[3] =='2':
        pygame.draw.rect(canvas, secondaryColour, (colourChanges[1].position[0],colourChanges[1].position[1],colourChanges[1].size[0],colourChanges[1].size[1]),10)
    elif importSettings[3] =='3':
        pygame.draw.rect(canvas, secondaryColour, (colourChanges[2].position[0],colourChanges[2].position[1],colourChanges[2].size[0],colourChanges[2].size[1]),10)
    elif importSettings[3] =='4':
        pygame.draw.rect(canvas, secondaryColour, (colourChanges[3].position[0],colourChanges[3].position[1],colourChanges[3].size[0],colourChanges[3].size[1]),10)
    
    if button_states[0]==1: #when the mouse has been clicked
        for i in range (len(resolutionSizes)): #iterates through all the resolution buttons
            if resolutionSizes[i].clicked(mousePos) == True: #if the button has been pressed
                if i ==1: #if the first button had been pressed then it...
                    importSettings[2]= '[1280, 720]' #changes the resolution in the settings array
                #checks if the otehr buttons were pressed
                elif i ==2:
                    importSettings[2]= '[1366, 768]'
                elif i ==3:
                    importSettings[2]= '[1920, 1080]'
                elif i ==4:
                    importSettings[2]= 'FULLSCREEN'
                saveFile.newResolution('accounts/settings.csv',importSettings) #rewrites this into the CSV file with the new resolution
                
        '''SAME SHIT AS THE ONE ABOVE
        for count,obj in enumerate(resolutionSizes): #returns the resolution button object and control number ('count')
            if obj.clicked(mousePos) == True: #if one of the buttons have been pressed then
                #using the 'count' variable, this finds the corresponding new resolution
                if count ==1: #if the first button had been pressed then it...
                    importSettings[2]= '[1280, 720]' #changes the resolution in the settings array
                elif count ==2:
                    importSettings[2]= '[1366, 768]'
                elif count ==3:
                    importSettings[2]= '[1920, 1080]'
                elif count ==4:
                    importSettings[2]= 'FULLSCREEN'
                saveFile.newResolution('accounts/settings.csv',importSettings) #rewrites this into the CSV file
        '''
        for count,obj in enumerate(colourChanges):
            if obj.clicked(mousePos)==True:
                if count ==0:
                    importSettings[3] = '1'
                elif count ==1:
                    importSettings[3] = '2'
                elif count ==2:
                    importSettings[3] = '3'
                elif count ==3:
                    importSettings[3] = '4'
                saveFile.newResolution('accounts/settings.csv',importSettings)
            
        if updateButton.clicked(mousePos)==True: #if the update button has been pressed
            maxWidth,maxHeight,canvas = getResolution(importSettings) #calls the resolution function to return a new window dimension size and window object
            baseColour,contrastColour,secondaryColour,tertiaryColour = colourScheme(importSettings) #calls the colour function to change the main colours in the game

'''---------------------------------Profile Screen-----------------------'''
def profileStats(): #returns the profile values stored in the CSV file
    getValues = saveFile.readProfile("accounts/profile.csv",1)
    name = getValues[1]
    killNumber = getValues[2]
    gameNumber = getValues[3]
    highScore = getValues[4]
    points = getValues[5]
    return name,killNumber,gameNumber,highScore,points
def profileChangePoints(change): #uniquely changes the amount of spendable points that can be used in teh shop
    getValues = saveFile.readProfile("accounts/profile.csv",1)
    getValues[5] = int(getValues[5])+change #fifth value holds the number of spendable points in the shop (adds the unique number change)
    saveFile.saveProfile("accounts/profile.csv",getValues)#saves this to the character profile
def profileMenu(name,killNumber,gameNumber,highScore,points,canvas): #takes statistic arguements
    levels = saveFile.readFrom("accounts/levels.csv",1) #takes the profile levels (purchased in teh ing-game shop)
    #prints all the necessary game statistics on the game window
    MenuRender.typeSurface("Profile: "+name,contrastColour,(30,30),maxHeight//8*2,canvas)
    MenuRender.typeSurface("Number of Kills: "+killNumber,contrastColour,(30,30+maxHeight//8*2),maxHeight//8,canvas)
    MenuRender.typeSurface("Games Played: "+gameNumber,contrastColour,(30,30+maxHeight//8*3),maxHeight//8,canvas)
    MenuRender.typeSurface("High Score: "+highScore,contrastColour,(30,30+maxHeight//8*4),maxHeight//8,canvas)
    MenuRender.typeSurface("Spendable Points: "+points,contrastColour,(30,30+maxHeight//8*5),maxHeight//8,canvas)
    displayLevels = ("Acceleration Level:"+str(levels[2])+",  Health Level:"+str(levels[3])+",  Shield Level:"+str(levels[4])+",  Damage Level:"+str(levels[5]))
    MenuRender.typeSurface(displayLevels,contrastColour,(30,30+maxHeight//8*6.5),30,canvas)
'''--------------------------GUI loop----------------------------------'''
shoppingStack = []
lastState =1

done=False
button=[False,False,False,False,False,False] #flags for the buttons [play,shop,control,exit,settings,profile]

while not done: #while the player has no pressed exit
    pygame.display.update() #updates the frames of the game
    
    mousePos=pygame.mouse.get_pos()#gets the position of the mouse
    for event in pygame.event.get():
        button_states=pygame.mouse.get_pressed()#takes the button state (if it has been pressed)
        if event.type==pygame.QUIT: #if pygame closes, the game window is terminated
            done=True
            pygame.quit()
    canvas.fill(baseColour) #fills the game with the background colour value
    '''-----------------------------------------------------------------------'''

    if button[0]==True: #displays the Play Menu if the corresponding flag is true
        baseScreen()
        lastState=playMenu(*initPlayMenuObj(lastState))
    elif button[1]==True: #displays the Shop Menu if the corresponding flag is true
        baseScreen()
        lastState=shopMenu(*initShopMenuObj(lastState))
    elif button[2]==True: #displays the Control Menu if the corresponding flag is true
        baseScreen()
        initControlScreenObj(initControlMenuObj())
    elif button[3]==True: #displays the settings menu if the corresponding flag is true
        baseScreen()
        settingsScreen(*initSettingsMenuObj())
    elif button[4]==True: #displays the profile if the corresponding flag is true
        baseScreen()
        profileMenu(*profileStats(),canvas)
    else: #If no flags are toggled, the Main Menu screen is displayed
        displayMenu(*initMenuobj(ButtonDimension_X,ButtonDimension_Y),canvas) #calls the function to display the Game Menu
    '''-----------------------------------------------------------------------'''
    clock.tick(32)
    
pygame.close()
