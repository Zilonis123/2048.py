import pygame as p

def drawBoard(render) -> None:

    # Get configuration values
    BORDER_RADIUS: int = render.config["tile-border-radius"]
    TILE_MARGIN: int = render.config["tile-margin"]
    TILE_SIZE: int = render.config["tile-size"]
    size: int = render.game.size
    matrix: list[list[int]] = render.game.matrix

    # Draw the tiles

    width: int = len(matrix[0]) * (TILE_SIZE + TILE_MARGIN) - TILE_MARGIN
    height: int = len(matrix) * (TILE_SIZE + TILE_MARGIN) - TILE_MARGIN


    OFFSET_X, OFFSET_Y = (render.WIDTH - width) // 2, (render.HEIGHT - height) // 2


    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            value: int = matrix[row][col]
            color: dict = render.config["colors"].get(str(value), "WHITE")

            rect = p.Rect(
                    col * (TILE_SIZE + TILE_MARGIN) + OFFSET_X,
                    row * (TILE_SIZE + TILE_MARGIN) + OFFSET_Y,
                    TILE_SIZE,
                    TILE_SIZE,
                )


            p.draw.rect(render.screen,color["background"],rect)

            font = p.font.Font(None, 36)
            text = font.render(str(value), True, color["font"])
            text_rect = text.get_rect(center=rect.center)

            render.screen.blit(text, text_rect)
