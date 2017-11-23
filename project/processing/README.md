# Processing pipeline
This document describes the data processing pipeline steps that goes from a wikipedia dump to actionable datasets.

## Pipeline steps

| Name | Job | Input | Output | Description |
| ---- | --- | ----- | ------ | ----------- |
| Pages extraction | `page_extraction.py` (Cluster)| XML page article dump file | `battle-pages-`**v**`.jsonlist` | Selects all battle-related pages and write them in JSON format, one page per line |
| Fields extraction | `fields_extraction.py` (Local)| `battle-pages-`**v**`.json`  | `battle-fields-`**v**`.json`  | Parses the wikitext data the pages to extract (yet unparsed) fields |

