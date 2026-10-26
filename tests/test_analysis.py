import unittest
import sys
import os
sys.path.insert(0,os.path.join( os.path.dirname(__file__),"..","src"))
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import analysis as an
import database as db

class TestAnalysis(unittest.TestCase):
    def setUp(self):
        engine = create_engine("sqlite:///:memory:")
        db.Base.metadata.create_all(engine)
        session = sessionmaker(bind=engine)()
        self.session = session
        td_row = db.TrainingData(X=1.1,Y1=1.2,Y2=1.2,Y3=1.3,Y4=1.4)
        self.session.add(td_row)
        if_row = db.IdealFunction(X=1.1, **{f"Y{idx}":idx+0.5 for idx in range(1,51)})
        self.session.add(if_row)
        self.session.commit()

    def tearDown(self):
        self.session.close()

    def test_analys_training_data(self):
        ideal_functions = an.analyse_training_data(self.session)
        self.assertEquals(ideal_functions[0], 1)

    def test_analys_test_mapping(self):
        ideal_functions = an.analyse_training_data(self.session)
        max_allowed = an.analyse_test_mapping("dataset/test.csv", ideal_functions, self.session)
        self.assertAlmostEqual(max_allowed[0],0.3)


if __name__=="__main__":
    unittest.main()