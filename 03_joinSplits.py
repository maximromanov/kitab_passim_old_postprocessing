import datetime, os, gzip, shutil, random
startTime = datetime.datetime.now()

folder = "./parts/"

# Annotation:
# 1. Splitting big SRT file into sections (shell script)
# 2. Splitting each section into individual sources (sections)
# 3. Joining sections on individual sources into individual sources (true one2many)
# 4. Splitting one2many > one2one (largest SRT is 1,7Gb, Tarikh madinat Dimashq, I think)
# 5. Adding page references into David's SRT files

# 1. Splitting big SRT file into sections (shell script)
###!/bin/bash
##
###SBATCH --mem=32000
###SBATCH --mail-type=ALL                     # notifications for job done
###SBATCH --mail-user=maxim.romanov@tufts.edu # send-to address
##
##cd /cluster/home/mroman01/working/passimResults/passim-Arabic-10500-100/
##zcat bidirectional.srt.gz | split -l 3000000 -a 3 -d - bidiSplit/bidi.
##cd bidiSplit/
##gzip *

##zcat pall.proc.srt.gz | split -l 3000000 -a 3 -d - parts/part.

# 0. reorder line
# {print $0; print $1,$3,$2,$4,$5,$6,$8,$7,$10,$9,$13,$14,$11,$12,$16,$15}
# [l[1-1],l[3-1],l[2-1],l[4-1],l[5-1],l[6-1],l[8-1],l[7-1],l[10-1],l[9-1],l[13-1],l[14-1],l[11-1],l[12-1],l[16-1],l[15-1]]


# 3. Joining sections on individual sources into individual sources (true one2many)
def joinSplits(folder):
    trgFolder = folder + "3_sources/"
    if os.path.exists(trgFolder):
        shutil.rmtree(trgFolder)
    os.makedirs(trgFolder)

    splitFolder = folder+"2_split/"
    splitFolders = os.listdir(splitFolder)

    for fldr in splitFolders:
        procFolder = splitFolder + fldr
        splitFiles = os.listdir(procFolder)
        for fl in splitFiles:
            if fl.endswith(".srt"):
                with open(procFolder+"/"+fl, "r", encoding="utf8") as ftemp:
                    fread = ftemp.read()
                    if os.path.isfile(trgFolder+fl):
                        print("\tAppending to %s" % fl)
                        with open(trgFolder+fl, "a", encoding="utf8") as fa:
                            fa.write(fread)
                    else:
                        print("Saving new file %s" % fl)
                        with open(trgFolder+fl, "w", encoding="utf8") as fb:
                            fb.write(fread)

joinSplits(folder)

print("Processing time: " + str(datetime.datetime.now()-startTime))
print("Tada!")
