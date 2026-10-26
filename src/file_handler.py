"""
    file_handler is a module to read files and make them ready to use and save in databse.
    Functions:
        Dataloader: is the parent class in this Module. It hass a file_path and load_data function.
        TrainingDataLoader: is the child class of Dataloader for reading and saving training data.
        IdealFunctionLoader: is the child class of Dtaloader for reading and saving ideal functions.
        TestMappingLoader: is child of DataLoader also an iterable class to read the test mappings line by line and also save them to database.
"""
import pandas as pd
import logging
import database as db

logger = logging.getLogger(__name__)

class DataLoader:
    """ Dataloader: is the parent class in this Module. It hass a file_path and load_data function."""
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    def load_data(self):
        try:
            self.data = pd.read_csv(self.file_path)
            return self.data
        except FileNotFoundError as e:
            logger.exception(f"File not found from {self.file_path}")
            raise FileNotFoundError(f"File not found from {self.file_path}") from e
        except pd.errors.EmptyDataError as e:
            logger.exception(f"No data: {self.file_path} is empty")
            raise ValueError(f"No data: {self.file_path} is empty") from e
        except pd.errors.ParserError as e:
            logger.exception(f"Parsing error: {self.file_path} is malformed")
            raise ValueError(f"Parsing error: {self.file_path} is malformed") from e

class TrainingDataLoader(DataLoader):
    """ TrainingDataLoader: is the child class of Dataloader for reading and saving training data."""
    def __init__(self, file_path):
        super().__init__(file_path)

    def save_to_database(self, session):
        if self.data is None:
            self.data = self.load_data()

        for _, row in self.data.iterrows():
            training_data = db.TrainingData(
                X=row['x'],
                Y1=row['y1'],
                Y2=row['y2'],
                Y3=row['y3'],
                Y4=row['y4']
            )
            session.add(training_data)

        session.commit()

class IdealFunctionLoader(DataLoader):
    """ IdealFunctionLoader: is the child class of Dtaloader for reading and saving ideal functions."""
    def __init__(self, file_path):
        super().__init__(file_path)

    def save_to_database(self, session):
        if self.data is None:
            self.data = self.load_data()

        for _, row in self.data.iterrows():
            ideal_function = db.IdealFunction(
                X=row['x'],
                **{f"Y{idx}" : row[f"y{idx}"] for idx in range(1,51)}
            )
            session.add(ideal_function)
        session.commit()

class TestMappingLoader(DataLoader):
    """ TestMappingLoader: is child of DataLoader also an iterable class to read the test mappings line by line and also save them to database."""
    def __init__(self,file_path):
        super().__init__(file_path)

    def __iter__(self):
        with open(self.file_path, "r", encoding="utf-8") as file:
            next(file)
            yield from file

    def save_to_database(self, session, x, y, delta_y, ideal_function_y):
        
        test_mapping = db.TestMapping(
            X=x,
            Y=y,
            Delta_Y=delta_y,
            Ideal_Function_Y=ideal_function_y
        )
        session.add(test_mapping)
        session.commit()