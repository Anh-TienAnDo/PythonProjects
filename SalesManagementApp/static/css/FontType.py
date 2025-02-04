from contants import FAMILY_FONT, FONT_SIZE

class FontType:
    @staticmethod
    def h1():
        return (FAMILY_FONT, 20, "bold")

    @staticmethod
    def h2():
        return (FAMILY_FONT, 16, "bold")

    @staticmethod
    def h3():
        return (FAMILY_FONT, 14, "bold")

    @staticmethod
    def h4():
        return (FAMILY_FONT, 12, "bold")

    @staticmethod
    def normal():
        return (FAMILY_FONT, FONT_SIZE, "bold")
    
    @staticmethod
    def mini():
        return (FAMILY_FONT, FONT_SIZE-2)
    
    @staticmethod
    def data():
        return (FAMILY_FONT, FONT_SIZE+4, "bold")
