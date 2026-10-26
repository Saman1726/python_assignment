import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__),"..","src"))

import database as db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class TestDatabase(unittest.TestCase):
    def setUp(self):
        engine = create_engine("sqlite:///:memory:")
        db.Base.metadata.create_all(engine)
        session = sessionmaker(bind=engine)
        self.session = session()

    def tearDown(self):
        self.session.close()

    def test_training_data(self):
        row = db.TrainingData(X=1.4, Y1=1.5, Y2=1.6, Y3=1.7, Y4=1.8)
        self.session.add(row)
        self.session.commit()
        res = self.session.query(db.TrainingData).first()
        self.assertEqual(res.X, 1.4)

    def test_test_mapping(self):
        row = db.TestMapping(X=1.2, Y=1.3, Delta_Y=1.4, Ideal_Function_Y=None)
        self.session.add(row)
        self.session.commit()
        res = self.session.query(db.TestMapping).first()
        self.assertEqual(res.X, 1.2)

    def test_ideal_function(self):
        row = db.IdealFunction(X=1.1, **{f"Y{idx}":idx+0.5 for idx in range(1,51)})
        self.session.add(row)
        self.session.commit()
        res = self.session.query(db.IdealFunction).first()
        self.assertEqual(res.X, 1.1)

if __name__=="__main__":
    unittest.main()