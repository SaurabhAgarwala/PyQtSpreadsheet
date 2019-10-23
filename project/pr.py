import sys
import os
import csv
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QTableWidget, QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QFileDialog
from PyQt5.QtWidgets import qApp, QAction


class MyTable(QTableWidget):
    def __init__(self, r, c):
        super().__init__(r, c)
        self.check_change = True
        self.init_ui()

    def init_ui(self):
        # self.cellChanged.connect(self.c_current)
        self.show()

    def c_current(self):
        if self.check_change:
            print('Hello I am called')
            row = self.currentRow()
            col = self.currentColumn()
            value = self.item(row, col)
            value = value.text()
            print("The current cell is ", row, ", ", col)
            print("In this cell we have: ", value)

    def open_sheet(self):
        self.check_change = False
        path = QFileDialog.getOpenFileName(self, 'Open CSV', os.getenv('HOME'), 'CSV(*.csv)')
        if path[0] != '':
            with open(path[0], newline='') as csv_file:
                self.setRowCount(0)
                self.setColumnCount(10)
                my_file = csv.reader(csv_file, dialect='excel')
                for row_data in my_file:
                    row = self.rowCount()
                    self.insertRow(row)
                    if len(row_data) > 10:
                        self.setColumnCount(len(row_data))
                    for column, stuff in enumerate(row_data):
                        item = QTableWidgetItem(stuff)
                        self.setItem(row, column, item)
            self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.check_change = True

    def save_sheet(self):
        path = QFileDialog.getSaveFileName(self, 'Save CSV', os.getenv('HOME'), 'CSV(*.csv)')
        if path[0] != '':
            with open(path[0], 'w') as csv_file:
                writer = csv.writer(csv_file, dialect='excel')
                for row in range(self.rowCount()):
                    row_data = []
                    for column in range(self.columnCount()):
                        item = self.item(row, column)
                        if item is not None:
                            row_data.append(item.text())
                        else:
                            row_data.append('')
                    writer.writerow(row_data)
            self.setEditTriggers(QTableWidget.NoEditTriggers)

    def edit_sheet(self):
        self.setEditTriggers(QTableWidget.DoubleClicked | QTableWidget.AnyKeyPressed)

    def add_data(self):
        self.check_change = False
        # print('add_data called')
        self.window = Window(self)
        self.check_change = True


class Window(QWidget):

    def __init__(self,table):
        super().__init__()
        self.table = table
        self.init_ui()

    def init_ui(self):
        self.label1 = QLabel('Enter the row number where data is to be inserted.')
        self.row_number = QLineEdit()
        self.label2 = QLabel('Enter the comma separated data corresponding to the entered row number')
        self.data = QLineEdit()
        self.add = QPushButton('Add Data')

        v_box = QVBoxLayout()
        v_box.addWidget(self.label1)
        v_box.addWidget(self.row_number)
        v_box.addWidget(self.label2)
        v_box.addWidget(self.data)
        v_box.addWidget(self.add)

        self.setLayout(v_box)
        self.setWindowTitle('Add New Data')

        self.add.clicked.connect(self.data_added)

        self.show()

    def data_added(self):
        self.row_number = int(self.row_number.text())
        self.data = self.data.text().split(',')
        self.table.insertRow(self.row_number-1)
        if len(self.data) > self.table.columnCount():
            self.table.setColumnCount(len(self.data))
        for column, stuff in enumerate(self.data):
            item = QTableWidgetItem(stuff)
            self.table.setItem(self.row_number-1, column, item)
        # print('data added completed')        
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.close()
        # print('data added closed')


class Sheet(QMainWindow):
    def __init__(self):
        super().__init__()

        self.form_widget = MyTable(100, 100)
        self.setCentralWidget(self.form_widget)

        # Set up menu
        bar = self.menuBar()
        
        file = bar.addMenu('&File')

        add_data_action = QAction('&Add Data',self)
        add_data_action.setShortcut('Ctrl+A')

        load_action = QAction('&Load', self)
        load_action.setShortcut('Ctrl+L')

        save_action = QAction('&Save', self)
        save_action.setShortcut('Ctrl+S')

        quit_action = QAction('&Quit', self)

        file.addAction(add_data_action)
        file.addAction(load_action)
        file.addAction(save_action)
        file.addAction(quit_action)

        add_data_action.triggered.connect(self.form_widget.add_data)
        load_action.triggered.connect(self.form_widget.open_sheet)
        save_action.triggered.connect(self.form_widget.save_sheet)
        quit_action.triggered.connect(self.quit_app)


        edit = bar.addMenu('&Edit')

        edit_action = QAction('&Edit Data',self)
        edit_action.setShortcut('Ctrl+E')

        edit.addAction(edit_action)

        edit_action.triggered.connect(self.form_widget.edit_sheet)

        self.show()

    def quit_app(self):
        qApp.quit()

app = QApplication(sys.argv)
sheet = Sheet()
sys.exit(app.exec_())
