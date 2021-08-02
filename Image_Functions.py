import random

from PIL import Image


def image_palette_les(pfp):
    pal_img = Image.new('P', (25, 25))
    palette = [212, 44, 0, 162, 1, 97, 209, 97, 162, 253, 152, 85, 255, 255, 255] * 51
    for i in range(3):
        palette.append(255)
    pal_img.putpalette(palette)
    pfp = pfp.convert('RGB')
    pfp = pfp.quantize(palette=pal_img)
    return pfp


def image_palette_gay(pfp):
    pal_img = Image.new('P', (36, 36))
    palette = [255, 0, 0, 253, 140, 0, 255, 229, 0, 17, 159, 11, 6, 68, 179, 194, 46, 220] * 42
    for i in range(12):
        num = [255, 0][random.randint(0, 1)]
        palette.append(num)
    pal_img.putpalette(palette)
    pfp = pfp.convert('RGB')
    pfp = pfp.quantize(palette=pal_img)
    return pfp


def image_palette_bi(pfp):
    pal_img = Image.new('P', (36, 36))
    palette = [214, 2, 112, 155, 79, 151, 0, 56, 167] * 85
    for i in range(3):
        palette.append(255)
    pal_img.putpalette(palette)
    pfp = pfp.convert('RGB')
    pfp = pfp.quantize(palette=pal_img)
    return pfp


def transparent_layered_image_mask(trans_img, pfp, mask, quords):
    mask = mask.convert('L')
    img = Image.new('RGBA', trans_img.size)
    img.paste(pfp, quords)
    img.paste(trans_img, (0, 0), trans_img)
    img = Image.composite(img, trans_img, mask)
    return img
