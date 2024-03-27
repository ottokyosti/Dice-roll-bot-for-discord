import re
import random
import os
from dotenv import load_dotenv

class DiceMachine():
    def __init__(self, dice_notation):
        load_dotenv()
        self._rolls = []
        self._dice_notation_str = dice_notation
        self._dice_notation = self.__validate(dice_notation)
        self._result = 0
        self._emojis = {"EMOJI_POS": None, "EMOJI_NEG": None}
        for item in self._emojis:
            self._emojis[item] = os.environ.get(item)
            self._emojis[item] = self._emojis[item] if self._emojis[item] is not None else ""

    @property
    def rolls(self):
        return self._rolls

    @rolls.setter
    def rolls(self, value):
        self._rolls = value

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

    @property
    def result(self):
        return self._result
    
    @result.setter
    def result(self, value):
        self._result = value

    @property
    def emojis(self):
        return self._emojis
    
    @emojis.setter
    def emojis(self, value):
        self._emojis = value

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
        if len(self._dice_notation) == 0:
            return
        
        equation = []
        for i in range(len(self._dice_notation)):
            if "d" in self._dice_notation[i]:
                split = re.findall(r"\d+", self._dice_notation[i])
                if len(split) > 1:
                    rolls = self.__generate_rolls(split[0], split[1])
                else:
                    rolls = self.__generate_rolls("1", split[0])
                self._rolls.append({"notation": self._dice_notation[i], "rolls": rolls})
                equation.append(str(sum(rolls)))
            else:
                equation.append(self._dice_notation[i])
        joined_equation = "".join(equation)
        result = eval(joined_equation)
        self._result = result if result > 0 else 1

    def roll_to_string(self):
        if len(self._dice_notation) == 0:
            return "Incorrect dice notation!"

        if len(self._rolls) == 1:
            special_case_string = f"Heität: {self._dice_notation_str}\n"
            if 20 in self._rolls[0]["rolls"]:
                special_case_string += f"{self._emojis['EMOJI_POS']} Kritikaalinen suksessi! Heitit **20**! {self._emojis['EMOJI_POS']} Lopullinen summa tho oli **{self._result}**"
            elif 1 in self._rolls[0]["rolls"]:
                special_case_string += f"{self._emojis['EMOJI_NEG']} Juu thruu shit **1**! {self._emojis['EMOJI_NEG']} Lopullinen summa tho oli **{self._result}**"
            else:
                special_case_string += f"Heitit **{self._rolls[0]['rolls'][0]}**! Lopullinen summa tho oli **{self._result}**"
            return special_case_string
        
        roll_string = f"Heität: {self._dice_notation_str}\nNopanheitot:\n"

        for item in self._rolls:
            notation = item["notation"]
            rolls = item["rolls"]
            roll_string += f"{notation}: **{', '.join(str(roll) for roll in rolls)}**,\n"

        roll_string = roll_string.rstrip(", ")
        roll_string += f"Lopullinen summa tho oli **{self._result}**"
        
        return roll_string