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

def reformatLine(line):
    l = line.split("\t")
    lineNew = "\t".join([l[1-1],l[3-1],l[2-1],l[4-1],l[5-1],l[6-1],l[8-1],l[7-1],l[10-1],l[9-1],l[13-1],l[14-1],l[11-1],l[12-1],l[16-1],l[15-1]])
    #print(l)
    #input(lineNew.split("\t"))
    return(lineNew)

# 2. Splitting each section into individual sources (sections)  
def splitPartsIntoSources(folder):
    print("Processing split files...")
    
    listOfIs = []
    for i in os.listdir(folder):
        if i.endswith(".gz"):
            listOfIs.append(i)

    if len(listOfIs) != 0:
        file = random.choice(listOfIs)
        print(file)
        
        tempFile = file[:-3]+".temp"
        os.rename(folder + file, folder + tempFile)
        
        fileFolder = folder + "_split/" + file[:-3] + "/"
        if os.path.exists(fileFolder):
            shutil.rmtree(fileFolder)
        os.makedirs(fileFolder)
        
        counter = 0
        dic = {}
        with gzip.open(folder+tempFile,'rt', encoding='utf-8') as fin:
            for lineRaw in fin:
                #lineRaw = lineRaw.replace("\n", "")
                l = [lineRaw, reformatLine(lineRaw)]
                for line in l:
                    #print(line)
                    counter += 1
                    srtID = line.split("\t")[8].split("_")[0]
                    #input(srtID)
                    if srtID in dic:
                        dic[srtID] = dic[srtID]+line
                    else:
                        dic[srtID] = line
                    if counter % 50000 == 0:
                        print("{:,}".format(counter))
                        print("\tProcessing time: " + str(datetime.datetime.now()-startTime))
                        for k,v in dic.items():
                            with open(fileFolder+"%s.srt" % k, "a", encoding="utf-8") as f:
                                f.write(v)
                        dic = {}
                    
        for k,v in dic.items():
            with open(fileFolder+"%s.srt" % k, "a", encoding="utf-8") as f:
                f.write(v)

        # move processed file and rename it back to *.gz
        if os.path.exists(folder+"_processed/"):
            pass
        else:
            os.makedirs(folder+"_processed/")
            
        os.rename(folder + tempFile, folder+"_processed/" + file)
        
    else:
        print("All files have been processed...")
        

splitPartsIntoSources(folder)
splitPartsIntoSources(folder)
splitPartsIntoSources(folder)
splitPartsIntoSources(folder)
splitPartsIntoSources(folder)

print("Processing time: " + str(datetime.datetime.now()-startTime))
print("Tada!")
