import unittest
from diceFunctions import DiceMachine

class TestDiceFunctions(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.dm = DiceMachine("d20")

    def test_validation(self):
        print("\nTesting validation with valid values:\n")
        print("Does 'd20' get through validation?")
        print(f"Expected value: ['d20'] | Actual value: {self.dm.validate("d20")}")
        self.assertEqual(self.dm.validate("d20"), ["d20"])
        print("Does '2d8 + 3 - d8' get through validation?")
        print(f"Expected value: ['2d8', '+', '3', '-', 'd8'] | Actual value: {self.dm.validate("d20")}")
        self.assertEqual(self.dm.validate("2d8 + 3 - d8"), ["2d8", "+", "3", "-", "d8"])
        print("Does 'd81+302+43d8' get through validation?")
        print(f"Expected value: ['d81', '+', '302', '+', '43d8'] | Actual value: {self.dm.validate("d81+302+43d8")}")
        self.assertEqual(self.dm.validate("d81+302+43d8"), ["d81", "+", "302", "+", "43d8"])

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
            print(f"Expected value: [] | Actual value: {self.dm.validate(value)}")
            self.assertEqual(self.dm.validate(value), [])
        print("Validation testing done")

if __name__ == "__main__":
    unittest.main()