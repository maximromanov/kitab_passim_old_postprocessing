# passim_srt_kitab

Postprocessing `passim` initial output (old version)[^passim] into the format used in the KITAB-Project.

1. Running `make` does the trick. It takes `pall.proc.srt.gz` and:
	1. splits it into smaller parts (keeps them unzipped)
	2. then splits every part and creates all individual files for each book
	3. merges output from each part (one-to-many, T1-to-T2, T1-to-T2, T1-to-Tx...)
	4. splits merged output into pairs (one-to-one), and stores all pairs for T1 into one zipped file.

[^passim]: [https://github.com/maximromanov/passim](https://github.com/maximromanov/passim)



