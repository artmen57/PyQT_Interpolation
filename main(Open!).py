import xalglib
import numpy as np
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
        self.Her_spl.stateChanged.connect(self.change)
        self.CR_spl.stateChanged.connect(self.change)
        self.Cub_spl.stateChanged.connect(self.change)
        self.Aki_spl.stateChanged.connect(self.change)
        self.mon_spl.stateChanged.connect(self.change)
        self.lin_spl.stateChanged.connect(self.change)
        
    def change(self,int):
        try:
            if self.Her_spl.isChecked()==True:
                self.plot_data(self.data)
            elif self.lin_spl.isChecked()==True:
                self.plot_data(self.data)
            elif self.CR_spl.isChecked()==True:
                self.plot_data(self.data)
            elif self.Cub_spl.isChecked()==True:
                self.plot_data(self.data)
            elif self.Aki_spl.isChecked()==True:
                self.plot_data(self.data)
            elif self.mon_spl.isChecked()==True:
                self.plot_data(self.data)
            else:
                self.plot_data(self.data)
        except Exception as e:
            print(e);pass    

    def F_Open(self):
        headers=["X","Y"]
        path=QFileDialog.getOpenFileName(filter="CSV(*.csv)")[0]; 
        self.data=read_csv(path,delimiter=";",header=None,names=headers)
        numRows=len(self.data.index)
        self.table.setColumnCount(len(self.data.columns))
        self.table.setRowCount(numRows)
        self.table.setHorizontalHeaderLabels(headers)
        for i in range(numRows):
            for j in range(len(self.data.columns)):
                self.table.setItem(i,j,QTableWidgetItem(str(self.data.iat[i,j])))
        self.table.resizeColumnsToContents()
        print(path)
        self.plot_data(self.data)
        
    def plot_data(self,data=DataFrame):
        x=data["X"].to_list()
        y=data["Y"].to_list()
        x2 =np.linspace(min(x), max(x), 500)
        
        if self.Her_spl.isChecked()==True:
            s2=xalglib.spline1dbuildhermite(x,y)
            y22 = np.array([xalglib.spline1dcalc(s2, x) for x in x2])
            self.plot.canvas.ax.plot(x2, y22,color="red")
        elif self.lin_spl.isChecked()==True:
            s2=xalglib.spline1dbuildlinear(x,y)
            y22 = np.array([xalglib.spline1dcalc(s2, x) for x in x2])
            self.plot.canvas.ax.plot(x2, y22,color="yellow")
        elif self.CR_spl.isChecked()==True:
            s2=xalglib.spline1dbuildcatmullrom(x,y)
            y22 = np.array([xalglib.spline1dcalc(s2, x) for x in x2])
            self.plot.canvas.ax.plot(x2, y22,color="orange")
        elif self.Cub_spl.isChecked()==True:
            s2=xalglib.spline1dbuildcubic(x,y)
            y22 = np.array([xalglib.spline1dcalc(s2, x) for x in x2])
            self.plot.canvas.ax.plot(x2, y22, label='cubic')
        elif self.Aki_spl.isChecked()==True:
            s2=xalglib.spline1dbuildakima(x,y)
            y22 = np.array([xalglib.spline1dcalc(s2, x) for x in x2])
            self.plot.canvas.ax.plot(x2, y22,color="green")
        elif self.mon_spl.isChecked()==True:
            s2=xalglib.spline1dbuildmonotone(x,y)
            y22 = np.array([xalglib.spline1dcalc(s2, x) for x in x2])
            self.plot.canvas.ax.plot(x2, y22,color="black")
        else:
            self.plot.canvas.ax.clear()
        self.plot.canvas.ax.grid(True)
        self.plot.canvas.ax.scatter(x, y,color="blue")
        self.plot.canvas.draw()
    
if __name__=='__main__':
    app=qtw.QApplication([])
    window=window()
    window.show()
    app.exec()