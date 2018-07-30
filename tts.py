import os
import random

# export=GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials
def synthesize_text(text, output_filename, output_dir, voice=None):
    """
    Synthesizes speech from the input string of text.
    Female voice = 0, Male voice = 1
    output filename doesn't need extension
    """
    from google.cloud import texttospeech_v1beta1 as texttospeech
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.types.SynthesisInput(text=text)

    genders = (texttospeech.enums.SsmlVoiceGender.FEMALE, texttospeech.enums.SsmlVoiceGender.MALE)
    if not voice:
        gender = genders[random.randrange(0, 2)]
    else:
        gender = genders[voice]

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-US',
        ssml_gender=gender)

    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    response = client.synthesize_speech(input_text, voice, audio_config)

    # The response's audio_content is binary.
    mp3_filepath = os.path.join(output_dir, "%s.mp3" % output_filename)
    with open(mp3_filepath, 'wb') as out:
        out.write(response.audio_content)
        print('Audio content written to file %s' % mp3_filepath)
    
    wav_name = os.path.join(output_dir, "%s.wav" % output_filename)
    print('Audio content re-written to file %s' % wav_name)
    os.system("mpg321 -w %s %s" % (wav_name, mp3_filepath))
    print('Deleting mp3')
    os.remove(mp3_filepath)

#synthesize_text('Welcome to the story collector. By dialing 8 you can record a new story that will be come a part of Redial. You will have one minute to record a first person story. Pretend that you are telling your story to a friend.', 'record', '/home/pi/Desktop/telephone-project/recordings/instructions')

synthesize_text('Welcome to Redial. This old phone houses personal stories that are told and retold by people, just like you! You will hear a story and then retell the story in your own words back to the phone. You can see how the stories change overtime by visiting retellproject.com. To get started, dial a number from one to eight to hear and retell a story. Dial nine to record your own story or leave a comment. Dial zero to here these instructions again.', 'operator', '/home/pi/Desktop/telephone-project/recordings/instructions')
#synthesize_text('Now retell the story in your own words while mantaining the first person perspective. Focus more on how the story teller felt and less on the specific words. Recording will start in 3, 2, 1.', 'retell', '/home/pi/Desktop/telephone-project/recordings/instructions')
#synthesize_text('You will hear a story and then retell the story. Story will start in 3, 2, 1.', 'listen', '/home/pi/Desktop/telephone-project/recordings/instructions')
