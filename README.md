# kitab_passim_old_postprocessing

Postprocessing `passim` initial output ([old version, forked from dasmiq](https://github.com/maximromanov/passim)) into the format used in the KITAB-Project.

1. Running `make` does the trick. It takes `pall.proc.srt.gz` and:
	1. splits it into smaller parts (keeps them unzipped); runs a single process
	2. then splits every part and creates all individual files for each book; runs 12 processes (`python3`, `multiprocessing`)
	3. merges output from each part (one-to-many, T1-to-T2, T1-to-T2, T1-to-Tx...); runs a single process
	4. splits merged output into pairs (one-to-one), and stores all pairs for T1 into one zipped file; runs 12 processes (`python3`, `multiprocessing`)

```
postprocess_passim_output :
	mkdir parts
	zcat pall.proc.srt.gz | split -n r/50 --additional-suffix=".srt" -a 3 -d - parts/part.
	python3 02_splitPartsIntoSources_multi_srt.py
	python3 03_joinSplits.py
	python3 04_one2one_srt_multiprocessing.py
```



