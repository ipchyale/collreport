# collection-report
A tutorial example of a photographic collection report  

## Data Processing

You will receive data from collaborators in several files, together with folders of texture images and digitized prints.

### Thickness and Gloss

Let's start with the easiest: thickness and gloss data. They are easiest because the data is already structured, and in fact tabular. Typically, a collaborator will provide a single Excel workbook that contains both gloss and thickness measurements, possibly in different worksheets. Let's say you receive a file called ``gloss_thickness.xlsx`` that has two sheets, ``gloss`` and ``thickness``. Processing this data is as simple as:

```
tf = pd.read_excel("gloss_thickness.xlsx", sheet_name = "thickness")
gf = pd.read_excel("gloss_thickness.xlsx", sheet_name = "gloss")
```

### Color

Color is a bit trickier, because our color software, Spectrashop, exports to a non-tabular data format. I've written a parser for these files, but occasionally you'll encounter a file with a structure that the parser doesn't expect (this happens as a result of the way Spectrashop is used). As time goes on, we will improve the parser to handle all possible file structures.

In the ideal case (and assuming you've cloned the ss2csv folder into your home directory), parsing a color file is as follows:

```
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

### Texture

Texture is the trickiest of the three, because it involves unstructured data (images), and because there are a few different ways we model texture. The most important texture model we use, the one that appears in the "glyph", is _roughness_. Roughness is actually pretty straightforward to obtain because both Jack and I have built some software around it:

```
import sys, glob, os
sys.path.append(os.path.expanduser("~") + "/" + "ivpy/src")
from ivpy import *
from ivpy.extract import extract

DIR = "/path/to/texture/files"

tiffpaths = glob.glob(os.path.join(DIR, "*.tif"))
df = pd.DataFrame({"tiffpath":tiffpaths})

attach(df, "tiffpath")

df["roughness"] = extract("rougness")
```
