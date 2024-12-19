from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QLineEdit, QWidget, QErrorMessage
from PyQt6.QtGui import QPixmap, QMovie, QPainter, QAction
from PyQt6 import QtCore
import sys
import random
import sqlite3

from captainFalcon import MainWindow as MW


z: int = 70
i: int = 850
x: int = 810
y:int = 516
usr = ""
pas = ""

class SignInWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(SignInWindow, self).__init__()
        self.mainWidget = QWidget(self)
        self.setCentralWidget(self.mainWidget)



        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)


        label = QLabel(self)
        pixmap = QPixmap("pics/bg.png")
        resizePixmap = pixmap.scaled(i, i)
        label.setGeometry(0,0,x,y)
        label.setPixmap(resizePixmap)
        self.mainWidget = QWidget(self)
        self.mainWidget.setStyleSheet("border-radius: 10px;")
        self.setCentralWidget(self.mainWidget)

        col = random.randint(1,10)
        icn = random.randint(1,10)


        gifmap = QMovie("pics/img.gif")

        l1 = QLabel(self)
        l1.setMovie(gifmap)
        gifmap.start()
        l1.setFixedSize(500,500)
        l1.setScaledContents(True)
        gifmap.setSpeed(400)
        l1.move(300,8)
        butt = QPushButton(self)

        self.signInUser = QLineEdit(self)
        self.signInUser.cursorRect()
        self.signInUser.setGeometry(6, 342-z, 290, 50)
        self.signInUser.setPlaceholderText("Username")
        self.signInUser.setStyleSheet('''background-color: #232323;
                                 border-radius:5px;
                                 font-family: Cascadia Mono NF;
                                 font-size: 15px;
                                 padding: 10px;'''
                                 )

        self.signInPass = QLineEdit(self)
        self.signInPass.setGeometry(6, 400-z,290,50)
        self.signInPass.setPlaceholderText("Password")



        self.signInPass.setEchoMode(QLineEdit.EchoMode.Password)
        self.signInPass.setStyleSheet('''background-color: #232323;
                                 border-radius:5px; 
                                 font-family: Cascadia Mono NF;
                                 font-size: 15px;
                                 padding: 10px;'''
                                 )



        #420
        butt.setGeometry(6, 442, 290, 50)
        butt.setText("Sign In 󰌧")
        butt.clicked.connect(self.openApp)



        l4 = QLabel(self)
        l4.setText("")
        l4.setAlignment(Qt.AlignmentFlag.AlignCenter)
        l4.show()
        l4.setGeometry(100,50,100,100)


        enter = QAction()
        enter.setShortcut("Return")
        enter.triggered.connect(self.openApp)
        self.addAction(enter)


        icon_dict = {
            1: "",
            2: "",
            3: "",
            4: "",
            5: "",
            6: "",
            7: "",
            8: "󰠭",
            9: "󰟪",
            10: "פּ"
        }
        l4.setText(icon_dict[1])

        color_dict = {
            1: "#2d9ce6",
            2: "#c45000",
            3: "#e62db5",
            4: "#8e2de6",
            5: "#2de6c7",
            6: "#e62d2d",
            7: "#008083",
            8: "#e62da8",
            9: "#2db9e6"
        }
        butt.setStyleSheet(f"background-color: {color_dict[1]}; \
                            border-radius:5px; \
                            font-family:Cascadia Mono NF; \
                            font-size: 20px; \
                            color: #f4ead8;")


        l4.setStyleSheet(f"background-color:  {color_dict[1]}; \
                         border-radius:35px; \
                         font-family: Cascadia Mono NF;\
                         font-size: 50px;\
                         color: #f4ead8;")



        self.setWindowTitle("Rock my socks!")
        self.setFixedSize(x, y)


    def openApp(self):
        usr = self.signInUser.text()
        pas = self.signInPass.text()

        conMan = sqlite3.connect("Ref.sqlite")
        c = conMan.cursor()

        c.execute("SELECT * FROM user WHERE user_id = ? and user_password = ?", (usr,pas,) )
        check = c.fetchone()


        if usr == check[0] and pas == check[2]:

            self.window = MW()
            self.window.show()
            self.close()

        else:
            error = QErrorMessage(self)
            error.showMessage("Incorrect username or password")
            




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = SignInWindow()
    MainWindow.show()

    sys.exit(app.exec())

#N.B.  An unlimited amount of further steps to be taken.