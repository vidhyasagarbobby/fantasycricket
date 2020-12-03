# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Fantasy_Cricket.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import sqlite3
Cricket=sqlite3.connect("cricket.db")
cur=Cricket.cursor()

class Ui_MainWindow(QtWidgets.QWidget):
    def selected(self, item):
        sql="select value from stats where player='"+item.text()+"'"
        val=[val[0] for val in cur.execute(sql)]
        if (self.batcount+self.bowcount+self.arcount+self.wkcount)>=11:
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.setWindowTitle("Error")
            self.error_dialog.showMessage("Cannot add more than 11 members in a Team.")
        elif (self.points_available-val[0])<0:
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.setWindowTitle("Error")
            self.error_dialog.showMessage("Insufficient points.")
        
        else:
            if self.rb1.isChecked()==True:
                self.batcount+=1
                self.l2.setText(str(self.batcount))
                self.select(item)
                self.bat.remove(item.text())
            elif self.rb2.isChecked()==True:
                self.bowcount+=1
                self.l4.setText(str(self.bowcount))
                self.select(item)
                self.bow.remove(item.text())
            elif self.rb3.isChecked()==True:
                self.arcount+=1
                self.l6.setText(str(self.arcount))
                self.select(item)
                self.ar.remove(item.text())
            elif self.rb4.isChecked()==True:
                if(self.wkcount==0):
                    self.wkcount=1
                    self.l8.setText(str(self.wkcount))
                    self.select(item)
                    self.wk.remove(item.text())
                else:
                    self.error_dialog = QtWidgets.QErrorMessage()
                    self.error_dialog.setWindowTitle("Error")
                    self.error_dialog.showMessage("Cannot select more than 1 WicketKeeper.")

    def select(self, item):
        sql="select value from stats where player='"+item.text()+"'"
        val=[val[0] for val in cur.execute(sql)]
        self.points_available-=val[0]
        self.points_used+=val[0]
        self.l13.setText(str(self.points_available))
        self.l15.setText(str(self.points_used))
        self.team.append(item.text())
        self.listWidget_2.addItem(item.text())
        self.listWidget_2.sortItems()
        self.listWidget.takeItem(self.listWidget.row(item))

    def deselected(self, item):
        try:
            sql="select ctg from stats where player='"+item.text()+"'"
            array=[player[0] for player in cur.execute(sql)]
            if array[0]=="BAT":
                self.batcount-=1
                self.l2.setText(str(self.batcount))
                self.deselect(item)
                if self.rb1.isChecked()==True:
                    self.listWidget.addItem(item.text())
                    self.listWidget.sortItems()
                self.bat.append(item.text())
            elif array[0]=="BWL":
                self.bowcount-=1
                self.l4.setText(str(self.bowcount))
                self.deselect(item)
                if self.rb2.isChecked()==True:
                    self.listWidget.addItem(item.text())
                    self.listWidget.sortItems()
                self.bow.append(item.text())
            elif array[0]=="AR":
                self.arcount-=1
                self.l6.setText(str(self.arcount))
                self.deselect(item)
                if self.rb3.isChecked()==True:
                    self.listWidget.addItem(item.text())
                    self.listWidget.sortItems()
                self.ar.append(item.text())
            elif array[0]=="WK":
                self.wkcount=0
                self.l8.setText(str(self.wkcount))
                self.deselect(item)
                if self.rb4.isChecked()==True:
                    self.listWidget.addItem(item.text())
                    self.listWidget.sortItems()
                self.wk.append(item.text())
            self.team.remove(item.text())
            self.listWidget_2.takeItem(self.listWidget_2.row(item))
        except Exception as e:
            print(e)

    def deselect(self, item):
        sql="select value from stats where player='"+item.text()+"'"
        val=[val[0] for val in cur.execute(sql)]
        self.points_available+=val[0]
        self.points_used-=val[0]
        self.l13.setText(str(self.points_available))
        self.l15.setText(str(self.points_used))
        
    def menuFunction(self, action):
        txt=(action.text())
        if txt=="NEW Team":
            self.newTeam()
        elif txt=="SAVE Team":
            self.saveTeam()
        elif txt=="OPEN Team":
            self.openTeam()
        elif txt=="EVALUATE Team":
            self.evaluateTeam()
            
    def newTeam(self):
        self.listWidget.clear()
        self.listWidget_2.clear()
        self.rb1.setChecked(False)
        self.rb2.setChecked(False)
        self.rb3.setChecked(False)
        self.rb4.setChecked(False)
        text, ok = QtWidgets.QInputDialog.getText(self, 'New Team', 'Enter Team name:')
        if ok:
            self.l11.setText(str(text))
            teams=[teams[0] for teams in cur.execute("select distinct name from teams")]
            if text in teams:
                self.error_dialog=QtWidgets.QErrorMessage()
                self.error_dialog.setWindowTitle("Name Error")
                self.error_dialog.showMessage(text+" is already taken. Please try another name")
                self.l11.setText("")
            else:    
                self.team_name=text
                self.listWidget_2.clear()
                self.getPlayers()
                self.team=[]
                self.wkcount=0
                self.batcount=0
                self.bowcount=0
                self.arcount=0
                self.points_used=0
                self.setLabels()

    def saveTeam(self):
        try:
            if(self.batcount+self.bowcount+self.arcount+self.wkcount)!=11:
                self.error_dialog=QtWidgets.QErrorMessage()
                self.error_dialog.setWindowTitle("Error")
                self.error_dialog.showMessage("Please select 11 players for your team")
            else:
                for i in range(11):
                    sql="select value from stats where player='"+self.team[i]+"'"
                    val=[val[0] for val in cur.execute(sql)]
                    try:
                        cur.execute("insert into teams(name, players, value) values(?,?,?);",(self.team_name, self.team[i],val[0]))
                        Cricket.commit()
                    except Exception as e:
                        print(e)
                    
        except Exception as e:
            self.error_dialog=QtWidgets.QErrorMessage()
            self.error_dialog.setWindowTitle("Error")
            self.error_dialog.showMessage("Unable to SAVE Team")

    def openTeam(self):
        teams=[teams[0] for teams in cur.execute("select distinct name from teams")]
        try:
            item, ok = QtWidgets.QInputDialog.getItem(self, "Select Team", "Teams", teams, 0, False)
            if ok:
                sql="select players from teams where name='"+item+"'"
                self.team=[team[0] for team in cur.execute(sql)]
                self.getPlayers()
                self.points_used=0
                self.batc=len(self.bat)
                self.bowc=len(self.bow)
                self.arc=len(self.ar)
                self.wkc=len(self.wk)
                self.bat=list(set(self.bat) - set(self.team))
                self.bow=list(set(self.bow) - set(self.team))
                self.ar=list(set(self.ar) - set(self.team))
                self.wk=list(set(self.wk) - set(self.team))
                self.batcount=self.batc-len(self.bat)
                self.bowcount=self.bowc-len(self.bow)
                self.arcount=self.arc-len(self.ar)
                self.wkcount=self.wkc-len(self.wk)
                for i in range(11):
                    sql="select value from stats where player='"+self.team[i]+"'"
                    val=[val[0] for val in cur.execute(sql)]
                    self.points_used+=val[0]
                self.setLabels()
                self.l11.setText(item)
                self.rb1.setChecked(True)
                
        except Exception as e:
            print(e)
    def getPlayers(self):
        self.bat=[player[0] for player in cur.execute("select player from stats where ctg='BAT'")]
        self.bow=[player[0] for player in cur.execute("select player from stats where ctg='BWL'")]
        self.ar=[player[0] for player in cur.execute("select player from stats where ctg='AR'")]
        self.wk=[player[0] for player in cur.execute("select player from stats where ctg='WK'")]
    def setLabels(self):
        self.points_available=1000-self.points_used
        self.l13.setText(str(self.points_available))
        self.l2.setText(str(self.batcount))
        self.l4.setText(str(self.bowcount))
        self.l6.setText(str(self.arcount))
        self.l8.setText(str(self.wkcount))
        self.l15.setText(str(self.points_used))

    def evaluateTeam(self):
        try:
            self.team_name=self.l11.text()
            for player in self.team:
                sql="select * from match where Player='"+player+"'"
                cur.execute(sql)
                match=cur.fetchone()
                value=0
                if match[1]!=0:
                    value+=match[1]//2
                if match[1]>=50:
                    value+=5
                if match[1]>=100:
                    value+=10
                if match[2]!=0:
                    sr=(match[1]/match[2])*100
                    if sr>=80 and sr<100:
                        value+=2
                    if sr>=100:
                        value+=4
                value+=match[3]
                value+=match[4]*2
                value+=match[8]*10
                if match[8]>=3:
                    value+=5
                if match[8]>=5:
                    value+=10
                if match[5]!=0:    
                    er=(match[7]/match[5])*6
                    if er<=4.5 and er>3.5:
                        value+=4
                    if er<=3.5 and er>2:
                        value+=7
                    if er<=2:
                        value+=10
                value+=(match[9]+match[10]+match[11])*10
                cur.execute("update teams set value=%d where players='%s'"%(value, player))
                Cricket.commit()
            sql="select players from teams where name='"+self.team_name+"'"
            players=[player[0] for player in cur.execute(sql)]
            sql="select value from teams where name='"+self.team_name+"'"
            values=[value[0] for value in cur.execute(sql)]
            self.tableWidget = QtWidgets.QTableWidget()
            self.tableWidget.setWindowTitle(self.team_name)
            self.tableWidget.setGeometry(100,200,250,400)
            self.tableWidget.setRowCount(12)
            self.tableWidget.setColumnCount(2)
            self.tableWidget.setItem(0,0, QTableWidgetItem("Player"))
            self.tableWidget.setItem(0,1, QTableWidgetItem("Value"))
            for i in range(11):
                    self.tableWidget.setItem(i+1,0, QTableWidgetItem(players[i]))
                    self.tableWidget.setItem(i+1,1, QTableWidgetItem(str(values[i])))
            self.tableWidget.show()
                
        except Exception as e:
                print(e)
    def showPlayers(self, rb):
        try:
            if  rb.isChecked() == True:
                if rb.text()=="BAT":
                    self.listWidget.clear()
                    self.listWidget.addItems(self.bat)
                    self.listWidget.sortItems()
                if rb.text() == "BOW":
                    self.listWidget.clear()
                    self.listWidget.addItems(self.bow)
                    self.listWidget.sortItems()
                if rb.text()== "AR":
                    self.listWidget.clear()
                    self.listWidget.addItems(self.ar)
                    self.listWidget.sortItems()
                if rb.text()=="WK":
                    self.listWidget.clear()
                    self.listWidget.addItems(self.wk)
                    self.listWidget.sortItems()
            self.listWidget_2.clear()
            self.listWidget_2.addItems(self.team)
            self.listWidget_2.sortItems()

        except Exception as e:
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.setWindowTitle("Error")
            self.error_dialog.showMessage('Please select "NEW Team"')
            rb.setChecked(False)
                           
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(750, 450)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(30, 20, 690, 60))
        self.widget.setStyleSheet("Background-color: lightgrey")
        self.widget.setObjectName("widget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.widget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 20, 690, 40))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(3, 3, 3, 3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.l1 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Lucida Bright")
        font.setBold(True)
        font.setWeight(100)
        self.l1.setFont(font)
        self.l1.setObjectName("l1")
        self.horizontalLayout.addWidget(self.l1)
        self.l2 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(100)
        self.l2.setFont(font)
        self.l2.setStyleSheet("color: blue")
        self.l2.setObjectName("l2")
        self.horizontalLayout.addWidget(self.l2)
        self.l3 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Lucida Bright")
        font.setBold(True)
        font.setWeight(100)
        self.l3.setFont(font)
        self.l3.setObjectName("l3")
        self.horizontalLayout.addWidget(self.l3)
        self.l4 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(100)
        self.l4.setFont(font)
        self.l4.setStyleSheet("color: blue")
        self.l4.setObjectName("l4")
        self.horizontalLayout.addWidget(self.l4)
        self.l5 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Lucida Bright")
        font.setBold(True)
        font.setWeight(100)
        self.l5.setFont(font)
        self.l5.setObjectName("l5")
        self.horizontalLayout.addWidget(self.l5)
        self.l6 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(100)
        self.l6.setFont(font)
        self.l6.setStyleSheet("color: blue")
        self.l6.setObjectName("l6")
        self.horizontalLayout.addWidget(self.l6)
        self.l7 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Lucida Bright")
        font.setBold(True)
        font.setWeight(100)
        self.l7.setFont(font)
        self.l7.setObjectName("l7")
        self.horizontalLayout.addWidget(self.l7)
        self.l8 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(100)
        self.l8.setFont(font)
        self.l8.setStyleSheet("color: blue")
        self.l8.setObjectName("l8")
        self.horizontalLayout.addWidget(self.l8)
        self.l9 = QtWidgets.QLabel(self.widget)
        self.l9.setGeometry(QtCore.QRect(0, 0, 200, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(False)
        font.setWeight(60)
        self.l9.setFont(font)
        self.l9.setObjectName("l9")
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setGeometry(QtCore.QRect(40, 140, 310, 250))
        self.widget_2.setStyleSheet("Background-color: white")
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.widget_2)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 310, 30))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.rb1 = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Lucida Bright")
        self.rb1.setFont(font)
        self.rb1.setObjectName("rb1")
        self.horizontalLayout_2.addWidget(self.rb1)
        self.rb2 = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Lucida Bright")
        self.rb2.setFont(font)
        self.rb2.setObjectName("rb2")
        self.horizontalLayout_2.addWidget(self.rb2)
        self.rb3 = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Lucida Bright")
        self.rb3.setFont(font)
        self.rb3.setObjectName("rb3")
        self.horizontalLayout_2.addWidget(self.rb3)
        self.rb4 = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Lucida Bright")
        self.rb4.setFont(font)
        self.rb4.setObjectName("rb4")
        self.horizontalLayout_2.addWidget(self.rb4)
        self.listWidget = QtWidgets.QListWidget(self.widget_2)
        self.listWidget.setGeometry(QtCore.QRect(0, 30, 310, 220))
        self.listWidget.setStyleSheet("border: white")
        self.listWidget.setObjectName("listWidget")
        self.widget_3 = QtWidgets.QWidget(self.centralwidget)
        self.widget_3.setGeometry(QtCore.QRect(390, 140, 310, 250))
        self.widget_3.setStyleSheet("Background-color: white")
        self.widget_3.setObjectName("widget_3")
        self.layoutWidget = QtWidgets.QWidget(self.widget_3)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 0, 310, 30))
        self.layoutWidget.setObjectName("layoutWidget")
        self.formLayout_3 = QtWidgets.QFormLayout(self.layoutWidget)
        self.formLayout_3.setContentsMargins(0, 0, 0, 0)
        self.formLayout_3.setObjectName("formLayout_3")
        self.l10 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Lucida Bright")
        font.setBold(True)
        font.setWeight(75)
        self.l10.setFont(font)
        self.l10.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.l10.setObjectName("l10")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.l10)
        self.l11 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.l11.setFont(font)
        self.l11.setStyleSheet("color: blue")
        self.l11.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.l11.setObjectName("l11")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.l11)
        self.listWidget_2 = QtWidgets.QListWidget(self.widget_3)
        self.listWidget_2.setGeometry(QtCore.QRect(0, 30, 310, 220))
        self.listWidget_2.setStyleSheet("border: white")
        self.listWidget_2.setObjectName("listWidget_2")
        self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(40, 110, 310, 20))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.formLayout = QtWidgets.QFormLayout(self.layoutWidget1)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.l12 = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Lucida Bright")
        font.setBold(True)
        font.setWeight(75)
        self.l12.setFont(font)
        self.l12.setObjectName("l12")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.l12)
        self.l13 = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.l13.setFont(font)
        self.l13.setStyleSheet("color: blue")
        self.l13.setObjectName("l13")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.l13)
        self.layoutWidget2 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget2.setGeometry(QtCore.QRect(390, 110, 310, 16))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.formLayout_2 = QtWidgets.QFormLayout(self.layoutWidget2)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.formLayout_2.setObjectName("formLayout_2")
        self.l15 = QtWidgets.QLabel(self.layoutWidget2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.l15.setFont(font)
        self.l15.setStyleSheet("color: blue")
        self.l15.setObjectName("l15")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.l15)
        self.l14 = QtWidgets.QLabel(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("Lucida Bright")
        font.setBold(True)
        font.setWeight(75)
        self.l14.setFont(font)
        self.l14.setObjectName("l14")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.l14)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 582, 21))
        self.menubar.setObjectName("menubar")
        self.menuManage_Teams = QtWidgets.QMenu(self.menubar)
        self.menuManage_Teams.setObjectName("menuManage_Teams")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNEW_Team = QtWidgets.QAction(MainWindow)
        self.actionNEW_Team.setObjectName("actionNEW_Team")
        self.actionOPEN_Team = QtWidgets.QAction(MainWindow)
        self.actionOPEN_Team.setObjectName("actionOPEN_Team")
        self.actionSAVE_Team = QtWidgets.QAction(MainWindow)
        self.actionSAVE_Team.setObjectName("actionSAVE_Team")
        self.actionEVALUATE_Team = QtWidgets.QAction(MainWindow)
        self.actionEVALUATE_Team.setObjectName("actionEVALUATE_Team")
        self.menuManage_Teams.addAction(self.actionNEW_Team)
        self.menuManage_Teams.addAction(self.actionOPEN_Team)
        self.menuManage_Teams.addAction(self.actionSAVE_Team)
        self.menuManage_Teams.addAction(self.actionEVALUATE_Team)
        self.menubar.addAction(self.menuManage_Teams.menuAction())
        self.listWidget.itemDoubleClicked.connect(self.selected)
        self.listWidget_2.itemDoubleClicked.connect(self.deselected)


        self.menuManage_Teams.triggered[QtWidgets.QAction].connect(self.menuFunction)
        self.rb1.toggled.connect(lambda: self.showPlayers(self.rb1))
        self.rb2.toggled.connect(lambda: self.showPlayers(self.rb2))
        self.rb3.toggled.connect(lambda: self.showPlayers(self.rb3))
        self.rb4.toggled.connect(lambda: self.showPlayers(self.rb4))
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Fantasy Cricket"))
        self.l1.setText(_translate("MainWindow", " Batsmen (BAT) :"))
        self.l2.setText(_translate("MainWindow", "0"))
        self.l3.setText(_translate("MainWindow", "Bowlers (BOW) :"))
        self.l4.setText(_translate("MainWindow", "0"))
        self.l5.setText(_translate("MainWindow", "All Rounder (AR) :"))
        self.l6.setText(_translate("MainWindow", "0"))
        self.l7.setText(_translate("MainWindow", "Wicket Keeper (WK) :"))
        self.l8.setText(_translate("MainWindow", "0"))
        self.l9.setText(_translate("MainWindow", " Your Selections"))
        self.rb1.setText(_translate("MainWindow", "BAT"))
        self.rb2.setText(_translate("MainWindow", "BOW"))
        self.rb3.setText(_translate("MainWindow", "AR"))
        self.rb4.setText(_translate("MainWindow", "WK"))
        self.l10.setText(_translate("MainWindow", "Team Name : "))
        self.l11.setText(_translate("MainWindow", ""))
        self.l12.setText(_translate("MainWindow", "Points Available : "))
        self.l13.setText(_translate("MainWindow", "1000"))
        self.l15.setText(_translate("MainWindow", "0"))
        self.l14.setText(_translate("MainWindow", "Points Used : "))
        self.menuManage_Teams.setTitle(_translate("MainWindow", "Manage Teams"))
        self.actionNEW_Team.setText(_translate("MainWindow", "NEW Team"))
        self.actionOPEN_Team.setText(_translate("MainWindow", "OPEN Team"))
        self.actionSAVE_Team.setText(_translate("MainWindow", "SAVE Team"))
        self.actionEVALUATE_Team.setText(_translate("MainWindow", "EVALUATE Team"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
