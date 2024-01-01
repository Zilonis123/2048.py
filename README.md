# 2048

## What is 2048?

2048 is a 4x4 tile-based sliding game where the goal is to reach the number 2048 on one of the tiles. Pressing a corresponding button, such as "w," moves all the tiles in that direction. If two tiles with the same number are adjacent, they merge into one. However, explaining it is not the best way to play a game, so let's get started!

## Downloading

Ensure you have [Python](https://python.org) installed on your local machine for the game to work.

Clone the repository:

```sh
git clone https://github.com/Zilonis123/2048.py && cd 2048.py
```

Afterwards, install the dependencies:

```sh
pip install -r requirements.txt
```

Now, you have successfully installed the "2048 GUI version." To run it, type:

```sh
python 2048.py
```

## How to play?

Use the controls "w," "d," "a," and "s" to merge tiles until you reach the 2048 tile.

### Controls

- `w` - Push the tiles up
- `d` - Push the tiles right
- `s` - Push the tiles down
- `a` - Push the tiles left
- `ctrl+z` - Undo the previous move
- `ctrl+r` - Reload the configuration file
- `ctrl+p` - Restart the game
- `ctrl+i` - An "AI" makes a move for you. Note that the "AI" is not very advanced and averages around 1000 points per game without using your brain.

## How to customize the "feel" of the game.

To customize the game, open `config.json`. Change options like tile colors and more.

**NOTE:** Some options in the configuration file shouldn't be reloaded with the `ctrl+r` shortcut, for example, the `WIDTH` and `HEIGHT` of the screen. It will cause visual bugs.

## Contributing

Your contributions are welcome! If you have suggestions to enhance the project, feel free to fork the repository and create a pull request. Alternatively, you can open an issue with the tag "enhancement". Don't forget to star the project if you find it useful!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
