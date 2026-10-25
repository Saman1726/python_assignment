import bokeh.plotting as bp

def plot_data(data):
    plot = bp.figure(title=data.label, x_axis_label='x axis', y_axis_label='y axis')
    plot.line(data.x, data.y, legend_label=data.label, line_width=2)
    bp.show(plot)