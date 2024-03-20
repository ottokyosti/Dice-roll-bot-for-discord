import re
import random
import unittest
from unittest.mock import patch
from diceFunctions import DiceMachine

class DiceValidator():
    @staticmethod
    def validate(diceStr: str):
        cleaned_str = diceStr.replace(" ", "")
        match = re.match(r"(?!.*[\+\-]{2,}|.*d{2,}|.*d[\+\-]|\d*d\d+d|^[\+\-]|.*[d\+\-]$)[\d\+\-d]+", cleaned_str)

        if match:
            return re.findall(r"\d*d\d+|[\+\-]|\d+", cleaned_str)
        return []
    
    @staticmethod
    def rolls_list(mult, dice):
        multInt = int(mult)
        diceInt = int(dice)
        rolls = [0 for _ in range(multInt)]
        for index in range(len(rolls)):
            rolls[index] = random.randint(1, diceInt)
        return rolls

class TestDiceFunctions(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.dice_machines = [DiceMachine("d20 + 5 + 3"), DiceMachine("2d4 + 2d4 - 6"), DiceMachine("d20")]

    def test_validation(self):
        print("\nTesting validation with valid values:\n")
        print("Does 'd20' get through validation?")
        print(f"Expected value: ['d20'] | Actual value: {DiceValidator.validate("d20")}")
        self.assertEqual(DiceValidator.validate("d20"), ["d20"])
        print("Does '2d8 + 3 - d8' get through validation?")
        print(f"Expected value: ['2d8', '+', '3', '-', 'd8'] | Actual value: {DiceValidator.validate("d20")}")
        self.assertEqual(DiceValidator.validate("2d8 + 3 - d8"), ["2d8", "+", "3", "-", "d8"])
        print("Does 'd81+302+43d8' get through validation?")
        print(f"Expected value: ['d81', '+', '302', '+', '43d8'] | Actual value: {DiceValidator.validate("d81+302+43d8")}")
        self.assertEqual(DiceValidator.validate("d81+302+43d8"), ["d81", "+", "302", "+", "43d8"])

        print("\nTesting validation with invalid values:\n")
        test_values = ["2dd2+43", 
                       "2d6-+3", 
                       "+2d8", 
                       "4d20 + 2 - d", 
                       "d100-", 
                       "s40 + d20", 
                       "d20 + d - 4",
                       "2d20d5-50",
                       "+",
                       "2d"]
        for value in test_values:
            print(f"Does '{value}' fail validation?")
            print(f"Expected value: [] | Actual value: {DiceValidator.validate(value)}")
            self.assertEqual(DiceValidator.validate(value), [])
    
    def test_random(self):
        print("\nTesting random values\n")
        print("Replacing random.randint function to return specific values...")
        with patch("random.randint", return_value = 4):
            result = DiceValidator.rolls_list(mult = "3", dice = "6")
        expected_result = [4, 4, 4]
        print(f"Expected result: {expected_result}, Actual result: {result}")
        self.assertEqual(result, expected_result)

    def test_roll(self):
        print("\nRolling dice 50 times\n")
        for _ in range(50):
            for value in self.dice_machines:
                value.roll()
            expected_results = [range(9, 29), range(-1, 27), range(1, 21)]
            for i in range(len(expected_results)):
                print(f"Expected result: {expected_results[i]}, Actual result: {self.dice_machines[i].result}")
                self.assertIn(self.dice_machines[i].result, expected_results[i])
            print()

if __name__ == "__main__":
    unittest.main()