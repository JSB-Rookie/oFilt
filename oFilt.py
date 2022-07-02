import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QTableView, QMainWindow,\
    QDateEdit, QMessageBox, QButtonGroup)
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, uic
import pandas as pd
import numpy as np
import scipy.stats as stats
import math
from PyQt5.QtCore import QDate
from datetime import datetime, date
from datetime import timedelta
from dateutil import parser
import webbrowser
import subprocess
import calendar

qtcreator_file  = "oFilt.ui" #Entering the Qt Designer file, then connecting to this file
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow,self).__init__(*args, **kwargs)
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

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
        horizLay3.addWidget(self.cbExc)
        
        horizLay4.addWidget(self.pbSpCp)
        horizLay4.addWidget(self.pbBidVol)
        horizLay4.addWidget(self.pbAskVol)
        horizLay4.addWidget(self.pbDeltas)
        horizLay4.addWidget(self.pbAskBid)
        
        vertLay.addWidget(self.pbRawData)
        vertLay.addWidget(self.pbLoadFile)
        vertLay.addWidget(self.pbReload)
        vertLay.addWidget(self.pbHiCallVol)
        vertLay.addWidget(self.pbLoCallVol)
        vertLay.addWidget(self.pbHiPutVol)
        vertLay.addWidget(self.pbLoPutVol)
        vertLay.addWidget(self.pbTightCalls)
        vertLay.addWidget(self.pbTightPuts)
        
        bg = QButtonGroup(self)
        bg.addButton(self.rbWeekly)
        bg.addButton(self.rbMonthly)
        
        bg2 = QButtonGroup(self)
        bg2.addButton(self.rbAll)
        bg2.addButton(self.rbCall)
        bg2.addButton(self.rbPut)
        
        mainLayout.addWidget(self.table)
        
        self.pbLoadFile.clicked.connect(self.loadData)
        self.pbClose.clicked.connect(self.close)
        self.cbFid.stateChanged.connect(self.opFid)
        self.cbExc.stateChanged.connect(self.opExl)
        self.pbRawData.clicked.connect(self.clickRaw)
        self.pbRawData.clicked.connect(self.seeAll)
        self.pbSpCp.clicked.connect(self.minMaxStrCur)
        self.pbBidVol.clicked.connect(self.minMaxBidVol)
        self.pbAskVol.clicked.connect(self.minMaxAskVol)
        self.pbDeltas.clicked.connect(self.minMaxDelta)
        self.pbAskBid.clicked.connect(self.maxAskMinusBid)
        self.pbReload.clicked.connect(self.reload)
        self.pbHiCallVol.clicked.connect(self.askCallVolAsk_50)
        self.pbLoCallVol.clicked.connect(self.bidCallVolBid_40)
        self.pbHiPutVol.clicked.connect(self.askPutVolAsk_50)
        self.pbLoPutVol.clicked.connect(self.bidPutVolBid_40)
        self.pbTightCalls.clicked.connect(self.tightCalls)
        self.pbTightPuts.clicked.connect(self.tightPuts)
        self.leFileName.returnPressed.connect(self.addDat)
        self.rbCall.clicked.connect(self.hidePutButtons)
        self.rbPut.clicked.connect(self.hideCallButtons)
        
        self.dfR = pd.DataFrame() #Only used for Raw Data display
        self.df = pd.DataFrame()
        self.df1 = pd.DataFrame()
        self.df2 = pd.DataFrame()
        self.df3 = pd.DataFrame()
        self.df4 = pd.DataFrame()
        self.df5 = pd.DataFrame()
        self.df6 = pd.DataFrame()
        self.df7 = pd.DataFrame()
        self.df8 = pd.DataFrame()
        self.df9 = pd.DataFrame()
        self.df10 = pd.DataFrame()
        self.df11 = pd.DataFrame()
        self.dfp = pd.DataFrame()#For the previous dataframe
        
        self.mTime1 = 0.0
        self.mTime2 = 0.0
        self.mTime3 = 0.0
        self.mTime4 = 0.0

        self.filNum = 0 #Flag to notify Table mode and widget
        self.cflag = False #Flag to signify a copy of dataframe has been made
        self.filtName = ""
        self.v = 0.10 #Volatility variable
    
    def seeAll(self):
        fileName = self.leFileName.text()
        try:
            self.dfR = pd.read_csv(fileName)
            self.dfR = self.dfR.fillna(0)
            self.model = TableModel(self.dfR)
            self.table.setModel(self.model)
        except:
            QMessageBox.about(self, "Incorrect File Name", \
                              "You must enter the correct file name!")
           
    def clickRaw(self):
        if len(self.leFileName.text()) == 0:
            QMessageBox.about(self, "Enter File Name", \
                              "You must enter a file name!")
        if len(self.leCurPri.text()) == 0:
            QMessageBox.about(self, "Enter Current Price", \
                              "You must enter the current price!")
         
    def loadData(self):
        #Reading the file copied from Fidelity or MarketWatch
        if len(self.leStrCurMax.text()) > 0 or \
            len(self.leStrCurMin.text()) > 0 or \
            len(self.leBidVolMin.text()) > 0 or \
            len(self.leBidVolMax.text()) > 0 or \
            len(self.leAskVolMin.text()) > 0 or \
            len(self.leAskVolMax.text()) > 0 or \
            len(self.leDelMin.text()) > 0 or \
            len(self.leDelMax.text()) > 0 or \
            len(self.leBidAsk.text()) > 0:
                self.leStrCurMin.clear()
                self.leStrCurMax.clear()
                self.leBidVolMin.clear()
                self.leBidVolMax.clear()
                self.leAskVolMin.clear()
                self.leAskVolMax.clear()
                self.leDelMin.clear()
                self.leDelMax.clear()
                self.leBidAsk.clear()   
        fileName = self.leFileName.text()
        try:
            self.df = pd.read_csv(fileName)
            self.df = self.df.fillna(0)
        except:
            QMessageBox.about(self, "Incorrect File Name", \
                              "You must enter the correct file name!")
                
        if self.rbWeekly.isChecked() == False and self.rbMonthly.isChecked() == False:
            QMessageBox.about(self, "Weekly or Monthly", "You must select either Weekly or Monthly!")
        
        if self.rbCall.isChecked() == False and self.rbPut.isChecked() == False and \
            self.rbAll.isChecked() == False:
                QMessageBox.about(self, "All, Calls or Puts", "You must select All, Calls or Puts!")
                        
        self.df = self.df.rename(columns=({'Delta.1': 'Delta_1', 'Ask.1': 'Ask_1', 'Bid.1': 'Bid_1'}))
        
        #Finding number of rows - rs - and columns - cs - in the table
        rs = self.df.shape[0]
        cs = self.df.shape[1]
        
        #Drop the following columns none of which will be used in filters
        self.df.drop('Change', inplace=True, axis=1)
        self.df.drop('Volume', inplace=True, axis=1)
        self.df.drop('Open Int', inplace=True, axis=1)
        self.df.drop('Imp Vol', inplace=True, axis=1)
        self.df.drop('Last', inplace=True, axis=1)
        self.df.drop('Action', inplace=True, axis=1)
        self.df.drop('Action.1', inplace=True, axis=1)
        self.df.drop('Last.1', inplace=True, axis=1)
        self.df.drop('Change.1', inplace=True, axis=1)
        self.df.drop('Volume.1', inplace=True, axis=1)
        self.df.drop('Open Int.1', inplace=True, axis=1)
        self.df.drop('Imp Vol.1', inplace=True, axis=1)
        
        #Making a new column for current price and fill with Current Price
        self.df["Current"] = float(self.leCurPri.text())
        
        #Adding ExpDate column
        rs = self.df.shape[0]
        exd = []
        for i in range(0, rs):
            exd.append("")
            i += i +1
        
        #Create and populate column ExpDate to be Column #1
        self.df.insert(0,"ExpDate", exd)
        
        #Populate ExpDate column for weekly options then for Monthly options
        if self.rbWeekly.isChecked() == True:
            #Determination of days from today to maturity date 
            self.days = self.calDayDiff()
            self.eDate1 = date.today() + timedelta(self.days)
            
            self.days2 = 7
            self.days3 = 14
            self.days4 = 21
            
            #Determination of actual maturity dates
            self.eDate2 = self.eDate1 + timedelta(self.days2)
            self.eDate3 = self.eDate1 + timedelta(self.days3)
            self.eDate4 = self.eDate1 + timedelta(self.days4)
            
            index = 0
            self.ct = 0
            self.df['Strike'] = self.df['Strike'].replace(np.nan, 0)
            for ind in self.df.index:
                if self.ct == 0:
                    self.df.at[ind, 'ExpDate'] = self.eDate1
                elif self.ct == 1:
                    self.df.at[ind, 'ExpDate'] = self.eDate2
                elif self.ct == 2:
                    self.df.at[ind, 'ExpDate'] = self.eDate3
                elif self.ct == 3:
                    self.df.at[ind, 'ExpDate'] = self.eDate4
                
                if self.df['Strike'][ind] == 0.00:
                    self.df = self.df.drop(index=ind)
                    self.ct = self.ct + 1
        elif self.rbMonthly.isChecked() == True:
            self.df['Strike'] = self.df['Strike'].replace(np.nan, 0)
            c = calendar.Calendar(firstweekday=calendar.SUNDAY)
            current_date = datetime.now()
            year = current_date.year
            month = current_date.month 
            day = current_date.day
            monthcal = c.monthdatescalendar(year, month)
            self.ct = 0
            third_friday = [day for week in monthcal for day in week if
                    day.weekday() == calendar.FRIDAY and day.month == month][2]
            
            if (current_date.day > third_friday.day):
                self.eDate1 = self.fridayEd1nm()
                self.eDate2 = self.fridayEd2nm()
            else:
                self.eDate1 = self.fridayEd1cm()
                self.eDate2 = self.fridayEd2cm()
                
            for ind in self.df.index:
                if self.ct == 0:
                    self.df.at[ind, 'ExpDate'] = self.eDate1
                elif self.ct == 1:
                    self.df.at[ind, 'ExpDate'] = self.eDate2
                
                if self.df['Strike'][ind] == 0.00:
                    self.df = self.df.drop(index=ind)
                    self.ct = self.ct + 1
                         
        #Create array to make Volatility-Bid Column for Calls and then Puts
        rs = self.df.shape[0]
        if self.rbCall.isChecked() == True:
            vol = []
            for i in range(0, rs):
                vol.append("")
                i = i +1 
            self.df.insert(8, 'VolatBid', vol)
        elif self.rbPut.isChecked() == True:
            vol_p = []
            for i in range(0, rs):
                vol_p.append("")
                i = i +1  
            self.df.insert(8, 'VolatBid_1', vol_p)
            
        #Create array to make Volatility-Ask Column for Calls and then Puts 
        if self.rbCall.isChecked() == True:
            volA = []
            for i in range(0, rs):
                volA.append("")
                i = i +1  
            self.df.insert(9, 'Volat-Ask', volA)
        elif self.rbPut.isChecked() == True:
            volB = []
            for i in range(0, rs):
                volB.append("")
                i = i +1 
            self.df.insert(9, 'Volat-Ask_1', volB)
         
        #Adding Result of Strike Price divided by current price
        self.df["StrkCurr"] = self.df["Strike"] / self.df["Current"]
        self.df['StrkCurr'] = pd.Series(["{0:.1f}%".format(val * 100) for val in self.df['StrkCurr']], index = self.df.index)
        
          
        #Conversion of self.df[Bid] from object to float for Calls and Puts
        if self.rbCall.isChecked() == True:
            self.df['Bid'] = self.df['Bid'].astype(float, errors = 'raise')
            self.df["Ask-Bid"] = (self.df["Ask"] - self.df["Bid"])
            self.df['Ask-Bid'] = pd.Series(["{0:.2f}".format(val) for val in self.df['Ask-Bid']], index = self.df.index)
        elif self.rbPut.isChecked() == True:
            self.df['Bid_1'] = self.df['Bid_1'].astype(float, errors = 'raise')
            self.df["Ask_1-Bid_1"] = (self.df["Ask_1"] - self.df["Bid_1"])
            self.df['Ask_1-Bid_1'] = pd.Series(["{0:.2f}".format(val) for val in self.df['Ask_1-Bid_1']], index = self.df.index)

        
        #Deletion of rows where Bid + Strike < current price
        rs = self.df.shape[0]
        self.df["Bid"] = self.df.Bid.astype(float)
        
        #The below code will discard Delta values of '--' and create a new dataframe - NOT A COPY
        self.df = self.df.loc[self.df['Delta'] != '--']
        self.df = self.df.loc[self.df['Delta'] != -1]
        
        
        self.df['Delta_1'] = self.df.Delta_1.astype(float)
        self.df['Delta'] = self.df.Delta.astype(float)
        self.df.reset_index(inplace = True, drop = True)
    
        
        self.df['Bid'] = self.df.Bid.astype(float)
        self.df['Ask'] = self.df.Ask.astype(float)
        
        
        #dataframe[‘column_name’].loc[dataframe.index[row_number]]
        bnum = self.df.columns.get_loc("Bid")
        snum = self.df.columns.get_loc("Strike")
        cnum = self.df.columns.get_loc("Current")
             
        rs = self.df.shape[0]
        self.df.reset_index(inplace = True, drop = True)
        
                
        #Creating table to accomdate Calls    
        if self.rbCall.isChecked() == True:
            self.filNum = self.filNum + 1
            self.df.drop('Bid_1', inplace=True, axis=1)
            self.df.drop('Ask_1', inplace=True, axis=1)
            self.df.drop('Delta_1', inplace=True, axis=1)
        #Creating table to accomdate Puts        
        elif self.rbPut.isChecked() == True:
            self.filNum = self.filNum + 1
            self.df.drop('Bid', inplace=True, axis=1)
            self.df.drop('Ask', inplace=True, axis=1)
            self.df.drop('Delta', inplace=True, axis=1)
            
        self.df.reset_index(inplace = True, drop = True)
                         
        #Calculation of expected call bid volatility
        if (len(self.leBidVolMin.text()) == 0 and (len(self.leBidVolMax.text())) == 0) \
            and (self.rbCall.isChecked() == True):
            index = 0 
            for index, row in self.df.iterrows():
                premK = float(self.df.loc[index, 'Bid'])
                premUK = 0.07
                vF = 0.0
                self.v = 0.05
                S = float(self.leCurPri.text())
                while (premUK < premK):
                    #Calculations on options with a very low premium don't give a significant answer
                    K = float(self.df.loc[index, 'Strike'])
                    r = 1.5
                    r = r / 100
                    t = self.matTime(index)
                    self.v = self.v + .05
                    d1_numerator = np.log(S/K) + (r + ((self.v * self.v)/2)) * t
                    d1_denominator = self.v * math.sqrt(t)
                    d1 = d1_numerator/d1_denominator
                    d2 = d1 - self.v * math.sqrt(t)
                    x = d1
                    firstFactor = S * stats.norm.cdf(x)
                    secondFactor = K * math.exp(-r*t) * stats.norm.cdf(d2)
                    premium = firstFactor - secondFactor
                    premUK = premium
                    
                premUK = 0.07    
                self.v = self.v - .05
                while(premUK < premK):
                    K = float(self.df.loc[index, 'Strike'])
                    r = 1.5
                    r = r / 100
                    self.v = self.v + 0.001
                    t = self.matTime(index)
                    d1_numerator = np.log(S/K) + (r + ((self.v * self.v)/2)) * t
                    d1_denominator = self.v * math.sqrt(t)
                    d1 = d1_numerator/d1_denominator
                    d2 = d1 - self.v * math.sqrt(t)
                    x = d1
                    firstFactor = S * stats.norm.cdf(x)
                    secondFactor = K * math.exp(-r*t) * stats.norm.cdf(d2)
                    premium = firstFactor - secondFactor
                    premUK = premium
                    
                vF = int(self.v * 100)
                vF = format(vF, ".2f")
                vF = float(self.v * 100)
                vF = round(vF, 2)
                rs = self.df.shape[0]
                self.df.loc[index, 'VolatBid'] = (str(vF) + "%")
                index = index + 1
                
        #Calculation of expected call Ask volatility
        if (len(self.leAskVolMin.text()) == 0 and (len(self.leAskVolMax.text())) == 0) \
             and (self.rbCall.isChecked() == True):
             index = 0 
             for index, row in self.df.iterrows():
                 premK = float(self.df.loc[index, 'Ask'])
                 premUK = 0.07
                 vF = 0.0
                 self.v = 0.05
                 S = float(self.leCurPri.text())
                 while (premUK < premK):
                     #Calculations on options with a very low premium don't give a significant answer
                     K = float(self.df.loc[index, 'Strike'])
                     r = 1.5
                     r = r / 100
                     self.v = self.v + .05
                     t = self.matTime(index)
                     d1_numerator = np.log(S/K) + (r + ((self.v * self.v)/2)) * t
                     d1_denominator = self.v * math.sqrt(t)
                     d1 = d1_numerator/d1_denominator
                     d2 = d1 - self.v * math.sqrt(t)
                     x = d1
                     firstFactor = S * stats.norm.cdf(x)
                     secondFactor = K * math.exp(-r*t) * stats.norm.cdf(d2)
                     premium = firstFactor - secondFactor
                     premUK = premium
                    
                 premUK = 0.07    
                 self.v = self.v - .05
                 while (premUK < premK):
                     #Calculations on options with a very low premium don't give a significant answer
                     K = float(self.df.loc[index, 'Strike'])
                     r = 1.5
                     r = r / 100
                     self.v = self.v + 0.001
                     t = self.matTime(index)
                     d1_numerator = np.log(S/K) + (r + ((self.v * self.v)/2)) * t
                     d1_denominator = self.v * math.sqrt(t)
                     d1 = d1_numerator/d1_denominator
                     d2 = d1 - self.v * math.sqrt(t)
                     x = d1
                     firstFactor = S * stats.norm.cdf(x)
                     secondFactor = K * math.exp(-r*t) * stats.norm.cdf(d2)
                     premium = firstFactor - secondFactor
                     premUK = premium
                     
                 vF = int(self.v * 100)
                 vF = format(vF, ".2f")
                 vF = float(self.v * 100)
                 vF = round(vF, 2)
                 rs = self.df.shape[0]
                 self.df.loc[index, 'Volat-Ask'] = (str(vF) + "%")
                 index = index + 1
                 
                 
         #calculation of Bid volatilities for Puts
        if (len(self.leBidVolMin.text()) == 0 and (len(self.leBidVolMax.text())) == 0) \
            and (self.rbPut.isChecked() == True):
            index = 0 
            for index, row in self.df.iterrows():
                premK = float(self.df.loc[index, 'Bid_1'])
                premUK = 0.07
                self.v = 0.05
                vF = 0.0
                S = float(self.leCurPri.text())
                while (premUK < premK):
                    #Calculations on options with a very low premium don't give a significant answer
                    K = float(self.df.loc[index, 'Strike'])
                    r = 1.5
                    r = r / 100
                    self.v = self.v + .05
                    t = self.matTime(index)
                    d1_numerator = np.log(S/K) + (r + ((self.v * self.v)/2)) * t
                    d1_denominator = self.v * math.sqrt(t)
                    d1 = d1_numerator/d1_denominator
                    d2 = d1 - self.v * math.sqrt(t)
                    x = -d2
                    y = -d1
                    factorOne = stats.norm.cdf(x) * K * math.exp(-r*t) 
                    factorTwo = stats.norm.cdf(y) * S
                    premiumP = factorOne - factorTwo
                    premUK = premiumP
                   
                vF = 0.0
                premUK = 0.07    
                self.v = self.v - .05
                while (premUK < premK):
                    #Calculations on options with a very low premium don't give a significant answer
                    S = float(self.leCurPri.text())
                    K = float(self.df.loc[index, 'Strike'])
                    r = 0.005
                    r = r / 100
                    self.v = self.v + 0.001
                    t = self.matTime(index)
                    d1_numerator = np.log(S/K) + (r + ((self.v * self.v)/2)) * t
                    d1_denominator = self.v * math.sqrt(t)
                    d1 = d1_numerator/d1_denominator
                    d2 = d1 - self.v * math.sqrt(t)
                    x = -d2
                    y = -d1
                    factorOne = stats.norm.cdf(x) * K * math.exp(-r*t) 
                    factorTwo = stats.norm.cdf(y) * S
                    premiumP = factorOne - factorTwo
                    premUK = premiumP
   
                vF = int(self.v * 100)
                vF = format(vF, ".2f")
                vF = float(self.v * 100)
                vF = round(vF, 2)
                rs = self.df.shape[0]
                   
                self.df.loc[index, 'VolatBid_1'] = (str(vF) + "%")
                
   
        #calculation of Ask volatilities for Puts
        if (len(self.leAskVolMin.text()) == 0 and (len(self.leAskVolMax.text())) == 0) \
            and (self.rbPut.isChecked() == True):
                index = 0 
                for index, row in self.df.iterrows():
                    premK = float(self.df.loc[index, 'Ask_1'])
                    premUK = 0.07
                    self.v = 0.05
                    vF = 0.0
                    while (premUK < premK):
                        #Calculations on options with a very low premium don't give a significant answer
                        S = float(self.leCurPri.text())
                        K = float(self.df.loc[index, 'Strike'])
                        r = 0.005
                        r = r / 100
                        self.v = self.v + .05
                        t = self.matTime(index)
                        d1_numerator = np.log(S/K) + (r + ((self.v * self.v)/2)) * t
                        d1_denominator = self.v * math.sqrt(t)
                        d1 = d1_numerator/d1_denominator
                        d2 = d1 - self.v * math.sqrt(t)
                        x = -d2
                        y = -d1
                        factorOne = stats.norm.cdf(x) * K * math.exp(-r*t) 
                        factorTwo = stats.norm.cdf(y) * S
                        premiumP = factorOne - factorTwo
                        premUK = premiumP
                            
                    premUK = 0.07
                    self.v = self.v - .05
                    vF = 0.0
                    while (premUK < premK):
                        #Calculations on options with a very low premium don't give a significant answer
                        S = float(self.leCurPri.text())
                        K = float(self.df.loc[index, 'Strike'])
                        r = 0.005
                        r = r / 100
                        self.v = self.v + 0.001
                        t = self.matTime(index)
                        d1_numerator = np.log(S/K) + (r + ((self.v * self.v)/2)) * t
                        d1_denominator = self.v * math.sqrt(t)
                        d1 = d1_numerator/d1_denominator
                        d2 = d1 - self.v * math.sqrt(t)
                        x = -d2
                        y = -d1
                        factorOne = stats.norm.cdf(x) * K * math.exp(-r*t) 
                        factorTwo = stats.norm.cdf(y) * S
                        premiumP = factorOne - factorTwo
                        premUK = premiumP

                    
                    vF = int(self.v * 100)
                    vF = format(vF, ".2f")
                    vF = float(self.v * 100)
                    vF = round(vF, 2)
                    rs = self.df.shape[0]
                        
                    self.df.loc[index, 'Volat-Ask_1'] = (str(vF) + "%")
          
        #Drop string '0.0%' from VolatBid in order to delete Bid < 0.1% AND Ask < 0.1 
        #all of which in the same row  
        if self.rbCall.isChecked() == True:          
            self.df = self.df.loc[self.df['VolatBid'] != '0.0%']
            self.df.reset_index(inplace = True, drop = True)
            self.df = self.df.loc[self.df['Volat-Ask'] != '0.0%']
            self.df.reset_index(inplace = True, drop = True)
            
        #Drop string '0.0%' from VolatBid-1 in order to delete Bid < 0.1% AND Ask < 0.1 
        #all of which in the same row 
        if self.rbPut.isChecked() == True:          
            self.df = self.df.loc[self.df['Volat-Ask_1'] != '0.0%']
            self.df.reset_index(inplace = True, drop = True)
            self.df = self.df.loc[self.df['VolatBid_1'] != '0.0%']
            self.df.reset_index(inplace = True, drop = True)
        
        #Delete rows with 5.1% VoltBid or VoltBid_1; In these rows the Bid +
        #the Strike value will be < the Current value 
        if self.rbPut.isChecked() == True:
            self.df = self.df.loc[self.df['VolatBid_1'] != '5.1%']  
        elif self.rbCall.isChecked() == True:
            self.df = self.df.loc[self.df['VolatBid'] != '5.1%']
        
        self.df.reset_index(inplace = True, drop = True)
        
        #Determining which dataframe will be shown.
        if self.filNum > 0:
            self.df = self.df.dropna()
            self.model = TableModel(self.df)
            self.table.setModel(self.model) 
        else:
            self.df = self.df.dropna()
            self.model = TableModel(self.df)
            self.table.setModel(self.model) 

    #When the rbCall button is selected, the buttons acting on Puts will hide
    def hidePutButtons(self):
        self.pbTightPuts.setVisible(False)
        self.pbLoPutVol.setVisible(False)
        self.pbHiPutVol.setVisible(False)
        self.pbTightCalls.setVisible(True)
        self.pbLoCallVol.setVisible(True)
        self.pbHiCallVol.setVisible(True)
        self.lbDefFil.move(1379,249)
    
    #When the rbPut button is selected, the buttons acting on Calls will hide
    def hideCallButtons(self):
        self.pbTightPuts.setVisible(True)
        self.pbLoPutVol.setVisible(True)
        self.pbHiPutVol.setVisible(True)
        self.pbTightCalls.setVisible(False)
        self.pbLoCallVol.setVisible(False)
        self.pbHiCallVol.setVisible(False)
        self.lbDefFil.move(1379,400)
       
    #The number of days until Friday from the current date. Day 4 = Friday and
    #Day 0 is Monday    
    def calDayDiff(self):
        if ((datetime.today().weekday()) == 0):
            daydiff = 4
        elif((datetime.today().weekday()) == 1):
            daydiff = 3
        elif((datetime.today().weekday()) == 2):
            daydiff = 2
        elif((datetime.today().weekday()) == 3):
            daydiff = 1
        elif((datetime.today().weekday()) == 4):
            daydiff = 7
        elif((datetime.today().weekday()) == 5):
            daydiff = 6
        elif((datetime.today().weekday()) == 6):
            daydiff = 5

        return daydiff
        
    def calc_mat_time1(self):
        if self.rbWeekly.isChecked() == True :
            self.mTime1 = self.calDayDiff() / 365.25
            return self.mTime1
        elif self.rbMonthly.isChecked() == True:
            d1 = datetime.now().date()
            d2 = self.eDate1
            delta = d2 - d1
            self.mTime1 = delta.days / 365.25
            return self.mTime1
              
    def calc_mat_time2(self):
        if self.rbWeekly.isChecked() == True:
            self.mTime2 = (self.calDayDiff() + 7) / 365.25
            return self.mTime2
        elif self.rbMonthly.isChecked() == True:
            d1 = datetime.now().date()
            d2 = self.eDate2
            delta = d2 - d1
            self.mTime2 = delta.days / 365.25
            return self.mTime2
        
    def calc_mat_time3(self):
        self.mTime3 = (self.calDayDiff() + 14) / 365.25
        return self.mTime3
        
    def calc_mat_time4(self):
        self.mTime4 = (self.calDayDiff() + 21) / 365.25
        return self.mTime4
    
    #User in the current month determining eDate1 
    #cm = current month
    def fridayEd1cm(self):
        c = calendar.Calendar(firstweekday=calendar.SUNDAY)
        current_date = datetime.now()
        year = current_date.year
        month = current_date.month
        day = current_date.day
        monthcal = c.monthdatescalendar(year, month)
        
        try:
            third_friday = [day for week in monthcal for day in week if
                    day.weekday() == calendar.FRIDAY and day.month == month][2]
            eDate1 = third_friday
            return eDate1
        except IndexError:
            print('No date found')
    
    #User in the current month determining eDate2
    #cm = current month
    def fridayEd2cm(self):
        c = calendar.Calendar(firstweekday=calendar.SUNDAY)
        current_date = datetime.now()
        year = current_date.year
        month = current_date.month + 1
        day = current_date.day
        monthcal = c.monthdatescalendar(year, month)
        
        try:
            third_friday = [day for week in monthcal for day in week if
                    day.weekday() == calendar.FRIDAY and day.month == month][2]
            eDate2 = third_friday
            return eDate2
        except IndexError:
            print('No date found')
            
    #User in before options for edate1 determining determining eDate1 
    #nm = next month
    def fridayEd1nm(self):
        c = calendar.Calendar(firstweekday=calendar.SUNDAY)
        current_date = datetime.now()
        year = current_date.year
        month = current_date.month + 1
        day = current_date.day
        monthcal = c.monthdatescalendar(year, month)
        
        try:
            third_friday = [day for week in monthcal for day in week if
                    day.weekday() == calendar.FRIDAY and day.month == month][2]
            eDate1 = third_friday
            return eDate1
        except IndexError:
            print('No date found')
        
    #User in before options for edate1 determining determining eDate2   
    #nm = next month
    def fridayEd2nm(self):
        c = calendar.Calendar(firstweekday=calendar.SUNDAY)
        current_date = datetime.now()
        year = current_date.year
        month = current_date.month + 2
        day = current_date.day
        monthcal = c.monthdatescalendar(year, month)
        
        try:
            third_friday = [day for week in monthcal for day in week if
                    day.weekday() == calendar.FRIDAY and day.month == month][2]
            eDate2 = third_friday
            return eDate2
        except IndexError:
            print('No date found')

    def matTime(self, index):
        if self.df.loc[index, 'ExpDate'] == self.eDate1:
            self.mTime1 = self.calc_mat_time1()
            return self.mTime1
        elif self.df.loc[index, 'ExpDate'] == self.eDate2:
            self.mTime2 = self.calc_mat_time2()
            return self.mTime2
        elif self.df.loc[index, 'ExpDate'] == self.eDate3:
            self.mTime3 = self.calc_mat_time3()
            return self.mTime3
        elif self.df.loc[index, 'ExpDate'] == self.eDate4:
            self.mTime3 = self.calc_mat_time4()
            return self.mTime4    
    
    def minMaxStrCur(self):
        #If the user has been running filters and has not filtered data from
        #StrkCurr, then the code in if below will use filtered data from prior 
        #filters and reduce the number of rows further
        #dfp stands for "dataframe previous" and cflag is for "copy flag";
        if self.cflag == True and self.filtName != 'mmStrCur':
            self.df1 = self.dfp.copy()
        #In the elif below the user has filtered StrkCurr before and has returned
        #to do additional filtering of StrkCurr
        elif (self.cflag == True and self.filtName == 'mmStrCur') or \
            self.cflag == False:
                self.df1 = self.df.copy()
                self.filtName = 'mmStrCur'
            
        rs = self.df1.shape[0]
            
        if (len(self.leStrCurMin.text()) > 0 and (len(self.leStrCurMax.text())) > 0) or \
                (len(self.leStrCurMin.text()) == 0 and (len(self.leStrCurMax.text())) > 0) or \
                (len(self.leStrCurMin.text()) > 0 and (len(self.leStrCurMax.text())) == 0) and \
                (self.rbCall.isChecked() == True):
            self.filNum = self.filNum + 1
            #Change values in StrkCurr from percentages to floats
            self.df1['StrkCurr'] = self.df1['StrkCurr'].str.rstrip("%").astype('float')
            #Filter done using floats
            scMin = self.leStrCurMin.text() or '0.00'
            scMax = self.leStrCurMax.text() or '200.0'
            self.df1 = (self.df1.loc[self.df1['StrkCurr'] >= float(scMin)]) 
            self.df1 = (self.df1.loc[self.df1["StrkCurr"] <= float(scMax)])
            self.df1 = self.df1.sort_values(by = ['ExpDate', 'StrkCurr'], ascending = [True, True])
            
            #Strings returned to Strkurr will now be converted to floats, then to percentages
            self.df1["StrkCurr"] = pd.to_numeric(self.df1["StrkCurr"], downcast="float")
            self.df1['StrkCurr'] = pd.Series(["{0:.1f}%".format(val) for val in self.df1['StrkCurr']], index = self.df1.index)
            
            self.df1.reset_index(drop = True, inplace = True)
                        
            self.model = TableModel(self.df1)
            self.table.setModel(self.model) 

        elif (len(self.leStrCurMin.text()) > 0 and (len(self.leStrCurMax.text())) > 0) or \
                (len(self.leStrCurMin.text()) == 0 and (len(self.leStrCurMax.text())) > 0) or \
                (len(self.leStrCurMin.text()) > 0 and (len(self.leStrCurMax.text())) == 0) and \
                (self.rbPut.isChecked() == True):
            self.filNum = self.filNum + 1
            #Change values in StrkCurr from percentages to floats
            self.df1['StrkCurr'] = self.df1['StrkCurr'].str.rstrip("%").astype('float')
            
            #Filter done using floats
            scMin = self.leStrCurMin.text()
            scMax = self.leStrCurMax.text()
            self.df1 = (self.df1.loc[self.df1['StrkCurr'] >= float(scMin)]) 
            self.df1 = (self.df1.loc[self.df1["StrkCurr"] <= float(scMax)])
            self.df1 = self.df1.sort_values(by = ['ExpDate', 'StrkCurr'], ascending = [True, True])
            
            #Strings returned to Strkurr will now be converted to floats, then to percentages
            self.df1["StrkCurr"] = pd.to_numeric(self.df1["StrkCurr"], downcast="float")
            self.df1['StrkCurr'] = pd.Series(["{0:.1f}%".format(val) for val in self.df1['StrkCurr']], index = self.df1.index)
            
            self.df1.reset_index(drop = True, inplace = True)
                        
            self.model = TableModel(self.df1)
            self.table.setModel(self.model) 
            
        #Create 'dataframe past' or dfp fo future filters to use    
        self.dfp = self.df1.copy() 
        self.cflag = True
        self.filtName = 'mmStrCur'
        
    def minMaxBidVol(self):
        if self.cflag == True and self.filtName != 'mmBidVol':
            self.df2 = self.dfp.copy()
        elif (self.cflag == True and self.filtName == 'mmBidVol') or \
            self.cflag == False:
                self.df2 = self.df.copy()
                self.filtName = 'mmBidVol'
            
        if (len(self.leBidVolMin.text()) > 0 and (len(self.leBidVolMax.text())) > 0) or \
                (len(self.leBidVolMin.text()) == 0 and (len(self.leBidVolMax.text())) > 0) or \
                (len(self.leBidVolMin.text()) > 0 and (len(self.leBidVolMax.text())) == 0) \
                and self.rbCall.isChecked() == True:
            self.filNum = self.filNum + 1
            
            #Change values in VolatBid from percentages to floats
            self.df2['VolatBid'] = self.df2['VolatBid'].str.rstrip("%").astype('float')
            
            #Filter done using floats
            volMin = self.leBidVolMin.text() or '0.00'
            volMax = self.leBidVolMax.text() or '1000.0'
            self.df2 = (self.df2.loc[self.df2['VolatBid'] >= float(volMin)]) 
            self.df2 = (self.df2.loc[self.df2["VolatBid"] <= float(volMax)])
            self.df2 = self.df2.sort_values(by = ['ExpDate', 'VolatBid'], ascending = [True, True])
                                            
            #Strings returned to VolatBid will now be converted to floats, then to percentages
            self.df2["VolatBid"] = pd.to_numeric(self.df2["VolatBid"], downcast="float")
            self.df2['VolatBid'] = pd.Series(["{0:.1f}%".format(val) for val in self.df2['VolatBid']], index = self.df2.index)
            
            self.df2.reset_index(drop = True, inplace = True)
            
            self.model = TableModel(self.df2)
            self.table.setModel(self.model) 
           
        elif  (len(self.leBidVolMin.text()) > 0 and (len(self.leBidVolMax.text())) > 0) or \
                (len(self.leBidVolMin.text()) == 0 and (len(self.leBidVolMax.text())) > 0) or \
                (len(self.leBidVolMin.text()) > 0 and (len(self.leBidVolMax.text())) == 0) \
                and self.rbPut.isChecked() == True:
            self.filNum = self.filNum + 1
            
            #Change values in VolatBid_1 from percentages to floats
            self.df2['VolatBid_1'] = self.df2['VolatBid_1'].str.rstrip("%").astype('float')
            
            #Filter done using floats
            volMin = self.leBidVolMin.text()
            volMax = self.leBidVolMax.text()
            self.df2 = (self.df2.loc[self.df2['VolatBid_1'] >= float(volMin)]) 
            self.df2 = (self.df2.loc[self.df2["VolatBid_1"] <= float(volMax)])
            self.df2 = self.df2.sort_values(by = ['ExpDate', 'VolatBid_1'], ascending = [True, True])
            
            #Strings returned to VolatBid will now be converted to floats, then to percentages
            self.df2["VolatBid_1"] = pd.to_numeric(self.df2["VolatBid_1"], downcast="float")
            self.df2['VolatBid_1'] = pd.Series(["{0:.1f}%".format(val) for val in self.df2['VolatBid_1']], index = self.df2.index)
            
            self.df2.reset_index(drop = True, inplace = True)
                                            
            self.model = TableModel(self.df2)
            self.table.setModel(self.model) 
            
        self.dfp = self.df2.copy()
        self.cflag = True
        self.filtName = 'mmBidVol'
        
    def askCallVolAsk_50(self):
        if self.rbCall.isChecked() == True:
            self.df7 = self.df.copy()
            self.filNum = self.filNum + 1
            
            #Change values in Volat-Ask from percentages to floats
            self.df7['Volat-Ask'] = self.df7['Volat-Ask'].str.rstrip("%").astype('float')
            
            #Filter done using floats
            volMin = 50.0
            self.df7 = (self.df7.loc[self.df7['Volat-Ask'] >= float(volMin)]) 
            self.df7 = self.df7.sort_values(by = ['ExpDate', 'Volat-Ask'], ascending = [True, True])
            
            #Strings returned to VolatAsk will now be converted to floats, then to percentages
            self.df7["Volat-Ask"] = pd.to_numeric(self.df7["Volat-Ask"], downcast="float")
            self.df7['Volat-Ask'] = pd.Series(["{0:.1f}%".format(val) for val in self.df7['Volat-Ask']], index = self.df7.index)
            
            self.df7.reset_index(inplace = True, drop = True)
            
            self.model = TableModel(self.df7)
            self.table.setModel(self.model)
            
    def bidCallVolBid_40(self):
        if self.rbCall.isChecked() == True:
            self.df8 = self.df.copy()
            self.filNum = self.filNum + 1
            
            #Change values in Volat-Ask from percentages to floats
            self.df8['VolatBid'] = self.df8['VolatBid'].str.rstrip("%").astype('float')
            
            #Filter done using floats
            volMax = 40.0
            self.df8 = (self.df8.loc[self.df8['VolatBid'] <= float(volMax)]) 
            self.df8 = self.df8.sort_values(by = ['ExpDate', 'VolatBid'], ascending = [True, True])
            
            #Strings returned to VolatAsk will now be converted to floats, then to percentages
            self.df8["VolatBid"] = pd.to_numeric(self.df8["VolatBid"], downcast="float")
            self.df8['VolatBid'] = pd.Series(["{0:.1f}%".format(val) for val in self.df8['VolatBid']], index = self.df8.index)
            
            self.df8.reset_index(inplace = True, drop = True)
            
            self.model = TableModel(self.df8)
            self.table.setModel(self.model)
            
    def askPutVolAsk_50(self):
        if self.rbPut.isChecked() == True:
            self.df9 = self.df.copy()
            self.filNum = self.filNum + 1
            
            #Change values in Volat-Ask from percentages to floats
            self.df9['Volat-Ask_1'] = self.df9['Volat-Ask_1'].str.rstrip("%").astype('float')
            
            #Filter done using floats
            volMin = 50.0
            self.df9 = (self.df9.loc[self.df9['Volat-Ask_1'] >= float(volMin)]) 
            self.df9 = self.df9.sort_values(by = ['ExpDate', 'Volat-Ask_1'], ascending = [True, True])
            
            #Strings returned to VolatAsk will now be converted to floats, then to percentages
            self.df9["Volat-Ask_1"] = pd.to_numeric(self.df9["Volat-Ask_1"], downcast="float")
            self.df9['Volat-Ask_1'] = pd.Series(["{0:.1f}%".format(val) for val in self.df9['Volat-Ask_1']], index = self.df9.index)
            
            self.df9.reset_index(inplace = True, drop = True)
            
            self.model = TableModel(self.df9)
            self.table.setModel(self.model)
            
    def bidPutVolBid_40(self):
        if self.rbPut.isChecked() == True:
            self.df10 = self.df.copy()
            self.filNum = self.filNum + 1
            
            #Change values in Volat-Ask from percentages to floats
            self.df10['VolatBid_1'] = self.df10['VolatBid_1'].str.rstrip("%").astype('float')
            
            #Filter done using floats
            volMax = 40.0
            self.df10 = (self.df10.loc[self.df10['VolatBid_1'] <= float(volMax)]) 
            self.df10 = self.df10.sort_values(by = ['ExpDate', 'VolatBid_1'], ascending = [True, True])
            
            #Strings returned to VolatAsk will now be converted to floats, then to percentages
            self.df10["VolatBid_1"] = pd.to_numeric(self.df10["VolatBid_1"], downcast="float")
            self.df10['VolatBid_1'] = pd.Series(["{0:.1f}%".format(val) for val in self.df10['VolatBid_1']], index = self.df10.index)
            
            self.df10.reset_index(inplace = True, drop = True)
            
            self.model = TableModel(self.df10)
            self.table.setModel(self.model)
            
    def tightCalls(self):
        if self.rbCall.isChecked() == True:
            self.df11 = self.df.copy()
            self.filNum = self.filNum + 1
            
            valMax = 1.0
            self.df11['Ask-Bid'] = self.df11['Ask-Bid'].astype(float)
            self.df11 = (self.df11.loc[self.df11['Ask-Bid'] < float(valMax)])
            self.df11 = self.df11.sort_values(by = ['ExpDate', 'Ask-Bid'], ascending = [True, True])

            self.df11.reset_index(inplace = True, drop = True)

            self.model = TableModel(self.df11)
            self.table.setModel(self.model)
            
    def tightPuts(self):
        if self.rbPut.isChecked() == True:
            self.df12 = self.df.copy()
            self.filNum = self.filNum + 1
            
            valMax = 1.0
            self.df12['Ask_1-Bid_1'] = self.df12['Ask_1-Bid_1'].astype(float)
            self.df12 = (self.df12.loc[self.df12['Ask_1-Bid_1'] < float(valMax)])
            self.df12 = self.df12.sort_values(by = ['ExpDate', 'Ask_1-Bid_1'], ascending = [True, True])
            
            self.df12.reset_index(inplace = True, drop = True)

            self.model = TableModel(self.df12)
            self.table.setModel(self.model)
        
    def minMaxAskVol(self):
        if self.cflag == True and self.filtName != 'mmAskVol':
            self.df3 = self.dfp.copy()
        elif (self.cflag == True and self.filtName == 'mmAskVol') or \
            self.cflag == False:
                self.df3 = self.df.copy()
                self.filtName = 'mmAskVol'
                
        if ((len(self.leAskVolMin.text())) > 0 and (len(self.leAskVolMax.text())) > 0) or \
                (len(self.leAskVolMin.text()) == 0 and (len(self.leAskVolMax.text())) > 0) or \
                (len(self.leAskVolMin.text()) > 0 and (len(self.leAskVolMax.text())) == 0) \
                and self.rbCall.isChecked() == True:
            self.filNum = self.filNum + 1
            
            #Change values in Volat-Ask from percentages to floats
            self.df3['Volat-Ask'] = self.df3['Volat-Ask'].str.rstrip("%").astype('float')
            
            #Filter done using floats
            volMin = self.leAskVolMin.text() or '0.00'
            volMin = float(volMin)
            
            volMax = self.leAskVolMax.text() or '1000.0'
            volMax = float(volMax)
            
            self.df3 = (self.df3.loc[self.df3['Volat-Ask'] >= float(volMin)]) 
            self.df3 = (self.df3.loc[self.df3["Volat-Ask"] <= float(volMax)])
            self.df3 = self.df3.sort_values(by = ['ExpDate', 'Volat-Ask'], ascending = [True, True])
            
            #Strings returned to VolatAsk will now be converted to floats, then to percentages
            self.df3["Volat-Ask"] = pd.to_numeric(self.df3["Volat-Ask"], downcast="float")
            self.df3['Volat-Ask'] = pd.Series(["{0:.1f}%".format(val) for val in self.df3['Volat-Ask']], index = self.df3.index)
            
            self.df3.reset_index(drop = True, inplace = True)
                                            
            self.model = TableModel(self.df3)
            self.table.setModel(self.model)
        
        elif (len(self.leAskVolMin.text()) > 0 and (len(self.leAskVolMax.text())) > 0) or \
                (len(self.leAskVolMin.text()) == 0 and (len(self.leAskVolMax.text())) > 0) or \
                (len(self.leAskVolMin.text()) > 0 and (len(self.leAskVolMax.text())) == 0) \
                and self.rbPut.isChecked() == True:
            self.filNum = self.filNum + 1
            
            #Change values in Volat-Ask from percentages to floats
            self.df3['Volat-Ask_1'] = self.df3['Volat-Ask_1'].str.rstrip("%").astype('float')
            
            #Filter done using floats
            volMin = self.leAskVolMin.text()
            volMin = float(volMin)
            
            volMax = self.leAskVolMax.text()
            volMax = float(volMax)
            
            self.df3 = (self.df3.loc[self.df3['Volat-Ask_1'] >= float(volMin)]) 
            self.df3 = (self.df3.loc[self.df3["Volat-Ask_1"] <= float(volMax)])
            self.df3 = self.df3.sort_values(by = ['ExpDate', 'Volat-Ask_1'], ascending = [True, True])
            
            #Strings returned to VolatBid will now be converted to floats, then to percentages
            self.df3["Volat-Ask_1"] = pd.to_numeric(self.df3["Volat-Ask_1"], downcast="float")
            self.df3['Volat-Ask_1'] = pd.Series(["{0:.1f}%".format(val) for val in self.df3['Volat-Ask_1']], index = self.df3.index)
            
            self.df3.reset_index(drop = True, inplace = True)
                                            
            self.model = TableModel(self.df3)
            self.table.setModel(self.model)
            
        self.dfp = self.df3.copy()
        self.cflag = True
        self.filtName = 'mmAskVol'
        
    def minMaxDelta(self):
        if self.cflag == True and self.filtName != 'mmDelta':
            self.df4 = self.dfp.copy()
        elif (self.cflag == True and self.filtName == 'mmDelta') or \
            self.cflag == False:
                self.df4 = self.df.copy()
                self.filtName = 'mmDelta'
        
        if (len(self.leDelMax.text()) > 0 and (len(self.leDelMin.text())) > 0) or \
                (len(self.leDelMax.text()) == 0 and (len(self.leDelMin.text())) > 0) or \
                (len(self.leDelMax.text()) > 0 and (len(self.leDelMin.text())) == 0) and \
                self.rbCall.isChecked() == True:
            self.filNum = self.filNum + 1
            dtMax = self.leDelMax.text() or '0.00'
            dtMin = self.leDelMin.text() or '1.00'
            self.df4 = self.df4.loc[self.df4['Delta'] >= float(dtMin)]
            self.df4 = self.df4.loc[self.df4['Delta'] <= float(dtMax)]
            self.df4 = self.df4.sort_values(by = ['ExpDate', 'Delta'], ascending = [True, True])
            
            self.df4.reset_index(drop = True, inplace = True)
            
            self.model = TableModel(self.df4)
            self.table.setModel(self.model) 
        elif (len(self.leDelMax.text()) > 0 and (len(self.leDelMin.text())) > 0) or \
            (len(self.leDelMax.text()) == 0 and (len(self.leDelMin.text())) > 0) or \
            (len(self.leDelMax.text()) > 0 and (len(self.leDelMin.text())) == 0) and \
            self.rbPut.isChecked() == True:
                
            self.filNum = self.filNum + 1
            
            dtMax = self.leDelMax.text()
            dtMin = self.leDelMin.text()
            
            self.df4 = self.df4.loc[self.df4['Delta_1'] >= float(dtMin)]
            self.df4 = self.df4.loc[self.df4['Delta_1'] <= float(dtMax)]
            self.df4 = self.df4.sort_values(by = ['ExpDate', 'Delta_1'], ascending = [True, True])
            
            self.df4.reset_index(drop = True, inplace = True)
            
            self.model = TableModel(self.df4)
            self.table.setModel(self.model) 
            
        self.dfp = self.df4.copy()
        self.cflag = True
        self.filtName = 'mmDelta'
            
    def maxAskMinusBid(self):
        if self.cflag == True:
            self.df5 = self.dfp.copy()
        else:
            self.df5 = self.df.copy()

        if len(self.leBidAsk.text()) > 0:
            if self.rbCall.isChecked() == True:
                self.df5['Ask-Bid'] = self.df5['Ask-Bid'].astype(float)

                self.filNum = self.filNum + 1
                abMax = self.leBidAsk.text()
                abMax = float(abMax)
                abMin = '0.000'
                abMin = float(abMin)
                self.df5 = self.df5.loc[self.df5['Ask-Bid'] >= float(abMin)]
                self.df5 = self.df5.loc[self.df5['Ask-Bid'] <= float(abMax)]
                self.df5 = self.df5.sort_values(by = ['ExpDate', 'Ask-Bid'], ascending = [True, True])
                
                self.df5.reset_index(drop = True, inplace = True)
                
                self.model = TableModel(self.df5)
                self.table.setModel(self.model) 
            elif self.rbPut.isChecked() == True:
                self.df5['Ask_1-Bid_1'] = self.df5['Ask_1-Bid_1'].astype(float)
                
                self.filNum = self.filNum + 1
                abMax = self.leBidAsk.text()
                abMax = float(abMax)
                abMin = '0.000'
                abMin = float(abMin)
                self.df5 = self.df5.loc[self.df5['Ask_1-Bid_1'] >= float(abMin)]
                self.df5 = self.df5.loc[self.df5['Ask_1-Bid_1'] <= float(abMax)]
                self.df5 = self.df5.sort_values(by = ['ExpDate', 'Ask_1-Bid_1'], ascending = [True, True])
                
                self.model = TableModel(self.df5)
                self.table.setModel(self.model) 
             
            self.dfp = self.df5.copy()
            self.cflag = True
        
    def opFid(self):
        if self.cbFid.isChecked() == True:
            webbrowser.open('https://www.fidelity.com/')
            
    def opExl(self):
        if self.cbExc.isChecked() == True:
            subprocess.check_call(['open', '-a', 'Microsoft Excel'])
        
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
        
    def addDat(self):
        newone = self.leFileName.text()
        today = date.today()
        filename = (newone + today.strftime("_%y%d%m"))
        self.leFileName.setText(filename + ".csv")
        
  
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


