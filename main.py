import sqlite3
import sys

from addEditCoffeeForm import Ui_Form as Ui2
from main1 import Ui_Form as Ui1
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem


class MyWidget(QWidget, Ui1):
    def __init__(self):
        super().__init__()
        self.new = Edit()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.run)
        self.pushButton_2.clicked.connect(self.edit)
        con = sqlite3.connect('data/coffee.sqlite')
        self.cur = con.cursor()

    def run(self):
        self.tableWidget.setColumnCount(7)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setHorizontalHeaderLabels(
            ['ID', 'Название сорта', 'Степень обжарки', 'Молотый / В зернах', 'Описание вкуса', 'Цена',
             'Объем упаковки'])
        result = self.cur.execute('select * from coffee').fetchall()
        self.tableWidget.setRowCount(len(result))
        for i in range(len(result)):
            for j in range(len(result[i])):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(result[i][j])))

    def edit(self):
        self.hide()
        self.new.show()


class Edit(QWidget, Ui2):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_2.clicked.connect(self.add_coffee)
        self.pushButton.clicked.connect(self.save)
        self.con = sqlite3.connect('data/coffee.sqlite')
        self.cur = self.con.cursor()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setHorizontalHeaderLabels(
            ['ID', 'Название сорта', 'Степень обжарки', 'Молотый / В зернах', 'Описание вкуса', 'Цена',
             'Объем упаковки'])
        result = self.cur.execute('select * from coffee').fetchall()
        self.row = len(result)
        self.tableWidget.setRowCount(self.row)
        for i in range(len(result)):
            for j in range(len(result[i])):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(result[i][j])))

    def add_coffee(self):
        self.row += 1
        self.cur.execute(f"""INSERT INTO coffee (id, Название_сорта, Степень_обжарки, Молотый_В_зернах, Описание_вкуса, 
        Цена, Объем_упаковки) VALUES ('{str(self.row)}', '', '', '', '', '', '')""")
        self.tableWidget.setRowCount(self.row)

    def save(self):
        for i in range(self.row):
            data = [self.tableWidget.item(i, x).text() for x in [1, 2, 3, 4, 5, 6, 0]]
            self.cur.execute(
                '''UPDATE coffee SET Название_сорта = ?, Степень_обжарки = ?, Молотый_В_зернах = ?,
                Описание_вкуса = ?, Цена = ?, Объем_упаковки = ? WHERE id = ?''',
                data)
        self.con.commit()
        self.hide()
        ex.show()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    sys.excepthook = except_hook
    ex.show()
    sys.exit(app.exec_())
