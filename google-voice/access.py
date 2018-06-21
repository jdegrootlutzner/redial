from google.cloud import storage
import wave

client = storage.Client()
bucket = client.get_bucket('telephone-project')
blob = bucket.get_blob('test/test.txt')
print(blob.download_as_string())



"""
When someone records a new story:
    - store the story on google cloud storage
        - write the url to reactive csv file
            http://telephone-project.storage.googleapis.com/{FILE_NAME}
                - {BUCKET_NAME} = 'telephone-project' in this case
                - {FILE_NAME} = 
        - write "Transcription in process" to the reactive csv file
    - transcribe the story
        - write trancription to a reactive csv file

"""
