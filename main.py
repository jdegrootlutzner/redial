import os
import time
import random
import subprocess
import RPi.GPIO as GPIO

"""
@author Julian DeGroot-Lutzner
@date Summer 2018

"""

GPIO.setwarnings( True )
GPIO.setmode( GPIO.BCM )

# GPIO output numbers
COUNTER_PIN = 2 # on the rotaty, blue and green wires
DIALING_PIN = 3 # on when dialing, off when resting, white wires
LEVER_PIN = 27 # lever that phone sits on, on when down, off when up

SOUND_CARD = 1 # location of usb sound card

# set up GPIOs 
GPIO.setup( COUNTER_PIN , GPIO.IN , pull_up_down = GPIO.PUD_DOWN )
GPIO.setup( DIALING_PIN , GPIO.IN , pull_up_down = GPIO.PUD_DOWN )
GPIO.setup( LEVER_PIN   , GPIO.IN , pull_up_down = GPIO.PUD_UP)

# global variables
c = 0 # c is the count on the rotary phone
busy = False # when true, user should be prevented from interacting


def print_statuses():
    """ Used for debugging, print the count and the status of the 
    different input pins """
    print("  c = " + str(c))
    print( "  counter pin = " + str( GPIO.input( COUNTER_PIN ) ) )
    print( "  dialing pin = " + str( GPIO.input( DIALING_PIN ) ) )
    print( "  lever pin = " + str( GPIO.input( LEVER_PIN ) ) ) 

def text_to_speech(text):
    """
    Plays text using sound card
    """
    cmd = 'espeak -s110 "%s" --stdout | aplay -D sysdefault:CARD=%s' % (text, SOUND_CARD)
    os.system(cmd)

text_to_speech("Hello. My name is Julian. I work at the Library Innovation Lab. I like to run.:")

def play(filename):
    print("getting filename", filename)
    code = os.system('aplay --device=plughw:0,0 %s' % filename)
    return code


def record(filename):
    code = os.system('arecord --device=plughw:0,0 --format=S16_LE --rate 44100 -V mono %s' % filename)
    return code


def play_story( story_number ):
    """ """
    # 

def easter_egg():
    """ If the user dials a number larger than 10, play a special story """


def main( pin ):
    """ Function called when dial returns to resting state. If the phone is 
    off the receiver and no other story is being played, then play a new story
    """
    global c, busy
    if busy or not GPIO.input( LEVER_PIN ):
        print( "busy = " + str(busy) +
                "   and   lever = " + str( GPIO.input( LEVER_PIN )))
    else:
        if c == 0:
            #do nothing 
            print( "no number dialed" )
        elif c >= 1 and c <= 10 :
            busy = True
            print( "playing story : " + str(c) )
            # play_story( c )
            if GPIO.event_detected( COUNTER_PIN ):
                print( "number dialed" )


            # wait until easter egg is over then set busy to false
            busy = False # temp, may be better to feed in bool to story call
        elif c > 10: 
            busy = True
            print( "easter egg")
            # wait until easter egg is over then set busy to false
            busy = False # temp, may be better to feed in bool to story call
        print("resetting")
        c = 0


def count( pin ):
    global c, busy
    if busy or not GPIO.input( LEVER_PIN ):
        print( "busy = " + str( busy ) 
                + "   and   lever = " + str( GPIO.input( LEVER_PIN )))
    else:
        c = c + 1
        print( "counting" , c )

#GPIO.add_event_detect( DIALING_PIN , GPIO.BOTH , callback = main )
GPIO.add_event_detect( COUNTER_PIN , GPIO.FALLING , callback=count , 
                                                    bouncetime=85 )

GPIO.add_event_detect( DIALING_PIN , GPIO.RISING , callback = main )



def cleanup():
    GPIO.remove_event_detect( COUNTER_PIN )
    GPIO.remove_event_detect( DIALING_PIN )
    GPIO.cleanup()

try:
    while True:
        time.sleep( 50000 )
except KeyboardInterrupt:
    cleanup()
    print( 'goodbye!' )
    exit()

cleanup()
exit()
