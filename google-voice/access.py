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
            http://{BUCKET_NAME}.storage.googleapis.com/{FILE_NAME}
                - {BUCKET_NAME} = 'telephone-project' in this case
                - {FILE_NAME} = 'name of story/ iteration of story'
        - write "Transcription in process" to the reactive csv file
    - transcribe the story
        - write trancription to a reactive csv file

"""

tags$audio(src = "telephone-project.storage.googleapis.com/prototype-story/1.wav", type = "audio/mp3", autoplay = NA, controls = NA)

"<HTML>
<audio src="telephone-project.storage.googleapis.com/prototype-story/1.wav" type="audio/wav" autoplay controls></audio>
</HTML>
"
