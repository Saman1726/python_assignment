import numpy as np
import database as db
import file_handler as fh
import logging

m_sqrt_2 = np.sqrt(2)

def analyse_training_data(session):
    delta_y1_dict = [0]*50
    delta_y2_dict = [0]*50
    delta_y3_dict = [0]*50
    delta_y4_dict = [0]*50
    training_data = session.query(db.TrainingData).all()

    for data in training_data:
        ideal_functions = session.query(db.IdealFunction).filter(db.IdealFunction.X == data.X).all()
        if not ideal_functions:
            continue
        
        for idx in range(1,51):
            function_y = f"Y{idx}"
            value_y = getattr(ideal_functions[0], function_y)
            delta_y1 = (data.Y1 - value_y) ** 2
            delta_y2 = (data.Y2 - value_y) ** 2
            delta_y3 = (data.Y3 - value_y) ** 2
            delta_y4 = (data.Y4 - value_y) ** 2
            delta_y1_dict[idx-1] += delta_y1
            delta_y2_dict[idx-1] += delta_y2
            delta_y3_dict[idx-1] += delta_y3
            delta_y4_dict[idx-1] += delta_y4

    ideal_function_y1 = delta_y1_dict.index(min(delta_y1_dict)) + 1
    ideal_function_y2 = delta_y2_dict.index(min(delta_y2_dict)) + 1
    ideal_function_y3 = delta_y3_dict.index(min(delta_y3_dict)) + 1
    ideal_function_y4 = delta_y4_dict.index(min(delta_y4_dict)) + 1

    return (ideal_function_y1, ideal_function_y2, ideal_function_y3, ideal_function_y4)

def max_delta_y(ideals, session):
    training_data = session.query(db.TrainingData).all()
    max_delta_y1 = None
    max_delta_y2 = None
    max_delta_y3 = None
    max_delta_y4 = None

    for data in training_data:
        ideal_functions = session.query(db.IdealFunction).filter(db.IdealFunction.X == data.X).all()
        if not ideal_functions:
            continue
        
        ideal_function_y1 = getattr(ideal_functions[0], f"Y{ideals[0]}")
        ideal_function_y2 = getattr(ideal_functions[0], f"Y{ideals[1]}")
        ideal_function_y3 = getattr(ideal_functions[0], f"Y{ideals[2]}")
        ideal_function_y4 = getattr(ideal_functions[0], f"Y{ideals[3]}")

        max_delta_y1 = abs(data.Y1 - ideal_function_y1) if max_delta_y1 is None else max(max_delta_y1, abs(data.Y1 - ideal_function_y1))
        max_delta_y2 = abs(data.Y2 - ideal_function_y2) if max_delta_y2 is None else max(max_delta_y2, abs(data.Y2 - ideal_function_y2))
        max_delta_y3 = abs(data.Y3 - ideal_function_y3) if max_delta_y3 is None else max(max_delta_y3, abs(data.Y3 - ideal_function_y3))
        max_delta_y4 = abs(data.Y4 - ideal_function_y4) if max_delta_y4 is None else max(max_delta_y4, abs(data.Y4 - ideal_function_y4))
    logging.info("Max delta Y values: %s, %s, %s, %s", max_delta_y1, max_delta_y2, max_delta_y3, max_delta_y4)
    return max_delta_y1, max_delta_y2, max_delta_y3, max_delta_y4   

def analyse_test_mapping(file_path, ideals, session):
    test_mappings = fh.TestMappingLoader(file_path)

    max_delta_y1, max_delta_y2, max_delta_y3, max_delta_y4 = max_delta_y(ideals, session)

    for line in test_mappings:
        x, y = line.strip().split(",")
        x = float(x)
        y = float(y)
        ideal_function = session.query(db.IdealFunction).filter(db.IdealFunction.X == x).first()
        if not ideal_function:
            continue
        
        ideal_function_y1 = getattr(ideal_function, f"Y{ideals[0]}")
        ideal_function_y2 = getattr(ideal_function, f"Y{ideals[1]}")
        ideal_function_y3 = getattr(ideal_function, f"Y{ideals[2]}")
        ideal_function_y4 = getattr(ideal_function, f"Y{ideals[3]}")

        testing_delta_y1 = abs(y - ideal_function_y1)
        testing_delta_y2 = abs(y - ideal_function_y2)
        testing_delta_y3 = abs(y - ideal_function_y3)
        testing_delta_y4 = abs(y - ideal_function_y4)   

        if testing_delta_y1 <= max_delta_y1 * m_sqrt_2:
            test_mappings.save_to_database(session,x,y,testing_delta_y1,f"Y{ideals[0]}")
        elif testing_delta_y2 <= max_delta_y2 * m_sqrt_2:
            test_mappings.save_to_database(session,x,y,testing_delta_y2,f"Y{ideals[1]}")
        elif testing_delta_y3 <= max_delta_y3 * m_sqrt_2:
            test_mappings.save_to_database(session,x,y,testing_delta_y3,f"Y{ideals[2]}")
        elif testing_delta_y4 <= max_delta_y4 * m_sqrt_2:
            test_mappings.save_to_database(session,x,y,testing_delta_y4,f"Y{ideals[3]}")
        else:
            test_mappings.save_to_database(session,x,y,None,None)


    return (max_delta_y1, max_delta_y2, max_delta_y3, max_delta_y4)

            