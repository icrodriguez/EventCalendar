from PyQt5 import uic
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QApplication
import pickle

Form, Window = uic.loadUiType("tracker.ui")

app =QApplication([])
window = Window()
form =Form()
form.setupUi(window)
window.show()

def save_to_file():
    global start_date, calc_date, description
    # start_date = QDate(2020, 12, 1)
    data_to_save = {'start': start_date, 'end' : calc_date, 'desc': description}
    file1 = open('config.txt', "wb")
    pickle.dump(data_to_save, file1)
    file1.close()

def read_from_file():
    global start_date, calc_date, description, current_date
    try:
        file1 = open('config.txt', "rb")
        data_to_load = pickle.load(file1)
        file1.close()
        start_date = data_to_load['start']
        calc_date = data_to_load['end']
        description = data_to_load['desc']
        print(start_date.toString('dd-MM-yyyy'), calc_date.toString('dd-MM-yyyy'), description)
        form.calendarWidget.setSelectedDate(calc_date)
        form.dateEdit.setDate(calc_date)
        form.plainTextEdit.setPlainText(description)
        delta_days_left = start_date.daysTo(current_date)
        delta_days_right = current_date.daysTo(calc_date)
        days_total = start_date.daysTo(calc_date)
        print("Денечки: ", delta_days_left, delta_days_right, days_total)
        procent = int(delta_days_left * 100 / days_total)
        print(procent)
        form.progressBar.setProperty("value", procent)
    except:
        print('не могу прочитать файл')



def on_click():
    global calc_date, description, start_date
    start_date = current_date
    calc_date = form.calendarWidget.selectedDate()
    description = form.plainTextEdit.toPlainText()
    # print(form.plainTextEdit.toPlainText())
    # print(form.dateEdit.dateTime().toString('dd-MM-yyyy'))
    print('clicked!')
    save_to_file()

def on_click_calendar():
    global start_date, calc_date
    # print(form.calendarWidget.selectedDate().toString('dd-MM-yyyy'))
    form.dateEdit.setDate(form.calendarWidget.selectedDate())
    calc_date = form.calendarWidget.selectedDate()
    delta_days = start_date.daysTo(calc_date)
    print(delta_days)
    form.label_3.setText("%s Days until Event" % delta_days)



def on_dateedit_change():
    global start_date, calc_date
    # print(form.dateEdit.dateTime().toString('dd-MM-yyyy'))
    form.calendarWidget.setSelectedDate(form.dateEdit.date())
    calc_date = form.dateEdit.date()
    delta_days = start_date.daysTo(calc_date)
    print(delta_days)
    form.label_3.setText("%s Days until Event" % delta_days)



form.pushButton.clicked.connect(on_click)
form.calendarWidget.clicked.connect(on_click_calendar)
form.dateEdit.dateChanged.connect(on_dateedit_change)


start_date = form.calendarWidget.selectedDate()
current_date = form.calendarWidget.selectedDate()
calc_date = form.calendarWidget.selectedDate()
description = form.plainTextEdit.toPlainText()
read_from_file()
form.label.setText("Event from %s" % start_date.toString('dd-MM-yyyy'))
on_click_calendar()

app.exec_()