import re

class DiceMachine():
    def __init__(self, dice_notation):
        self._rolls = []
        self._modifiers = []
        self._roll_information = {}
        self.dice_notation = dice_notation

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
    def roll_information(self):
        return self._roll_information

    @roll_information.setter
    def roll_information(self, value):
        self._roll_information = value
    
    @property
    def dice_notation(self):
        return self._dice_notation

    @dice_notation.setter
    def dice_notation(self, value):
        self._dice_notation = self.validate(value)

    def validate(self, diceStr: str):
        cleaned_str = diceStr.replace(" ", "")
        match = re.match(r"(?!.*[\+\-]{2,}|.*d{2,}|.*d[\+\-]|\d*d\d+d|^[\+\-]|.*[d\+\-]$)[\d\+\-d]+", cleaned_str)

        if match:
            return cleaned_str
        return ""
    
    def split_attributes(self, dice_notation: str):
        split = re.findall(r"\d*d\d+|[\+\-]|\d+", dice_notation)
        for value in split:
            if "d" in value:
                components = re.findall(r"\d+", value)
                self._roll_information.update({"dice": components[0], "modifier": components[1] if len(components) > 1 else "1"})
            else:
                self._modifiers.append(value)

        