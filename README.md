# 2048
## Whats 2048?
2048 is a 4x4 tile based sliding game where the goal is to get one tile to the number 2048. When pressing a button corresponding to a side for example "w" all the tiles move up and if there are the same number on two tiles next to eachother they join into one, but explaining is not the best way to play a game so.. let's begin

## Downloading
You have to have [python](https://python.org) installed on your local machine for this game to work. (There might be an executable file later)

Clone the repository
```git
git clone https://github.com/Zilonis123/2048.py && cd 2048.py
```
afterwards you have to install the dependencies
```sh
pip install -r requirements.txt
```
There you go you have succsesfully installed "2048 gui version"
to run it just type
```sh
python 2048.py
```
## How to play?
When you have started the game it's very straight forward from there.
### Controlls
`w` - Push the tiles up

`d` - Push the tiles right

`s` - Push the tiles down

`a` - Push the tiles left

`ctrl+z` - `Undo the previous move~ currently doesnt work

`ctrl+r` - Reload the configuration file

`ctrl+p` - Restart the game
## How to customize the feel
To customize the game you have to open the `config.json` file.
When you have opened the file you can customize the colors of the tiles and much more.

NOTE: Some options in the configuration file shouldn't (It will cause visual bugs) be reloaded with the `ctrl+r` shortcut for example the `WIDTH` and `HEIGHT` of the screen