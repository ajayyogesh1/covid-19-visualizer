from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd
import matplotlib.pyplot as plt
import requests
import folium as fs
import webbrowser

BASE_URL = "https://corona-server-app.herokuapp.com/"

class Ui_ShowMap(object):
    def setupUi(self, ShowMap):
        ShowMap.setObjectName("ShowMap")
        ShowMap.resize(500, 200)
        self.centralwidget = QtWidgets.QWidget(ShowMap)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, 461, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 60, 461, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.dateEdit = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit.setGeometry(QtCore.QRect(40, 110, 201, 51))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.dateEdit.setFont(font)
        self.dateEdit.setObjectName("dateEdit")
        self.btnMap = QtWidgets.QPushButton(self.centralwidget)
        self.btnMap.setGeometry(QtCore.QRect(270, 110, 191, 51))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.btnMap.setFont(font)
        self.btnMap.setObjectName("btnMap")
        ShowMap.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(ShowMap)
        self.statusbar.setObjectName("statusbar")
        ShowMap.setStatusBar(self.statusbar)
        self.retranslateUi(ShowMap)
        QtCore.QMetaObject.connectSlotsByName(ShowMap)
    def retranslateUi(self, ShowMap):
        _translate = QtCore.QCoreApplication.translate
        ShowMap.setWindowTitle(_translate("ShowMap", "MainWindow"))
        self.label.setText(_translate("ShowMap", "Enter A Date to Show Map With Corona Cases at that Particular  Date over 200 Countries"))
        self.label_2.setText(_translate("ShowMap", " At that Particular  Date over 200 Countries"))
        self.btnMap.setText(_translate("ShowMap", "Show Map"))
        self.dateEdit.setDate(QtCore.QDate.currentDate().addDays(-1))
        self.btnMap.clicked.connect(self.Plot)
        self.dateEdit.setMinimumDate(QtCore.QDate(2020,1,1))
        self.dateEdit.setMaximumDate(QtCore.QDate.currentDate().addDays(-1))    
    def postData(self, url, data):
        self.statusbar.showMessage("Gathering the Data from Server...")
        try:
            response = requests.post(url, json = data).json()["data"]
            self.statusbar.showMessage("Data gathered from the Server successfully.")
            return response
        except:
            self.statusbar.showMessage("Unable To Complete the Download. Check your Internet Connection And Firewalls")
    def Plot(self):
        self.statusbar.showMessage("Started Plotting Markers on Map.Please Wait")
        Map=fs.Map([20.59368,78.96288],tiles="Stamen Terrain",zoom_start=5)
        Date=self.dateEdit.date().toString('yyyy-MM-dd')
        requiredColumns = ["total_cases","new_cases","total_tests","new_tests","total_deaths", "new_deaths", "people_vaccinated", "people_fully_vaccinated"]
        columnHeadings = ["location", "latitude", "longitude", "total_cases","new_cases","total_tests","new_tests","total_deaths", "new_deaths", "people_vaccinated", "people_fully_vaccinated"]
        jsonData = {"date":Date, "columns":requiredColumns}
        mapData = pd.DataFrame(self.postData(BASE_URL + "/getMapData", jsonData), columns = columnHeadings).T
        # print(mapData)
        for row in mapData:
            text = """<strong style='font-family: "Helvetica Neue",Helvetica,Arial,sans-serif;font-size: 14px;line-height: 1.42857143;color: #333;'>
                            Total Cases &nbsp;&nbsp;: {:,}<br/>
                            New Cases &nbsp;&nbsp;&nbsp;: {:,}<br/>
                            Total Tests &nbsp;&nbsp;&nbsp;&nbsp;: {:,}<br/>
                            New Tests &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: {:,}<br/>
                            Total Deaths &nbsp;: {:,}<br/>
                            New Deaths &nbsp;&nbsp;: {:,}<br/>
                            First Dose &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: {:,}<br/>
                            Second Dose : {:,}
                        </strong>""".format(mapData[row][requiredColumns[0]], mapData[row][requiredColumns[1]], mapData[row][requiredColumns[2]], mapData[row][requiredColumns[3]], mapData[row][requiredColumns[4]], mapData[row][requiredColumns[5]], mapData[row][requiredColumns[6]], mapData[row][requiredColumns[7]])
            iframe = fs.IFrame(text)
            popup = fs.Popup(iframe,min_width=225,max_width=225)
            fs.Marker([mapData[row]['latitude'], mapData[row]['longitude']],radius=15,popup=popup,tooltip=mapData[row]['location'],icon=fs.Icon(color="red")).add_to(Map)
        fs.TileLayer('openstreetmap').add_to(Map)
        fs.TileLayer('stamenterrain').add_to(Map)
        fs.TileLayer('stamentoner').add_to(Map)
        fs.TileLayer('stamenwatercolor').add_to(Map)
        fs.TileLayer('cartodbpositron').add_to(Map)
        fs.TileLayer('cartodbdark_matter').add_to(Map)
        fs.LayerControl().add_to(Map)
        Map.save("Location.html")
        webbrowser.open("Location.html")
        self.statusbar.showMessage("The Cases are Plotted Successfully in the Map")
class Ui_CoronaVirus(object):
    def setupUi(self, CoronaVirus):
        CoronaVirus.setObjectName("CoronaVirus")
        CoronaVirus.setFixedSize(600,400)
        self.centralwidget = QtWidgets.QWidget(CoronaVirus)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 20, 111, 40))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.CountryCombo = QtWidgets.QComboBox(self.centralwidget)
        self.CountryCombo.setGeometry(QtCore.QRect(140, 20, 261, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.CountryCombo.setFont(font)
        self.CountryCombo.setObjectName("CountryCombo")
        self.CountryCombo.addItem("")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 70, 111, 40))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.FromDate = QtWidgets.QDateEdit(self.centralwidget)
        self.FromDate.setGeometry(QtCore.QRect(140, 70, 171, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.FromDate.setFont(font)
        self.FromDate.setObjectName("FromDate")
        self.ToDate = QtWidgets.QDateEdit(self.centralwidget)
        self.ToDate.setGeometry(QtCore.QRect(140, 120, 171, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.ToDate.setFont(font)
        self.ToDate.setObjectName("ToDate")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 120, 111, 40))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.btnPlot = QtWidgets.QPushButton(self.centralwidget)
        self.btnPlot.setGeometry(QtCore.QRect(190, 260, 231, 51))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.btnPlot.setFont(font)
        self.btnPlot.setObjectName("btnPlot")
        self.chkTest = QtWidgets.QCheckBox(self.centralwidget)
        self.chkTest.setGeometry(QtCore.QRect(40, 170, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.chkTest.setFont(font)
        self.chkTest.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.chkTest.setObjectName("chkTest")
        self.chkNAffect = QtWidgets.QCheckBox(self.centralwidget)
        self.chkNAffect.setGeometry(QtCore.QRect(320, 170, 231, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.chkNAffect.setFont(font)
        self.chkNAffect.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.chkNAffect.setObjectName("chkNAffect")
        self.chkNVaccine = QtWidgets.QCheckBox(self.centralwidget)
        self.chkNVaccine.setGeometry(QtCore.QRect(50, 210, 231, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.chkNVaccine.setFont(font)
        self.chkNVaccine.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.chkNVaccine.setObjectName("chkNVaccine")
        self.chkNDeath = QtWidgets.QCheckBox(self.centralwidget)
        self.chkNDeath.setGeometry(QtCore.QRect(320, 210, 231, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.chkNDeath.setFont(font)
        self.chkNDeath.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.chkNDeath.setObjectName("chkNDeath")
        self.chkAll = QtWidgets.QCheckBox(self.centralwidget)
        self.chkAll.setGeometry(QtCore.QRect(330, 120, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.chkAll.setFont(font)
        self.chkAll.setObjectName("chkAll")
        CoronaVirus.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(CoronaVirus)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 29))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        CoronaVirus.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(CoronaVirus)
        self.statusbar.setObjectName("statusbar")
        CoronaVirus.setStatusBar(self.statusbar)
        self.actionExit = QtWidgets.QAction(CoronaVirus)
        self.actionExit.setObjectName("actionExit")
        self.SwitchToMap = QtWidgets.QAction(CoronaVirus)
        self.SwitchToMap.setObjectName("SwitchToMap")
        self.menuFile.addAction(self.SwitchToMap)
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.retranslateUi(CoronaVirus)
        QtCore.QMetaObject.connectSlotsByName(CoronaVirus)
    def retranslateUi(self, CoronaVirus):
        _translate = QtCore.QCoreApplication.translate
        CoronaVirus.setWindowTitle(_translate("CoronaVirus", "MainWindow"))
        self.label.setText(_translate("CoronaVirus", "Country : "))
        self.CountryCombo.setItemText(0, _translate("CoronaVirus", "--Select Country--"))
        self.label_2.setText(_translate("CoronaVirus", "From : "))
        self.label_3.setText(_translate("CoronaVirus", "To : "))
        self.btnPlot.setText(_translate("CoronaVirus", " Plot Graph"))
        self.chkTest.setText(_translate("CoronaVirus", " New Tests"))
        self.chkNAffect.setText(_translate("CoronaVirus", " New Positive Cases"))
        self.chkNVaccine.setText(_translate("CoronaVirus", " New Vaccinations"))
        self.chkNDeath.setText(_translate("CoronaVirus", " New Deaths"))
        self.chkAll.setText(_translate("CoronaVirus", "All"))
        self.menuFile.setTitle(_translate("CoronaVirus", "File"))
        self.actionExit.setText(_translate("CoronaVirus", "Exit"))
        self.SwitchToMap.setText(_translate("CoronaVirus", "Switch to Map View"))
        self.btnPlot.clicked.connect(self.PlotGraph)
        self.chkAll.stateChanged.connect(self.Checkall)
        self.actionExit.triggered.connect(self.Exit)
        self.FromDate.setDate(QtCore.QDate(2020, 1, 1))
        self.ToDate.setDate(QtCore.QDate.currentDate().addDays(-1))
        self.FromDate.setMinimumDate(QtCore.QDate(2020, 1, 1))
        self.FromDate.setMaximumDate(QtCore.QDate.currentDate().addDays(-2))
        self.ToDate.setMinimumDate(QtCore.QDate(2020, 1, 2))
        self.ToDate.setMaximumDate(QtCore.QDate.currentDate().addDays(-1))
        self.ComboUpdate()
        self.SwitchToMap.triggered.connect(self.ShowMaps)
    def getData(self, url):
        self.statusbar.showMessage("Gathering the Data from Server...")
        try:
            response = requests.get(url).json()
            self.statusbar.showMessage("Data gathered from the Server successfully.")
            return response
        except:
            self.statusbar.showMessage("Unable To Complete the Download. Check your Internet Connection And Firewalls")
    def postData(self, url, data):
        self.statusbar.showMessage("Gathering the Data from Server...")
        try:
            response = requests.post(url, json = data).json()["data"]
            self.statusbar.showMessage("Data gathered from the Server successfully.")
            return response
        except:
            self.statusbar.showMessage("Unable To Complete the Download. Check your Internet Connection And Firewalls")
    def ShowMaps(self):
    	self.ui = Ui_ShowMap()
    	self.ui.setupUi(ShowMap)
    	ShowMap.show()
    def Exit(self):CoronaVirus.close()
    def Checkall(self):
        if self.chkAll.isChecked():
            for i in ShowDetails:eval("self."+i+".setChecked(True)")
        else:
            for i in ShowDetails:eval("self."+i+".setChecked(False)")
    def ComboUpdate(self):
        countryNames = self.getData(BASE_URL + "/getCountries")["location"]
        # print(countryNames)
        self.CountryCombo.addItems(countryNames)
    def PlotGraph(self):
        From,To,Temp=self.FromDate.date().toString('yyyy-MM-dd'),self.ToDate.date().toString('yyyy-MM-dd'),[]
        FFrom,TTo=pd.to_datetime(From),pd.to_datetime(To)
        for i in ShowDetails:
            if eval("self."+i+".isChecked()"):Temp.append(i)
        if self.CountryCombo.currentText()=="--Select Country--":self.statusbar.showMessage("Please Select a Country to Proceed Further")
        elif From==To and From<To:self.statusbar.showMessage("Please Select Different Dates to Proceed Further")
        elif len(Temp)==0:self.statusbar.showMessage("Please Select the CheckBoxes.")
        else:
            Dict={"chkNDeath":'new_deaths',"chkNVaccine":'new_vaccinations',"chkNAffect":'new_cases',"chkTest":'new_tests'}
            Temp=[Dict[i] for i in Temp]
            Temp.insert(0, "date")
            jsonData = {"location": self.CountryCombo.currentText(),
                        "from"    : From,
                        "to"      : To,
                        "columns" : Temp}
            postedData = self.postData(BASE_URL + "/getGraphData", jsonData)
            data = pd.DataFrame(postedData, columns = Temp)
            data.plot.bar(x=Temp[0],y=Temp[1:],title="Cases of Covid-19 in %s during %s to %s"%(self.CountryCombo.currentText(),FFrom.date(),TTo.date()))
            plt.show()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ShowMap = QtWidgets.QMainWindow()
    CoronaVirus = QtWidgets.QMainWindow()
    ShowDetails=["chkTest","chkNDeath","chkNVaccine","chkNAffect"]
    ui = Ui_CoronaVirus()
    ui.setupUi(CoronaVirus)
    CoronaVirus.show()
    sys.exit(app.exec_())
