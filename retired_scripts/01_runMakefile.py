import datetime, os, gzip, shutil, random
startTime = datetime.datetime.now()

folder = "./parts/"

# run make!

# Annotation:
# 1. Splitting big SRT file into sections (shell script)
# 2. Splitting each section into individual sources (sections)
# 3. Joining sections on individual sources into individual sources (true one2many)
# 4. Splitting one2many > one2one (largest SRT is 1,7Gb, Tarikh madinat Dimashq, I think)
# 5. Adding page references into David's SRT files

# 1. Splitting big SRT file into sections (shell script)

os.system("mkdir parts")
os.system("zcat pall.proc.srt.gz | split -l 3000000 -a 3 -d - parts/part.")
#os.system("zcat part.047.gz | split -l 3000000 -a 3 -d - parts/part.")
os.system("cd parts/ && for f in $(ls *); do gzip $f; done;")

print("Processing time: " + str(datetime.datetime.now()-startTime))
print("Tada!")
