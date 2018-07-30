import os
import time
import csv
import random
import subprocess
import RPi.GPIO as GPIO
from google.cloud import storage
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import wave

"""
@author Julian DeGroot-Lutzner
@date Summer 2018

"""
# Settings
STORY_DIRECTORY = '/home/pi/Desktop/telephone-project/recordings/story-wav-files'
INSTRUCTIONS_DIRECTORY = '/home/pi/Desktop/telephone-project/recordings/instructions'

# GPIO output numbers
COUNTER_PIN = 2 # on the rotaty, blue and green wires
DIALING_PIN = 3 # on when dialing, off when resting, white wires
LEVER_PIN = 27 # lever that phone sits on, on when down, off when up

SOUND_CARD = 1 # location of usb sound card
# Variables used for determining for naming new recording files
EVOLUTION_DIGITS = 3 # number if digits allocated for evol digits; i.e. 000-999
AUDIO_FILE_TYPE = '.wav' # file type of audio file
MAX_EVOLUTIONS = 10**EVOLUTION_DIGITS - 1 # max number of evolutions; i.e. 999
NUM_CHARS_FILE_TYPE = len(AUDIO_FILE_TYPE) # most usually 4
CHARS_BACK = EVOLUTION_DIGITS + NUM_CHARS_FILE_TYPE # num chars to upd. in rcrd

# Google Cloud parameters
BUCKET_NAME = 'telephone-project'
GOOGLE_APPLICATION_CREDENTIALS = '"/home/pi/Desktop/telephone-project/not-for-git/google-credentials.json"'

EASTER_EGG = ('Poopy-di scoop. Scoop-ditty-whoop. '
              'Whoop-di-scoop-di-poop. Poop-di-scoopty. '
              'Scoopty-whoop.'
             )

# global variables
new_record_count = 0
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
    code = os.system('aplay --device=plughw:%s,0 %s' % (SOUND_CARD, filename))
    return code

def record(filename):
    code = os.system('arecord --device=plughw:%s,0 --format=S16_LE --rate 44100 -V mono %s' % (SOUND_CARD, filename))
    return code

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))

def transcribe_audio(transcript_csv, gcs_uri):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    speech_client = speech.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code='en-US')

    operation = speech_client.long_running_recognize(config, audio)

    print('Waiting for transcription operation to complete...')
    response = operation.result(timeout=90)
    transcript = ''
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        transcript = transcript + result.alternatives[0].transcript + '.'

    # Write to row of csv file
    output_file = open(transcript_csv, 'a')
    csv.writer(output_file).writerow([transcript])
    output_file.close()
    print('Transcription complete')


def play_story(story_number):
    """
    """
    #play(intro)
    file_name = STORY_DIRECTORY + story_list[story_number-1]
    play(file_name)

def record_new_evolution(story_number):
    """
    """
    old_file = story_list[story_number - 1]
    last_evolution = int(old_file[-(CHARS_BACK):-(NUM_CHARS_FILE_TYPE)])
    if last_evolution < MAX_EVOLUTIONS:
        new_file = (old_file[:-(CHARS_BACK)] +
            '%03d' % (last_evolution + 1) +
            AUDIO_FILE_TYPE)
        record(STORY_DIRECTORY + new_file)
        story_list[story_number - 1] = new_file
        return new_file
    else:
        print('Wow, that is a lot of recordings')
        return None

def record_new_story():
    """"""
    # record audio in temp folder, when we are ready we will move to real direct
    # upload audio file to appropriate directory


def upload_story(source_file, dest_file):
    """
    """
    # When someone records a new story:
    # store the story on google cloud storage
    upload_blob(BUCKET_NAME, soure_file, dest_file)

    # write the url to reactive csv file
    #    http://{BUCKET_NAME}.storage.googleapis.com/{FILE_NAME}
    #   {BUCKET_NAME} = 'telephone-project' in this case
    #   {FILE_NAME} = 'story_number/ evolution of story'

    # write 'Transcription in process' to the reactive csv file
    # transcribe the story
    # write trancription to a reactive csv file

    # remoove old files (dont need to implement this right away)

def developer_mode():
    """ If the user dials a number larger than 10, play a special story """


def main( pin ):
    """ Function called when dial returns to resting state. If the phone is
    off the receiver and no other story is being played, then play a new story
    """
    global c, busy, special_c, attempting_dev_mode, new_record_count
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
        elif c >= 1 and c <= 8:
            busy = True
            print('playing story : ' + str(c))
            play(INSTRUCTIONS_DIRECTORY + '/listen.wav')
            play(INSTRUCTIONS_DIRECTORY + '/beep.wav')
            # play beep
            play_story(c)
            # play beep
            play(INSTRUCTIONS_DIRECTORY + '/beep.wav')
            play(INSTRUCTIONS_DIRECTORY + '/retell.wav')
            # change the countdown to an option for the user to dial when ready
            new_file = record_new_evolution(c)
            # can i do this next part in its own thread?
            upload_blob(BUCKET_NAME, STORY_DIRECTORY + new_file, 'temp-stories' + new_file)
            gsc_uri = ('gs://' + BUCKET_NAME + '/temp-stories' + new_file)
            # WE SHOULD EDIT A CSV FILE THAT IS HELD REMOTELY
            transcript_csv = STORY_DIRECTORY + new_file[:11] + 'transcript.csv'
            #transcribe_audio(transcript_csv,gsc_uri)
            # commenting this out for test run , can transcribe later
            busy = False 
        elif c == 9:
            # record a new story
            busy = True
            print('Record a new story')
            play(INSTRUCTIONS_DIRECTORY + '/record.wav')
            play(INSTRUCTIONS_DIRECTORY + '/beep.wav')
            record(STORY_DIRECTORY + '/new-recordings/' + str(new_record_count))
            new_record_count = new_record_count + 1
            busy = False
        elif c == 10:
            busy = True
            # Play more info about project
            print('Playing more info')
            play(INSTRUCTIONS_DIRECTORY + '/operator.wav')
            busy = False
        else:
            busy = True
            print('easter egg')
            text_to_speech(EASTER_EGG)
            attempting_dev_mode = True
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

'Hello! If this is your first time calling, please dial the operator for more information.'

OPERATOR_TEXT = 'Welcome to Redial. This old phone houses personal stories that are told and retold by people, just like you! You will hear a story and then retell the story in your own words back to the phone. You can see how the stories change overtime by visiting retellproject.com. To get started, dial a number from one to eight to hear and retell a story. Dial nine to record your own story or leave a comment. Dial zero to here these instructions again.'


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
