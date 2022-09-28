import csv

def writeTo(fileName,inpList): #overwrites the data in the file, replacing it with the input list
    with open(fileName, 'w', newline='') as file: #opens the file in write mode
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "accelerationLevel", "healthLevel", "shieldLevel", "damageLevel"])
        writer.writerow(inpList) #writes the new rwo with the input list

def readFrom(fileName,GetID): #reads from a specific record in the CSV file ('GetID')
    with open(fileName, 'r', newline='') as file: #opens the file in read mode
        reader = csv.reader(file, delimiter=',', quotechar=',',
                        quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            if row[0] == str(GetID):
                return row #returns a string array with the information from teh CSV file

def reset(fileName): #deletes all save progress and rewrites the file
    with open(fileName, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "accelerationLevel", "healthLevel", "shieldLevel", "damageLevel"])
        writer.writerow([1,"Acc1",0,0,0,0])



def createSettings(fileName):#deletes all save progress and rewrites/creates the save file
    with open(fileName, 'w', newline='') as file:
        writer = csv.writer(file,delimiter='/')
        writer.writerow(["ID", "Name", "resolution", "colourSchemeType","volume"])
        writer.writerow([1,"Acc1",[1280,720],1,50])#writes the new row with arbitrary settings values

def readSettings(fileName,GetID): #reads from a specific record in the CSV file ('GetID')
    with open(fileName, 'r', newline='') as file: #opens the file in read mode
        reader = csv.reader(file, delimiter='/', quotechar=',',
                        quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            if row[0] == str(GetID):
                return row#returns a string array with the information from teh CSV file
            
def newResolution(fileName,inpList):#overwrites the data in the file, replacing it with the input list
    with open(fileName, 'w', newline='') as file:#opens the file in write mode
        writer = csv.writer(file,delimiter='/')
        writer.writerow(["ID", "Name", "resolution", "colourSchemeType","volume"])
        writer.writerow(inpList)#writes the new row with the input list


def createProfile(fileName):
    with open(fileName, 'w', newline='') as file:
        writer = csv.writer(file,delimiter='/') #delimiter problem
        writer.writerow(["ID", "Name", "Enemy Kills", "Games Played","High Score","MoneyPoints"])
        writer.writerow([1,"acc1",0,0,0,0])
def readProfile(fileName,GetID):
    with open(fileName, 'r', newline='') as file:
        reader = csv.reader(file, delimiter='/', quotechar=',',
                        quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            if row[0] == str(GetID):
                return row
def saveProfile(fileName,inpList):
    with open(fileName, 'w', newline='') as file:
        writer = csv.writer(file,delimiter='/')
        writer.writerow(["ID", "Name", "Enemy Kills", "Games Played","High Score","MoneyPoints"])
        writer.writerow(inpList)

'''
reset('accounts/levels.csv')
createProfile("accounts/profile.csv")
createSettings("accounts/settings.csv")
'''
