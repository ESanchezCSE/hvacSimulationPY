import time
import pyrebase

# firebase configuration data need to access our realtime database.
firebaseConfig={
    "apiKey": "hidden",
    "authDomain": "hidden",
    "databaseURL": "hidden",
    "projectId": "hidden",
    "storageBucket": "hidden",
    "messagingSenderId": "hidden",
    "appId": "hidden"
}

firebase=pyrebase.initialize_app(firebaseConfig) #initialzation of our app data
db=firebase.database() # initialization of our database instance

# Global Variables
t = 5 # t is short for ticks. In this case every tick is 3 seconds. And every three seconds is twenty minutes simulated.

# array day1, day2, day3 containt the hourly temperatures for the dates
# 11/13 - 11/15 in the Fort Worth area
day = [[60, 60, 58, 56, 52, 53, 51, 55, 56, 60, 61, 64,
        69, 70, 71, 70, 66, 63, 64, 63, 61, 61, 63, 63],
        [61, 64, 66, 68, 68, 67, 67, 68, 72, 74, 79, 81,
        80, 80, 80, 80, 79, 77, 76, 76, 75, 75, 73, 71],
        [69, 65, 61, 57, 55, 53, 51, 50, 51, 55, 58, 60,
        61, 63, 64, 64, 63, 61, 57, 55, 53, 51, 50, 49]]

class acStatus:
    def __init__(self, status, houseTemp, targetTemp, heatingCooling):
        self.onOff = status
        self.currTemp = houseTemp
        self.targTemp = targetTemp
        self.heatCold = heatingCooling
    #def changeTemp(self, houseTemp, targetTemp, heatingCooling):


# @params
# status is the on or off state of the AV Unit
# houseTemp is the current temperature found inside the house
# targetTemp is the temperature the system wishes to achieve inside the house
#
# @returns a number that states the rate of change every tick within a house
# the nunmber is based on the average rate an AC cools, or heats up a house.
# this rate is 10 degrees every 3 hours.
def rateOfCoolingHeating(status, houseTemp, targetTemp):
    if(status == True):
        if(houseTemp < targetTemp):
            return(1)
        elif(houseTemp > targetTemp):
            return(-1)
        else:
            return(0)
    else:
        return(0)

# @params
# houseTemp is the current temperature found inside the house
# outsideTemp is the current temperautre found outside the house.
#
# @returns the rate of at which the house is warming or cooling depending on the outside temp.
def rateOfDecay(houseTemp, outsideTemp):
    diff = houseTemp - outsideTemp
    abs(diff)
    if(diff == 0):
        rate = 0
    elif(diff > 0 and diff < 3):
        rate = 0.1
    elif(diff >= 3 and diff < 5):
        rate = 0.2
    elif(diff >= 5 and diff < 9):
        rate = 0.3
    elif(diff >= 9 and diff < 12):
        rate = 0.4
    else:
        rate = .5
    if(houseTemp <= outsideTemp):
        return(rate)
    return(rate*-1)

# @params
# tick is the current tick hour. In this case every tick is twenty minutes simulated
# hour is the current hour after 12:00 am
#
# @returns the current hour.
def getCurrentHour(tick, hour):
    if(tick % 3 == 0):
        hour += 1
    hour = hour % 24
    return(hour)
    
# TODO:: This functions is to be used when reading in from the database.
def setTargetTemp(targetTemp):
    return(targetTemp)

if __name__ == "__main__":
    tickCounter = 0 # tickCounter is used to keep track of how many ticks since the start of the program.
    dayCounter = 0 # counts the numbers of days simulated after the start of the program
    hour = -1 # used to track the amount of hours passed 12:00 AM
    homeTempTarget = db.child("home").child("targetTemp").get().val()
    homeAC = acStatus(False, 80, homeTempTarget, 'POWEROFF') # Initialization of our home ac unit.
    while True:
        if(tickCounter % 216 < 72):
            dayCounter = 0
        elif((tickCounter % 216 >= 72) and (tickCounter % 216 < 144)):
            dayCounter = 1
        else:
            dayCounter = 2

        hour = getCurrentHour(tickCounter, hour)
        currOutsideTemp = day[dayCounter][hour]
        homeTempTarget = db.child("home").child("targetTemp").get().val()


#       The line of code below is used to debug.
        print("current temp: ",currOutsideTemp, "target temp, tickCounter, dayCounter, Hour", homeTempTarget, tickCounter, dayCounter, hour)
        data = {
                "currOutsideTemp": currOutsideTemp,
                "hour": hour,
                "currInsideTemp": homeAC.currTemp,
                "targetTemp": homeTempTarget}
        
        db.child("home").set(data)
#       homeAC.targTemp =  db.child("home").child("targetTemp").get()

        time.sleep(t)
        tickCounter += 1

