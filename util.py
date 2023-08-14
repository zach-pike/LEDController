def mult_rgb(rgb, scale):
    return (rgb[0] * scale, rgb[1] * scale, rgb[2] * scale)

def brightness_adjust(color, brightness_lvl):
    return mult_rgb(color, brightness_lvl)

def fade(t):
    theta = t % 360
    x = round((1 - abs((theta / 60) % 2 - 1)) * 255)

    if theta >= 0 and theta < 60:
        return ( 255, x, 0 )
    elif theta >= 60 and theta < 120:
        return ( x, 255, 0 )
    elif theta >= 120 and theta < 180:
        return ( 0, 255, x )
    elif theta >= 180 and theta < 240:
        return ( 0, x, 255 )
    elif theta >= 240 and theta < 300:
        return ( x, 0, 255 )
    elif theta >= 300 and theta < 360:
        return ( 255, 0, x )