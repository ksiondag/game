import constants

def meters_to_pixels( meters ):
    return 25.*meters

def pixels_to_meters( pixels ):
    return pixels/25.

def vertical_pixels_to_meters( pixels ):
    return pixels_to_meters( constants.PIXEL_FLOOR - pixels )

def vertical_meters_to_pixels( meters ):
    return constants.PIXEL_FLOOR - meters_to_pixels( meters )

def location_pixels_to_meters( pixel_x, pixel_y ):
    x = pixels_to_meters( pixel_x )
    y = vertical_pixels_to_meters( pixel_y )

    return x, y

def location_meters_to_pixels( x, y ):
    pixel_x = meters_to_pixels( x )
    pixel_y = vertical_meters_to_pixels( y )

    return pixel_x, pixel_y

