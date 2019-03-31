from enum import Enum


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
    Icon.Green: 'test/icon_green.png',
    Icon.Pink: 'test/icon_pink.png',
    Icon.Purple: 'test/icon_purple.png',
    Icon.Red: 'test/icon_red.png',
    Icon.Yellow: 'test/icon_yellow.png',

    Icon.BombGreen: 'test/icon_bomb_green.png',
    Icon.BombPink: 'test/icon_bomb_pink.png',
    Icon.BombPurple: 'test/icon_bomb_purple.png',
    Icon.BombRed: 'test/icon_bomb_red.png',
    Icon.BombYellow: 'test/icon_bomb_yellow.png',
}
