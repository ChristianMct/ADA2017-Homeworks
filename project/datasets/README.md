# Datasets

The purpose of this page is to achieve strong reproducibility and clarity in dataset provenance by summarising the different pipeline steps and the dataset versions they 
produced.

## Pages Extraction

Source file: ````hdfs:///datasets/wikipedia/enwiki-latest-pages-articles-multistream.xml````

Location: ````hdfs:///user/mouchet/datasets/````

| File  | Version | Size | Number of battle pages | Comment |
| --- | --- | --- | --- | --- |
| battle-pages-0.xml | 0.1 | 127 Mo | 24089 | Recursive "revision" schema |
| battle-pages-1.xml  | 0.2 | 131 Mo | 27255 | Switched to flat schema, included Sieges|
| battle-pages-2.json | 0.3 | 124 Mo | 27255 | Set output to JSON for easier python processing |

## Fields Extraction

| Source | File | Version | Size | Infobox count | Coords count | Comment |
| ---- | --- | ------- | ---- | ------------- | ------------ | ------- |
| battle-pages-2.json | battle-fields-0.json | 0.4 | 13 Mo | ? | ? | Extract infobox fields only |