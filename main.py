import sys
from turtle import color
import xalglib
from qt_ui              import Ui_MainWindow
from PyQt5              import (QtWidgets    as qtw,
                                QtCore       as qtc)
from PyQt5.QtWidgets    import QFileDialog, QTableWidgetItem 
from pandas             import (read_csv, DataFrame)

class window (qtw.QMainWindow,Ui_MainWindow):
    def __init__(self, *args, **kwargs) :
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.fopen.triggered.connect(self.F_Open)
        self.setWindowTitle("Hi_course")
        self.plrand.triggered.connect(self.plot_data)

    def F_Open(self):
        headers=["X","Y"]
        path=QFileDialog.getOpenFileName(filter="CSV(*.csv)")[0]; 
        data=read_csv(path,delimiter=";",header=None,names=headers)
        numRows=len(data.index)
        self.table.setColumnCount(len(data.columns))
        self.table.setRowCount(numRows)
        
        self.table.setHorizontalHeaderLabels(headers)
        for i in range(numRows):
            for j in range(len(data.columns)):
                self.table.setItem(i,j,QTableWidgetItem(str(data.iat[i,j])))
        self.table.resizeColumnsToContents()
        print(path)
        self.plot_data(data)

    def plot_data(self,data=DataFrame):
        print(data)
        self.plot.canvas.ax.grid(True)
        self.plot.canvas.ax.scatter(data["X"], data["Y"],color="red")
        self.plot.canvas.draw()


if __name__=='__main__':
    app=qtw.QApplication([])
    window=window()
    window.show()
    app.exec()