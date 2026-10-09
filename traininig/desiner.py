from PySide6.QtWidgets import (QApplication, QWidget, QLabel,
QPushButton, QHBoxLayout, QVBoxLayout , QLineEdit
)

app= QApplication()

window= QWidget()


window.setWindowTitle("From - [Preview] - Qt Dsiner")





label1= QLabel("User Name")
lineedit1= QLineEdit()

username = lineedit1.text()

label2= QLabel("Password")
lineedit2=QLineEdit()

password = lineedit2.text()

if username and password :
    print("you logged in!")
else:
    print("pls fill in both fields")

button1= QPushButton("Cancel")
button2= QPushButton("Confirm")


lo1= QHBoxLayout()
lo1.addWidget(label1)
lo1.addWidget(lineedit1)

lo2= QHBoxLayout()
lo2.addWidget(label2)
lo2.addWidget(lineedit2)

lo3= QHBoxLayout()
lo3.addWidget(button1)
lo3.addWidget(button2)

qvl= QVBoxLayout()
qvl.addLayout(lo1)
qvl.addLayout(lo2)
qvl.addLayout(lo3)

window.setLayout(qvl)

second_page= QWidget()

new_lbl= QLabel("you logged in!")


lo1_1= QHBoxLayout()
lo1_1.addWidget(new_lbl)

qvl2= QVBoxLayout()
qvl2.addLayout(lo1_1)

second_page.setLayout(qvl2)

secces_label= QLabel("you logged in", window)
secces_label.hide()

error_label= QLabel("", window)
error_label.hide()

def login():
    username = lineedit1.text()
    password = lineedit2.text()

    if username and password:
        error_label.hide()
        window.hide()
        second_page.show()
    else:
        error_label.setText("Please fill in both fields")
        error_label.show()

button2.clicked.connect(login)



window.show()

app.exec()
