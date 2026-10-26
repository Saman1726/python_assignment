"""
    database is a module to handle database entities. It is an ORM approach for using databse.
    classes: 
        TrainingData: is the ORM for training data table.
        IdealFunction: is the ORM for ideal function table.
        TestMapping: is the ORM for test mapping result table.
    Functions:
        init_db: is responsible for initialise the Database and create Tables.
"""
import sqlalchemy as db
import sqlalchemy.orm as orm
import os

Base = orm.declarative_base()

class TrainingData(Base):
    """ TrainingData: is the ORM for training data table."""
    __tablename__ = "training_data"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    X = db.Column(db.Float, nullable=False)
    Y1= db.Column(db.Float,nullable=False)
    Y2= db.Column(db.Float,nullable=False)
    Y3= db.Column(db.Float,nullable=False)
    Y4= db.Column(db.Float,nullable=False)

class IdealFunction(Base):
    """ IdealFunction: is the ORM for ideal function table."""
    __tablename__ = "ideal_function" 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    X = db.Column(db.Float, nullable=False)
    
for idx in range(1,51):
    setattr(IdealFunction, f"Y{idx}", db.Column(db.Float, nullable=False))

class TestMapping(Base):
    """ TestMapping: is the ORM for test mapping result table."""
    __tablename__ = "test_mapping"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    X = db.Column(db.Float, nullable=False)
    Y = db.Column(db.Float, nullable=False)
    Delta_Y = db.Column(db.Float, nullable=True)
    Ideal_Function_Y = db.Column(db.String, nullable=True)

def init_db():
    """ init_db: is responsible for initialise the Database and create Tables."""
    db_path = "assignment.db"
    if os.path.exists(db_path):
        os.remove(db_path)

    engine = db.create_engine(f"sqlite:///{db_path}")
    Base.metadata.create_all(engine)
    return engine

       