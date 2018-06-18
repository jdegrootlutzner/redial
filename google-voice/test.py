import csv
transcript = ""
for i in range(1,7):

    u = "he " + str(i) + "k"
    transcript = transcript + u
output_file = open('transcription-text', 'w')
csv_output_writer = csv.writer(output_file)
csv_output_writer.writerow(["transcriptions"])
csv_output_writer.writerow([transcript])
