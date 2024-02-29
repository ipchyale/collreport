from PIL import Image,ImageDraw,ImageFont
import os
#import textwrap
import numpy as np
from copy import deepcopy

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

def vconcat(*args,spacer=64,bg='white',rgba=False):
        
    canvas_width = max([i.width for i in args])
    canvas_height = sum([i.height for i in args]) + spacer*(len(args)-1)
    
    if rgba:
        canvas = Image.new('RGBA',(canvas_width,canvas_height),bg)
    else:
        canvas = Image.new('RGB',(canvas_width,canvas_height),bg)

    for i,arg in enumerate(args):
        if rgba:
            canvas.paste(arg,(0,spacer*i+sum([j.height for j in args[:i]])),arg)
        else:
            canvas.paste(arg,(0,spacer*i+sum([j.height for j in args[:i]])))
    
    return canvas

def hconcat(*args,spacer=64,bg='white',rgba=False):
        
        canvas_width = sum([i.width for i in args]) + spacer*(len(args)-1)
        canvas_height = max([i.height for i in args])
        
        if rgba:
            canvas = Image.new('RGBA',(canvas_width,canvas_height),bg)
        else:
            canvas = Image.new('RGB',(canvas_width,canvas_height),bg)
    
        for i,arg in enumerate(args):
            if rgba:
                canvas.paste(arg,(spacer*i+sum([j.width for j in args[:i]]),0),arg)
            else:
                canvas.paste(arg,(spacer*i+sum([j.width for j in args[:i]]),0))
        
        return canvas

def mat(im,bg='white',return_margin=False):
    
    matted = Image.new('RGB',(im.width + int(im.width * 0.2), im.height + int(im.width * 0.2)),bg)
    matted.paste(im,(int(im.width * 0.1),int(im.width * 0.1)))

    if return_margin:
        return matted, int(im.width * 0.1)
    else:
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

def get_text_size(font, text):
    if text:
        return font.getsize(text)
    else:
        return (0, 0)

def draw_text(draw, pos, text, font, fill):
    try:
        draw.text(pos, text=text, font=font, fill=fill)
    except Exception as e:
        print(f"Error drawing text: {e}")

def bottom_left_text(im,s,fonts=fonts,fontsize=45,fill='white'):

    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(fonts['regular'],fontsize)
    w,h = font.getsize(s)

    offset = 32
    draw.text((offset,im.height-h-offset),s,fill=fill,font=font)

    return im

def textline(s,fonts=fonts,fonttype='regular',fontsize=90,bg='white',fill = "dimgrey"):
    
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

def gmat(im,font=font,bg='white',top='WARM',right='MATTE',bottom='ROUGH',left='THICK',rgba=False):
    
    fill = "dimgrey"
    
    if im.size != (960,960):
        
        if any([im.width < 960, im.height < 960]):
            raise ValueError("Glyph must be at least 960x960 pixels")
        
        im.thumbnail((960,960),Image.Resampling.LANCZOS)
    
    if rgba:
        gmat = Image.new('RGBA',(1280,1280),bg)
    else:
        gmat = Image.new('RGB',(1280,1280),bg)
    
    if rgba:
        gmat.paste(im,(160,160),im)
    else:
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