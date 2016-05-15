make_a_folder :
	mkdir parts
	zcat pall.proc.srt.gz | split -n r/50 -a 3 -d - parts/part. # splitting into X lines, considering size
	python3 02_splitPartsIntoSources_multi_srt.py
	python3 03_joinSplits.py
	python3 04_one2one_srt_multiprocessing.py