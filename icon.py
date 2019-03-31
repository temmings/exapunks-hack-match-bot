from enum import Enum

from PIL import Image


class Icon(Enum):
    Empty = '.'
    Green = 'g'
    Pink = 'p'
    Purple = 'P'
    Red = 'r'
    Yellow = 'y'

    BombGreen = '^'
    BombPink = '*'
    BombPurple = '#'
    BombRed = '!'
    BombYellow = '='


IconFileDict = {
    Icon.Green: Image.open('test/icon_green.png'),
    Icon.Pink: Image.open('test/icon_pink.png'),
    Icon.Purple: Image.open('test/icon_purple.png'),
    Icon.Red: Image.open('test/icon_red.png'),
    Icon.Yellow: Image.open('test/icon_yellow.png'),

    Icon.BombGreen: Image.open('test/icon_bomb_green.png'),
    Icon.BombPink: Image.open('test/icon_bomb_pink.png'),
    Icon.BombPurple: Image.open('test/icon_bomb_purple.png'),
    Icon.BombRed: Image.open('test/icon_bomb_red.png'),
    Icon.BombYellow: Image.open('test/icon_bomb_yellow.png'),
}
