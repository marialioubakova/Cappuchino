import sqlite3
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget,QMessageBox
from addEditCoffeeForm import Ui_MainWindow
from add import Ui_Form

class SecondForm(QWidget, Ui_Form):
    def __init__(self,*args):

        super().__init__()
        self.row=args[-1]
        self.con = sqlite3.connect("coffee.db")
        self.setupUi(self)
        self.load()


    def load(self):
        cur = [res[0] for res in self.con.cursor().execute("""SELECT title FROM Degree_of_roasting""")]
        self.comboBox.addItems(cur)
        self.comboBox.setCurrentText(self.row[2])
        #self.comboBox.setText(self.row[2])
        self.spinBox.setValue(int(self.row[3]))
        self.lineEdit.setText(self.row[1])
        self.update()
        self.degres = [res[0] for res in self.con.cursor().execute("""SELECT title FROM Degree_of_roasting""")]
        self.comboBox.addItems(self.degres)

        self.pushButton.clicked.connect(self.change_save)
        self.close()


    def change_save(self):
        cur = self.con.cursor()
        deg = self.degres.index(self.comboBox.currentText()) + 1
        title = self.lineEdit.text()
        vol = self.spinBox.value()
        if title=='' or vol==0:
            msg = QMessageBox(self)
            msg.setText('Введите данные')

            msg.show()
        else:
            if self.row[1]=='':
                f = 'INSERT INTO Sorts_cofee (id,name,degree,volum)\
                            VALUES ({},"{}",{},{})'.format(self.row[0], title,deg,vol)
            else:

                f = 'UPDATE Sorts_cofee SET name="{}",' \
                    'degree = {},volum = {} WHERE ID = {}'.format(title,deg,vol,self.row[0])

            print(f)
            cur.execute(f)
            self.con.commit()
            self.close()



class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect("coffee.db")
        #self.pushButton_2.clicked.connect(self.show_result)
        self.pushButton_4.clicked.connect(self.open_second_form)
        self.pushButton.clicked.connect(self.show_result)
        self.pushButton_3.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.dele)

        self.titles = None

    def dele(self):
        try:
            if self.tableWidget.currentRow()<0:
                msg = QMessageBox(self)
                msg.setText('Нет выделенных элементов')

                msg.show()
            else:
                i = self.tableWidget.currentRow()
                print(i)
                f = 'DELETE FROM Sorts_cofee WHERE ID = {}'.format(int(i+1))
                print(f)
                cur = self.con.cursor()
                cur.execute(f)
                self.con.commit()
        except BaseException as el:
            print(el)


    def open_second_form(self):
        if self.tableWidget.currentRow()<0:
            msg = QMessageBox(self)
            msg.setText('Нет выделенных элементов')

            msg.show()
        else:
            i=self.tableWidget.currentRow()
            #rows = list(set([i.row() for i in self.tableWidget.selectedItems()])) #номера выделенных строк
            #ids = [self.tableWidget.item(i, 0).text() for i in rows]
            #row = self.tableWidget.selectedItems()
            row = [i+1]
            for j  in range(1,4):
                row.append(self.tableWidget.item(i, j).text())
            print(row)

            self.second_form = SecondForm(self,row)
            self.second_form.show()

    def add(self):
        max_id = self.tableWidget.rowCount()+1
        print('max_id',max_id)
        row=[max_id,'','',0]


        self.second_form = SecondForm(self,row)
        self.second_form.show()

    # показать таблицу
    def show_result(self):
        try:
            cur = self.con.cursor()
            res = cur.execute("""SELECT Sorts_cofee.ID, 
            name,
            Degree_of_roasting.title AS degree,
            volum
            FROM Sorts_cofee 
            INNER JOIN Degree_of_roasting 
            ON Degree_of_roasting.id = Sorts_cofee.degree""").fetchall()
            self.tableWidget.setHorizontalHeaderLabels(['id', 'name', 'degree', 'volum'])
            self.tableWidget.setRowCount(len(res))
            self.tableWidget.setColumnCount(4)
            for i, elem in enumerate(res):
                print(elem)
                for j, val in enumerate(elem):
                    print(val)
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        except BaseException as el:
            print('*', el)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
