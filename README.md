# Data Processing

You will receive data from collaborators in several files, together with folders of texture images and digitized prints.

## Walking a foldered directory

If your files are in multiple folders, you'll have to get them by walking the root:

```python
import os

DIR = "/path/to/your/root/directory/"

allfiles = []
for root,dirs,files in os.walk(DIR):
    for file in files:
        allfiles.append(root + "/" + file)
 ```

## Thickness and Gloss

Let's start with the easiest: thickness and gloss data. They are easiest because the data is already structured, and in fact tabular. Typically, a collaborator will provide a single Excel workbook that contains both gloss and thickness measurements, possibly in different worksheets. Let's say you receive a file called ``gloss_thickness.xlsx`` that has two sheets, ``gloss`` and ``thickness``. Processing this data is as simple as:

```python
tf = pd.read_excel("gloss_thickness.xlsx", sheet_name = "thickness")
gf = pd.read_excel("gloss_thickness.xlsx", sheet_name = "gloss")
```

## Color

Color is a bit trickier, because our color software, Spectrashop, exports to a non-tabular data format. I've written a parser for these files, but occasionally you'll encounter a file with a structure that the parser doesn't expect (this happens as a result of the way Spectrashop is used). As time goes on, we will improve the parser to handle all possible file structures.

In the ideal case (and assuming you've cloned the ss2csv folder into your home directory), parsing a color file is as follows:

```python
import sys, os
sys.path.append(os.path.expanduser("~"))
from ss2csv.ss2csv import file2table,cleancols

df = cleancols(file2table(example.txt))
```

You will, additionally, have to parse the `SAMPLE_ID1` column in order to extract what we might call the "metadata" of color measurements:

1. `idx` sample index, which is typically an institutional accession number
2. `mmode` illumination mode, either M0, M1, M2, or M3
3. `mloc` measurement location, either dmax, dmin, or dmid
4. `mtrial` measurement trial, usually 0, 1, or 2

## Texture

Texture is the trickiest of the three, because it involves unstructured data (images), and because there are a few different ways we model texture. 

### Roughness

The most important texture model we use, the one that appears in the "glyph", is _roughness_. Roughness is actually pretty straightforward to obtain because both Jack and I have built some software around it:

```python
import sys, glob, os
sys.path.append(os.path.expanduser("~") + "/" + "ivpy/src")
from ivpy import *
from ivpy.extract import extract

DIR = "/path/to/texture/files"

tiffpaths = glob.glob(os.path.join(DIR, "*.tif"))
df = pd.DataFrame({"tiffpath":tiffpaths})

attach(df, "tiffpath")

df["roughness"] = extract("roughness")
```

### Bandpass filtering

During the process of modeling roughness, we create a cropped, normalized, bandpass version of the original scope capture. The `extract()` function in `iv.py` does not save this processed image, but we can do so using the `utils` library in `iv.py`:

```python
from ivpy.utils import tifpass

attach(df,"tiffpath")
df["tiffpath_tifpass"] = tifpass(savedir="/path/to/folder/you/want/images/saved/to")
```

This will save the images as TIFFs. If you want to display them correctly in `iv.py`, you'll need to convert them to a file format like JPG. I use native Mac tools for that, but there are plenty of other options.

# Reporting

Once we've ingested the raw data files, we can begin producing our report. A report needn't contain every possible insight buried in the data; insights will emerge over time during a back-and-forth process with our collaborators. An initial report, however, needs simply to provide the interested parties with (typically visual) access to the collection and a sense of where it sits relevant to other collections, including the lab's reference collection.

## Data distributions and the LML reference collection

The most basic elements of our reporting involve simple data distributions, set against the LML reference collection (LMLRC). I recommend producing histograms that include both the collection in question and the LMLRC. This is easy to do with `iv.py`, using this approach:

1. Read in each dataset as a separate dataframe:

```python
cf = pd.read_csv("collection.csv")
lf = pd.read_csv("lml.csv")
```

2. Add a `grp` column to each dataframe:

```python
cf["grp"] = 'c'
lf["grp"] = 'l'
```

3. Create a basic icon for each group:

```python
from PIL import Image

im_c = Image.new('RGB',(64,64),"yellow")
im_l = Image.new('RGB',(64,64),"#001b2e")

im_c.save("c.jpg")
im_l.save("l.jpg")

cf["ipath"] = "c.jpg"
lf["ipath"] = "l.jpg"
```

4. Concatenate the two dataframes:

```python
df = pd.concatenate([cf,lf])
```

5. Use `iv.py` to make histograms using these icons:

```python
import sys, os
sys.path.append(os.path.expanduser("~") + "/" + "ivpy/src")
from ivpy import *

attach(df,"ipath")

histogram(xcol="roughness",bins=450,thumb=64,bg="grey")
```

![unit histogram](/hist.png)


