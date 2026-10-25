import bokeh.plotting as bp
from bokeh.models import HoverTool
import database as db
import numpy as np
import logging

m_sqrt_2 = np.sqrt(2)

def plot_data(session,ideals,max_allowed):
    bp.output_file("output/training.html")
    plot = bp.figure(title="Training Data", x_axis_label='x axis', y_axis_label='y axis')
    plot.add_tools(HoverTool(tooltips=[("X","@x"),("Y","@y")]))
    plot = plot_training_data(session,plot)
    plot = plot_ideal_functions(session,plot,ideals,max_allowed)
    plot = plot_test_mapping(session,plot,ideals)
    bp.show(plot)

def plot_training_data(session,plot):
    training_data = session.query(db.TrainingData).all()
    X = [data.X for data in training_data]
    Y1 = [data.Y1 for data in training_data]
    Y2 = [data.Y2 for data in training_data]
    Y3 = [data.Y3 for data in training_data]
    Y4 = [data.Y4 for data in training_data]

    plot.scatter(X, Y1, legend_label="Trainig Data Y1", size=7, color='red')
    plot.scatter(X, Y2, legend_label="Trainig Data Y2", size=7, color='green')
    plot.scatter(X, Y3, legend_label="Trainig Data Y3", size=7, color='blue')
    plot.scatter(X, Y4, legend_label="Trainig Data Y4", size=7, color='gold')

    return plot    

def plot_ideal_functions(session,plot,ideals,max_allowed):
    ideal_functions_data = session.query(db.IdealFunction).all()
    ideal_x = [data.X for data in ideal_functions_data]
    ideal_y1 = [getattr(data, f"Y{ideals[0]}") for data in ideal_functions_data]
    ideal_y2 = [getattr(data, f"Y{ideals[1]}") for data in ideal_functions_data]
    ideal_y3 = [getattr(data, f"Y{ideals[2]}") for data in ideal_functions_data]
    ideal_y4 = [getattr(data, f"Y{ideals[3]}") for data in ideal_functions_data]

    plot.line(ideal_x, ideal_y1, legend_label="Ideal F Y1", line_width=2, color='darkred')
    plot.line(ideal_x, ideal_y2, legend_label="Ideal F Y2", line_width=2, color='darkgreen')
    plot.line(ideal_x, ideal_y3, legend_label="Ideal F Y3", line_width=2, color='darkblue')
    plot.line(ideal_x, ideal_y4, legend_label="Ideal F Y4", line_width=2, color='darkorange')
    
    lower_y1 = [item - (max_allowed[0]*m_sqrt_2) for item in ideal_y1]
    lower_y2 = [item - (max_allowed[1]*m_sqrt_2) for item in ideal_y2]
    lower_y3 = [item - (max_allowed[2]*m_sqrt_2) for item in ideal_y3]
    lower_y4 = [item - (max_allowed[3]*m_sqrt_2) for item in ideal_y4]
    plot.line(ideal_x, lower_y1, line_dash="dashed", legend_label="Max Allowed Delta")
    plot.line(ideal_x, lower_y2, line_dash="dashed")
    plot.line(ideal_x, lower_y3, line_dash="dashed")
    plot.line(ideal_x, lower_y4, line_dash="dashed")

    upper_y1 = [item + (max_allowed[0]*m_sqrt_2) for item in ideal_y1]
    upper_y2 = [item + (max_allowed[1]*m_sqrt_2) for item in ideal_y2]
    upper_y3 = [item + (max_allowed[2]*m_sqrt_2) for item in ideal_y3]
    upper_y4 = [item + (max_allowed[3]*m_sqrt_2) for item in ideal_y4]
    plot.line(ideal_x, upper_y1, line_dash="dashed")
    plot.line(ideal_x, upper_y2, line_dash="dashed")
    plot.line(ideal_x, upper_y3, line_dash="dashed")
    plot.line(ideal_x, upper_y4, line_dash="dashed")
    
    return plot

def plot_test_mapping(session,plot,ideals):
    test_mapping = session.query(db.TestMapping).all()
    xy1 = {}
    xy2 = {}
    xy3 = {}
    xy4 = {}
    xy_none = {}
    xy_delta_upper = {}
    xy_delta_lower = {}
    for mapping in test_mapping:
        if f"Y{ideals[0]}" == mapping.Ideal_Function_Y:
            xy1[mapping.X] = mapping.Y
            xy_delta_upper[mapping.X] = mapping.Y + mapping.Delta_Y
            xy_delta_lower[mapping.X] = mapping.Y - mapping.Delta_Y
        elif f"Y{ideals[1]}" == mapping.Ideal_Function_Y:
            xy2[mapping.X] = mapping.Y
            xy_delta_upper[mapping.X] = mapping.Y + mapping.Delta_Y
            xy_delta_lower[mapping.X] = mapping.Y - mapping.Delta_Y
        elif f"Y{ideals[2]}" == mapping.Ideal_Function_Y:
            xy3[mapping.X] = mapping.Y
            xy_delta_upper[mapping.X] = mapping.Y + mapping.Delta_Y
            xy_delta_lower[mapping.X] = mapping.Y - mapping.Delta_Y
        elif f"Y{ideals[3]}" == mapping.Ideal_Function_Y:
            xy4[mapping.X] = mapping.Y
            xy_delta_upper[mapping.X] = mapping.Y + mapping.Delta_Y
            xy_delta_lower[mapping.X] = mapping.Y - mapping.Delta_Y
        else:
            xy_none[mapping.X] = mapping.Y

    plot.scatter(list(xy1.keys()), list(xy1.values()), marker='triangle', legend_label="Test Data Y1", size=7, color='darkred')
    plot.scatter(list(xy2.keys()), list(xy2.values()), marker='triangle',legend_label="Test Data Y2", size=7, color='darkgreen')
    plot.scatter(list(xy3.keys()), list(xy3.values()), marker='triangle',legend_label="Test Data Y3", size=7, color='darkblue')
    plot.scatter(list(xy4.keys()), list(xy4.values()), marker='triangle',legend_label="Test Data Y4", size=7, color='darkorange')

    plot.scatter(list(xy_none.keys()), list(xy_none.values()), marker='x',legend_label="Test Data not assigned", size=7, color='black')
    plot.scatter(list(xy_delta_upper.keys()), list(xy_delta_upper.values()), marker='square', legend_label="Test Delta Higher", size=7, color='violet')
    plot.scatter(list(xy_delta_lower.keys()), list(xy_delta_lower.values()), marker='square', legend_label="Test Delta Lower", size=7, color='gray')
    return plot    


    