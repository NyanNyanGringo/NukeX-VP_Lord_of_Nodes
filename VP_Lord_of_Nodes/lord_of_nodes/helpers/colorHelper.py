

def rgb_to_hex(r, g, b, zero_to_one_range):
    # zero_to_one_range True - R, G, B in range 1 to 0
    # zero_to_one_range False - R, G, B in range 0 to 255

    if zero_to_one_range:
        mult = 255
    else:
        mult = 1

    r = int(r * mult)
    g = int(g * mult)
    b = int(b * mult)
    hex = int("%02x%02x%02x%02x" % (r, g, b, 1), 16)

    return hex


def hex_to_rgb(hex):
    # use binar python operators to convert HEX to RGB

    hex = int(hex)
    r = (0xFF & hex >> 24) / 255.0
    g = (0xFF & hex >> 16) / 255.0
    b = (0xFF & hex >> 8) / 255.0

    return r, g, b
