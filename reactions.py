#Import required libraries
from multiprocessing import Process
from datetime import datetime
import RPi.GPIO as GPIO
import time
from random import uniform

#Set up GPIO numbering mode.
GPIO.setmode(GPIO.BCM)

#Store the GPIO pin numbers for components
indicator = 18
red = 23
green = 24
sw1 = 25
sw2 = 8

#Set up GPIO modes.
GPIO.setup(indicator, GPIO.OUT)
GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(sw1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(sw2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Flash the indicator LED to indicate test running.
def flash():
     try:
        #Flash LED
        while True:
            GPIO.output(indicator, False)
            time.sleep(0.1)
            GPIO.output(indicator, True)
            time.sleep(0.1)
     
     #Turn off the LED when test finishes. 
     finally:
        GPIO.output(indicator, False)

#Create a process to flash the LED whilst running the main program loop.
blink = Process(target = flash)

#Stop the test and calculate results
def stop(startTime):
    #Record end time.
    end = time.time()
    #Calculate reaction time.
    react = (end - startTime)
    Print the reaction time.
    print ('Your reaction time was ' + str(react) + 'seconds')
    #Turn off all LEDs
    GPIO.output(indicator, False)
    GPIO.output(red, False)
    GPIO.output(green, False)
    #Terminate the LED flash (triggers the finally statement and shuts off the LED).
    blink.terminate()
    #Wait one second (not strictly necessary but I had issues with wierd GPIO behaviour).
    time.sleep(1)
    #Exit the program.
    exit()

#Start the test.
def startTest():
    #Start the indicator LED flashing.
    blink.start()
    #Generate a random floating point number between zero point one and two (I didn't want the possibility of an instant change).
    duration = uniform(0.1, 2.0)
    #Turn on red in the RGB LED
    GPIO.output(red, True)
    #Wait for the randomly generated duration.
    time.sleep(duration)
    #Turn off the red...
    GPIO.output(red, False)
    #...and instantly turn on green and log the start time.
    time.sleep(0)
    GPIO.output(green, True)
    start = time.time()
    #Wait for the user's button press.
    while True:
        if GPIO.input(sw2) == False:
            #Begin the stop function and give it the start time.
            #I know the variable name is a little crappy and makes this line rather confusing.
            stop(start)

#Wait for the first button press.
def waitForButton():
    if GPIO.input(sw1) == False:
        #Start the test.
        startTest()

#Main loop (the function is not strictly necessary I just added it for easy building on top of this program).
def main():
    try:
        while True:

            #Self test (Cycles colours on the RGB LED so I can ensure correct wiring).
            GPIO.output(green, True)
            time.sleep(1)
            GPIO.output(green, False)
            time.sleep(0)
            GPIO.output(red, True)
            time.sleep(1)
            GPIO.output(red, False)
            
            
            while True:
                #Turn on the idicator light to show system ready.
                GPIO.output(indicator, True)
                #Wait for the first button press
                waitForButton()
    
    #Set all GPIO pins back to input on program exit.
    finally:
        GPIO.cleanup()

#Run the main function (again not strictly necessary).
main()








