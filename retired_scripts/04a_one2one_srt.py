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

# 4. Splitting one2many > one2one (largest SRT is 1,7Gb, Tarikh madinat Dimashq, I think)
def one2one(folder):
    print("Splitting one2many into one2one...")
    srcFolder = folder + "_sources/"

    listOfIs = []
    for i in os.listdir(srcFolder):
        if i.endswith(".srt"):
            listOfIs.append(i)

    subList = 200
    if len(listOfIs) > subList:
        listOfIsSample = random.sample(listOfIs, subList)
    else:
        listOfIsSample = listOfIs

    for i in listOfIsSample:
        if os.path.isfile(srcFolder+i):
            print("File %s is being processed..." % i)
            # rename into temp
            os.rename(srcFolder+i, srcFolder+i+".temp")
            # process: collect dic
            #input()
            dic = {}
            with open(srcFolder+i+".temp",'rt', encoding='utf8') as one2many:
                for line in one2many:
                    #print(line)
                    srtID = line.split("\t")[8].split("_")[0] + \
                            "_" + \
                            line.split("\t")[9].split("_")[0]
                    print(srtID)
                    if srtID in dic:
                        dic[srtID] = dic[srtID]+line
                    else:
                        dic[srtID] = line
            # save results
            trgFolder = folder + "_one2one/" + i.split(".")[0]
            print(folder + "_one2one/" + i.split(".")[0])
            if os.path.exists(trgFolder):
                shutil.rmtree(trgFolder)
                os.makedirs(trgFolder)
            else:
                os.makedirs(trgFolder)
            
            for k,v in dic.items():
                #with gzip.open(trgFolder+"/%s.srt.gz" % k, "wt", encoding="utf8") as f:
                with open(trgFolder+"/%s.srt" % k, "wt", encoding="utf8") as f:
                    f.write(v)

            # finish
            shutil.make_archive(trgFolder, 'zip', trgFolder) # zip the folder
            shutil.rmtree(trgFolder) # remove the folder
            os.rename(srcFolder+i+".temp", srcFolder+i+"") # rename into processed
            
        else:
            print("\tFile %s has been processed..." % i)
        
    print("Total Time: " + str(datetime.datetime.now()-startTime))

one2one(folder)
one2one(folder)
one2one(folder)
one2one(folder)
one2one(folder)

print("Processing time: " + str(datetime.datetime.now()-startTime))
print("Tada!")
