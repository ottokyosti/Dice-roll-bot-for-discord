import unittest
from diceFunctions import DiceMachine

class TestDiceFunctions(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.DM = DiceMachine("3d20 + 2")

    def test_validation(self):
        print("\nTesting validation with valid values:\n")
        test_values = ["d20", "2d4 + 21 + d8", "2d4+21+d8"]
        for value in test_values:
            print(f"Does '{value}' match with regex?")
            print(f"Expected value: {value.replace(" ", "")} | Actual value: {self.DM.validate(value)}")
            self.assertEqual(self.DM.validate(value), value.replace(" ", ""))

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
            print(f"Does '{value}' fail regex match?")
            print(f"Expected value: '' | Actual value: {self.DM.validate(value)}")
            self.assertEqual(self.DM.validate(value), "")
        print("Validation testing done")

if __name__ == "__main__":
    unittest.main()