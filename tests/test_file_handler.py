import unittest
import sys
import os
sys.path.insert(0,os.path.join(os.path.dirname(__file__),"..","src"))
import file_handler as fh

class TestFileHandler(unittest.TestCase):
    
    def test_training_data_loader(self):
        tdl = fh.TrainingDataLoader("dataset/train.csv")
        test_data = tdl.load_data()
        self.assertGreater(len(test_data),0)

    def test_ideal_function_loader(self):
        idl = fh.IdealFunctionLoader("dataset/ideal.csv")
        test_data = idl.load_data()
        self.assertGreater(len(test_data),0)

    def test_test_mapping_loader(self):
        tml = fh.TestMappingLoader("dataset/test.csv")
        iterator = iter(tml)
        test_data = next(iterator)
        self.assertEqual(len(test_data), 1)

if __name__=="__main__":
    unittest.main()
