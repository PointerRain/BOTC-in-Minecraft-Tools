import os

from PIL import Image
from colorsys import rgb_to_hsv, hsv_to_rgb

def rgb2hsv(r, g, b):
    """
    Converts from RGB255 to unit HSV.
    """
    return rgb_to_hsv(r/255, g/255, b/255)

def hsv2rgb(h, s, v):
    """
    Converts from unit HSV to RGB255.
    """
    return [round(i*255) for i in hsv_to_rgb(h, s, v)]

def map_colours(v, v1, v2, c1, c2):
    """
    Maps a value from one range to another.
    """
    p = (v - v1) / (v2 - v1)
    return lerp_tuple(c1, c2, p)

def lerp_tuple(c1, c2, p):
    return tuple(round(c1[i] + p * (c2[i] - c1[i])) for i in range(len(c1)))

bord = Image.open('border.png').convert('RGBA')
border = bord.load()

for filename in os.listdir('icons'):
    if not filename.endswith('.png'):
        continue
    print(filename)

    img = Image.open(f'icons/{filename}').convert('RGBA')
    width, height = img.size
    image = img.load()

    tf = Image.open(f'base.png').convert('RGBA')
    townsfolk = tf.load()

    ou = Image.open(f'base.png').convert('RGBA')
    outsider = ou.load()

    mi = Image.open(f'base.png').convert('RGBA')
    minion = mi.load()

    de = Image.open(f'base.png').convert('RGBA')
    demon = de.load()

    fa = Image.open(f'base.png').convert('RGBA')
    fabled = fa.load()

    tr = Image.open(f'base.png').convert('RGBA')
    traveller = tr.load()
    good_tr = Image.open(f'base.png').convert('RGBA')
    good_traveller = good_tr.load()
    evil_tr = Image.open(f'base.png').convert('RGBA')
    evil_traveller = evil_tr.load()

    minv = 1
    maxv = 0
    for x in range(width):
        for y in range(height):
            r, g, b, a = image[x, y]
            if a == 0:
                continue
            if border[x, y][3] == 255:
                continue

            h,s,v = rgb2hsv(r, g, b)
            minv = min(v, minv)
            maxv = max(v, maxv)
            townsfolk_colour = map_colours(v, 0.2784313725490196, 0.40784313725490196, (0, 89, 183), (0, 138, 212))
            outsider_colour = map_colours(v, 0.2784313725490196, 0.40784313725490196, (0, 149, 183), (0, 208, 212))
            minion_colour = map_colours(v, 0.2784313725490196, 0.40784313725490196, (147, 15, 19), (196, 47, 49))
            demon_colour = map_colours(v, 0.2784313725490196, 0.40784313725490196, (114, 11, 14), (161, 17, 22))
            fabled_colour = map_colours(v, 0.2784313725490196, 0.40784313725490196, (166, 84, 0), (219, 186, 0))
            if a == 255:
                townsfolk[x, y] = (*townsfolk_colour, 255)
                outsider[x, y] = (*outsider_colour, 255)
                minion[x, y] = (*minion_colour, 255)
                demon[x, y] = (*demon_colour, 255)
                fabled[x, y] = (*fabled_colour, 255)
                if x < width // 2:
                    traveller[x, y] = (*townsfolk_colour, 255)
                    good_traveller[x, y] = (*townsfolk_colour, 255)
                    evil_traveller[x, y] = (*fabled_colour, 255)
                else:
                    traveller[x, y] = (*minion_colour, 255)
                    good_traveller[x, y] = (*fabled_colour, 255)
                    evil_traveller[x, y] = (*minion_colour, 255)
            else:
                townsfolk[x, y] = lerp_tuple(townsfolk[x, y], (*townsfolk_colour, 255), a/400)
                outsider[x, y] = lerp_tuple(outsider[x, y], (*outsider_colour, 255), a/300)
                minion[x, y] = lerp_tuple(minion[x, y], (*minion_colour, 255), a/300)
                demon[x, y] = lerp_tuple(demon[x, y], (*demon_colour, 255), a/400)
                traveller[x, y] = lerp_tuple(traveller[x, y], (*fabled_colour, 255), a/400)


    # tf.save(f'textures/good/{filename}')
    # mi.save(f'textures/evil/{filename}')
    tf.save(f'generated/textures/item/townsfolk/{filename}')
    ou.save(f'generated/textures/item/outsider/{filename}')
    mi.save(f'generated/textures/item/minion/{filename}')
    de.save(f'generated/textures/item/demon/{filename}')
    fa.save(f'generated/textures/item/fabled/{filename}')
    tr.save(f'generated/textures/item/traveller/{filename}')
    good_tr.save(f'generated/textures/item/good_traveller/{filename}')
    evil_tr.save(f'generated/textures/item/evil_traveller/{filename}')
