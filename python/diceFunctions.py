import re
import random

class DiceMachine():
    def __init__(self, dice_notation = "d20"):
        self._rolls = []
        self._modifiers = []
        self._dice_notation_str = dice_notation
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
    def dice_notation_str(self):
        return self._dice_notation_str
    
    @dice_notation_str.setter
    def dice_notation_str(self, value):
        self._dice_notation_str = value
    
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
    
    def __generate_rolls(self, mult, dice):
        multInt = int(mult)
        diceInt = int(dice)
        rolls = [0 for _ in range(multInt)]
        for index in range(len(rolls)):
            rolls[index] = random.randint(1, diceInt)
        return rolls
    
    def roll(self):
        total_sum = 0
        for value in self._dice_notation:
            if "d" in value:
                split = re.findall(r"\d+", value)
                if len(split) > 1:
                    rolls = self.__generate_rolls(split[0], split[1])
                else:
                    rolls = self.__generate_rolls("1", split[0])
                self._rolls.append({"notation": value, "rolls": rolls})
                total_sum = total_sum + sum(rolls)
                
                