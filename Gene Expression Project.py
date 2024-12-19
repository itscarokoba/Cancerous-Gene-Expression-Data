import glob
import dearpygui.dearpygui as dpg
import pandas
from io import StringIO
import ctypes
import dearpygui.dearpygui as dpg

# Get screen dimensions.
user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

x_values = []
y_values = []
bioseries = "bioseries"

# X VALUES.
for i in range(400, 460):
    x_values.append(i)

# Dummy y VALUES.
for i in range(400, 460):
    y_values.append(-1)

# Read data set.
file_path = "Dataset.txt"
with open(file_path, 'r') as f:
    lines = f.readlines()

start_index = 0
line_number = 0

# Read amount of lines until table starts.
for line in lines:
    if(line.startswith("!series_matrix_table_begin")):
        start_index = line_number + 1
        break
    else:
        line_number += 1

# Lists all of the genes.
table_lines = lines[start_index: len(lines)-1]
data_str = "".join(table_lines)
df = pandas.read_csv(StringIO(data_str), sep="\t")
print(df)
gene_names = list(df["ID_REF"])

# Printing expression values.
def find_gene(gene_to_find):
    user_row = 0
    for i in range(len(df)):
        gene = df.loc[i]    
        if df.loc[i][0] == gene_to_find:    
            user_row = i
            break
    return user_row

# Title of window and screen dimensions.
dpg.create_context()
dpg.create_viewport(title='Caroline Kobayashi Cancer Study Analysis', x_pos=0, y_pos=0, width=screen_width, height=screen_height)
dpg.maximize_viewport()

# Axes and tag (tells dearpygui the variables associated with the axes) set up.
selected_value = None
y_axis_tag = "y_axis"
x_axis_tag = "x_axis"
def combo_callback(sender, app_data, user_data):
    new_y = []
    global selected_value
    selected_value = app_data
    print(f"New Selection: {selected_value}")
    gene_expression_values = df.loc[find_gene(selected_value)]
    for i in range(1, len(gene_expression_values)):
        new_y.append(gene_expression_values[i].item())
    dpg.configure_item(bioseries, y = new_y)
    dpg.set_axis_limits(x_axis_tag, 400, 453.5)
    dpg.set_axis_limits(y_axis_tag, 0, max(new_y))
    print(len(gene_expression_values))

# Overview of window set up.
with dpg.window(label="Example Window", tag="primary_window", no_title_bar=True, no_move=True, no_resize=True, no_collapse=True, no_close=True):
    dpg.add_text("Prostate and Breast Cancer Gene Expression Levels across Biosamples")
    dpg.add_text("Select a gene: ")
    dpg.add_same_line()
    dpg.add_combo(gene_names, callback = combo_callback)
    with dpg.plot(label = "Comparative Gene Expression Profiles Across Biosamples", height = 400, width = -1):
        dpg.add_plot_legend()
        #create x axis.
        dpg.add_plot_axis(dpg.mvXAxis, label="Biosamples",tag = x_axis_tag)
        #create y axis.
        dpg.add_plot_axis(dpg.mvYAxis, label="Expression Value", tag = y_axis_tag)
        dpg.add_scatter_series(x_values, y_values, parent=dpg.last_item(), id = bioseries)

# Dearpygui startup components.
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("primary_window", True)
dpg.start_dearpygui()
dpg.destroy_context()
file_path = "Dataset.txt"
with open(file_path, 'r') as f:
    lines = f.readlines()