import io, os, csv

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

# Instantiates a client
client = speech.SpeechClient()

def main():
    # Initialize csv file to write trancriptions to
    output_file = open('transcription-text', 'w')
    csv_output_writer = csv.writer(output_file)
    csv_output_writer.writerow(["transcriptions"])
    for i in range(1,7):
        print("Transcribing story " + str(i))
        gsc_uri = "gs://telephone-project/prototype-story/" + str(i) + ".wav"
        transcribe_gcs(gsc_uri,
                    csv_output_writer)
    print("Done!")

def transcribe_gcs(gcs_uri, csv_output_writer):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=22050,
        #44100
        language_code='en-US')

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    response = operation.result(timeout=600)
    transcript = ""
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        transcript = transcript + result.alternatives[0].transcript + "\n"

    # Write to row of csv file
    csv_output_writer.writerow([transcript])


def transcribe_interview():
    output_file = open('michelle-transcription', 'w')
    csv_output_writer = csv.writer(output_file)
    gsc_uri = "gs://telephone-project/test/michelle-interview.wav"
    transcribe_gcs(gsc_uri, csv_output_writer)

"""
gcs_uri = gs://<bucket_name>/<file_path_inside_bucket>



"""
transcribe_interview()
#main()
