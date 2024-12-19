import os, sqlite3, sys, datetime

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QLabel, QPushButton, QLineEdit, QWidget, QTableWidget, QTableWidgetItem, QMdiArea,
                             QHBoxLayout, QSizePolicy,QToolBar,
                             QCheckBox, QMdiSubWindow, QComboBox, QTextEdit, QVBoxLayout, QDialog, QHeaderView,
                             QMessageBox, QErrorMessage,
                             )
from PyQt6.QtGui import QPixmap, QAction, QCloseEvent, QTextTable, QKeySequence, QShortcut
from PyQt6 import QtGui, QtWidgets, QtCore

gh, i, x, y, z =450, 850, 1300, 800, 30
titleKol = "background-color: #008083;"
pageKol = "background-color: rgba(14,42,55,255);"

kool = (f"font-family: Cascadia Mono NF;"
        f"background-color: #191919;"
        f"color: #ffffff")

komboKol = (f"font-family: Cascadia Mono NF;"
            f"background-color: #232323;"
            f"color: #ffffff")




class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        self.confirm_close = True
        super(MainWindow, self).__init__()
        self.mainWidget = QWidget(self)
        self.setCentralWidget(self.mainWidget)

        self.dialog = None


        # self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        # self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        # self.lineBacker()
        self.setStyleSheet(f"font-family: Cascadia Mono NF;"
                           f"color:#ffffff;"
                           f"background-color:off")


        self.lineBacker()


        wid = QWidget(self)
        screen = QVBoxLayout(wid)
        screen.setSpacing(0)
        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)
        search = QHBoxLayout()
        search.setSpacing(0)
        self.searchBar = QTableWidget()
        self.searchBar.setStyleSheet("background-color: off;")
        self.searchBar.setColumnCount(11)
        self.searchBar.setRowCount(1)
        self.searchBar.setFixedSize(1000, 34)

        self.next = QPushButton("Next Page")
        self.next.clicked.connect(self.pageFlip)

        self.notepad = QVBoxLayout()
        self.notepad.setSpacing(0)
        self.notepad.setContentsMargins(1, 1, 1, 1)




        #table view switch
        toggleViewShortcut = QAction(self)
        toggleViewShortcut.setShortcut("Tab")
        toggleViewShortcut.triggered.connect(self.tabSwitch)
        self.addAction(toggleViewShortcut)


        self.refer = QTableWidget(self)
        self.refer.setColumnCount(13)
        self.refer.setRowCount(0)
        self.refer.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.refer.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)

        self.refer.horizontalHeader().setStretchLastSection(True)
        self.refer.horizontalHeader().setVisible(True)
        self.refer.verticalHeader().setVisible(False)
        self.refer.setHorizontalHeaderLabels(['Ref #', 'Name', 'Title', 'Type', 'Author(s)', 'Year', 'Subject', 'Notes',
                                              'Bibliography', 'Status', 'Importance', 'Created Date', 'Last Edit'])
        self.refer.verticalScrollBar().setFixedSize(0, 0)
        self.refer.horizontalScrollBar().setFixedSize(0, 0)

        self.refer.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignLeft)
        self.refer.horizontalHeader().setStyleSheet(titleKol)
        self.refer.setStyleSheet(pageKol + """
               font-family: Cascadia Mono NF;
               font-size:15px ;
               """)
        self.refer.setColumnWidth(0, 70)
        self.refer.setColumnWidth(4, 175)
        self.refer.setColumnWidth(8, 200)
        self.refer.setColumnWidth(11, 120)
        self.refer.setColumnWidth(12, 120)

        if not self.emptyTable():
            self.loadTable()

        #search bar
        self.reference_No = QLineEdit(self)
        self.reference_No.setPlaceholderText("Reference #")
        self.reference_No.setStyleSheet(kool)
        self.reference_Name = QLineEdit(self)
        self.reference_Name.setPlaceholderText("Name")
        self.reference_Name.setStyleSheet(kool)
        self.reference_Title = QLineEdit(self)
        self.reference_Title.setPlaceholderText("Title")
        self.reference_Title.setStyleSheet(kool)
        self.reference_Type_Code = QComboBox(self)
        self.reference_Type_Code.setStyleSheet(komboKol)
        self.reference_Type_Code.setPlaceholderText("Type")
        self.reference_Type_Code.addItems(['Audiobook', 'Book', 'Bookshelf', 'Documentary', 'E-Book', 'Journal Article', 'Video'])
        self.authors = QLineEdit(self)
        self.authors.setPlaceholderText("Author(s)")
        self.authors.setStyleSheet(kool)
        self.year_Of_Publication = QLineEdit(self)
        self.year_Of_Publication.setPlaceholderText("Year")
        self.year_Of_Publication.setStyleSheet(kool)
        self.subject_Code = QComboBox(self)
        self.subject_Code.setPlaceholderText("Subject")
        self.subject_Code.addItems(self.db2subj())
        self.subject_Code.setStyleSheet(komboKol)
        self.reference_Status = QComboBox(self)
        self.reference_Status.setPlaceholderText("Status")
        self.reference_Status.setStyleSheet(komboKol)
        self.reference_Status.addItems(["Draft", "Read", "Cite More", "Cited"])
        self.importance = QComboBox(self)
        self.importance.setPlaceholderText("Importance")
        self.importance.addItems(["", "", "", "", ""])
        self.importance.setStyleSheet(komboKol)
        self.importance.setFixedWidth(125)

        self.dlt = QPushButton(self)
        self.dlt.setGeometry(0, 0, 50, 50)
        self.dlt.setText("")
        self.dlt.clicked.connect(self.clearSearch)
        self.dlt.setStyleSheet("""
        font-family: Cascadia Mono NF;
        font-size: 40px;
        border-radius: 25px;
        """)

        self.gripper = QPushButton(self)
        self.gripper.setGeometry(0,0,50,50)
        self.gripper.setText("")
        self.gripper.clicked.connect(self.repGrip)
        self.gripper.setStyleSheet("""
        font-family: Cascadia Mono NF;
        font-size: 40px;
        border-radius: 25px;
        """)
        self.test = QPushButton(self)
        self.test.setGeometry(0,0,50,50)
        self.test.setText("")
        self.test.clicked.connect(self.repGrep)
        self.test.setStyleSheet("""
        font-family: Cascadia Mono NF;
        font-size: 40px;
        border-radius: 25px;
        """)



        self.nah = QPushButton(self)
        self.nah.setGeometry(0,0,50,50)
        self.nah.setText("")
        self.nah.clicked.connect(self.subjectation)
        self.nah.setStyleSheet("""
        font-family: Cascadia Mono NF;
        font-size: 40px;
        border-radius: 25px;
        """)




        self.srch = QPushButton(self)
        self.srch.setGeometry(0, 0, 50, 50)
        self.srch.setText("")
        self.srch.clicked.connect(self.search)
        self.srch.setStyleSheet("""
        font-family: Cascadia Mono NF;
        font-size: 40px;
        border-radius: 25px;
        """)

        search.addWidget(self.searchBar)
        search.addWidget(self.dlt)
        search.addWidget(self.gripper)
        search.addWidget(self.test)
        search.addWidget(self.nah)
        search.addWidget(self.srch)
        search.addWidget(self.next)



        #adjust of search bar
        self.searchBar.horizontalHeader().setVisible(False)
        self.searchBar.verticalHeader().setVisible(False)
        self.searchBar.setStyleSheet("background-color: transparent;")
        self.searchBar.hideColumn(7)
        self.searchBar.hideColumn(8)
        self.searchBar.setCellWidget(0, 0, self.reference_No)
        self.searchBar.setCellWidget(0, 1, self.reference_Name)
        self.searchBar.setCellWidget(0, 2, self.reference_Title)
        self.searchBar.setCellWidget(0, 3, self.reference_Type_Code)
        self.searchBar.setCellWidget(0, 4, self.authors)
        self.searchBar.setCellWidget(0, 5, self.year_Of_Publication)
        self.searchBar.setCellWidget(0, 6, self.subject_Code)
        self.searchBar.setCellWidget(0, 9, self.reference_Status)
        self.searchBar.setCellWidget(0, 10, self.importance)




        self.layout.addWidget(self.refer)

        self.layout.setContentsMargins(0, 1, 0, 1)
        screen.addLayout(search)
        screen.addLayout(self.layout)
        screen.setContentsMargins(1, 1, 1, 1)
        self.setCentralWidget(wid)
        self.setWindowTitle("Rock my socks!")
        self.resize(x,y)




    def toggleBoldFont(self):
        cursor = self.notion.textCursor()
        if cursor.hasSelection():
            currentCharFormat = cursor.charFormat()
            currentCharFormat.setFontWeight(
                600 if currentCharFormat.fontWeight() != 600 else 400)
            cursor.mergeCharFormat(currentCharFormat)

    def toggleItalicFont(self):
        cursor = self.notion.textCursor()
        if cursor.hasSelection():
            currentCharFormat = cursor.charFormat()
            currentCharFormat.setFontItalic(not currentCharFormat.fontItalic())
            cursor.mergeCharFormat(currentCharFormat)

    def toggleUnderlineFont(self):
        cursor = self.notion.textCursor()
        if cursor.hasSelection():
            currentCharFormat = cursor.charFormat()
            currentCharFormat.setFontUnderline(
                not currentCharFormat.fontUnderline())
            cursor.mergeCharFormat(currentCharFormat)

    def increaseFontSize(self):
        cursor = self.notion.textCursor()
        if cursor.hasSelection():
            currentCharFormat = cursor.charFormat()
            currentSize = currentCharFormat.fontPointSize() or 12
            currentCharFormat.setFontPointSize(currentSize + 2)
            cursor.mergeCharFormat(currentCharFormat)

    def decreaseFontSize(self):
        cursor = self.notion.textCursor()
        if cursor.hasSelection():
            currentCharFormat = cursor.charFormat()
            currentSize = currentCharFormat.fontPointSize() or 12
            newSize = max(2, currentSize - 2)
            currentCharFormat.setFontPointSize(newSize)
            cursor.mergeCharFormat(currentCharFormat)

    def createShortcuts(self):
        QShortcut(QKeySequence("Ctrl+B"), self, self.toggleBoldFont)

        QShortcut(QKeySequence("Ctrl+I"), self, self.toggleItalicFont)

        QShortcut(QKeySequence("Ctrl+U"), self, self.toggleUnderlineFont)

        QShortcut(QKeySequence("Ctrl+Shift+="), self, self.increaseFontSize)

        QShortcut(QKeySequence("Ctrl+Shift+-"), self, self.decreaseFontSize)




    def openNote(self, Num):


        if hasattr(self, 'dialog') and self.dialog is not None:
            self.dialog.close()

        self.createShortcuts()


        for ranger in range(8, 13):
            self.refer.setColumnHidden(ranger, True)

        rowData = self.db2table("referee")


        self.notion = QTextEdit()



        self.notion.setFixedHeight(gh)
        self.notion.setHtml(rowData[Num][7])
        self.notion.setStyleSheet("background-color: dark gray;"
                                  "color: white;")
        self.notion.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.dialog = QDialog()
        self.dialog.setStyleSheet("background-color: off")
        self.layout.addWidget(self.dialog)
        self.dialog.setFixedWidth(600)
        self.dialog.setWindowTitle('Table Dialog')
        self.dialog.resize(1300, 600)

        refNum = QLabel(str(Num+1))











        self.listed = QTableWidget(13, 1)
        self.listed.setFixedHeight(900)
        self.listed.setStyleSheet("background-color: black;")
        self.listed.setVerticalHeaderLabels(['Ref #', 'Name', 'Title', 'Type', 'Author(s)', 'Year', 'Subject', 'Notes',
                                             'Bibliography', 'Status', 'Importance', 'Created Date', 'Last Edit'])
        self.listed.horizontalHeader().setVisible(False)
        self.listed.horizontalHeader().setStretchLastSection(True)
        clear = "background-color: none;"
        combo = QComboBox()
        combo.setStyleSheet(clear)
        combo.setPlaceholderText("-")
        combo.addItems(["", "", "", "", ""])
        combo.setCurrentIndex(int(rowData[Num][10]) - 1)

        typeBox = QComboBox()
        typeBox.setPlaceholderText("-")
        typeBox.setStyleSheet(clear)

        typeBox.addItems(['Audiobook', 'Book', 'Bookshelf', 'Documentary', 'E-Book', 'Journal Article', 'Video'])
        typeBox.setCurrentIndex(int(rowData[Num][3])-1)

        subject = QComboBox()
        subject.setPlaceholderText("-")
        subject.setStyleSheet(clear)
        subject.addItems(self.db2subj())


        subject.setCurrentIndex(int(rowData[Num][6]) - 1)

        status = QComboBox()
        status.setPlaceholderText("-")
        status.setStyleSheet(clear)
        status.addItems(["Draft", "Read", "Cite More", "Cited"])
        status.setCurrentIndex(int(rowData[Num][9]) - 1)

        NM = QTableWidgetItem(rowData[Num][1])
        RT = QTableWidgetItem(rowData[Num][2])
        AU = QTableWidgetItem(rowData[Num][4])
        YR = QTableWidgetItem(rowData[Num][5])
        BI = QTableWidgetItem(rowData[Num][8])

        DT = QLabel(rowData[Num][11])

        self.noEdit = QLabel()

        self.listed.setCellWidget(0, 0, refNum)
        self.listed.setItem(1, 0, NM)
        self.listed.setItem(2, 0, RT)
        self.listed.setCellWidget(3, 0, typeBox)
        self.listed.setItem(4, 0, AU)
        self.listed.setItem(5, 0, YR)
        self.listed.setCellWidget(6, 0, subject)
        self.listed.setCellWidget(7, 0, self.notion)
        self.listed.setItem(8, 0, BI)
        self.listed.setCellWidget(9, 0, status)
        self.listed.setCellWidget(10, 0, combo)
        self.listed.setCellWidget(11, 0, DT)
        self.listed.setCellWidget(12, 0, self.noEdit)



        self.listed.setRowHeight(7,gh)

        win = QVBoxLayout()
        foo = QVBoxLayout()
        foo.addWidget(self.listed)
        bar = QHBoxLayout()
        bar.setSpacing(0)
        foo.setSpacing(0)
        win.setSpacing(0)
        bar.setContentsMargins(0, 0, 0, 0)
        foo.setContentsMargins(0, 0, 0, 0)
        win.setContentsMargins(0, 0, 0, 0)

        self.cancel = QPushButton("Cancel")
        self.dlt = QPushButton("Delete")
        self.dlt.clicked.connect(lambda: self.garbageMan(Num))
        self.cancel.clicked.connect(self.closedShop)
        self.save = QPushButton("Save")
        self.save.clicked.connect(lambda: self.updateDB(Num))

        bar.addWidget(self.cancel)
        bar.addWidget(self.dlt)
        bar.addWidget(self.save)

        win.addLayout(bar)
        win.addLayout(foo)

        self.dialog.setLayout(win)
        self.dialog.exec()


    def garbageMan(self, Num):

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Icon.Warning)
        msgBox.setWindowTitle("Confirmation")
        msgBox.setText("Are you sure you want to delete this item?")
        msgBox.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        response = msgBox.exec()
        if response == QMessageBox.StandardButton.Yes:
            self.refer.removeRow(Num)
            conMan = sqlite3.connect("Ref.sqlite")
            c = conMan.cursor()
            c.execute('''DELETE FROM Referee WHERE ReferenceNum = ?''', (str(Num + 1),))
            conMan.commit()
            conMan.close()

            self.dialog.close()

            for i in range(self.refer.columnCount()):
                self.refer.setColumnHidden(i, False)





    def updateDB(self, Num):

        DateEdit = datetime.datetime.now()
        self.noEdit.setText(DateEdit.strftime("%B %d %Y %I:%M %p"))

        for i in range(13):
            self.refer.setColumnHidden(i,False)


        conMan = sqlite3.connect("Ref.sqlite")
        c = conMan.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS Referee
                     (ReferenceNum, Name, Title, Type, Authors, Year, Subject, Notes, Bibliography,
                     Status, Importance, CreatedDate, LastEdit)''')

        c.execute('''UPDATE Referee SET
                         ReferenceNum = ?, Name = ?, Title = ?, Type = ?, Authors = ?, Year = ?,
                         Subject = ?, Notes = ?, Bibliography = ?, Status = ?,
                         Importance = ?, CreatedDate = ?, LastEdit = ?
                         WHERE ReferenceNum = ?''', tuple(self.rowMaister()) + ((str(Num + 1),)))
        conMan.commit()
        conMan.close()


        self.dialog.close()


        col = self.refer.columnCount()

        rowData = self.db2table("referee")
        for j in range(col):
            if j in [3, 6, 9, 10]:
                self.refer.cellWidget(Num, j).setCurrentIndex(int(rowData[Num][j]) - 1)
                self.refer.cellWidget(Num, j).setEnabled(False)
            elif j in [0, 1, 2, 4, 5, 8, 11,12]:
                self.refer.setItem(Num, j, QTableWidgetItem(str(rowData[Num][j])))
            else:
                self.refer.setItem(Num, j, QTableWidgetItem(None))





    def repGrip(self):
        if hasattr(self, 'dialog') and self.dialog is not None:
            self.dialog.close()
        for ranger in range(8, 13):
            self.refer.setColumnHidden(ranger, True)

        self.notion = QTextEdit()
        self.notion.setFixedHeight(gh)
        self.notion.setStyleSheet("background-color: dark gray;"
                                  "color: white;")
        self.notion.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.dialog = QDialog()
        self.dialog.setStyleSheet("background-color: off")
        self.layout.addWidget(self.dialog)
        self.dialog.setFixedWidth(600)
        self.dialog.setWindowTitle('Table Dialog')
        self.dialog.resize(1300, 600)
        refNum = QLabel(str(self.refer.rowCount() + 1))

        self.createShortcuts()



        self.listed = QTableWidget(13, 1)
        self.listed.setFixedHeight(900)
        self.listed.setRowHeight(7,gh)
        self.listed.setStyleSheet("background-color: black;")
        self.listed.setVerticalHeaderLabels(['Ref #', 'Name', 'Title', 'Type', 'Author(s)', 'Year', 'Subject', 'Notes',
                                             'Bibliography', 'Status', 'Importance', 'Created Date', 'Last Edit'])
        self.listed.horizontalHeader().setVisible(False)
        self.listed.horizontalHeader().setStretchLastSection(True)
        clear = "background-color: none;"
        combo = QComboBox()
        combo.setStyleSheet(clear)
        combo.setPlaceholderText("-")
        combo.addItems(["", "", "", "", ""])


        typeBox = QComboBox()
        typeBox.setPlaceholderText("-")
        typeBox.setStyleSheet(clear)
        typeBox.addItems(['Audiobook', 'Book', 'Bookshelf', 'Documentary', 'E-Book', 'Journal Article', 'Video'])

        subject = QComboBox()
        subject.setPlaceholderText("-")
        subject.setStyleSheet(clear)
        subject.addItems(self.db2subj())

        status = QComboBox()
        status.setPlaceholderText("-")
        status.setStyleSheet(clear)
        status.addItems(["Draft", "Read", "Cite More", "Cited"])

        DateTime = datetime.datetime.now()
        DT = QLabel()
        DT.setText(DateTime.strftime("%B %d %Y %I:%M %p"))

        noEdit = QLabel("-")

        self.listed.setCellWidget(0, 0, refNum)
        self.listed.setCellWidget(3, 0, typeBox)
        self.listed.setCellWidget(6, 0, subject)
        self.listed.setCellWidget(7, 0, self.notion)
        self.listed.setCellWidget(9, 0, status)
        self.listed.setCellWidget(10, 0, combo)
        self.listed.setCellWidget(11, 0, DT)
        self.listed.setCellWidget(12, 0, noEdit)

        win = QVBoxLayout()
        foo = QVBoxLayout()
        foo.addWidget(self.listed)
        bar = QHBoxLayout()
        bar.setSpacing(0)
        foo.setSpacing(0)
        win.setSpacing(0)
        bar.setContentsMargins(0, 0, 0, 0)
        foo.setContentsMargins(0, 0, 0, 0)
        win.setContentsMargins(0, 0, 0, 0)

        self.cancel = QPushButton("Cancel")
        self.cancel.clicked.connect(self.closedShop)
        self.save = QPushButton("Save")
        self.save.clicked.connect(self.row2Db)

        bar.addWidget(self.cancel)
        bar.addWidget(self.save)

        win.addLayout(bar)
        win.addLayout(foo)
        self.dialog.setLayout(win)
        self.dialog.exec()

    def repGrep(self):
        if hasattr(self, 'dialog') and self.dialog is not None:
            self.dialog.close()

        self.dialog = QDialog()
        self.dialog.setStyleSheet("background-color: off")
        self.layout.addWidget(self.dialog)
        self.dialog.setFixedWidth(600)
        self.dialog.resize(1300, 600)


        self.system = QTableWidget(7, 2)
        self.system.horizontalHeader().setVisible(False)
        self.system.horizontalHeader().setStretchLastSection(True)
        self.comboAPP = QComboBox()
        self.comboAPP.addItems(["Dark Mode", "Light Mode"])
        self.system.setCellWidget(0, 1, self.comboAPP)
        self.system.setItem(1,1,QTableWidgetItem("Tab"))

        for ranger in range(8, 13):
            self.refer.setColumnHidden(ranger, True)


        self.system.setColumnWidth(0, 150)
        self.system.setItem(0, 0, QTableWidgetItem("Appearance"))
        self.system.setItem(1, 0, QTableWidgetItem("Tab Switch"))
        self.system.setItem(2, 0, QTableWidgetItem("Bold Font"))
        self.system.setItem(3, 0, QTableWidgetItem("Italic Font"))
        self.system.setItem(4, 0, QTableWidgetItem("Underline Font"))
        self.system.setItem(5, 0, QTableWidgetItem("Size Up Font"))
        self.system.setItem(6, 0, QTableWidgetItem("Size Down Font"))
        cancel = QPushButton("Cancel")
        cancel.clicked.connect(self.closedShop)

        


        save = QPushButton("Save")
        save.clicked.connect(self.updateGUI)

        win = QVBoxLayout()
        foo = QVBoxLayout()
        foo.addWidget(self.system)
        bar = QHBoxLayout()
        bar.addWidget(save)
        bar.addWidget(cancel)
        bar.setSpacing(0)
        foo.setSpacing(0)
        win.setSpacing(0)
        bar.setContentsMargins(0, 0, 0, 0)
        foo.setContentsMargins(0, 0, 0, 0)
        win.setContentsMargins(0, 0, 0, 0)

        win.addLayout(bar)
        win.addLayout(foo)
        self.dialog.setLayout(win)
        self.dialog.exec()


    def updateGUI(self):
        if self.comboAPP.currentIndex() == 0:
            self.setStyleSheet("background-color: #191919; color: #ffffff;")
            titleKol = "background-color: #008083;"
            pageKol = "background-color: rgba(14,42,55,255);"
            kool = (f"font-family: Cascadia Mono NF;"
                    f"background-color: #191919;"
                    f"color: #ffffff")

            komboKol = (f"font-family: Cascadia Mono NF;"
                        f"background-color: #232323;"
                        f"color: #ffffff")


        elif self.comboAPP == 1:
            self.setStyleSheet("background-color: #ffffff; color: #000000;")
            titleKol = "background-color: #ADD8E6;"
            pageKol = "background-color: rgba(255,255,255,255);"
            kool = (f"font-family: Cascadia Mono NF;"
                    f"background-color: #fbfbfb;"
                    f"color: #000000")

            komboKol = (f"font-family: Cascadia Mono NF;"
                        f"background-color: #fbfbfb;"
                        f"color: #000000")







    def subjectation(self):

        if hasattr(self, 'dialog') and self.dialog is not None:
            self.dialog.close()

        self.dialog = QDialog()
        self.layout.addWidget(self.dialog)
        self.dialog.resize(500, 300)

        self.subjectate = QTableWidget(0, 1)

        subLen = self.dbLen("subjects")
        subData= self.db2table("subjects")
        for i in range(subLen):
            self.subjectate.insertRow(i)
            self.subjectate.setItem(i, 0, QTableWidgetItem(subData[i][1]))




        self.subjectate.horizontalHeader().setVisible(False)
        self.subjectate.horizontalHeader().setStretchLastSection(True)
        rowPos = self.subjectate.rowCount()
        clear = "background-color: ;"


        win = QVBoxLayout()
        foo = QVBoxLayout()
        foo.addWidget(self.subjectate)
        bar = QHBoxLayout()
        bar.setSpacing(0)
        foo.setSpacing(0)
        win.setSpacing(0)
        bar.setContentsMargins(0, 0, 0, 0)
        foo.setContentsMargins(0, 0, 0, 0)
        win.setContentsMargins(0, 0, 0, 0)

        self.add = QPushButton("Add")
        self.close = QPushButton("Close")
        self.save = QPushButton("Save")
        self.close.clicked.connect(self.closedShop)
        self.remove = QPushButton("Remove")
        self.remove.clicked.connect(self.trashCan)
        self.add.clicked.connect(lambda : self.subjectate.insertRow(rowPos))
        self.save.clicked.connect(self.subject2db)

        bar.addWidget(self.add)
        bar.addWidget(self.remove)
        bar.addWidget(self.save)
        bar.addWidget(self.close)

        win.addLayout(bar)
        win.addLayout(foo)
        self.dialog.setLayout(win)
        self.dialog.exec()

    def db2subj(self):
        conMan = sqlite3.connect("Ref.sqlite")
        c = conMan.cursor()

        c.execute('''SELECT subject_Name FROM subjects''')
        return [row[0] for row in c.fetchall()]


    def trashCan(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Icon.Warning)
        msgBox.setWindowTitle("Confirmation")
        msgBox.setText("Are you sure you want to delete this item?")
        msgBox.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        response = msgBox.exec()
        if response == QMessageBox.StandardButton.Yes:
            if self.subjectate.rowCount() > 0:
                rowPos = self.subjectate.rowCount()
                self.subjectate.removeRow(rowPos-1)


                conMan = sqlite3.connect("Ref.sqlite")
                c = conMan.cursor()

                c.execute('''DELETE FROM subjects WHERE subject_Code = ?''',str(rowPos-1))

                conMan.commit()
                conMan.close()


    def closedShop(self):
        self.dialog.close()
        for i in range(13):
            self.refer.setColumnHidden(i,False)

    def subject2db(self):
        conMan = sqlite3.connect("Ref.sqlite")
        c = conMan.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS subjects
                     (subject_Code INT PRIMARY KEY, subject_Name TEXT)''')

        for i in range(int(self.subjectate.rowCount())):
            x = self.subjectate.item(i, 0).text()
            c.execute("SELECT 1 FROM subjects WHERE subject_Code = ?", (i,))
            if c.fetchone() is None:
                c.execute("INSERT INTO subjects VALUES (?, ?)", (i, x))
        conMan.commit()
        conMan.close()

        for i in range(int(self.dbLen("subjects"))):
            self.subject_Code.clear()
        self.subject_Code.addItems(self.db2subj())

        self.dialog.close()


    def pageFlip(self):
        col = self.refer.columnCount()
        if not self.columsHidden():
            for i in range(col):
                self.refer.setColumnHidden(i, not self.refer.isColumnHidden(i))

    def columsHidden(self):
        col = self.refer.columnCount()
        hidden = []
        isHidden = [True, True, True, True, True, True, True, True, True, True, True, True, True]

        for i in range(col):
            if not self.refer.isColumnHidden(i):
                hidden.append(True)

        if hidden == isHidden:
            return True
        else:
              return False

    def dbSearch(self):
        conMan = sqlite3.connect("Ref.sqlite")
        c = conMan.cursor()
        res: list
        Squery = self.searchQuery()
        hunter = "SELECT * FROM referee WHERE ReferenceNum = ?"

    def searchQuery(self):
        query = []
        for i in range(11):
            try:
                query.insert(i,str(self.searchBar.cellWidget(0, i).text()))
            except AttributeError:
                try:
                    query.insert(i,str(self.searchBar.item(0, i).text()))
                except AttributeError:
                    try:
                        query.insert(i,str(self.searchBar.cellWidget(0, i).currentIndex() + 1))
                    except AttributeError:
                        query.insert(i,None)
        return query

    def clearSearch(self):
        rowposition = self.refer.rowCount()
        self.reference_No.clear()
        self.reference_Name.clear()
        self.reference_Title.clear()
        self.reference_Type_Code.setCurrentIndex(-1)
        self.authors.clear()
        self.year_Of_Publication.clear()
        self.subject_Code.setCurrentIndex(-1)
        self.reference_Status.setCurrentIndex(-1)
        self.importance.setCurrentIndex(-1)

        for i in range(rowposition):
            self.refer.showRow(i)

    def tabSwitch(self):
        if self.dialog is not None:
            col = self.refer.columnCount()
            if self.dialog.isVisible() and self.refer.isColumnHidden(8):
                for ranger in range(8,col):
                    self.refer.setColumnHidden(ranger, False)

                self.dialog.hide()
            elif self.dialog.isVisible() and self.refer.isColumnHidden(0):
                for ranger in range(0,col):
                    self.refer.setColumnHidden(ranger, False)

                self.dialog.hide()
            elif not (self.refer.isColumnHidden(8) and self.refer.isColumnHidden(0)):
                for ranger in range(8, col):
                    self.refer.setColumnHidden(ranger, True)


                self.dialog.show()


    def adjustCellWidth(self):
        self.refer.setColumnWidth(4, 175)
        self.refer.setColumnWidth(0, 70)
        self.refer.setColumnWidth(12, 120)
        self.refer.setColumnWidth(11, 120)
        self.refer.setColumnWidth(8, 200)

    def lineBacker(self):
        l1 = QLabel(self)
        pixmap = QPixmap("pics/bg.png")
        resizePixmap = pixmap.scaled(i, i)
        l1.setGeometry(0, 0, x, y)
        l1.setPixmap(resizePixmap)
        l2 = QLabel(self)
        pixmap = QPixmap("pics/bg.png")
        resizePixmap = pixmap.scaled(i, i)
        l2.setGeometry(i, 0, x, y)
        l2.setPixmap(resizePixmap)
        l3 = QLabel(self)
        pixmap = QPixmap("pics/bg.png")
        resizePixmap = pixmap.scaled(i, i)
        l3.setGeometry(0, y, x, y)
        l3.setPixmap(resizePixmap)
        l4 = QLabel(self)
        pixmap = QPixmap("pics/bg.png")
        resizePixmap = pixmap.scaled(i, i)
        l4.setGeometry(i, y, x, y)
        l4.setPixmap(resizePixmap)

    def rowMaister(self):
        rowData = []
        lenR = self.listed.rowCount()
        for row in range(lenR):

            if row != 7:
                try:
                    rowData.append(str(self.listed.item(row, 0).text()))
                except AttributeError:
                    try:
                        rowData.append(str(self.listed.cellWidget(row, 0).text()))
                    except AttributeError:
                        try:
                            rowData.append(str(self.listed.cellWidget(row, 0).currentIndex() + 1))
                        except AttributeError:
                            rowData.append("")
            else:
                rowData.append(str(self.notion.toHtml()))

        return rowData



    def row2Db(self):
        for i in range(13):
            self.refer.setColumnHidden(i,False)

        conMan = sqlite3.connect("Ref.sqlite")
        c = conMan.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS Referee
                     (ReferenceNum, Name, Title, Type, Authors, Year, Subject, Notes, Bibliography, 
                     Status, Importance, CreatedDate, LastEdit)''')

        c.execute("INSERT INTO referee VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", self.rowMaister())
        conMan.commit()
        conMan.close()
        self.dialog.close()
        self.rowLoader()







    def rowLoader(self):
        rowPos = self.refer.rowCount()
        self.refer.insertRow(rowPos)
        col = self.refer.columnCount()
        refNum = QLabel(str(self.refer.rowCount()))
        clear = "background-color: none;"
        combo = QComboBox()
        combo.setStyleSheet(clear)
        combo.setPlaceholderText("-")
        combo.addItems(["", "", "", "", ""])
        note = QPushButton()
        note.setText("Open ")
        note.setStyleSheet(clear)
        note = QPushButton("Open ")
        Num = int(refNum.text())
        note.clicked.connect(lambda: self.openNote(int(Num -1)))
        typeBox = QComboBox()
        typeBox.setPlaceholderText("-")
        typeBox.setStyleSheet(clear)
        typeBox.addItems(['Audiobook', 'Book', 'Bookshelf', 'Documentary', 'E-Book', 'Journal Article', 'Video'])
        subject = QComboBox()
        subject.setPlaceholderText("-")
        subject.setStyleSheet(clear)
        subject.addItems(self.db2subj())

        status = QComboBox()

        status.setPlaceholderText("-")
        status.setStyleSheet(clear)
        status.addItems(["Draft", "Read", "Cite More", "Cited"])

        DateTime = datetime.datetime.now()
        DT = QLabel()

        noEdit = QLabel("-")





        self.refer.setCellWidget(rowPos, 3, typeBox)
        self.refer.setCellWidget(rowPos, 6, subject)
        self.refer.setCellWidget(rowPos, 7, note)
        self.refer.setCellWidget(rowPos, 9, status)
        self.refer.setCellWidget(rowPos, 10, combo)


        for j in range(col):
            rowData = self.db2table("referee")
            if j in [3, 6, 9, 10]:
                self.refer.cellWidget(rowPos, j).setCurrentIndex(int(rowData[rowPos][j]) - 1)
                self.refer.cellWidget(rowPos, j).setEnabled(False)
            elif j in [0, 1, 2, 4, 5, 8, 11,12]:
                self.refer.setItem(rowPos, j, QTableWidgetItem(str(rowData[rowPos][j])))
            else:
                self.refer.setItem(rowPos, j, QTableWidgetItem(None))



    def loadTable(self):
        rowCount = self.dbLen("referee")
        for i in range(rowCount):
            self.rowLoader()



    def db2table(self,db):
        conMan = sqlite3.connect("Ref.sqlite")
        c = conMan.cursor()
        c.execute(f"SELECT * FROM {db}")
        row = c.fetchall()

        conMan.close()
        return row



    def dbLen(self,db):
        conn = sqlite3.connect("Ref.sqlite")
        c = conn.cursor()

        c.execute(f"SELECT COUNT(*) FROM {db}")

        result = c.fetchone()

        return result[0]
    def emptyTable(self):
        conn = sqlite3.connect("Ref.sqlite")
        c = conn.cursor()

        c.execute(f"SELECT COUNT(*) FROM referee")

        count = c.fetchone()[0]
        return count == 0

    def search(self):
        searchQ = self.searchQuery()

        conMan = sqlite3.connect("Ref.sqlite")
        c = conMan.cursor()

        columns_list = ["ReferenceNum", "Name", "Title", "Type", "Authors", "Year", "Subject",
                        "Notes", "Bibliography", "Status", "Importance", "CreatedDate", "LastEdit"]

        query_conditions = []
        params = []
        for i in range(len(searchQ)):
            if searchQ[i] not in ["", "0", None]:
                query_conditions.append(f"{columns_list[i]} LIKE ?")
                params.append(f"%{searchQ[i]}%")

        query_string = " AND ".join(query_conditions)

        rows = []
        if query_string:
            c.execute(f"SELECT * FROM referee WHERE {query_string}", tuple(params))
            rows = c.fetchall()

        conMan.close()

        hidden = [int(row[0]) - 1 for row in rows]

        for i in range(self.refer.rowCount()):
            if i in hidden:
                self.refer.showRow(i)
            else:
                self.refer.hideRow(i)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec())