from PIL import Image,ImageDraw,ImageFont
import os
#import textwrap
import numpy as np
from copy import deepcopy

class CollectionItem:
    def __init__(self):
        self.acc = '' 
        self.artist = ''
        self.nationality = ''
        self.active = ''
        self.title = ''
        self.date = ''
        self.medium = ''
        self.dims = ''
        self.credit = ''
        self.printpath = '' 
        self.imagelight = [] # list of floats
        self.basesat = [] # list of floats
        self.mappath = ''
        self.fluorescence = [] # list of floats (AUC)
        self.goosepath = ''
        self.color = [] # list of dicts with color data
        self.texture = [] # list of dicts with texture data

FONTDIR = os.path.expanduser("~") + "/fonts/"

fonts = {
    "thin":FONTDIR+"Roboto-Thin.ttf",
    "light":FONTDIR+"Roboto-Light.ttf",
    "regular":FONTDIR+"Roboto-Regular.ttf",
    "medium":FONTDIR+"Roboto-Medium.ttf",
    "bold":FONTDIR+"Roboto-Bold.ttf",
    "black":FONTDIR+"Roboto-Black.ttf",
    "thin-i":FONTDIR+"Roboto-ThinItalic.ttf",
    "light-i":FONTDIR+"Roboto-LightItalic.ttf",
    "regular-i":FONTDIR+"Roboto-Italic.ttf",
    "medium-i":FONTDIR+"Roboto-MediumItalic.ttf",
    "bold-i":FONTDIR+"Roboto-BoldItalic.ttf",
    "black-i":FONTDIR+"Roboto-BlackItalic.ttf",
    "serif":FONTDIR+"RobotoSerif-Thin.ttf"
}

font = ImageFont.truetype(fonts['regular'],45)
font_large = ImageFont.truetype(fonts['regular'],90)
font_serif = ImageFont.truetype(fonts['serif'],36)

def slider_pos(val,valmin,valrange,slider_width):
    pct = (val - valmin) / valrange
    pos = int(pct * (slider_width - slider_width * 0.2) + slider_width * 0.1)

    return pos

def slider(title,collvals,colltrials,lmlvals=None,
           font=font,bg='white',rounding_digits=0,pegfill=None,collfill=None):
    
    fill = "dimgrey"
    lmlfill = "lightgrey"
    
    if collfill is None:
        collfill = "#c99277" # a dusty orange color

    if pegfill is None:
        pegfill = bg
    
    canvas = Image.new('RGB',(1000,200),bg)
    slider_width,slider_height = canvas.size
    draw = ImageDraw.Draw(canvas)
    
    # the slider bar
    draw.line([(int(slider_width*0.1),int(slider_height*0.5)),(int(slider_width*0.9),int(slider_height*0.5))],width=int(slider_width/125),fill=fill)

    # min and max values across both lmlvals and collvals
    valmin = min([min(lmlvals),min(collvals)])
    valmax = max([max(lmlvals),max(collvals)])
    valrange = valmax - valmin

    # distribution ticks
    tick_height = slider_height / 8
    
    # lmlvals is a list of all values in the lml paper collection
    if lmlvals is not None:
        for lmlval in lmlvals:
            pos = slider_pos(lmlval,valmin,valrange,slider_width)
            draw.line([(pos,int(slider_height*0.5-tick_height/2)),(pos,int(slider_height*0.5+tick_height/2))],width=int(slider_width/1000),fill=lmlfill)

    # collvals is a list of all values in the print collection
    for collval in collvals:
        pos = slider_pos(collval,valmin,valrange,slider_width)
        draw.line([(pos,int(slider_height*0.5-tick_height/2)),(pos,int(slider_height*0.5+tick_height/2))],width=int(slider_width/1000),fill=collfill)
    
    # median peg should sit atop the distribution ticks
    try:
        itemval = np.median(colltrials)
    except:
        # in case `colltrials` is a single value
        itemval = np.median([colltrials])

    try:
        peg = slider_pos(itemval,valmin,valrange,slider_width)
        draw.rounded_rectangle([(peg-15,70),(peg+15,130)],radius=5,fill=pegfill,outline=fill,width=4)
    except:
        pass

    # collection trials sit above the median peg
    if isinstance(colltrials,list):
        for k,colltrial in enumerate(colltrials):
            pos = slider_pos(colltrial,valmin,valrange,slider_width)
            top_offset = 8
            peg_top = 70
            trial_spacer = 8
            draw.line([(pos-15,peg_top - top_offset - trial_spacer * k),(pos+15,peg_top - top_offset - trial_spacer * k)],width=4,fill=fill)
    
    # we print the minimum and maximum values on the slider, along with the title
    if rounding_digits is not None:
        if rounding_digits==0:
            valmin = round(valmin) # returns int
            valmax = round(valmax) # returns int
        else:
            valmin = round(valmin,rounding_digits)
            valmax = round(valmax,rounding_digits)
        
    draw.text((int(slider_width*0.1),int(slider_height*0.75)),text=str(valmin),font=font,fill=fill)
    
    vmaxWidth,_ = font.getsize(str(valmax))
    draw.text((int(slider_width*0.9)-vmaxWidth,int(slider_height*0.75)),text=str(valmax),font=font,fill=fill)
    
    titleWidth,_ = font.getsize(title)
    draw.text((int(slider_width/2-titleWidth/2),int(slider_height*0.75)),text=title,font=font,fill=fill)
    
    return canvas

def info_panel(idx,title='',font=font,font_large=font_large,bg='white'):
    
    fill = "dimgrey"
    
    fontWidthIdx,fontHeightIdx = font_large.getsize(idx)
    fontWidthTitle,fontHeightTitle = font.getsize(title)

    spacer = font_large.getsize("1")[0] # thin space
    panelWidth = fontWidthIdx + fontWidthTitle + spacer
    
    canvas = Image.new('RGB',(panelWidth,fontHeightIdx),bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.text((0,0),text=idx,font=font_large,fill=fill)
    draw.text((fontWidthIdx+spacer,fontHeightIdx-fontHeightTitle),text=title,font=font,fill=fill)
    
    return canvas

def tombstone(tombstone_dict, fonts=fonts, bg='white'):
    
    fill = "dimgrey"

    line_spacer = 16
    section_spacer = 32

    font = ImageFont.truetype(fonts['regular'],30)
    font_artist = ImageFont.truetype(fonts['bold'],45)
    font_title = ImageFont.truetype(fonts['regular-i'],30)

    data = {
        'artist': {'font': font_artist, 'text': tombstone_dict.get('artist')},
        'nationality': {'font': font, 'text': tombstone_dict.get('nationality')},
        'active': {'font': font, 'text': tombstone_dict.get('active')},
        'title': {'font': font_title, 'text': tombstone_dict.get('title')},
        'date': {'font': font, 'text': tombstone_dict.get('date')},
        'medium': {'font': font, 'text': tombstone_dict.get('medium')},
        'dims': {'font': font, 'text': tombstone_dict.get('dims')},
        'credit': {'font': font, 'text': tombstone_dict.get('credit')}
    }

    tombstoneWidth = 0
    tombstoneHeight = 0

    for key, value in data.items():
        try:
            fontWidth, fontHeight = get_text_size(value['font'], value['text'])
        except:
            fontWidth, fontHeight = (0,0)
        tombstoneWidth = max(tombstoneWidth, fontWidth)
        tombstoneHeight += fontHeight + line_spacer

        if key == 'active' or key == 'date':
            tombstoneHeight += section_spacer

    tombstone_text = Image.new('RGB',(tombstoneWidth,tombstoneHeight),bg)
    draw = ImageDraw.Draw(tombstone_text)
    
    currHeight = 0

    for key, value in data.items():
        try:
            fontWidth, fontHeight = get_text_size(value['font'], value['text'])
        except:
            fontWidth, fontHeight = (0,0)
        draw_text(draw, (0, currHeight), value['text'], value['font'], fill)
        currHeight += fontHeight + line_spacer

        if key == 'active' or key == 'date':
            currHeight += section_spacer

    return tombstone_text

def left_panel(collection_item,special_panel,bg='white'):

    infopanel = info_panel(collection_item.acc,bg=bg)
    #infopanel.thumbnail((48/infopanel.height*infopanel.width,48),Image.Resampling.LANCZOS)

    try:
        print_image = Image.open(collection_item.printpath)
    except:
        print_image = Image.new('RGB',(1024,1024),"dimgrey")

    print_image = draw_outline(print_image,1,'black')
    print_image.thumbnail((1024,1024),Image.Resampling.LANCZOS)

    tombstone_dict = {
        'artist': collection_item.artist,
        'nationality': collection_item.nationality,
        'active': collection_item.active,
        'title': collection_item.title,
        'date': collection_item.date,
        'medium': collection_item.medium,
        'dims': collection_item.dims,
        'credit': collection_item.credit
    }

    tombstone_text = tombstone(tombstone_dict,bg=bg)

    column = vconcat(infopanel,print_image,tombstone_text,spacer=64,bg=bg)

    if special_panel is not None:
        column = vconcat(column,special_panel,spacer=192,bg=bg)

    return column, infopanel.height

def condition_panel(collection_item,collvals,bg):

    imagelight_slider = slider('IMAGE LIGHTNESS (%)',
                               collvals['imagelight'],
                               collection_item.imagelight,
                               pegfill='magenta',bg=bg)
    basesat_slider = slider('BASE SATURATION (%)',
                            collvals['basesat'],
                            collection_item.basesat,
                            pegfill='cyan',bg=bg)
                    
    kmap = Image.open(collection_item.mappath)
    kmap = draw_outline(kmap,1,'black')
    kmap = hfit(kmap,imagelight_slider.width,bg=bg)

    panel = vconcat(kmap,imagelight_slider,basesat_slider,spacer=64)

    return panel

def uv_panel(collection_item,collvals,lmlvals,bg):

    uv_slider = slider('FLUORESCENCE',
                       collvals['fluorescence'],
                       collection_item.fluorescence,
                       lmlvals['fluorescence'],
                       rounding_digits=2,bg=bg)
    
    goosebump_plot = Image.open(collection_item.goosepath)
    goosebump_plot = draw_outline(goosebump_plot,1,'black')
    goosebump_plot = hfit(goosebump_plot,uv_slider.width,bg=bg)

    panel = vconcat(goosebump_plot,uv_slider,spacer=64,bg=bg)

    return panel

def coloricon_single(c,s,loc,label=None,fonts=fonts,bg='white'):

    font_size_loc = int(s/12)
    font_loc = ImageFont.truetype(fonts['regular'],font_size_loc)

    font_size_label = int(s/8)
    font_label = ImageFont.truetype(fonts['regular'],font_size_label)

    im = Image.new('RGB',(s,s),bg)
    draw = ImageDraw.Draw(im)
    draw.rounded_rectangle(
        [(s/32, s/32), (s - s/32, s - s/32)],radius=int(s*0.15625),fill=c,outline='black',width=1
    )

    if label is not None:

        if loc=='base':
            fill = "black"
        elif loc=='image':
            fill = "white"

        Lab = label.split(',')
        L = 'L: ' + Lab[0]
        a = 'a*: ' + Lab[1]
        b = 'b*: ' + Lab[2]
        Lw,Lh = font_label.getsize(L)
        aw,ah = font_label.getsize(a)
        bw,bh = font_label.getsize(b)

        topoffset = s / 5
        spacer = s / 16
        draw.text((s/2 - Lw/2, topoffset ), L, font=font_label, fill=fill)
        draw.text((s/2 - aw/2, topoffset + spacer + Lh), a, font=font_label, fill=fill)
        draw.text((s/2 - bw/2, topoffset + spacer + Lh + spacer + ah), b, font=font_label, fill=fill)

        locw,loch = font_loc.getsize(loc.upper())
        draw.text((s/2 - locw/2, s - loch - loch - loch), loc.upper(), font=font_loc, fill=fill)

    return im

def middle_panel(collection_item,infopanel_height,bg='white'):

    mlocs = list(set([item['mloc'] for item in collection_item.color]))

    locrows = []
    for mloc in mlocs:
        mtrials = [item for item in collection_item.color if item['mloc'] == mloc]
        coloricons = []
        for mtrial in mtrials:
            label = str(round(mtrial['LAB_L'],2)) + "," + str(round(mtrial['LAB_A'],2)) + "," + str(round(mtrial['LAB_B'],2))
            _ = coloricon_single(mtrial['hex'],330,mloc,label,bg=bg)
            coloricons.append(_)
        locrow = hconcat(*coloricons,spacer=17,bg=bg)
        locrows.append(locrow)

    colorvis = vconcat(*locrows,spacer=17,bg=bg)

    """
    To find the median texture image, we need to look at the roughness values 
    for each texture trial in collection_item.texture. Whichever is closest to 
    the median is the median texture image. We then need to grab its tifpath.
    """

    if len(collection_item.texture) > 0: # if there are no texture images, collection_item.texture is an empty list
        texture_trials = deepcopy(collection_item.texture)
        
        roughness_trials = [item['roughness'] for item in texture_trials]
        roughness_trials.sort()
        median_roughness = roughness_trials[len(roughness_trials)//2]
        
        median_texture_trial = [item for item in texture_trials if item['roughness'] == median_roughness][0]
        median_texture_tifpath = median_texture_trial['tifpath']
        median_texture_image = Image.open(median_texture_tifpath)
        median_texture_image.thumbnail((1024,1024),Image.Resampling.LANCZOS)
        median_texture_image = bottom_left_text(median_texture_image,"σ = "+str(round(median_roughness,3)))

        texture_trials = [item for item in texture_trials if item['tifpath'] != median_texture_tifpath]

        if len(texture_trials) > 0:
            xspacer = 32
            thumbw = int((1024 - xspacer) / 2)

            texture_trials.sort(key=lambda x: x['roughness'])
            texture_images = [Image.open(item['tifpath']) for item in texture_trials]
            for im in texture_images:
                im.thumbnail((thumbw,thumbw),Image.Resampling.LANCZOS)
            texture_images = [bottom_left_text(item,"σ = "+str(round(texture_trials[i]['roughness'],3))) for i,item in enumerate(texture_images)]

            texture_images = hconcat(*texture_images,spacer=xspacer,bg=bg)
            texture_images = vconcat(median_texture_image,texture_images,spacer=64,bg=bg)

    else:
        texture_images = Image.new('RGB',(1024,1024),color="dimgrey")

    colorvis_texture = vconcat(colorvis,texture_images,spacer=64,bg=bg)
    top_spacer = Image.new('RGB',(texture_images.width,infopanel_height),bg)
    panel = vconcat(top_spacer,colorvis_texture,spacer=64,bg=bg)

    return panel

def right_panel(collection_item,collvals,lmlvals,bg='white'):
    
    glyph = Image.open(collection_item.glyphpath)
    matted_glyph = gmat(glyph,bg=bg)

    colltrials_bstar_base = [item['LAB_B'] for item in collection_item.color if item['mloc'] == 'base']
    colltrials_bstar_image = [item['LAB_B'] for item in collection_item.color if item['mloc'] == 'image']

    sliders = vconcat(
        slider('THICKNESS (mm)',collvals['thickness'],collection_item.thickness,lmlvals['thickness'],bg=bg,rounding_digits=None),
        slider('ROUGHNESS (σ)',collvals['roughness'],collection_item.roughness,lmlvals['roughness'],bg=bg,rounding_digits=2),
        slider('GLOSS (GU)',collvals['gloss'],collection_item.gloss,lmlvals['gloss'],bg=bg),
        slider('BASE WARMTH (b*)',collvals['bstar_base'],colltrials_bstar_base,lmlvals['bstar_base'],bg=bg),
        slider('IMAGE WARMTH (b*)',collvals['bstar_image'],colltrials_bstar_image,lmlvals['bstar_image'],bg=bg),
        spacer=64,bg=bg
    )

    matted_glyph.thumbnail((sliders.width,sliders.width),Image.Resampling.LANCZOS)
    panel = vconcat(matted_glyph,sliders,spacer=0,bg=bg)

    return panel

def item_report(collection_item,lmlvals,collvals,special_panel=None,bg='white'):

    if special_panel is not None:
        if special_panel == 'uv':
            special_panel = uv_panel(collection_item,collvals,lmlvals,bg)
        elif special_panel == 'condition':
            special_panel = condition_panel(collection_item,collvals,bg)
    
    left, infopanel_height = left_panel(collection_item,special_panel,bg)
    middle = middle_panel(collection_item,infopanel_height,bg)
    right = right_panel(collection_item,collvals,lmlvals,bg=bg)

    report = hconcat(left,middle,right,spacer=192,bg=bg)
    matted_report = mat(report,bg=bg)

    return matted_report

def bottom_left_text(im,s,fonts=fonts,fontsize=45,fill='white'):

    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(fonts['regular'],fontsize)
    w,h = font.getsize(s)

    offset = 32
    draw.text((offset,im.height-h-offset),s,fill=fill,font=font)

    return im

def vconcat(*args,spacer=64,bg='white'):
    
    canvas_width = max([i.width for i in args])
    canvas_height = sum([i.height for i in args]) + spacer*(len(args)-1)
    canvas = Image.new('RGB',(canvas_width,canvas_height),bg)

    for i,arg in enumerate(args):
        canvas.paste(arg,(0,spacer*i+sum([j.height for j in args[:i]])))
    
    return canvas

def hconcat(*args,spacer=64,bg='white'):
        
        canvas_width = sum([i.width for i in args]) + spacer*(len(args)-1)
        canvas_height = max([i.height for i in args])
        canvas = Image.new('RGB',(canvas_width,canvas_height),bg)
    
        for i,arg in enumerate(args):
            canvas.paste(arg,(spacer*i+sum([j.width for j in args[:i]]),0))
        
        return canvas

def mat(im,bg='white'):
    
    matted = Image.new('RGB',(im.width + int(im.width * 0.2), im.height + int(im.height * 0.2)),bg)
    matted.paste(im,(int(im.width * 0.1),int(im.height * 0.1)))

    return matted

def hfit(im,fitwidth,bg='white',position='center'):

    im_copy = deepcopy(im)

    if fitwidth < im_copy.width:
        # resize to fit width but keep aspect ratio
        im_copy.thumbnail((fitwidth,fitwidth/im_copy.width*im_copy.height),Image.Resampling.LANCZOS)

    if position == 'center':
        width_offset = int((fitwidth - im_copy.width) / 2)
    elif position == 'left':
        width_offset = 0
    elif position == 'right':
        width_offset = fitwidth - im_copy.width
    
    matted = Image.new('RGB',(fitwidth, im_copy.height),bg)
    matted.paste(im_copy,(width_offset,0))

    return matted

def vfit(im,fitheight,bg='white',position='center'):

        im_copy = deepcopy(im)
    
        if fitheight < im_copy.height:
            # resize to fit height but keep aspect ratio
            im_copy.thumbnail((fitheight/im_copy.height*im_copy.width,fitheight),Image.Resampling.LANCZOS)
    
        if position == 'center':
            height_offset = int((fitheight - im_copy.height) / 2)
        elif position == 'top':
            height_offset = 0
        elif position == 'bottom':
            height_offset = fitheight - im_copy.height
        
        matted = Image.new('RGB',(im_copy.width,fitheight),bg)
        matted.paste(im_copy,(0,height_offset))
    
        return matted

def gmat(im,font=font,bg='white',top='WARM',right='MATTE',bottom='ROUGH',left='THICK'):
    
    fill = "dimgrey"
    
    if im.size != (960,960):
        
        if any([im.width < 960, im.height < 960]):
            raise ValueError("Glyph must be at least 960x960 pixels")
        
        im.thumbnail((960,960),Image.Resampling.LANCZOS)
    
    gmat = Image.new('RGB',(1280,1280),bg)
    
    try:
        gmat.paste(im,(160,160),im)
    except:
        gmat.paste(im,(160,160))
    
    draw = ImageDraw.Draw(gmat)
    
    fontWidth,_ = font.getsize(top)
    draw.text((int(640-fontWidth/2),150),text=top,font=font,fill=fill)
    
    _,fontHeight = font.getsize(right)
    draw.text((1080,int(640-fontHeight/2)),text=right,font=font,fill=fill)
    
    fontWidth,_ = font.getsize(bottom)
    draw.text((int(640-fontWidth/2),1080),text=bottom,font=font,fill=fill)
    
    fontWidth,fontHeight = font.getsize(left)
    draw.text((int(200-fontWidth),int(640-fontHeight/2)),text=left,font=font,fill=fill)
    
    return gmat

def glyph_legend(side=200,bg='white'):

    fill = "dimgrey"
    
    im = Image.new('RGB', (side,side), bg)
    draw = ImageDraw.Draw(im)
    halfside = int( side / 2 )

    draw.line([(halfside,0),(halfside,side)],
              fill=fill,
              width=round(side/200))
    draw.line([(0,halfside),(side,halfside)],
              fill=fill,
              width=round(side/200))

    sSixth = side / 6;
    sThird = side / 3;
    sHalf = side / 2;
    sTwoThird = side * 2/3;
    sFiveSixth = side * 5/6;

    draw.line([(sHalf,0),(side,sHalf)],fill=fill,width=round(side/200))
    draw.line([(side,sHalf),(sHalf,side)],fill=fill,width=round(side/200))
    draw.line([(sHalf,side),(0,sHalf)],fill=fill,width=round(side/200))
    draw.line([(0,sHalf),(sHalf,0)],fill=fill,width=round(side/200))

    draw.line([(sHalf,sSixth),(sFiveSixth,sHalf)],fill=fill,width=round(side/200))
    draw.line([(sFiveSixth,sHalf),(sHalf,sFiveSixth)],fill=fill,width=round(side/200))
    draw.line([(sHalf,sFiveSixth),(sSixth,sHalf)],fill=fill,width=round(side/200))
    draw.line([(sSixth,sHalf),(sHalf,sSixth)],fill=fill,width=round(side/200))

    draw.line([(sHalf,sThird),(sTwoThird,sHalf)],fill=fill,width=round(side/200))
    draw.line([(sTwoThird,sHalf),(sHalf,sTwoThird)],fill=fill,width=round(side/200))
    draw.line([(sHalf,sTwoThird),(sThird,sHalf)],fill=fill,width=round(side/200))
    draw.line([(sThird,sHalf),(sHalf,sThird)],fill=fill,width=round(side/200))

    return gmat(mat(im))

def coloricon(base,tone,side,labels=False,fonts=fonts,bg='white'):

    font_size = int(side/16)
    font = ImageFont.truetype(fonts['regular'],font_size)
    font_thin = ImageFont.truetype(fonts['thin'],font_size)

    if bg is None:
        im = Image.new('RGBA',(side,side),bg)
    else:
        im = Image.new('RGB',(side,side),bg)
    
    draw = ImageDraw.Draw(im)
    
    draw.rounded_rectangle(
        [(side/16,side/16),(side - side/16, side - side/16)],radius=int(side*0.15625),fill=base
    )
   
    draw.rounded_rectangle(
        [(side/2 - side/4, side/2 - side/4), (side/2 + side/4, side/2 + side/4)],radius=int(side*0.15625),fill=tone
    )

    if labels:
        top = "SPECTROPHOTOMETER"
        top_width = font_thin.getsize(top)[0]
        draw.text((side/2 - top_width/2, font_size), top, font=font_thin, fill="black")

        DMIN = "BASE"
        DMIN_width,DMIN_height = font.getsize(DMIN)
        draw.text((side/2 - DMIN_width/2, side - DMIN_height - font_size), DMIN, font=font, fill="black")

        DMAX = "TONE"
        DMAX_width,DMAX_height = font.getsize(DMAX)
        draw.text((side/2 - DMAX_width/2, side/2 - DMAX_height/2), DMAX, font=font, fill="white")
    
    return im

def get_text_size(font, text):
    if text:
        return font.getsize(text)
    else:
        return (0, 0)

def draw_text(draw, pos, text, font, fill):
    if text:
        draw.text(pos, text=text, font=font, fill=fill)

def textline(s,fonts=fonts,fonttype='regular',fontsize=90,bg='white'):
    
    fill = "dimgrey"
    
    font = ImageFont.truetype(fonts[fonttype],fontsize)
    w,h = font.getsize(s)
    
    canvas = Image.new('RGB',(w,h),bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.text((0,0),text=s,font=font,fill=fill)
    
    return canvas

def draw_outline(im,width,linecolor):
        
        draw = ImageDraw.Draw(im)
        draw.rectangle([(0,0),(im.width-1,im.height-1)],outline=linecolor,width=width)
        
        return im

# def block_text(s,fonts=fonts,fontsize=36,width=70,bg='white'):

#     swrapped = textwrap.fill(s,width=width)
    
#     fill = "dimgrey"

#     font = ImageFont.truetype(fonts['serif'],fontsize)
        
#     blockWidth,blockHeight = font.getsize_multiline(swrapped)
#     vincr = int(blockHeight * 0.1)
#     canvas = Image.new('RGB',(blockWidth,blockHeight + vincr),bg)
#     draw = ImageDraw.Draw(canvas)
#     draw.multiline_text((0,0), swrapped, font=font, fill=fill)
    
#     return canvas