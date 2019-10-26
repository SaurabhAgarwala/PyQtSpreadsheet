###############################################################################
# 
# Spreadsheet Application
# 
# Written by Saurabh Agarwala (saur.agarwala@gmail.com, 171it237.saurabh@nitk.edu.in)
#
# Github Repo: https://github.com/SaurabhAgarwala/PyQtSpreadsheet 
#
###############################################################################

import sys
import os
import csv
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget,\
     QTableWidget, QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QFileDialog
from PyQt5.QtWidgets import qApp, QAction


# Defining the main application window
class Sheet(QMainWindow):
    def __init__(self):
        # Initiliasing from parent class
        super().__init__()

        # Creating the spreadsheet table with 100 rows and 100 columns
        self.form_widget = MyTable(100, 100)         
        self.setCentralWidget(self.form_widget)
        self.setWindowTitle('The Spreadsheet')
        self.setGeometry(250,150,1000,600)

        # Menu Bar setup
        bar = self.menuBar()
        
        # Creating File menu
        file = bar.addMenu('&File')

        # Creating File menu options
        # Creating Add Data option of File menu
        add_data_action = QAction('&Add Data',self)
        add_data_action.setShortcut('Ctrl+A')

        # Creating Load option of File menu
        load_action = QAction('&Load', self)
        load_action.setShortcut('Ctrl+L')

        # Creating Save option of File menu
        save_action = QAction('&Save', self)
        save_action.setShortcut('Ctrl+S')

        # Creating Quit option of File menu
        quit_action = QAction('&Quit', self)
        quit_action.setShortcut('Ctrl+Q')

        # Adding options to the File menu
        file.addAction(add_data_action)
        file.addAction(load_action)
        file.addAction(save_action)
        file.addAction(quit_action)

        # Linking File menu options created with their corresponding actions
        add_data_action.triggered.connect(self.form_widget.add_data)
        load_action.triggered.connect(self.form_widget.open_sheet)
        save_action.triggered.connect(self.form_widget.save_sheet)
        quit_action.triggered.connect(self.quit_app)


        # Creating Edit menu
        edit = bar.addMenu('&Edit')

        # Creating Edit Data option of Edit menu
        edit_action = QAction('&Edit Data',self)
        edit_action.setShortcut('Ctrl+E')

        # Adding Edit Data option to the File menu
        edit.addAction(edit_action)

        # Linking Edit Data option with its corresponding action
        edit_action.triggered.connect(self.form_widget.edit_sheet)


        # Creating Plot menu
        plot = bar.addMenu('&Plot')
        
        # Creating Plot Data option of the Plot menu
        plot_action = QAction('&Plot Data',self)
        plot_action.setShortcut('Ctrl+P')

         # Adding Plot Data option to the Plot menu
        plot.addAction(plot_action)

        # Linking Plot Data option with its corresponding action        
        plot_action.triggered.connect(self.form_widget.plot_graph)

        # Calling the application to show up
        self.show()

    # Defining Quit Application option under File menu
    def quit_app(self):
        qApp.quit()


# Defining the spreadsheet table
class MyTable(QTableWidget):
    
    # Setting up the table with the passed number of rows and columns
    def __init__(self, r, c):
        super().__init__(r, c)
        # Calling the table to show up in the main application window.
        self.show()

    # Defining the Load option under the File menu
    def open_sheet(self):
        # Triggering the load file dialog box with HOME as the defalut location and .csv files filtered
        path = QFileDialog.getOpenFileName(self, 'Open CSV', os.getenv('HOME'), 'CSV(*.csv)')
        if path[0] != '':
            # Reading the data from the opened .csv file
            with open(path[0], newline='') as csv_file:
                self.setRowCount(0)
                self.setColumnCount(10)
                my_file = csv.reader(csv_file, dialect='excel')
                # Populating the spreadsheet table with the read data
                for row_data in my_file:
                    row = self.rowCount()
                    self.insertRow(row)
                    if len(row_data) > 10:
                        self.setColumnCount(len(row_data))
                    for column, stuff in enumerate(row_data):
                        item = QTableWidgetItem(stuff)
                        self.setItem(row, column, item)
            # Making the populated spreadsheet Read-Only                        
            self.setEditTriggers(QTableWidget.NoEditTriggers)

    # Defining the Save option under the File menu
    def save_sheet(self):
        # Triggering the save file as CSV dialog box with HOME as the default location and .csv files filtered
        path = QFileDialog.getSaveFileName(self, 'Save CSV', os.getenv('HOME'), 'CSV(*.csv)')
        if path[0] != '':
            with open(path[0], 'w') as csv_file:
                writer = csv.writer(csv_file, dialect='excel')
                # Saving the data of the spreadsheet table in a file
                for row in range(self.rowCount()):
                    row_data = []
                    for column in range(self.columnCount()):
                        item = self.item(row, column)
                        if item is not None:
                            row_data.append(item.text())
                        else:
                            row_data.append('')
                    writer.writerow(row_data)
            # Making the spreadsheet Read-Only                        
            self.setEditTriggers(QTableWidget.NoEditTriggers)

    # Defining the Add Data option under the File menu
    def add_data(self):
        # Calling the Add Data Window to add new data and passing this table object to it
        self.add_data_window = AddDataWindow(self)
    
    # Defining the Edit Data option under the File menu
    def edit_sheet(self):
        # Making the spreadsheet editable which enables editing a cell by selecting it 
        # and typing or double clicking it
        self.setEditTriggers(QTableWidget.DoubleClicked | QTableWidget.AnyKeyPressed)
    
    # Defining the Plot Data option under the Plot menu
    def plot_graph(self):
        # Extracting the data objects from the selected cells
        data = self.selectedItems()
        # Extracting text from the selected data objects
        d = [(dt.text()) for dt in data]
        # Splitting the extracted data into y-axis data and x-axis data
        d_len = len(d)
        yd = d[:d_len//2]
        xd = d[d_len//2:]
        # Removing the data of the blank cells
        while '' in yd:
            yd.remove('')
        while '' in xd:
            xd.remove('')
        # Converting the data into integer for plotting
        x = [int(i) for i in xd]
        y = [int(i) for i in yd]
        
        # Creating the Plot Graph window and passing the data of x and y axes to it
        self.plot_graph_window = PlotGraphWindow(x,y)


# Defining the Add Data Window
class AddDataWindow(QWidget):

    # Initializing the window
    def __init__(self,table):
        super().__init__()
        self.setWindowTitle('Add New Data')
        self.move(400,300)
        self.table = table
        self.init_ui()

    # Setting up the window widgets and layouts
    def init_ui(self):
        self.label1 = QLabel('Enter the row number where data is to be inserted.')
        self.row_number = QLineEdit()
        self.label2 = QLabel('Enter the comma separated data corresponding to the entered row number')
        self.data = QLineEdit()
        self.addData = QPushButton('Add Data')

        # Defining the window layout
        v_box = QVBoxLayout()
        v_box.addWidget(self.label1)
        v_box.addWidget(self.row_number)
        v_box.addWidget(self.label2)
        v_box.addWidget(self.data)
        v_box.addWidget(self.addData)

        # Setting up the window layout
        self.setLayout(v_box)

        # Linking Add Data button with its corresponding action        
        self.addData.clicked.connect(self.data_added)

        # Calling the window to show up
        self.show()

    # Defining the function for the Add Data button
    def data_added(self):
        self.row_number = int(self.row_number.text())
        self.data = self.data.text().split(',')
        # Creating a new row at the entered row number
        self.table.insertRow(self.row_number-1)
        if len(self.data) > self.table.columnCount():
            self.table.setColumnCount(len(self.data))
        # Populating the new row with the data entered
        for column, stuff in enumerate(self.data):
            item = QTableWidgetItem(stuff)
            self.table.setItem(self.row_number-1, column, item)
        # Making the spreadsheet Read-Only
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.close()


# Defining the Plot Graph Window
class PlotGraphWindow(QWidget):
    
    # Initializing the window    
    def __init__(self,xdata,ydata):
        super().__init__()
        self.setWindowTitle('Plot Graphs')
        self.xdata = xdata
        self.ydata = ydata
        self.xdata_str = str(xdata)
        self.ydata_str = str(ydata)
        self.init_ui()

    # Setting up the window widgets and layouts
    def init_ui(self):
        self.xdatalabel = QLabel('X-axis data: ' + self.xdata_str)
        self.ydatalabel = QLabel('Y-axis data: ' + self.ydata_str)
        self.title_label = QLabel('Enter the tilte of the plot:')
        self.title = QLineEdit()
        self.xlabels_label = QLabel('Enter the lable of the X-axis:')
        self.xlabel = QLineEdit()
        self.ylabels_label = QLabel('Enter the lable of the Y-axis:')
        self.ylabel = QLineEdit()
        self.plot_scatter = QPushButton('Plot Scatter Points')
        self.plot_scatter_line = QPushButton('Plot Scatter Points with Smooth Lines')
        self.plot_line = QPushButton('Plot Lines')

        # Defining the window layout
        v_box = QVBoxLayout()
        v_box.addWidget(self.xdatalabel)
        v_box.addWidget(self.ydatalabel)
        v_box.addWidget(self.title_label)
        v_box.addWidget(self.title)
        v_box.addWidget(self.xlabels_label)
        v_box.addWidget(self.xlabel)
        v_box.addWidget(self.ylabels_label)
        v_box.addWidget(self.ylabel)
        v_box.addWidget(self.plot_scatter)
        v_box.addWidget(self.plot_scatter_line)
        v_box.addWidget(self.plot_line)

        # Setting up the window layout
        self.setLayout(v_box)

        # Linking all Plot Graph buttons with their corresponding actions
        self.plot_scatter.clicked.connect(self.plotScatter)
        self.plot_scatter_line.clicked.connect(self.plotScatterLine)
        self.plot_line.clicked.connect(self.plotLine)

        # Calling the window to show up
        self.show()
    
    # Defining the functions setting the plot type for all Plot Graph buttons
    def plotScatter(self):
        self.plot_type = 'bo'
        self.plotGraph()

    def plotScatterLine(self):
        self.plot_type = '-bo'
        self.plotGraph()

    def plotLine(self):
        self.plot_type = '-b'
        self.plotGraph()

    # Defining the Plot Graph function
    def plotGraph(self): 
        plt.title(self.title.text())
        plt.xlabel(self.xlabel.text())
        plt.ylabel(self.ylabel.text())
        plt.plot(self.xdata,self.ydata,self.plot_type)
        # Showing the graph
        plt.show()    


# Creating and running the application
app = QApplication(sys.argv)
sheet = Sheet()
sys.exit(app.exec_())
