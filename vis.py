from PIL import Image,ImageDraw,ImageFont
import os
import textwrap
import numpy as np

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

def slider(title,val,vmin,vmax,font=font,theme='light'):
    
    if theme=='light':
        bg = "white"
    elif theme=='dark':
        bg = "#212121"
        
    fill = "grey"
    
    canvas = Image.new('RGB',(1000,200),bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.line([(100,100),(900,100)],width=8,fill=fill)
    
    vrange = vmax - vmin
    pct = (val - vmin) / vrange
    pos = int(pct * 800) + 100
    
    draw.rounded_rectangle([(pos-15,70),(pos+15,130)],radius=5,fill=bg,outline=fill,width=4)
    
    draw.text((100,150),text=str(vmin),font=font,fill=fill)
    
    vmaxWidth,_ = font.getsize(str(vmax))
    draw.text((900-vmaxWidth,150),text=str(vmax),font=font,fill=fill)
    
    titleWidth,_ = font.getsize(title)
    draw.text((int(500-titleWidth/2),150),text=title,font=font,fill=fill)
    
    return canvas

def gmat(im,font=font,theme='light',top='WARM',right='MATTE',bottom='ROUGH',left='THICK'):

    if theme=='light':
        bg = "white"
    elif theme=='dark':
        bg = "#212121"
    
    fill = "grey"
    
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

def info_panel(idx,title,font=font,font_large=font_large,theme='light'):
    
    if theme=='light':
        bg = "white"
    elif theme=='dark':
        bg = "#212121"
    
    fill = "grey"
    
    fontWidthIdx,fontHeightIdx = font_large.getsize(idx)
    fontWidthTitle,fontHeightTitle = font.getsize(title)

    spacer = font_large.getsize("M")[0] # M is the widest character in a font, usually
    panelWidth = fontWidthIdx + fontWidthTitle + spacer
    
    canvas = Image.new('RGB',(panelWidth,fontHeightIdx),bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.text((0,0),text=idx,font=font_large,fill=fill)
    draw.text((fontWidthIdx+spacer,fontHeightIdx-fontHeightTitle),text=title,font=font,fill=fill)
    
    return canvas

def draw_outline(im,width,linecolor):
        
        draw = ImageDraw.Draw(im)
        draw.rectangle([(0,0),(im.width-1,im.height-1)],outline=linecolor,width=width)
        
        return im

def item_report(df,i,glyphcol,pcol,xcol,tcol,gcol,wcol,rcol,tonecol,contrastcol,mapcol,dminhexcol,dmaxhexcol,idx_title,idx_subtitle,theme='light'):
    
    if theme=='light':
        bg = "white"
    elif theme=='dark':
        bg = "#212121"
        
    glyph = Image.open(df[glyphcol].loc[i])
    
    tmin = df[tcol].min()
    tmax = df[tcol].max()
    gmin = round(df[gcol].min())
    gmax = round(df[gcol].max())
    cmin = round(df[wcol].min())
    cmax = round(df[wcol].max())
    rmin = round(df[rcol].min(),1)
    rmax = round(df[rcol].max(),1)
    tonemin = round(df[tonecol].min())
    tonemax = round(df[tonecol].max())
    contrastmin = round(df[contrastcol].min()*100)
    contrastmax = round(df[contrastcol].max()*100)
    
    t,g,c,r,tn,ctrst = df[tcol].loc[i],round(df[gcol].loc[i]),round(df[wcol].loc[i]),round(df[rcol].loc[i],1),round(df[tonecol].loc[i]),round(df[contrastcol].loc[i]*100)
    
    sliders = vconcat(slider('THICKNESS (mm)',t,tmin,tmax,font,theme=theme),
                           slider('GLOSS (GU)',g,gmin,gmax,font,theme=theme),
                           slider('BASE WARMTH (b*)',c,cmin,cmax,font,theme=theme),
                           slider('ROUGHNESS (σ)',r,rmin,rmax,font,theme=theme),
                           slider('TONE WARMTH (b*)',tn,tonemin,tonemax,font,theme=theme),
                           slider('CONTRAST (%)',ctrst,contrastmin,contrastmax,font,theme=theme),
                           spacer=0)
    
    matted_glyph = gmat(glyph,theme=theme)
    matted_glyph.thumbnail((sliders.width,sliders.width),Image.Resampling.LANCZOS)
    
    glyph_and_sliders = vconcat(matted_glyph,sliders,spacer=0)
    
    print_image = Image.open(df[pcol].loc[i])
    print_image = draw_outline(print_image,1,'black')

    texture_image = Image.open(df[xcol].loc[i])
    
    print_image.thumbnail((1024,1024),Image.Resampling.LANCZOS)
    texture_image.thumbnail((1024,1024),Image.Resampling.LANCZOS)

    contrast_map = Image.open(df[mapcol].loc[i])
    contrast_map = draw_outline(contrast_map,1,'black')
    
    dminhex = df[dminhexcol].loc[i]
    dmaxhex = df[dmaxhexcol].loc[i]
    cicon = coloricon(dminhex,dmaxhex,s=480)
    cicon = draw_outline(cicon,1,'black')

    color_vis = hconcat(cicon,contrast_map,spacer=32)
    
    images = vconcat(print_image,texture_image,color_vis,spacer=64)
    
    infopanel = info_panel(idx_title,idx_subtitle)
    infopanel.thumbnail((48/infopanel.height*infopanel.width,48),Image.Resampling.LANCZOS)
    
    infopanel_and_images = vconcat(infopanel,images,spacer=64)
    
    report = hconcat(infopanel_and_images,glyph_and_sliders,spacer=128)
    
    matted_report = mat(report)
    
    return matted_report

def vconcat(*args,spacer=64,theme='light'):
    
    if theme=='light':
        bg = "white"
    elif theme=='dark':
        bg = "#212121"

    canvas_width = max([i.width for i in args])
    canvas_height = sum([i.height for i in args]) + spacer*(len(args)-1)
    canvas = Image.new('RGB',(canvas_width,canvas_height),bg)

    for i,arg in enumerate(args):
        canvas.paste(arg,(0,spacer*i+sum([j.height for j in args[:i]])))
    
    return canvas

def hconcat(*args,spacer=64,theme='light'):
        
        if theme=='light':
            bg = "white"
        elif theme=='dark':
            bg = "#212121"
    
        canvas_width = sum([i.width for i in args]) + spacer*(len(args)-1)
        canvas_height = max([i.height for i in args])
        canvas = Image.new('RGB',(canvas_width,canvas_height),bg)
    
        for i,arg in enumerate(args):
            canvas.paste(arg,(spacer*i+sum([j.width for j in args[:i]]),0))
        
        return canvas

def block_text(s,font=font_serif,width=70,theme='light'):

    swrapped = textwrap.fill(s,width=width)
    
    if theme=='light':
        bg = "white"
        fill = "#212121"
    elif theme=='dark':
        bg = "#212121"
        fill = "grey"
        
    blockWidth,blockHeight = font.getsize_multiline(swrapped)
    vincr = int(blockHeight * 0.1)
    canvas = Image.new('RGB',(blockWidth,blockHeight + vincr),bg)
    draw = ImageDraw.Draw(canvas)
    draw.multiline_text((0,0), swrapped, font=font, fill=fill)
    
    return canvas

def mat(im,theme='light'):

    if theme=='light':
        bg = "white"
    elif theme=='dark':
        bg = "#212121"
    
    matted = Image.new('RGB',(im.width + int(im.width * 0.2), im.height + int(im.height * 0.2)),bg)
    matted.paste(im,(int(im.width * 0.1),int(im.height * 0.1)))

    return matted

def glyph_legend(side=200,theme='light'):

    if theme=='light':
        bg = "white"
    elif theme=='dark':
        bg = "#212121"
    
    fill = "grey"
    
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

def coloricon(base,tone,s,labels=True,fonts=fonts):

    font_size = int(s/16)
    font = ImageFont.truetype(fonts['thin'],font_size)

    im = Image.new('RGB',(s,s),base)
    draw = ImageDraw.Draw(im)
    draw.rounded_rectangle(
        [(s/2 - s/4, s/2 - s/4), (s/2 + s/4, s/2 + s/4)],radius=int(s*0.15625),fill=tone
    )

    if labels:
        top = "SPECTROPHOTOMETER"
        top_width = font.getsize(top)[0]
        draw.text((s/2 - top_width/2, font_size), top, font=font, fill="black")

        DMIN = "DMIN"
        DMIN_width,DMIN_height = font.getsize(DMIN)
        draw.text((s/2 - DMIN_width/2, s - DMIN_height - font_size), DMIN, font=font, fill="black")

        DMAX = "DMAX"
        DMAX_width,DMAX_height = font.getsize(DMAX)
        draw.text((s/2 - DMAX_width/2, s/2 - DMAX_height/2), DMAX, font=font, fill="white")
    
    return im

def table_of_contents(d,width,fonts=fonts,theme='light'):

    font_size = int(width/64)
    font = ImageFont.truetype(fonts['thin'],font_size)
    
    if theme=='light':
        bg = "white"
        fill = "#212121"
    elif theme=='dark':
        bg = "#212121"
        fill = "grey"
        
    toclines = []    
    for k in d.keys():
        ndots = 1
        while font.getsize(k.upper() + '.' * ndots + str(d[k]))[0] < width:
            ndots+=1
        ndots-=1
        s = k.upper() + '.' * ndots + str(d[k])
        height = font.getsize(s)[1]
        tocline = Image.new('RGB',(width,height),bg)
        draw = ImageDraw.Draw(tocline)
        draw.text((0,0),text=s,font=font,fill=fill)
        toclines.append(tocline)
        
    return vconcat(*toclines,spacer=int(width/64))




