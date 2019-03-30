from enum import Enum


class Icon(Enum):
    Empty = '.'
    Green = '^'
    Pink = '*'
    Purple = '#'
    Red = '!'
    Yellow = '='

    BombRed = 'r'
    BombGreen = 'g'
    BombPink = 'b'
    BombPurple = 'p'
    BombYellow = 'y'

    Unknown = '?'


class IconRGBColor(Enum):
    Green = (17, 177, 148) # (19, 188, 158), (22, 195, 161)
    Pink = (226, 20, 166) # (211, 22, 118)
    Purple = (23, 63, 181)
    Red = (198, 22, 46) # (223, 38, 67), (248, 64, 98), (238, 62, 95)
    Yellow = (218, 163, 63) # (220, 165, 66), (218, 164, 66)

    BombPurple = (19, 20, 54)


IconColorDict = {
    IconRGBColor.Purple: Icon.Purple,
    IconRGBColor.Yellow: Icon.Yellow,
    IconRGBColor.Red: Icon.Red,
    IconRGBColor.Green: Icon.Green,
    IconRGBColor.Pink: Icon.Pink,
}
