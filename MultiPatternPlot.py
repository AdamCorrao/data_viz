'''
Script functionality:
Generalized tool to plot 1D data. GUI selection tool to pick data to plot. Mouse action options for plot interaction.
User edits 1st section where prompted for column delimiter, header/footer rows, and plot settings.
Options for systematic x/y offsets, axis labels, and plot dimensions. Error checks for data consistency and shape.
Compatible with any text file (e.g., .xy, .xye, .dat, .chi, .csv) or number of columns (i.e., x/y error columns)
Required libraries:
-Scientific computing libraries (e.g., NumPy, Pandas) ; matplotlib ; tkinter ; tkfilebrowser ; colorama ; mplcursors
-These libraries are all freely available and can be routinely installed (e.g., "pip install mplcursors")
Author: Adam A. Corrao
Date written: June 28th, 2022
Date last edited: October 21st, 2022
'''
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import mplcursors
import pandas as pd
import os
import tkfilebrowser
from tkinter import *
from tkinter import filedialog
import sys
from colorama import Fore, Back, init
mpl.rcParams['mathtext.default'] = 'regular'
init(autoreset=True)
os.system('cls')

#######################################Section for user to edit as needed###############################################
# data delimiter, header / footer rows
delim = ''  # delimiter in files to plot - defaulted as whitespace. change as needed (typically , or \t)
header_rows = 1  # number of header rows to ignore when reading files - defaulted to 1 assuming column labels to ignore
footer_rows = 0  # number of footer rows to ignore when reading files - defaulted to 0 assuming no footer

mouse_action = 'click'  # options are 'click' or 'hover' or 'None'
# click = left click line in plot for pop-up with label and x,y coords, right click to deselect
# hover = hover mouse over line in plot displays pop-up

# plot settings
x_offset = 0  # x-axis offset between patterns (from one to next)
y_offset = 100  # y-axis offset between patterns (from one to next)
x_axis_label = r'2$\theta$ (degrees)'  # x-axis label
y_axis_label = 'Intensity (counts)'  # y-axis label
plot_width = 7  # width of plot in inches. if set to 0, will plot with mpl default
plot_height = 7  # height of plot in inches. if set to 0, will plot with mpl default
max_legend_size = 10  # maximum number of legend entries (i.e. data files) - plotting more than this turns legend off


########################Automated data selection, reading, error checking, plotting below here##########################
# pattern select
txt_ext = '*.xy *.xye *.dat *.chi *.csv *.txt *.xls *.xlsx'
root = Tk()
root.geometry('200x200')
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
fullfiles = filedialog.askopenfilenames(initialdir='', filetypes=(('text files', txt_ext), ('all files', '*.*')))
files = []
filepaths = []
root.destroy()
if not fullfiles:
    print(Back.RED + 'No selection made\nPlease run script again\n')
    sys.exit()
else:
    for f in fullfiles:
        normfullfile = os.path.normpath(f)  # gives normalized filepath regardless of os or delimiter
        file = normfullfile.split(os.sep)[-1]  # splits on last instances of delimiter os.sep, gets filename
        filepath = normfullfile.partition(file)[0]
        files.append(file)
        filepaths.append(filepath)
    print(Fore.GREEN + 'File(s) selected: ')
    for file in files:
        print('\t' + file)

# creates arrays of x,y points for offset plotting. Rounds based on dec points given in x and y offset float / int
x_decpoints = len(str(x_offset).split('.')[-1])
y_decpoints = len(str(y_offset).split('.')[-1])
x_offset_array = np.round(np.linspace(0, ((len(files) - 1) * x_offset), len(files)), x_decpoints)
y_offset_array = np.round(np.linspace(0, ((len(files) - 1) * y_offset), len(files)), y_decpoints)

# Plot
numcolumns = []
for filepath, file in zip(filepaths, files):
    data = np.genfromtxt(filepath + os.sep + file, skip_header=header_rows, skip_footer=footer_rows, delimiter=delim)
    numcolumns.append(np.shape(data)[1])

if not all(numcolumns) is True:  # check to ensure that selected files have same number of columns
    print(Back.RED + 'Number of columns in selected files do not match\nData must have same number of columns\n')
    sys.exit()

if numcolumns[0] is 2 or numcolumns[0] is 3:  # if 2 or 3 columns, assumes x and y are 1st and 2nd, 3rd is Y error
    for filepath, file, x, y in zip(filepaths, files, x_offset_array, y_offset_array):
        data = np.genfromtxt(filepath + os.sep + file, skip_header=header_rows, skip_footer=footer_rows,
                             delimiter=delim)
        plt.plot((data[:, 0] + x), (data[:, 1] + y), label=file)

if numcolumns[0] >= 4:  # if 4 or more columns present, asks for user input to define x and y columns
    print(Fore.CYAN + '\n4 or more columns found in selected data')
    xcolumn = input(Fore.YELLOW + '\nWhich data column is the x-axis? Input pythonic index (e.g., first = 0, '
                                  'second = 1, ...) and press Enter\n')
    ycolumn = input(Fore.YELLOW + '\nWhich data column is the y-axis? Input pythonic index (e.g., first = 0, '
                                  'second = 1, ...) and press Enter\n')
    for filepath, file, x, y in zip(filepaths, files, x_offset_array, y_offset_array):
        data = np.genfromtxt(filepath + os.sep + file, skip_header=header_rows, skip_footer=footer_rows,
                             delimiter=delim)
        plt.plot((data[:, int(xcolumn)] + x), (data[:, int(ycolumn)] + y), label=file)
plt.xlabel(x_axis_label)
plt.ylabel(y_axis_label)

# mouse action
if mouse_action is 'click':
    mplcursors.cursor()
if mouse_action is 'hover':
    mplcursors.cursor(hover=True)

if len(files) > max_legend_size:
    print(Fore.RED + 'Number of legend entries exceeds user defined max legend size, no legend on plot')
else:
    plt.legend(loc='upper right')  # legend location can be changed as needed

if plot_width is 0 or plot_height is 0:
    print('Plot width or height is 0')
    plt.show()
else:
    plt.rcParams["figure.figsize"] = (plot_width, plot_height)
    plt.show()
