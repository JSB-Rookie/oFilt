import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QTableView, QMainWindow, QDateEdit
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, uic
import pandas as pd
import numpy as np
import scipy.stats as stats
import math
from PyQt5.QtCore import QDate
from datetime import datetime, date
from datetime import timedelta, date
from dateutil import parser
import webbrowser
import subprocess

qtcreator_file  = "oFilt.ui" #Entering the Qt Designer file, then connecting to this file
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow,self).__init__(*args, **kwargs)
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.pbLoadFile.clicked.connect(self.loadData)
        
        #Setting default dates for five calanders
        self.deCurDat.setDate(QDate.currentDate())
        self.deExpDat1.setDate(QDate.currentDate())
        self.deExpDat2.setDate(QDate.currentDate())
        self.deExpDat3.setDate(QDate.currentDate())
        self.deExpDat4.setDate(QDate.currentDate())        
        
        #Initializing the layouts for the MainWindow
        mainLayout = QVBoxLayout()
        horizLay1 = QHBoxLayout()
        horizLay2 = QHBoxLayout()
        horizLay3 = QHBoxLayout()
        horizLay4 = QHBoxLayout()
        vertLay = QVBoxLayout()
        
        horizLay1.addWidget(self.lbCurPri)
        horizLay1.addWidget(self.leCurPri)
        horizLay1.addWidget(self.fNameLabel)
        horizLay1.addWidget(self.leFileName)
        horizLay1.addWidget(self.lbCurDat)
        horizLay1.addWidget(self.deCurDat)
        
        
        #Adding the four following layouts to horizLay1 Layout
        horizLay1.addLayout(mainLayout)
        horizLay1.addLayout(horizLay2)
        horizLay1.addLayout(horizLay3)
        horizLay1.addLayout(horizLay4)
        horizLay1.addLayout(vertLay)
        
        horizLay2.addWidget(self.lbStrCurMin)
        horizLay2.addWidget(self.leStrCurMin)
        horizLay2.addWidget(self.lbBidVolMin)
        horizLay2.addWidget(self.leBidVolMin)
        horizLay2.addWidget(self.lbAskVolMin)
        horizLay2.addWidget(self.leAskVolMin)
        horizLay2.addWidget(self.lbDelMin)
        horizLay2.addWidget(self.leDelMin)
        
        
        horizLay3.addWidget(self.lbStrCurMax)
        horizLay3.addWidget(self.leStrCurMax)
        horizLay3.addWidget(self.lbBidVolMax)
        horizLay3.addWidget(self.leBidVolMax)
        horizLay3.addWidget(self.lbAskVolMax)
        horizLay3.addWidget(self.leAskVolMax)
        horizLay3.addWidget(self.lbDelMax)
        horizLay3.addWidget(self.leDelMax)
        horizLay3.addWidget(self.lbBidAsk)
        horizLay3.addWidget(self.leBidAsk)
        horizLay3.addWidget(self.rbCall)
        horizLay3.addWidget(self.rbPut)
        horizLay3.addWidget(self.cbFid)
        horizLay3.addWidget(self.cbMarWat)
        horizLay3.addWidget(self.cbExc)
        
        horizLay4.addWidget(self.pbSpCp)
        horizLay4.addWidget(self.pbBidVol)
        horizLay4.addWidget(self.pbAskVol)
        horizLay4.addWidget(self.pbDeltas)
        horizLay4.addWidget(self.pbAskBid)
        
        vertLay.addWidget(self.pbRawData)
        vertLay.addWidget(self.pbLoadFile)
        vertLay.addWidget(self.pbReload)
        vertLay.addWidget(self.lbExpDat1)
        vertLay.addWidget(self.deExpDat1)
        vertLay.addWidget(self.pbMatTim1)
        vertLay.addWidget(self.leMatTim1)
        vertLay.addWidget(self.lbExpDat2)
        vertLay.addWidget(self.deExpDat2)
        vertLay.addWidget(self.pbMatTim2)
        vertLay.addWidget(self.leMatTim2)
        vertLay.addWidget(self.lbExpDat3)
        vertLay.addWidget(self.deExpDat3)
        vertLay.addWidget(self.pbMatTim3)
        vertLay.addWidget(self.leMatTim3)
        vertLay.addWidget(self.lbExpDat4)
        vertLay.addWidget(self.deExpDat4)
        vertLay.addWidget(self.pbMatTim4)
        vertLay.addWidget(self.leMatTim4)
        vertLay.addWidget(self.laDelRow_1)
        vertLay.addWidget(self.leDelRow_1)
        vertLay.addWidget(self.laDelRow_2)
        vertLay.addWidget(self.leDelRow_2)
        vertLay.addWidget(self.laDelRow_3)
        vertLay.addWidget(self.leDelRow_3)
        vertLay.addWidget(self.laDelRow_4)
        vertLay.addWidget(self.leDelRow_4)
        
        mainLayout.addWidget(self.table)
        
        self.pbMatTim1.clicked.connect(self.calc_mat_time1)
        self.pbMatTim2.clicked.connect(self.calc_mat_time2)
        self.pbMatTim3.clicked.connect(self.calc_mat_time3)
        self.pbMatTim4.clicked.connect(self.calc_mat_time4)
        
        self.pbClose.clicked.connect(self.close)
        self.cbFid.stateChanged.connect(self.opFid)
        self.cbExc.stateChanged.connect(self.opExl)
        self.cbMarWat.stateChanged.connect(self.opMW)
        self.pbRawData.clicked.connect(self.seeAll)
        self.pbSpCp.clicked.connect(self.minMaxStrCur)
        self.pbBidVol.clicked.connect(self.minMaxBidVol)
        self.pbAskVol.clicked.connect(self.minMaxAskVol)
        self.pbDeltas.clicked.connect(self.minMaxDelta)
        self.pbAskBid.clicked.connect(self.maxAskMinusBid)
        self.pbReload.clicked.connect(self.reload)
        
        
        self.df = pd.DataFrame()
        self.df1 = pd.DataFrame()
        self.df2 = pd.DataFrame()
        self.df3 = pd.DataFrame()
        self.df4 = pd.DataFrame()
        self.df5 = pd.DataFrame()
        self.dfp = pd.DataFrame()
        
        self.filNum = 0
        self.cflag = False
    
    def seeAll(self):
        fileName = self.leFileName.text()
        self.df = pd.read_csv(fileName)
        self.df = self.df.fillna(0)
        self.model = TableModel(self.df)
        self.table.setModel(self.model)
        
    def loadData(self):
        #Reading the file copied from Fidelity or MarketWatch
        fileName = self.leFileName.text()
        self.df = pd.read_csv(fileName)
        self.df = self.df.fillna(0)
        rs = self.df.shape[0]
        print("rs is: ", rs)
        #Delete unwanted rows
        if len(self.leDelRow_1.text()) > 0:
            self.delRow()
        if len(self.leDelRow_2.text()) > 0:
            self.delRow_2()
        if len(self.leDelRow_3.text()) > 0:
            self.delRow_3()
        if len(self.leDelRow_4.text()) > 0:
            self.delRow_4()
        
        #Finding number of rows - rs - and columns - cs - in the table
        rs = self.df.shape[0]
        cs = self.df.shape[1]
        
        print("cs is: ", cs)
        print("rs is now: ", rs)
        
        #Drop the following columns none of which will be used in filters
        self.df.drop('Change', inplace=True, axis=1)
        self.df.drop('Volume', inplace=True, axis=1)
        self.df.drop('Open Int', inplace=True, axis=1)
        self.df.drop('Last', inplace=True, axis=1)
        self.df.drop('Action', inplace=True, axis=1)
        self.df.drop('Action.1', inplace=True, axis=1)
        self.df.drop('Last.1', inplace=True, axis=1)
        self.df.drop('Change.1', inplace=True, axis=1)
        self.df.drop('Volume.1', inplace=True, axis=1)
        self.df.drop('Open Int.1', inplace=True, axis=1)
        
        #Adding ExpDate column
        exd = []
        for i in range(0, rs):
            exd.append("")
            i += i +1
        
        #Create and populate column ExpDate to be Column #1
        self.df.insert(0,"ExpDate", exd)
        
        #Create array to make Volatility-Bid Column for Calls and then Puts
        if self.rbCall.isChecked():
            vol = []
            for i in range(0, rs):
                vol.append("")
                i = i +1 
            self.df.insert(8, 'Volat-Bid', vol)
        elif self.rbPut.isChecked():
            vol_p = []
            for i in range(0, rs):
                vol_p.append("")
                i = i +1  
            self.df.insert(8, 'Volat-Bid.1', vol_p)
            
        #Create array to make Volatility-Ask Column for Calls and then Puts 
        if self.rbCall.isChecked():
            volA = []
            for i in range(0, rs):
                volA.append("")
                i = i +1  
            self.df.insert(9, 'Volat-Ask', volA)
        elif self.rbPut.isChecked():
            volB = []
            for i in range(0, rs):
                volB.append("")
                i = i +1 
            self.df.insert(9, 'Volat-Ask.1', volB)

        #Making a new column for current price and fill with Current Price
        self.df["Current"] = float(self.leCurPri.text())
        
        #Adding Result of Strike Price divided by current price
        self.df["Strk/Curr"] = self.df["Strike"] / self.df["Current"]
        
        #Conversion of self.df[Bid] from object to float for Calls and Puts
        if self.rbCall.isChecked():
            self.df['Bid'] = self.df['Bid'].astype(float, errors = 'raise')
            self.df["Ask-Bid"] = self.df["Ask"] - self.df["Bid"]
        elif self.rbPut.isChecked():
            self.df['Bid.1'] = self.df['Bid.1'].astype(float, errors = 'raise')
            self.df["Ask.1-Bid.1"] = self.df["Ask.1"] - self.df["Bid.1"]
            
        #Compare ExpDate1 with the current date & If different proceed
        #to insert the earliest expiratory date in ExpDate column
        if (self.deExpDat1.date != self.deCurDat.date):
            date_input = self.deExpDat1.text()
            datetimeobject = datetime.strptime(date_input, '%d %b %Y')
            eDate1 = datetimeobject.date()
            #Setting first Date of ExpDate column row 0
            self.df.loc[0, 'ExpDate'] = eDate1
            #Moving to index first row 
            index = 0
            rs = self.df.shape[0]
            if len(self.leDelRow_1.text()) > 0:
                while index != int(self.leDelRow_1.text()):
                    self.df.loc[index,'ExpDate'] = eDate1
                    index = index + 1
            else:
                while index <= rs: 
                    self.df.loc[index,'ExpDate'] = eDate1
                    index = index + 1
        
        #Compare ExpDate2 with the current date; If different proceed
        #to insert the second expiratory date in ExpDate column
        if (self.deExpDat2.date != self.deCurDat.date):
            #Skipping Rows that have no data
            index = index + 1
            #Initializing date to insert for second table values
            date_inputC = self.deCurDat.text()
            datetimeobjectC = datetime.strptime(date_inputC, '%d %b %Y')
            eDateC = datetimeobjectC.date()
            #Inserting ExpDate2 to insert for second table values
            date_input2 = self.deExpDat2.text()
            datetimeobject2 = datetime.strptime(date_input2, '%d %b %Y')
            eDate2 = datetimeobject2.date()
            
            rs = self.df.shape[0]
        
            #Moving thru 
            if (eDate2 != eDateC): 
                if len(self.leDelRow_2.text()) > 0:
                    while (index != int(self.leDelRow_2.text())):
                        self.df.loc[index,'ExpDate'] = eDate2
                        index = index + 1
                else:
                    while (index != rs):
                        self.df.loc[index,'ExpDate'] = eDate2
                        index = index + 1
                    self.df.loc[index,'ExpDate'] = eDate2
                    
        #Compare ExpDate3 with the current date; If different proceed and
        #insert third expiratory date into ExpDate column
        if (self.deExpDat3.date != self.deCurDat.date):
            #Skipping Rows that have no data
            index = index + 1
            #Initializing date to insert for third table values
            date_inputC = self.deCurDat.text()
            datetimeobjectC = datetime.strptime(date_inputC, '%d %b %Y')
            eDateC = datetimeobjectC.date()
            #Inserting ExpDate2 to insert for third table values
            date_input3 = self.deExpDat3.text()
            datetimeobject3 = datetime.strptime(date_input3, '%d %b %Y')
            eDate3 = datetimeobject3.date()
            
            rs = self.df.shape[0]
        
            #Moving thru 
            if (eDate3 != eDateC): 
                if len(self.leDelRow_3.text()) > 0:
                    while (index != int(self.leDelRow_3.text())):
                        self.df.loc[index,'ExpDate'] = eDate3
                        index = index + 1
                else:
                    while (index != rs):
                        self.df.loc[index,'ExpDate'] = eDate3
                        index = index + 1
                    self.df.loc[index,'ExpDate'] = eDate3
                    
        #Compare ExpDate4 with the current date; If different proceed and
        #insert fourth expiratory date into ExpDate column
        if (self.deExpDat4.date != self.deCurDat.date):
             #Skipping Rows that have no data
             index = index + 1
             #Initializing date to insert for third table values
             date_inputC = self.deCurDat.text()
             datetimeobjectC = datetime.strptime(date_inputC, '%d %b %Y')
             eDateC = datetimeobjectC.date()
             #Inserting ExpDate2 to insert for third table values
             date_input4 = self.deExpDat4.text()
             datetimeobject4 = datetime.strptime(date_input4, '%d %b %Y')
             eDate4 = datetimeobject4.date()
             
             rs = self.df.shape[0]
         
             #Moving thru 
             if (eDate4 != eDateC): 
                 if len(self.leDelRow_4.text()) > 0:
                     while (index != int(self.leDelRow_4.text())):
                         self.df.loc[index,'ExpDate'] = eDate4
                         index = index + 1
                 else:
                     while (index != rs):
                         self.df.loc[index,'ExpDate'] = eDate4
                         index = index + 1
                     self.df.loc[index,'ExpDate'] = eDate4
        
        #integers representing rows to be deleted
        dr1 = 0 
        dr2 = 0
        dr3 = 0
        dr4 = 0
        
        #Getting the values from the deleted row line edits 
        if len(self.leDelRow_1.text()) > 0:
            dr1 = int(self.leDelRow_1.text())
        if len(self.leDelRow_2.text()) > 0:
            dr2 = int(self.leDelRow_2.text())
        if len(self.leDelRow_3.text()) > 0:
            dr3 = int(self.leDelRow_3.text())
        if len(self.leDelRow_4.text()) > 0:
            dr4 = int(self.leDelRow_4.text())
        
        dataTypeSeries = self.df.dtypes
        print(dataTypeSeries)
        
        #Making a copy of df which is only a copy and any changes to the copied
        #file, will not change the original dataframe(df)
        self.df1 = self.df.copy()
        
        #Creating table to accomdate Calls    
        if self.rbCall.isChecked():
            self.filNum = self.filNum + 1
            self.df1.drop('Bid.1', inplace=True, axis=1)
            self.df1.drop('Ask.1', inplace=True, axis=1)
            self.df1.drop('Delta.1', inplace=True, axis=1)
            self.df1.drop('Imp Vol.1', inplace=True, axis=1)
        #Creating table to accomdate Puts        
        elif self.rbPut.isChecked():
            self.filNum = self.filNum + 1
            self.df1.drop('Bid', inplace=True, axis=1)
            self.df1.drop('Ask', inplace=True, axis=1)
            self.df1.drop('Delta', inplace=True, axis=1)
            self.df1.drop('Imp Vol', inplace=True, axis=1)
                         
        #Calculation of expected call bid volatility
        if (len(self.leBidVolMin.text()) == 0 and (len(self.leBidVolMax.text())) == 0) \
            and (self.rbCall.isChecked()):
            index = 0 
            for index, row in self.df1.iterrows():
                if (index != 0) and ((dr1 == index) or (dr2 == index) or \
                                     (dr3 == index) or (dr4 == index)): 
                    index = index + 1
                        
                premK = float(self.df1.loc[index, 'Bid'])
                premUK = 0.07
                v = 0.10
                vF = 0.0
                while (premUK < premK):
                    #Calculations on options with a very low premium don't give a significant answer
                    S = float(self.leCurPri.text())
                    K = float(self.df1.loc[index, 'Strike'])
                    r = 0.005
                    r = r / 100
                    v = v + .001
                    t = self.matTime()
                    d1_numerator = np.log(S/K) + (r + ((v * v)/2)) * t
                    d1_denominator = v * math.sqrt(t)
                    d1 = d1_numerator/d1_denominator
                    d2 = d1 - v * math.sqrt(t)
                    x = d1
                    firstFactor = S * stats.norm.cdf(x)
                    secondFactor = K * math.exp(-r*t) * stats.norm.cdf(d2)
                    premium = firstFactor - secondFactor
                    premUK = premium
                    vF = int(v * 100)
                    vF = format(vF, ".2f")
                    vF = float(v * 100)
                    vF = round(vF, 2)
                    rs = self.df1.shape[0]
                    
                self.df1.loc[index, 'Volat-Bid'] = (str(vF) + "%")
                
        #Calculation of expected call Ask volatility
        if (len(self.leAskVolMin.text()) == 0 and (len(self.leAskVolMax.text())) == 0) \
             and (self.rbCall.isChecked()):
             index = 0 
             for index, row in self.df1.iterrows():
                 if (index != 0) and ((dr1 == index) or (dr2 == index) or \
                                      (dr3 == index) or (dr4 == index)): 
                     index = index + 1
                         
                 premK = float(self.df1.loc[index, 'Ask'])
                 premUK = 0.07
                 v = 0.10
                 vF = 0.0
                 while (premUK < premK):
                     #Calculations on options with a very low premium don't give a significant answer
                     S = float(self.leCurPri.text())
                     K = float(self.df1.loc[index, 'Strike'])
                     r = 0.005
                     r = r / 100
                     v = v + .001
                     t = self.matTime()
                     d1_numerator = np.log(S/K) + (r + ((v * v)/2)) * t
                     d1_denominator = v * math.sqrt(t)
                     d1 = d1_numerator/d1_denominator
                     d2 = d1 - v * math.sqrt(t)
                     x = d1
                     firstFactor = S * stats.norm.cdf(x)
                     secondFactor = K * math.exp(-r*t) * stats.norm.cdf(d2)
                     premium = firstFactor - secondFactor
                     premUK = premium
                     vF = int(v * 100)
                     vF = format(vF, ".2f")
                     vF = float(v * 100)
                     vF = round(vF, 2)
                     rs = self.df1.shape[0]
                     
                 self.df1.loc[index, 'Volat-Ask'] = (str(vF) + "%")

        #calculation of Bid volatilities for Puts
        if (len(self.leBidVolMin.text()) == 0 and (len(self.leBidVolMax.text())) == 0) \
            and (self.rbPut.isChecked()):
                index = 0 
                for index, row in self.df1.iterrows():
                    if (index != 0) and ((dr1 == index) or (dr2 == index) or \
                                         (dr3 == index) or (dr4 == index)): 
                        index = index + 1
                            
                    premK = float(self.df1.loc[index, 'Bid.1'])
                    premUK = 0.07
                    v = 0.10
                    vF = 0.0
                    while (premUK < premK):
                        #Calculations on options with a very low premium don't give a significant answer
                        S = float(self.leCurPri.text())
                        K = float(self.df1.loc[index, 'Strike'])
                        r = 0.005
                        r = r / 100
                        v = v + .001
                        t = self.matTime()
                        d1_numerator = np.log(S/K) + (r + ((v * v)/2)) * t
                        d1_denominator = v * math.sqrt(t)
                        d1 = d1_numerator/d1_denominator
                        d2 = d1 - v * math.sqrt(t)
                        x = -d2
                        y = -d1
                        factorOne = stats.norm.cdf(x) * K * math.exp(-r*t) 
                        factorTwo = stats.norm.cdf(y) * S
                        premiumP = factorOne - factorTwo
                        premUK = premiumP
                        vF = int(v * 100)
                        vF = format(vF, ".2f")
                        vF = float(v * 100)
                        vF = round(vF, 2)
                        rs = self.df.shape[0]
                        
                    self.df1.loc[index, 'Volat-Bid.1'] = (str(vF) + "%")
        
        
        #calculation of Ask volatilities for Puts
        if (len(self.leAskVolMin.text()) == 0 and (len(self.leAskVolMax.text())) == 0) \
            and (self.rbPut.isChecked()):
                index = 0 
                for index, row in self.df1.iterrows():
                    if (index != 0) and ((dr1 == index) or (dr2 == index) or \
                                         (dr3 == index) or (dr4 == index)): 
                        index = index + 1
                            
                    premK = float(self.df1.loc[index, 'Ask.1'])
                    premUK = 0.07
                    v = 0.10
                    vF = 0.0
                    while (premUK < premK):
                        #Calculations on options with a very low premium don't give a significant answer
                        S = float(self.leCurPri.text())
                        K = float(self.df1.loc[index, 'Strike'])
                        r = 0.005
                        r = r / 100
                        v = v + .001
                        t = self.matTime()
                        d1_numerator = np.log(S/K) + (r + ((v * v)/2)) * t
                        d1_denominator = v * math.sqrt(t)
                        d1 = d1_numerator/d1_denominator
                        d2 = d1 - v * math.sqrt(t)
                        x = -d2
                        y = -d1
                        factorOne = stats.norm.cdf(x) * K * math.exp(-r*t) 
                        factorTwo = stats.norm.cdf(y) * S
                        premiumP = factorOne - factorTwo
                        premUK = premiumP
                        vF = int(v * 100)
                        vF = format(vF, ".2f")
                        vF = float(v * 100)
                        vF = round(vF, 2)
                        rs = self.df.shape[0]
                        
                    self.df1.loc[index, 'Volat-Ask.1'] = (str(vF) + "%")

        #Determining which dataframe will be shown.
        if self.filNum > 0:
            self.model = TableModel(self.df1)
            self.table.setModel(self.model) 
        else:
            self.model = TableModel(self.df)
            self.table.setModel(self.model)  
        
    def calc_mat_time1(self):
        d1 = datetime.now().date()
        date_input = self.deExpDat1.text()
        datetimeobject = datetime.strptime(date_input, '%d %b %Y')
        d2 = datetimeobject.date()
        delta = d2 - d1
        matTime = delta.days / 365.25
        self.leMatTim1.setFocus()
        self.leMatTim1.setText(str("{:.4f}".format(matTime)))
        
    def calc_mat_time2(self):
        d1 = datetime.now().date()
        date_input = self.deExpDat2.text()
        datetimeobject = datetime.strptime(date_input, '%d %b %Y')
        d2 = datetimeobject.date()
        delta = d2 - d1
        matTime = delta.days / 365.25
        self.leMatTim2.setFocus()
        self.leMatTim2.setText(str("{:.4f}".format(matTime)))
        
    def calc_mat_time3(self):
        d1 = datetime.now().date()
        date_input = self.deExpDat3.text()
        datetimeobject = datetime.strptime(date_input, '%d %b %Y')
        d2 = datetimeobject.date()
        delta = d2 - d1
        matTime = delta.days / 365.25
        self.leMatTim3.setFocus()
        self.leMatTim3.setText(str("{:.4f}".format(matTime)))
        
    def calc_mat_time4(self):
        d1 = datetime.now().date()
        date_input = self.deExpDat4.text()
        datetimeobject = datetime.strptime(date_input, '%d %b %Y')
        d2 = datetimeobject.date()
        delta = d2 - d1
        matTime = delta.days / 365.25
        self.leMatTim4.setFocus()
        self.leMatTim4.setText(str("{:.4f}".format(matTime)))
        
    def minMaxStrCur(self):
        if self.cflag == True:
            self.df1 = self.dfp.copy()
        elif self.cflag == False:
            self.df1 = self.df1.copy()
            #Because cflag is false df1 will be the dataframe used here
            #If another filter had been used first dfp would have been 
            #created at the end of the filter query and then copied to df1 here
            #dfp stands for "dataframe previous" and cflag is for "copy flag"           
            
        if (len(self.leStrCurMin.text()) > 0 and (len(self.leStrCurMax.text())) > 0) \
            and (self.rbCall.isChecked()):
            self.filNum = self.filNum + 1
            scMin = self.leStrCurMin.text()
            scMax = self.leStrCurMax.text()
            self.df1 = (self.df1.loc[self.df1['Strk/Curr'] >= float(scMin)]) 
            self.df1 = (self.df1.loc[self.df1["Strk/Curr"] <= float(scMax)])
            self.df1 = self.df1.sort_values(by = 'Strk/Curr')
            self.model = TableModel(self.df1)
            self.table.setModel(self.model) 
        if (len(self.leStrCurMin.text()) > 0 and (len(self.leStrCurMax.text())) > 0) \
            and (self.rbPut.isChecked()):
            self.filNum = self.filNum + 1
            #Get results from StrikePrice/CurrentPrice Minium
            scMin = self.leStrCurMin.text()
            self.df1 = self.df1.loc[self.df1['Strk/Curr'] >= float(scMin)]
            #Get results from StrikePrice/CurrentPrice Maximum
            scMax = self.leStrCurMax.text()
            self.df1 = self.df1.loc[self.df1["Strk/Curr"] <= float(scMax)]
            self.df1 = self.df1.sort_values(by = 'Strk/Curr')
            self.model = TableModel(self.df1)
            self.table.setModel(self.model) 
            
        self.dfp = self.df1.copy() 
        self.cflag = True
        
    def minMaxBidVol(self):
        if self.cflag == True:
            self.df2 = self.dfp.copy()
        else:
            self.df2 = self.df1.copy()
        
        if (len(self.leBidVolMin.text()) > 0 and (len(self.leBidVolMax.text())) > 0) \
            and self.rbCall.isChecked():
            self.filNum = self.filNum + 1
            #Get results from Volat-Bib Minium
            volMin = self.leBidVolMin.text()
            volMin = float(volMin)
            #Get results from Volat-Bib Maximum
            volMax = self.leBidVolMax.text()
            volMax = float(volMax)
            #Convert percent values to floats in Volat-Bid
            self.df2['Volat-Bid'] = self.df2['Volat-Bid'].str.rstrip("%").astype(float)
            self.df2 = self.df2.loc[self.df2['Volat-Bid'] >= float(volMin)]
            self.df2 = self.df2.loc[self.df2['Volat-Bid'] <= float(volMax)]
            self.df2 = self.df2.sort_values(by = 'Volat-Bid')
            self.model = TableModel(self.df2)
            self.table.setModel(self.model) 
        elif (len(self.leBidVolMin.text()) > 0 and (len(self.leBidVolMax.text())) > 0) \
            and self.rbPut.isChecked():
            self.filNum = self.filNum + 1
            #Get results from Volat-Bib Minium
            volMin = self.leBidVolMin.text()
            volMin = float(volMin)
            #Get results from Volat-Bib Maximum
            volMax = self.leBidVolMax.text()
            volMax = float(volMax)
            #Convert percent values to floats in Volat-Bid
            self.df2['Volat-Bid.1'] = self.df2['Volat-Bid.1'].str.rstrip("%").astype(float)
            self.df2 = self.df2.loc[self.df2['Volat-Bid.1'] >= float(volMin)]
            self.df2 = self.df2.loc[self.df2['Volat-Bid.1'] <= float(volMax)]
            self.df2 = self.df2.sort_values(by = 'Volat-Bid.1')
            self.model = TableModel(self.df2)
            self.table.setModel(self.model) 
            
        self.dfp = self.df2.copy()
        self.cflag = True
        
            
    def minMaxAskVol(self):
        if self.cflag == True:
            self.df3 = self.dfp.copy()
        else:
            self.df3 = self.df1.copy()
        
        if (len(self.leAskVolMin.text()) > 0 and (len(self.leAskVolMax.text())) > 0) \
            and self.rbCall.isChecked():
            self.filNum = self.filNum + 1
            #Get results from Volat-Bib Minium
            volMin = self.leAskVolMin.text()
            volMin = float(volMin)
            #Get results from Volat-Bib Maximum
            volMax = self.leAskVolMax.text()
            volMax = float(volMax)
            #Convert percent values to floats in Volat-Bid
            self.df3['Volat-Ask'] = self.df3['Volat-Ask'].str.rstrip("%").astype(float)
            self.df3 = self.df3.loc[self.df3['Volat-Ask'] >= float(volMin)]
            self.df3 = self.df3.loc[self.df3['Volat-Ask'] <= float(volMax)]
            self.df3 = self.df3.sort_values(by = 'Volat-Ask')
            self.model = TableModel(self.df3)
            self.table.setModel(self.model) 
        elif (len(self.leAskVolMin.text()) > 0 and (len(self.leAskVolMax.text())) > 0) \
            and self.rbPut.isChecked():
            self.filNum = self.filNum + 1
            #Get results from Volat-Bib Minium
            volMin = self.leAskVolMin.text()
            volMin = float(volMin)
            #Get results from Volat-Bib Maximum
            volMax = self.leAskVolMax.text()
            volMax = float(volMax)
            #Convert percent values to floats in Volat-Bid
            self.df3['Volat-Ask.1'] = self.df3['Volat-Ask.1'].str.rstrip("%").astype(float)
            self.df3 = self.df3.loc[self.df3['Volat-Ask.1'] >= float(volMin)]
            self.df3 = self.df3.loc[self.df3['Volat-Ask.1'] <= float(volMax)]
            self.df3 = self.df3.sort_values(by = 'Volat-Ask.1')
            self.model = TableModel(self.df3)
            self.table.setModel(self.model) 
            
        self.dfp = self.df3.copy()
        self.cflag = True
            
    def minMaxDelta(self):
        if self.cflag == True:
            self.df4 = self.dfp.copy()
        else:
            self.df4 = self.df1.copy()
        
        if (len(self.leDelMax.text()) > 0 and (len(self.leDelMin.text())) > 0) and \
            self.rbCall.isChecked():
            self.filNum = self.filNum + 1
            dtMax = self.leDelMax.text()
            dtMin = self.leDelMin.text()
            self.df4 = self.df4.loc[self.df4['Delta'] >= float(dtMin)]
            self.df4 = self.df4.loc[self.df4['Delta'] <= float(dtMax)]
            self.df4 = self.df4.sort_values(by = 'Delta')
            self.model = TableModel(self.df4)
            self.table.setModel(self.model) 
        elif (len(self.leDelMax.text()) > 0 and (len(self.leDelMin.text())) > 0) and \
            self.rbPut.isChecked():
            self.filNum = self.filNum + 1
            dtMax = self.leDelMax.text()
            dtMin = self.leDelMin.text()
            self.df4 = self.df4.loc[self.df4['Delta.1'] >= float(dtMin)]
            self.df4 = self.df4.loc[self.df4['Delta.1'] <= float(dtMax)]
            self.df4 = self.df4.sort_values(by = 'Delta.1')
            self.model = TableModel(self.df4)
            self.table.setModel(self.model) 
            
        self.dfp = self.df4.copy()
        self.cflag = True
            
    def maxAskMinusBid(self):
        if self.cflag == True:
            self.df5 = self.dfp.copy()
        else:
            self.df5 = self.df1.copy()
        
        if len(self.leBidAsk.text()) > 0:
            if self.rbCall.isChecked():
                self.filNum = self.filNum + 1
                abMax = self.leBidAsk.text()
                self.df5 = self.df5.loc[self.df1['Ask-Bid'] >= 0.0000]
                self.df5 = self.df5.loc[self.df1['Ask-Bid'] <= float(abMax)]
                self.df5 = self.df5.sort_values(by = 'Ask-Bid')
                self.model = TableModel(self.df5)
                self.table.setModel(self.model) 
            elif self.rbPut.isChecked():
                self.filNum = self.filNum + 1
                abMax = self.leBidAsk.text()
                self.df5 = (self.df5.loc[self.df5['Ask-Bid.1'] >= 0.0000]) and \
                (self.df5.loc[self.df5['Ask-Bid.1'] <= float(abMax)])
                self.df5 = self.df5.sort_values(by = 'Ask-Bid.1')
                self.model = TableModel(self.df5)
                self.table.setModel(self.model) 
                
            self.dfp = self.df5.copy()
            self.cflag = True
        
    def opFid(self):
        if self.cbFid.isChecked():
            webbrowser.open('https://www.fidelity.com/')
            
    def opExl(self):
        if self.cbExc.isChecked():
            subprocess.check_call(['open', '-a', 'Microsoft Excel'])
            
    def opMW(self):
        if self.cbMarWat.isChecked():
            webbrowser.open('https://www.marketwatch.com/')
            
    def delRow(self):
        if len(self.leDelRow_1.text()) > 0:
            x = self.leDelRow_1.text()
            y = int(x)
            self.df = self.df.drop(self.df.index[y]) 
            self.model = TableModel(self.df)
            
    def delRow_2(self):
        if len(self.leDelRow_2.text()) > 0:
            x = self.leDelRow_2.text()
            y = int(x) - 1
            self.df = self.df.drop(self.df.index[y]) 
            self.model = TableModel(self.df)
            
    def delRow_3(self):
        if len(self.leDelRow_3.text()) > 0:
            x = self.leDelRow_3.text()
            y = int(x) - 2
            self.df = self.df.drop(self.df.index[y]) 
            self.model = TableModel(self.df)

    def delRow_4(self):
        if len(self.leDelRow_4.text()) > 0:
            x = self.leDelRow_4.text()
            y = int(x) - 3
            self.df = self.df.drop(self.df.index[y]) 
            self.model = TableModel(self.df)
            
    def matTime(self):
        if len(self.leDelRow_1.text()) == False:
            return float(self.leMatTim1.text())
        elif len(self.leDelRow_1.text()) > 0 and len(self.leDelRow_2.text()) == False:
            return float(self.leMatTim2.text())
        elif len(self.leDelRow_2.text()) > 0 and len(self.leDelRow_3.text()) == False:
            return float(self.leMatTim2.text())
        elif len(self.leDelRow_3.text()) > 0 and len(self.leDelRow_4.text()) == False:
            return float(self.leMatTim3.text())
        elif len(self.leDelRow_4.text()) > 0:
            return float(self.leMatTim4.text())
        
    def reload(self):
        self.leStrCurMin.clear()
        self.leStrCurMax.clear()
        self.leBidVolMin.clear()
        self.leBidVolMax.clear()
        self.leAskVolMin.clear()
        self.leAskVolMax.clear()
        self.leDelMin.clear()
        self.leDelMax.clear()
        self.leBidAsk.clear()
        self.loadData()
        
        
        
        
class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]
    
    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])
            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])

if __name__== '__main__':
    app = QApplication(sys.argv)
    demo = MainWindow()
    demo.show()
    sys.exit(app.exec())


