import database as db
db.init_db
import logging
import file_handler as fh
import analysis as an
import visualisation as vi
import os

logfile_path = "server.log"
if os.path.exists(logfile_path):
    os.remove(logfile_path)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='server.log', filemode='a')

def main():

    session = db.orm.sessionmaker(bind=db.engine)()
    training_data = fh.TrainingDataLoader("dataset/train.csv")
    training_data.save_to_database(session)
    
    ideal_function = fh.IdealFunctionLoader("dataset/ideal.csv")
    ideal_function.save_to_database(session)
    

    ideal_functions = an.analyse_training_data(session)
    logging.info("Ideal functions identified: %s", ideal_functions)

    max_allowed = an.analyse_test_mapping("dataset/test.csv", ideal_functions, session)

    vi.plot_data(session, ideal_functions, max_allowed)
    
if __name__ == "__main__":
    main()