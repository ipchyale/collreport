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

def slider_pos(val,vmin,vrange,slider_width):
    pct = (val - vmin) / vrange
    pos = int(pct * (slider_width - slider_width * 0.2) + slider_width * 0.1)

    return pos

def slider(title,val,vmin,vmax,allvals,mtrials,font=font,theme='light',rounding_digits=0):
    
    if theme=='light':
        bg = "white"
    elif theme=='dark':
        bg = "#212121"
        
    fill = "grey"
    
    canvas = Image.new('RGB',(1000,200),bg)
    slider_width,slider_height = canvas.size
    draw = ImageDraw.Draw(canvas)
    
    draw.line([(int(slider_width*0.1),int(slider_height*0.5)),(int(slider_width*0.9),int(slider_height*0.5))],width=int(slider_width/125),fill=fill)

    vrange = vmax - vmin

    # distribution ticks
    tick_height = slider_height / 8
    for allval in allvals:
        pos = slider_pos(allval,vmin,vrange,slider_width)
        draw.line([(pos,int(slider_height*0.5-tick_height/2)),(pos,int(slider_height*0.5+tick_height/2))],width=int(slider_width/1000),fill=fill)
    
    # median peg should sit atop the distribution ticks
    try:
        peg = slider_pos(val,vmin,vrange,slider_width)
        draw.rounded_rectangle([(peg-15,70),(peg+15,130)],radius=5,fill=bg,outline=fill,width=4)
    except:
        pass

    # trial ticks
    if "ROUGH" in title:
        try:
            mtrials = [item[1] for item in mtrials] # this iteration, passed to `slider()`, was failing when allvals_i.textures was empty
        except:
            mtrials = None

    if mtrials is not None:
        for k,mtrial in enumerate(mtrials):
            pos = slider_pos(mtrial,vmin,vrange,slider_width)
            top_offset = 8
            peg_top = 70
            trial_spacer = 8
            draw.line([(pos-15,peg_top - top_offset - trial_spacer * k),(pos+15,peg_top - top_offset - trial_spacer * k)],width=4,fill=fill)
    
    if rounding_digits is not None:
        if rounding_digits==0:
            vmin = round(vmin) # returns int
            vmax = round(vmax) # returns int
        else:
            vmin = round(vmin,rounding_digits)
            vmax = round(vmax,rounding_digits)
        
    draw.text((int(slider_width*0.1),int(slider_height*0.75)),text=str(vmin),font=font,fill=fill)
    
    vmaxWidth,_ = font.getsize(str(vmax))
    draw.text((int(slider_width*0.9)-vmaxWidth,int(slider_height*0.75)),text=str(vmax),font=font,fill=fill)
    
    titleWidth,_ = font.getsize(title)
    draw.text((int(slider_width/2-titleWidth/2),int(slider_height*0.75)),text=title,font=font,fill=fill)
    
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

def tombstone(tombstone_dict,fonts=fonts,theme='light'):
    
    if theme=='light':
        bg = "white"
    elif theme=='dark':
        bg = "#212121"
    
    fill = "grey"

    """
    [artist] <- bold, biggest
    [nationality][active]

    [worktitle][year] <- italic, bigger and normal, bigger

    [medium]
    [dims]
    [credit]
    """

    artist = tombstone_dict.get('artist')
    nationality = tombstone_dict.get('nationality')
    active = tombstone_dict.get('active')
    worktitle = tombstone_dict.get('worktitle')
    year = tombstone_dict.get('year')
    medium = tombstone_dict.get('medium')
    dims = tombstone_dict.get('dims')
    credit = tombstone_dict.get('credit')

    font = ImageFont.truetype(fonts['regular'],30)
    font_artist = ImageFont.truetype(fonts['bold'],45)
    font_worktitle = ImageFont.truetype(fonts['regular-i'],30)

    fontWidthArtist,fontHeightArtist = font_artist.getsize(artist)
    fontWidthWorktitle,fontHeightWorktitle = font_worktitle.getsize(worktitle)
    fontWidthNationality,fontHeightNationality = font.getsize(nationality)
    fontWidthActive,fontHeightActive = font.getsize(active)
    fontWidthYear,fontHeightYear = font.getsize(year)
    fontWidthMedium,fontHeightMedium = font.getsize(medium)
    fontWidthDims,fontHeightDims = font.getsize(dims)
    fontWidthCredit,fontHeightCredit = font.getsize(credit)

    line_spacer = 16
    section_spacer = 32

    tombstoneWidth = max([fontWidthArtist,fontWidthNationality+line_spacer+fontWidthActive,fontWidthWorktitle+line_spacer+fontWidthYear,fontWidthMedium,fontWidthDims,fontWidthCredit])
    tombstoneHeight = fontHeightArtist + line_spacer + max([fontHeightNationality,fontHeightActive]) + section_spacer * 2 + max([fontHeightWorktitle,fontHeightYear]) + section_spacer + fontHeightMedium + line_spacer + fontHeightDims + line_spacer + fontHeightCredit
    tombstone_text = Image.new('RGB',(tombstoneWidth,tombstoneHeight),bg)

    draw = ImageDraw.Draw(tombstone_text)
    draw.text((0,0),text=artist,font=font_artist,fill=fill)
    draw.text((0,fontHeightArtist+line_spacer),text=nationality,font=font,fill=fill)
    draw.text((fontWidthNationality+line_spacer,fontHeightArtist+line_spacer),text=active,font=font,fill=fill)
    draw.text((0,fontHeightArtist+line_spacer+max([fontHeightNationality,fontHeightActive])+section_spacer*2),text=worktitle,font=font_worktitle,fill=fill)
    draw.text((fontWidthWorktitle+line_spacer,fontHeightArtist+line_spacer+max([fontHeightNationality,fontHeightActive])+section_spacer*2),text=year,font=font,fill=fill)
    draw.text((0,fontHeightArtist+line_spacer+max([fontHeightNationality,fontHeightActive])+section_spacer*2+max([fontHeightWorktitle,fontHeightYear])+section_spacer),text=medium,font=font,fill=fill)
    draw.text((0,fontHeightArtist+line_spacer+max([fontHeightNationality,fontHeightActive])+section_spacer*2+max([fontHeightWorktitle,fontHeightYear])+section_spacer+fontHeightMedium+line_spacer),text=dims,font=font,fill=fill)
    draw.text((0,fontHeightArtist+line_spacer+max([fontHeightNationality,fontHeightActive])+section_spacer*2+max([fontHeightWorktitle,fontHeightYear])+section_spacer+fontHeightMedium+line_spacer+fontHeightDims+line_spacer),text=credit,font=font,fill=fill)

    return tombstone_text

def draw_outline(im,width,linecolor):
        
        draw = ImageDraw.Draw(im)
        draw.rectangle([(0,0),(im.width-1,im.height-1)],outline=linecolor,width=width)
        
        return im

def item_report(df,i,glyphcol,pcol,xcol,tcol,gcol,wcol,rcol,tonecol,contrastcol,discolorcol,mapcol,acc,subacc,tombstone_dict,allvals,theme='light'):
    
    if theme=='light':
        bg = "white"
    elif theme=='dark':
        bg = "#212121"
        
    glyph = Image.open(df[glyphcol].loc[i])
    
    fademax = 100 - df[contrastcol].min()*100
    fademin = 100 - df[contrastcol].max()*100
    nonnull_fade_vals = [100 - item * 100 for item in df[contrastcol][df[contrastcol].notnull()]]

    discolormin = df[discolorcol].min()*100
    discolormax = df[discolorcol].max()*100
    nonnull_discolor_vals = df[discolorcol][df[discolorcol].notnull()] * 100

    """
    `allvals` cols:
        accplate,
        thicknessvals,
        glossvals,
        bstars_base,
        bstars_tone,
        rgbhex_base,
        rgbhex_tone,
        label_base,
        label_tone,
        texturevals
    """

    thicknessvals_flattened = [item for sublist in allvals.thicknessvals[allvals.thicknessvals.notnull()] for item in sublist]
    tmin = min(thicknessvals_flattened)
    tmax = max(thicknessvals_flattened)
    
    glossvals_flattened = [item for sublist in allvals.glossvals[allvals.glossvals.notnull()] for item in sublist]
    gmin = min(glossvals_flattened)
    gmax = max(glossvals_flattened)
    
    bstars_base_flattened = [item for sublist in allvals.bstars_base[allvals.bstars_base.notnull()] for item in sublist]
    cmin = min(bstars_base_flattened)
    cmax = max(bstars_base_flattened)
    
    bstars_tone_flattened = [item for sublist in allvals.bstars_tone[allvals.bstars_tone.notnull()] for item in sublist]
    tonemin = min(bstars_tone_flattened)
    tonemax = max(bstars_tone_flattened)

    texture_pairs = allvals.texturevals[allvals.texturevals.notnull()]
    texture_lists = [[float(i[1]) for i in item] for item in texture_pairs]
    texturevals_flattened = [item for sublist in texture_lists for item in sublist]
    rmin = min(texturevals_flattened)
    rmax = max(texturevals_flattened)

    accplate = df.accplate.loc[i]
    allvals_i = allvals[allvals.accplate==accplate].iloc[0]

    # medians for slider pegs    
    t = df[tcol].loc[i]
    g = df[gcol].loc[i]
    c = df[wcol].loc[i]
    r = df[rcol].loc[i]
    tn = df[tonecol].loc[i]
    fdg = 100 - df[contrastcol].loc[i]*100
    dsc = df[discolorcol].loc[i]*100

    sliders = vconcat(slider('THICKNESS (mm)',t,tmin,tmax,thicknessvals_flattened,allvals_i.thicknessvals,font,theme=theme,rounding_digits=None),
                      slider('ROUGHNESS (σ)',r,rmin,rmax,texturevals_flattened,allvals_i.texturevals,font,theme=theme,rounding_digits=2),
                      slider('GLOSS (GU)',g,gmin,gmax,glossvals_flattened,allvals_i.glossvals,font,theme=theme),
                      slider('BASE WARMTH (b*)',c,cmin,cmax,bstars_base_flattened,allvals_i.bstars_base,font,theme=theme),
                      slider('TONE WARMTH (b*)',tn,tonemin,tonemax,bstars_tone_flattened,allvals_i.bstars_tone,font,theme=theme),
                      spacer=64,theme=theme)
    
    matted_glyph = gmat(glyph,theme=theme)
    matted_glyph.thumbnail((sliders.width,sliders.width),Image.Resampling.LANCZOS)

    glyph_and_sliders = vconcat(matted_glyph,sliders,spacer=0,theme=theme)

    contrast_map = Image.open(df[mapcol].loc[i])
    contrast_map = draw_outline(contrast_map,1,'black')
    contrast_map = wfit(contrast_map,glyph_and_sliders.width,theme=theme)

    contrast = vconcat(contrast_map,
                       slider('FADING (%)',fdg,fademin,fademax,nonnull_fade_vals,None,font,theme=theme),
                       slider('DISCOLORATION (%)',dsc,discolormin,discolormax,nonnull_discolor_vals,None,font,theme=theme),
                       spacer=64,theme=theme)
    
    print_image = Image.open(df[pcol].loc[i])
    print_image = draw_outline(print_image,1,'black')
    print_image.thumbnail((1024,1024),Image.Resampling.LANCZOS)

    median_texture_path = df[xcol].loc[i]
    
    try:
        median_texture_image = Image.open(median_texture_path)
        median_texture_image.thumbnail((1024,1024),Image.Resampling.LANCZOS)
        median_texture_image = bottom_left_text(median_texture_image,"σ = "+str(round(r,3)),fonts=fonts)
    except:
        median_texture_image = Image.new('RGB',(1024,1024),"#dcdcdc")

    xspacer = 32
    thumbw = int((1024 - xspacer) / 2)
    
    try:
        additional_texture_images = [Image.open(path) for path,_ in allvals_i.texturevals if path!=median_texture_path]
        if len(additional_texture_images) > 0:
            for im in additional_texture_images:
                im.thumbnail((thumbw,thumbw),Image.Resampling.LANCZOS)
            additional_texture_vals = [str(round(textureval,3)) for path,textureval in allvals_i.texturevals if path!=median_texture_path]
            additional_texture_images = [bottom_left_text(im,"σ = "+textureval,fonts=fonts) for im,textureval in zip(additional_texture_images,additional_texture_vals)]
        else:
            additional_texture_images = [Image.new('RGB',(thumbw,thumbw),"#dcdcdc") for _ in range(2)]
    except:
        additional_texture_images = [Image.new('RGB',(thumbw,thumbw),"#dcdcdc") for _ in range(2)]
    
    additional_texture_images = hconcat(*additional_texture_images,spacer=xspacer,theme=theme)
    texture_images = vconcat(median_texture_image,additional_texture_images,spacer=64,theme=theme)

    hexes_base = allvals_i.rgbhex_base
    hexes_tone = allvals_i.rgbhex_tone
    labels_base = allvals_i.label_base
    labels_tone = allvals_i.label_tone

    bases = hconcat(*[coloricon_single(hexes_base[j],330,'base',labels_base[j]) for j in range(len(hexes_base))],spacer=17,theme=theme)
    tones = hconcat(*[coloricon_single(hexes_tone[j],330,'tone',labels_tone[j]) for j in range(len(hexes_tone))],spacer=17,theme=theme)
    colorvis = vconcat(bases,tones,spacer=17,theme=theme)

    tombstone_text = tombstone(tombstone_dict)
    
    infopanel = info_panel(acc,subacc)
    #infopanel.thumbnail((48/infopanel.height*infopanel.width,48),Image.Resampling.LANCZOS)
    
    infopanel_print_tombstone = vconcat(infopanel,print_image,tombstone_text,spacer=64,theme=theme)
    infopanel_print_tombstone_contrast = vconcat(infopanel_print_tombstone,contrast,spacer=192,theme=theme)

    colorvis_texture = vconcat(colorvis,texture_images,spacer=64,theme=theme)
    top_spacer = Image.new('RGB',(texture_images.width,infopanel.height),bg)
    spacer_colorvis_texture = vconcat(top_spacer,colorvis_texture,spacer=64,theme=theme)
    
    report = hconcat(infopanel_print_tombstone_contrast,spacer_colorvis_texture,glyph_and_sliders,spacer=192,theme=theme)
    
    matted_report = mat(report)
    
    return matted_report

def bottom_left_text(im,s,fonts=fonts,fontsize=45,fill='white'):

    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(fonts['regular'],fontsize)
    w,h = font.getsize(s)

    offset = 32
    draw.text((offset,im.height-h-offset),s,fill=fill,font=font)

    return im

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

def block_text(s,fonts=fonts,fontsize=36,width=70,theme='light'):

    swrapped = textwrap.fill(s,width=width)
    
    if theme=='light':
        bg = "white"
        fill = "#212121"
    elif theme=='dark':
        bg = "#212121"
        fill = "grey"

    font = ImageFont.truetype(fonts['serif'],fontsize)
        
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

def wfit(im,fitwidth,theme='light',position='center'):

    if theme=='light':
        bg = "white"
    elif theme=='dark':
        bg = "#212121"

    if fitwidth < im.width:
        im.thumbnail((fitwidth,fitwidth),Image.Resampling.LANCZOS)

    if position == 'center':
        width_offset = int((fitwidth - im.width) / 2)
    elif position == 'left':
        width_offset = 0
    elif position == 'right':
        width_offset = fitwidth - im.width
    
    matted = Image.new('RGB',(fitwidth, im.height),bg)
    matted.paste(im,(width_offset,0))

    return matted

def hfit(im,fitheight,theme='light',position='center'):
        
        if theme=='light':
            bg = "white"
        elif theme=='dark':
            bg = "#212121"
    
        if fitheight < im.height:
            im.thumbnail((fitheight,fitheight),Image.Resampling.LANCZOS)
    
        if position == 'center':
            height_offset = int((fitheight - im.height) / 2)
        elif position == 'top':
            height_offset = 0
        elif position == 'bottom':
            height_offset = fitheight - im.height
        
        matted = Image.new('RGB',(im.width,fitheight),bg)
        matted.paste(im,(0,height_offset))
    
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

def coloricon_single(c,s,loc,label=None,fonts=fonts,theme='light'):

    if theme=='light':
        bg = "white"
    elif theme=='dark':
        bg = "#212121"

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
        elif loc=='tone':
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

def toc(d,width,fonts=fonts,theme='light'):

    font_size = int(width/32)
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

def textline(s,fonts=fonts,fonttype='regular',fontsize=90,theme='light'):
    
    if theme=='light':
        bg = "white"
    elif theme=='dark':
        bg = "#212121"
    
    fill = "grey"
    
    font = ImageFont.truetype(fonts[fonttype],fontsize)
    w,h = font.getsize(s)
    
    canvas = Image.new('RGB',(w,h),bg)
    draw = ImageDraw.Draw(canvas)
    
    draw.text((0,0),text=s,font=font,fill=fill)
    
    return canvas






