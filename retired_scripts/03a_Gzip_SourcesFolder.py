import datetime, os, gzip, shutil, random
startTime = datetime.datetime.now()

folder = "./parts/"

# Annotation:
# 1. Splitting big SRT file into sections (shell script)
# 2. Splitting each section into individual sources (sections)
# 3. Joining sections on individual sources into individual sources (true one2many)
# 4. Splitting one2many > one2one (largest SRT is 1,7Gb, Tarikh madinat Dimashq, I think)
# 5. Adding page references into David's SRT files

# 3a. Gzip _sources subFolder
os.system("cd parts/_sources/ && for f in $(ls *.srt); do gzip $f; done;")



print("Processing time: " + str(datetime.datetime.now()-startTime))
print("Tada!")
