from enum import IntEnum


class Icon(IntEnum):
    Empty = 0

    Green = 1
    Pink = 2
    Purple = 4
    Red = 8
    Yellow = 16

    BombGreen = 32
    BombPink = 64
    BombPurple = 128
    BombRed = 256
    BombYellow = 512


class IconType(IntEnum):
    """
    アイコンの区分を表す。
    同一のアイコンが連結した場合に消滅する数を値として持つ。
    """
    Normal = 4
    Bomb = 2


IconToStringDict = {
    Icon.Empty: '.',

    Icon.Green: 'g',
    Icon.Pink: 'p',
    Icon.Purple: 'P',
    Icon.Red: 'r',
    Icon.Yellow: 'y',

    Icon.BombGreen: '^',
    Icon.BombPink: '*',
    Icon.BombPurple: '#',
    Icon.BombRed: '!',
    Icon.BombYellow: '=',
}

IconTypeDict = {
    IconType.Normal: (
        Icon.Green,
        Icon.Pink,
        Icon.Purple,
        Icon.Red,
        Icon.Yellow),
    IconType.Bomb: (
        Icon.BombGreen,
        Icon.BombPink,
        Icon.BombPurple,
        Icon.BombRed,
        Icon.BombYellow),
}

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
