# Config.json

This file explains the purpose of each value in `config.json`.

## Values

### Width and Height

Set the width and height of the game screen. Avoid changing these variables during the game, as the entire rendering system depends on them.

### screen-color

Defines the color of the game's background. Accepts text, hexcode, and RGB values (text is not encouraged).

### show-tile-background

Determines whether the game tiles should have a background.

### give-points-for-turn

If set to true, this option rewards the player with "score" each time a new tile is created (2 or 4 points, depending on the tile).

### colors

You can customize the appearance of each tile by changing a value in the `colors` section. For example:

```json
"0": {
    "background": "black",
    "font": "red"
}
```

- The `background` value sets the tile's background color.
- The `font` value, despite its name, determines the font color.
- The key of the value corresponds to the tile number being changed (in this example, tile 0).
