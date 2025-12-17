class Equipment:
    def __init__(self, id=None, name="", pnumber=""):
        self.id = id
        self.name = name
        self.pnumber = pnumber

    def __str__(self):
        return f"Equipment(id={self.id}, name={self.name}, pnumber={self.pnumber})"
