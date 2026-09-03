import pygame

def is_mouse_over_image(image, pos, scale): # vrati True, ak je mys nad netransparentnou castou obrazku
    mouse_x, mouse_y = pygame.mouse.get_pos()
    width = int(image.get_width() * scale)
    height = int(image.get_height() * scale)
    relative_x = mouse_x - pos.x
    relative_y = mouse_y - pos.y
    if 0 <= relative_x < width and 0 <= relative_y < height:
        original_x = int(relative_x / scale)
        original_y = int(relative_y / scale)
        return image.get_at((original_x, original_y)).a > 0
    return False