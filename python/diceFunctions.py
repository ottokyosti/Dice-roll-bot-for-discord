import re

class DiceMachine():
    def __init__(self, dice_notation = "d20"):
        self._rolls = []
        self._modifiers = []
        self._dice_notation = self.__validate(dice_notation)

    @property
    def rolls(self):
        return self._rolls

    @rolls.setter
    def rolls(self, value):
        self._rolls = value

    @property
    def modifiers(self):
        return self._modifiers

    @modifiers.setter
    def modifiers(self, value):
        self._modifiers = value
    
    @property
    def dice_notation(self):
        return self._dice_notation

    @dice_notation.setter
    def dice_notation(self, value):
        self._dice_notation = self.__validate(value)

    def __validate(self, diceStr: str):
        cleaned_str = diceStr.replace(" ", "")
        match = re.match(r"(?!.*[\+\-]{2,}|.*d{2,}|.*d[\+\-]|\d*d\d+d|^[\+\-]|.*[d\+\-]$)[\d\+\-d]+", cleaned_str)

        if match:
            return re.findall(r"\d*d\d+|[\+\-]|\d+", cleaned_str)
        return []