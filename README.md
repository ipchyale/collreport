# collection-report
A tutorial example of a photographic collection report  

## Data Processing

You will receive data from collaborators in several files, together with folders of texture images and digitized prints.

### Thickness and Gloss

Let's start with the easiest: thickness and gloss data. They are easiest because the data is already structured, and in fact tabular. Typically, a collaborator will provide a single Excel workbook that contains both gloss and thickness measurements, possibly in different worksheets. Let's say you receive a file called ``gloss_thickness.xlsx`` that has two tabs, ``gloss`` and ``thickness``. Processing this data is as simple as:

``
tf = pd.read_excel("gloss_thickness.xlsx", sheet_name = "thickness")
gf = pd.read_excel("gloss_thickness.xlsx", sheet_name = "gloss")
``

