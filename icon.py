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


class IconRGBColor(Enum):
    """
    探索範囲のピクセルに特定のRGBのピクセルが含まれているか？の判定に利用する
    """
    Green = (18, 182, 153)
    Pink = (255, 177, 214)
    Purple = (157, 94, 250)
    Red = (255, 196, 183)
    Yellow = (237, 165, 24)

    BombGreen = (205, 233, 244)
    BombPink = (213, 207, 226)
    BombPurple = (137, 159, 172)
    BombRed = (222, 251, 255)
    BombYellow = (245, 181, 128)


IconColorDict = {
    Icon.Green: IconRGBColor.Green,
    Icon.Pink: IconRGBColor.Pink,
    Icon.Purple: IconRGBColor.Purple,
    Icon.Red: IconRGBColor.Red,
    Icon.Yellow: IconRGBColor.Yellow,

    Icon.BombGreen: IconRGBColor.BombGreen,
    Icon.BombPink: IconRGBColor.BombPink,
    Icon.BombPurple: IconRGBColor.BombPurple,
    Icon.BombRed: IconRGBColor.BombRed,
    Icon.BombYellow: IconRGBColor.BombYellow,
}
