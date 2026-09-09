import pygame
import math
from konstanty import *

def is_mouse_over_image(image, pos, mys_realna_pozicia): # vrati True, ak je mys nad netransparentnou castou obrazku
    image = pygame.transform.scale( image, (int(image.get_width() * OBRAZOK_SCALE_OFFSET), int(image.get_height() * OBRAZOK_SCALE_OFFSET)) )
    mouse_x, mouse_y = mys_realna_pozicia.x, mys_realna_pozicia.y
    width = int(image.get_width())
    height = int(image.get_height())
    relative_x = mouse_x - pos.x
    relative_y = mouse_y - pos.y
    if 0 <= relative_x < width and 0 <= relative_y < height:
        original_x = int(relative_x)
        original_y = int(relative_y)
        return image.get_at((original_x, original_y)).a > 0
    return False

def circle_through_points(a, b, r): # ak sa to neda, tak zvolim najmensie r take aby sa to dalo
    x1, y1 = a
    x2, y2 = b
    dx = x2 - x1
    dy = y2 - y1
    d = math.hypot(dx, dy)
    if d > 2 * r:
        r = d/2

    # Midpoint of AB
    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2

    # Distance from midpoint to either possible center
    h = math.sqrt(r*r - (d/2)**2)

    # Unit vector perpendicular to AB
    nx = -dy / d
    ny = dx / d

    # Two possible centers
    centers = [
        (mx + h * nx, my + h * ny),
        (mx - h * nx, my - h * ny)
    ]

    result = []

    for cx, cy in centers:
        # (x-cx)^2 + (y-cy)^2 = r^2
        #
        # x^2 - 2cx*x + y^2 - 2cy*y = r^2 - cx^2 - cy^2
        #
        # x^2 + kx + y^2 + ly = m

        k = -2 * cx
        l = -2 * cy
        m = r*r - cx*cx - cy*cy
        result.append((k, l, m))

    return result[0]