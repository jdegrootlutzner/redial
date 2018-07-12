import os
import time
import csv
import random
import subprocess
import RPi.GPIO as GPIO
from google.cloud import storage
import wave

"""
@author Julian DeGroot-Lutzner
@date Summer 2018

"""
# Settings 
STORY_DIRECTORY = '/home/pi/Desktop/telephone-project/story-wav-files'

# GPIO output numbers
COUNTER_PIN = 2 # on the rotaty, blue and green wires
DIALING_PIN = 3 # on when dialing, off when resting, white wires
LEVER_PIN = 27 # lever that phone sits on, on when down, off when up

SOUND_CARD = 1 # location of usb sound card

# Google Cloud parameters
BUCKET_NAME = 'telephone-project'
GOOGLE_APPLICATION_CREDENTIALS = '"/home/pi/Desktop/telephone-project/not-for-git/google-credentials.json"'

EASTER_EGG = ('Poopy-di scoop. Scoop-ditty-whoop. '
              'Whoop-di-scoop-di-poop. Poop-di-scoopty. '
              'Scoopty-whoop.'
             )

# global variables
c = 0 # c is the count on the rotary phone
busy = False # when true, user should be prvntd frm actn excpt for spc_action
special_c = 0 # a count on the rotary that is used within a spc_action
attempting_dev_mode = False # user attempting to enter developer mode

# set up GPIOs 
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)
GPIO.setup(COUNTER_PIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(DIALING_PIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(LEVER_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# set up google-cloud-storage
#os.system('export GOOGLE_APPLICATION_CREDENTIALS=%s' % GOOGLE_APPLICATION_CREDENTIALS)
#client = storage.Client()
#bucket = client.get_bucket(BUCKET_NAME)
#blob = bucket.get_blob('test/test.txt')
#print(blob.download_as_string())


# import list of location of the 9 stories on the phone
input_file = open('story-info.csv', 'r')
story_list = next(csv.reader(input_file))
input_file.close()


def print_statuses():
    """ Used for debugging, print the count and the status of the 
    different input pins """
    print('  c = ' + str(c))
    print('  counter pin = ' + str(GPIO.input(COUNTER_PIN)))
    print('  dialing pin = ' + str(GPIO.input(DIALING_PIN)))
    print('  lever pin = ' + str(GPIO.input(LEVER_PIN))) 

def text_to_speech(text):
    """
    Plays text using sound card
    """
    cmd = 'espeak -s110 "%s" --stdout | aplay -D sysdefault:CARD=%s' % (text, SOUND_CARD)
    os.system(cmd)

text_to_speech('Hello.')

def play(filename):
    print('getting filename', filename)
    code = os.system('aplay --device=plughw:0,0 %s' % filename)
    return code

def record(filename):
    code = os.system('arecord --device=plughw:0,0 --format=S16_LE --rate 44100 -V mono %s' % filename)
    return code


def play_story(story_number):
    """
    """
    #play(intro)
    file_name = STORY_DIRECTORY + story_list[story_number-1]
    print(file_name)
    play(file_name)

play_story(1)

def record_story(story_number):
    """
    """


def upload_story():
    '''
    When someone records a new story:
    - store the story on google cloud storage
        - write the url to reactive csv file
            http://{BUCKET_NAME}.storage.googleapis.com/{FILE_NAME}
                - {BUCKET_NAME} = 'telephone-project' in this case
                - {FILE_NAME} = 'name of story/ iteration of story'
        - write 'Transcription in process' to the reactive csv file
    - transcribe the story
        - write trancription to a reactive csv file
    '''

def developer_mode():
    """ If the user dials a number larger than 10, play a special story """


def main( pin ):
    """ Function called when dial returns to resting state. If the phone is 
    off the receiver and no other story is being played, then play a new story
    """
    global c, busy, special_c, attempting_dev_mode
    print('busy', busy)
    if not GPIO.input(LEVER_PIN):
        # If the phone is on the hook, do not allow anything to happen
        print('Receiver lever down. You cannot use the rotary dial.')
    elif busy:
        # If an event is happening, check to see if we are in a special event
        # if we are not in a special event, then do nothing
        if attempting_dev_mode:
            if special_c == 5:
                print('Developer mode unlocked')
            else:
                print('Nothing')
            attempting_dev_mode = False
            busy = False
        else:
            print('Busy. You are already using the phone.')

    else:
        # This is the case in which no event has been called yet. 
        # Allow the user to dial a number and signal an event
        if c == 0:
            #do nothing 
            print('no number dialed')
        elif c >= 1 and c <= 10 :
            busy = True
            print('playing story : ' + str(c))
            # play_story( c )
            if GPIO.event_detected(COUNTER_PIN):
                print('number dialed')


            # wait until event is over then set busy to false
            busy = False # temp, may be better to feed in bool to story call
        elif c > 10: 
            busy = True
            print('easter egg')
            #text_to_speech(EASTER_EGG)
            attempting_dev_mode = True
            #YOU ARE HERE - FIGURING OUT LOCK ________ 
        print('resetting')
        c = 0
        special_c = 0

def count(pin):
    global c, busy, special_c, special_action
    if (not GPIO.input(LEVER_PIN)):
        print('Receiver lever down. You cannot use the rotary dial.')
    elif busy:
        if attempting_dev_mode:
            special_c = special_c + 1
            print('special_c', special_c)
        else:
            print('Busy. You are already using the phone.')
    else:
        c = c + 1
        print('counting' , c)

#GPIO.add_event_detect( DIALING_PIN , GPIO.BOTH , callback = main )
GPIO.add_event_detect(COUNTER_PIN, GPIO.FALLING, callback=count, 
                                                    bouncetime=85)

GPIO.add_event_detect(DIALING_PIN, GPIO.RISING, callback = main)



def cleanup():
    # Close GPIO connections
    GPIO.remove_event_detect(COUNTER_PIN)
    GPIO.remove_event_detect(DIALING_PIN)
    GPIO.cleanup()

    # Write story locations to a csv file 
    output_file = open('story-info.csv.tmp', 'w')
    csv.writer(output_file).writerow(story_list)
    output_file.close()
    # move tmp file to original csv file
    os.system('mv story-info.csv.tmp story-info.csv')       

try:
    while True:
        time.sleep(50000)
except KeyboardInterrupt:
    cleanup()
    print('goodbye!')
    exit()

'''
tags$audio(src = "telephone-project.storage.googleapis.com/prototype-story/1.wav", type = "audio/mp3", autoplay = NA, controls = NA)

"<HTML>
<audio src="telephone-project.storage.googleapis.com/prototype-story/1.wav" type="audio/wav" autoplay controls></audio>
</HTML>
"
'''

cleanup()
exit()
