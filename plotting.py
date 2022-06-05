from motion_capture import df
from bokeh.plotting import figure, show, output_file

p=figure(x_axis_type="datetime",height=100,width=500,sizing_mode = "scale_width", title="Motion Graph")
p.yaxis.minor_tick_line_color=None #removes horizontal lines from y axis
p.yaxis.ticker.desired_num_ticks=1 #removes scale from y grid

q=p.quad(left=df["Start"],right=df["End"],bottom=0,top=1,color="green")

output_file("Graph.html")
show(p)