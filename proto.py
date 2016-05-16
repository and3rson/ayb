class Codes:
    IAC = '\xFF'
    WILL = '\xFB'
    WONT = '\xFC'
    DO = '\xFD'
    DONT = '\xFE'

    ECHO = '\x01'
    SUPPRESS_GO_AHEAD = '\x03'
    NAWS = '\x1F'
    LINE_MODE = '\x22'

    SB = '\xFA'

    # _reversed = dict(
    #     250='SB'
    # )

    @classmethod
    def reverse(cls, code):
        for k in dir(Codes):
            v = getattr(Codes, k)
            if v == code:
                return k
        return None
