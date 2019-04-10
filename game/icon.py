from enum import IntEnum, unique


@unique
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

    @classmethod
    def to_char(cls, icon):
        return {
            cls.Empty: '.',

            cls.Green: 'g',
            cls.Pink: 'p',
            cls.Purple: 'P',
            cls.Red: 'r',
            cls.Yellow: 'y',

            cls.BombGreen: '^',
            cls.BombPink: '*',
            cls.BombPurple: '#',
            cls.BombRed: '!',
            cls.BombYellow: '=',
        }[icon]

    def __str__(self):
        return self.to_char(self)

    def __repr__(self):
        return 'Icon<%s, "%s", %d>' % (self.name, self.to_char(self), self.value)


class IconType(IntEnum):
    """
    アイコンの区分を表す。
    同一のアイコンが連結した場合に消滅する数を値として持つ。
    """
    Normal = 4
    Bomb = 2


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

IconBombEraseDict = {
    Icon.BombGreen: Icon.Green,
    Icon.BombPink: Icon.Pink,
    Icon.BombPurple: Icon.Purple,
    Icon.BombRed: Icon.Red,
    Icon.BombYellow: Icon.Yellow,
}

IconFileDict = {
    Icon.Green: 'images/icon_green.png',
    Icon.Pink: 'images/icon_pink.png',
    Icon.Purple: 'images/icon_purple.png',
    Icon.Red: 'images/icon_red.png',
    Icon.Yellow: 'images/icon_yellow.png',
    Icon.BombGreen: 'images/icon_bomb_green.png',
    Icon.BombPink: 'images/icon_bomb_pink.png',
    Icon.BombPurple: 'images/icon_bomb_purple.png',
    Icon.BombRed: 'images/icon_bomb_red.png',
    Icon.BombYellow: 'images/icon_bomb_yellow.png',
}
