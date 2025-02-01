from contants import FAMILY_FONT

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
        return (FAMILY_FONT, 12, "bold")
    
    @staticmethod
    def mini():
        return (FAMILY_FONT, 10)
    
    @staticmethod
    def data():
        return (FAMILY_FONT, 16, "bold")
