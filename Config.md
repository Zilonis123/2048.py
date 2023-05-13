# Config.json
This md file will explain what each value in `config.json` does
## Values
### Width and Height
Establish the width and height of the game screen. These variables shouldn't be changed during the game because the whole rendering system depends them.

### screen-color
What color is the game's background accepts text, hexcode and rgb values (text is not encouraged)

### show-tile-background
Should the game tiles have a background?

### give-points-for-turn
If true this setting will give the player "score" each time a new tile is created (will give 2 or 4 depending what tile is made)

### colors
You can change a value in colors to something like 
```json
"0": {
    "background": "black",
    "font": "red"
}
```
the background value is the tiles background and the font although named incorrectly is the font color. The key of the value is the tile in the example we are changing the tile 0