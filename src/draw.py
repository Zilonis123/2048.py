import pygame as p

def drawBoard(render) -> None:
    # Get screen dimensions from render
    width: int = render.WIDTH
    height: int = render.HEIGHT

    size: int = render.game.size

    # Get configuration values
    border_radius: int = render.config["Rect-Border-Radius"]
    bg_offset: int = render.config["background-offset"]
    background_size: int = render.config["background-size"]

    # Calculate middle of the screen
    MIDDLE: tuple[int, int] = (width // 2, height // 2)

    # Calculate background position
    loc: tuple[int, int] = (MIDDLE[0] - background_size // 2, MIDDLE[1] - background_size // 2)
    background_loc: tuple[int, int] = (loc[0]-bg_offset, loc[1]-bg_offset)

    # Create rect
    bg_rect = p.Rect(background_loc, (background_size + bg_offset*2, background_size + bg_offset*2))

    if render.config["show-tile-background"]:
        p.draw.rect(render.screen, p.Color("Orange"), bg_rect, border_radius=border_radius)

    # Font
    font = p.font.Font('freesansbold.ttf', 32)

    gap = background_size//30
    bwidth = (background_size - (gap * 3)) / size
    bheight = (background_size - (gap * 3)) / size

    for i in range(size):
        for j in range(size):
            # What tile are we on?
            tile = render.game.map[i][j]

            l = (j * bwidth + loc[0] + (gap * j), i * bheight + loc[1] + (gap * i))  # (x, y)
            rect = p.Rect(l, (bwidth, bheight))

            # Determine the color
            tile_info = render.config["colors"][str(tile)]
            background_color = p.Color(tile_info["background"])

            # Draw the tile
            p.draw.rect(render.screen, background_color, rect, border_radius=border_radius)

            if tile != 0:
                font_color = tile_info["font"]

                text = font.render(str(tile), True, font_color, background_color)

                text_rect = text.get_rect()
                text_rect.center = rect.center

                render.screen.blit(text, text_rect)
