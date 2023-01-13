from PIL import Image,ImageDraw,ImageFont
import os
import textwrap

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
font_serif = ImageFont.truetype(fonts['serif'],30)

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

def slider_panel(*args):
    
    n = len(args)
    metacanvas = Image.new('RGB',(1000,n*200))
    
    for i,arg in enumerate(args):
        metacanvas.paste(arg,(0,i*200))
    
    return metacanvas

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
    gmat.paste(im,(160,160),im)
    
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
    
    canvas = Image.new('RGB',(fontWidthIdx*2+fontWidthTitle,fontHeightIdx),bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.text((0,0),text=idx,font=font_large,fill=fill)
    draw.text((fontWidthIdx + int(fontWidthIdx/4),fontHeightIdx-fontHeightTitle),text=title,font=font,fill=fill)
    
    return canvas

def item_report(df,i,glyphcol,pcol,xcol,tcol,gcol,wcol,rcol,idx_title,idx_subtitle,theme='light'):
    
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
    
    t,g,c,r = df[tcol].loc[i],round(df[gcol].loc[i]),round(df[wcol].loc[i]),round(df[rcol].loc[i],1)
    
    sliders = slider_panel(slider('THICKNESS (mm)',t,tmin,tmax,font,theme=theme),
                           slider('GLOSS (GU)',g,gmin,gmax,font,theme=theme),
                           slider('WARMTH (b*)',c,cmin,cmax,font,theme=theme),
                           slider('ROUGHNESS (σ)',r,rmin,rmax,font,theme=theme))
    
    matted_glyph = gmat(glyph,theme=theme)
    matted_glyph.thumbnail((sliders.width,sliders.width),Image.Resampling.LANCZOS)
    
    glyph_and_sliders = Image.new('RGB',(matted_glyph.width,matted_glyph.height+sliders.height),bg)
    
    glyph_and_sliders.paste(matted_glyph,(0,0))
    glyph_and_sliders.paste(sliders,(0,matted_glyph.height))
    
    print_image = Image.open(df[pcol].loc[i])
    texture_image = Image.open(df[xcol].loc[i])
    
    print_image.thumbnail((1024,1024),Image.Resampling.LANCZOS)
    texture_image.thumbnail((1024,1024),Image.Resampling.LANCZOS)
    
    images = Image.new('RGB',(1024,print_image.height+texture_image.height+64),bg)
    
    images.paste(print_image,(0,0))
    images.paste(texture_image,(0,print_image.height+64))
    
    infopanel = info_panel(idx_title,idx_subtitle)
    infopanel.thumbnail((1024,1024),Image.Resampling.LANCZOS)
    
    images_and_infopanel = Image.new('RGB',(1024,images.height+infopanel.height+64),bg)
    images_and_infopanel.paste(infopanel,(0,0))
    images_and_infopanel.paste(images,(0,infopanel.height+64))
    
    report = Image.new('RGB',
                       (images_and_infopanel.width+glyph_and_sliders.width+128,
                       (max(images_and_infopanel.height,glyph_and_sliders.height))),
                       bg)
    
    report.paste(images_and_infopanel,(0,0))
    report.paste(glyph_and_sliders,(images_and_infopanel.width+128,0))
    
    matted_report = mat(report)
    
    return matted_report

def heading_text_image(hdg,txt,im,theme='light'):
    
    if theme=='light':
        bg = "white"
    elif theme=='dark':
        bg = "#212121"
        
    canvas = Image.new('RGB',(max(hdg.width,txt.width,im.width),
                              hdg.height+txt.height+hdg.height+im.height+hdg.height),bg)
    
    canvas.paste(hdg,(0,0))
    canvas.paste(txt,(0,hdg.height+hdg.height))
    canvas.paste(im,(0,hdg.height+hdg.height+txt.height+hdg.height))
    
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




