# pysimsfar

This package edits Sims 1 .far files.

## Installation

```pip install pysimsfar```

## Usage

Get bytes of an entry by file name:

```python
from pysimsfar.far import Far

f = Far(r"C:\Program Files (x86)\Maxis\The Sims\UIGraphics\UIGraphics.far")
bytes = f.get_bytes("Studiotown\largeback.bmp")
```

Get bytes of an entry:

```python
from pysimsfar.far import Far

f = Far(r"C:\Program Files (x86)\Maxis\The Sims\UIGraphics\UIGraphics.far")
for entry in f.manifest.manifest_entries:
    if entry.file_name == "Studiotown\largeback.bmp":
        bytes = f.get_bytes(entry)
```

Print each entry's file name.

```python
from pysimsfar.far import Far

f = Far(r"C:\Program Files (x86)\Maxis\The Sims\UIGraphics\UIGraphics.far")
for entry in f.manifest.manifest_entries:
    print(entry.file_name)
```