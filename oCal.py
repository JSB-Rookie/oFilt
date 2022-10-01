import sys
import numpy as np
import scipy.stats as stats
import math
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import (QPushButton, QLabel, QLineEdit, QDateEdit, QRadioButton, QWidget,
    QCalendarWidget, QApplication, QMainWindow, QFormLayout)
from datetime import datetime, date
from dateutil import parser
from PyQt5.QtGui import *
from PyQt5.QtCore import QDate



qtcreator_file  = "oCal.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.pushButtonPremiumC.hide()
        self.pushButtonPremiumP.hide()
        self.pushButtonVolatilityC.hide()
        self.pushButtonVolatilityP.hide()
        self.premiumLabel.hide()
        self.premiumLE.hide()
        self.premiumInputLE.setValidator(QDoubleValidator(0.99,99.99,2))
        self.currentPriceLE.setValidator(QDoubleValidator(0.99,9999.99,2))
        self.strikePriceLE.setValidator(QDoubleValidator(0.99,9999.99,2))
        self.volatilityLE_1.setValidator(QDoubleValidator(00.01,99.99,2))
        self.riskFreeRateLE.setValidator(QDoubleValidator(00.10, 99.99,2))
        self.volatilityLabel_2.hide()
        self.volatilityLE_2.hide()
        self.rbCP.clicked.connect(self.rbCPclick)
        self.rbCV.clicked.connect(self.rbCVclick)
        self.rbPP.clicked.connect(self.rbPPclick)
        self.rbPV.clicked.connect(self.rbPVclick)
        self.pbClose.clicked.connect(self.closeIt)
        
        self.currentDateDE.setDate(QDate.currentDate())
        
        self.expiratoryDateDateEdit.setDate(QDate.currentDate())
        self.expiratoryDateDateEdit.editingFinished.connect(self.calcMaturityTime)
        
        self.pushButtonPremiumC.clicked.connect(self.d1_n_d)
        self.pushButtonPremiumP.clicked.connect(self.putIt)
        self.pushButtonVolatilityC.clicked.connect(self.calCV)
        self.pushButtonVolatilityP.clicked.connect(self.calPV)
        self.pushButtonClear.clicked.connect(self.clear)
        
        

        
    def CalculatePorV(self):
        value = self.calc_p_vLE.text()
        x = float(value)
        y = 9
        z = x * y 
        self.currentPriceLE.setText(str(z))
    """
    def theNowDate(self):
        now = datetime.now()
        self.currentDateDE.setText(now.strftime('%d %b %Y'))
    """
    def calcMaturityTime(self):
        d1 = datetime.now().date()
        #print("d1: ", d1)
        date_input = self.expiratoryDateDateEdit.text()
        #print("date_input", date_input)
        #self.expiratoryDateDateEdit.calendarPopup.setDateEditAcceptDelay(3000)
        datetimeobject = datetime.strptime(date_input, '%d %b %Y')
        d2 = datetimeobject.date()
        #print("d2 is: ", d2)
        delta = d2 - d1
        matTime = delta.days / 365.25
        self.timeToMaturityLE.setText(str("{:.4f}".format(matTime)))
    
    #Calculation of expected call option premium    
    def d1_n_d(self):
        S = float(self.currentPriceLE.text())
        K = float(self.strikePriceLE.text())
        r = float(self.riskFreeRateLE.text())
        r = r / 100
        v = self.volatilityLE_1.text()
        v = float(v)
        v = v / 100
        t = float(self.timeToMaturityLE.text())
        d1_numerator = np.log(S/K) + (r + ((v * v)/2)) * t
        d1_denominator = v * math.sqrt(t)
        d1 = d1_numerator/d1_denominator
        d2 = d1 - v * math.sqrt(t)
        x = d1
        firstFactor = S * stats.norm.cdf(x)
        secondFactor = K * math.exp(-r*t) * stats.norm.cdf(d2)
        premium = firstFactor - secondFactor
        premiumF = "%.2f" % premium
        self.premiumLE.show()
        self.premiumLabel.show()
        self.premiumLE.setText("$"+str(premiumF) + " per share")

    #Calculation of expected put option premium   
    def putIt(self):
        S = float(self.currentPriceLE.text())
        K = float(self.strikePriceLE.text())
        r = float(self.riskFreeRateLE.text())
        r = r / 100
        v = float(self.volatilityLE_1.text())
        v = v / 100
        t = float(self.timeToMaturityLE.text())
        d1_numerator = np.log(S/K) + (r + ((v * v)/2)) * t
        d1_denominator = v * math.sqrt(t)
        d1 = d1_numerator/d1_denominator
        d2 = d1 - v * math.sqrt(t)
        x = -d2
        y = -d1
        factorOne = stats.norm.cdf(x) * K * math.exp(-r*t) 
        factorTwo = stats.norm.cdf(y) * S
        premiumP = factorOne - factorTwo
        premiumFl = "%.2f" % premiumP
        self.premiumLE.show()
        self.premiumLabel.show()
        self.premiumLE.setText("$"+str(premiumFl) + " per share")

    def rbCPclick(self):
        self.pushButtonPremiumC.show()
        self.pushButtonPremiumP.hide()
        self.pushButtonVolatilityC.hide()
        self.pushButtonVolatilityP.hide()
        self.volatilityLabel_2.hide()
        self.volatilityLE_2.hide()
        self.volatilityLabel_1.show()
        self.volatilityLE_1.show()
        self.premiumInputLabel.hide()
        self.premiumInputLE.hide()
        self.premiumLabel.hide()
        self.premiumLE.hide()

    def rbCVclick(self):
        self.pushButtonPremiumC.hide()
        self.pushButtonPremiumP.hide()
        self.pushButtonVolatilityC.show()
        self.pushButtonVolatilityP.hide()
        self.volatilityLabel_2.hide()
        self.volatilityLE_2.hide()
        self.volatilityLabel_1.hide()
        self.premiumLE.hide()
        self.premiumLabel.hide()
        self.volatilityLE_1.hide()
        self.premiumInputLabel.show()
        self.premiumInputLE.show()

    def rbPPclick(self):
        self.pushButtonPremiumC.hide()
        self.pushButtonPremiumP.show()
        self.pushButtonVolatilityC.hide()
        self.pushButtonVolatilityP.hide()
        self.volatilityLabel_2.hide()
        self.volatilityLE_2.hide()
        self.volatilityLabel_1.show()
        self.volatilityLE_1.show()
        self.premiumInputLabel.hide()
        self.premiumInputLE.hide()
        self.premiumLabel.hide()
        self.premiumLE.hide()

    def rbPVclick(self):
        self.pushButtonPremiumC.hide()
        self.pushButtonPremiumP.hide()
        self.pushButtonVolatilityC.hide()
        self.pushButtonVolatilityP.show()
        self.volatilityLabel_2.hide()
        self.volatilityLE_2.hide()
        self.volatilityLabel_1.hide()
        self.volatilityLE_1.hide()
        self.premiumInputLabel.show()
        self.premiumInputLE.show()
        self.premiumLabel.hide()
        self.premiumLE.hide()
        
        
    #Calculation of expected call volatility
    def calCV(self):
        premK = float(self.premiumInputLE.text())
        premUK = 0.05
        v = 0.10
        self.volatilityLE_2.show()
        self.volatilityLabel_2.show()
        while premUK < premK:
            S = float(self.currentPriceLE.text())
            K = float(self.strikePriceLE.text())
            r = float(self.riskFreeRateLE.text())
            r = r / 100
            v = v + .001
            t = float(self.timeToMaturityLE.text())
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
            #vF = format(vF, ".2f")
            self.volatilityLabel_2.show()
            self.volatilityLE_2.show()
            self.volatilityLE_2.setText(str(vF) + "%")

    #Calculation of expected put volatility
    def calPV(self):
        premK = float(self.premiumInputLE.text())
        premUK = 0.05
        v = 0.10
        self.volatilityLE_2.show()
        self.volatilityLabel_2.show()
        while premUK < premK:
            S = float(self.currentPriceLE.text())
            K = float(self.strikePriceLE.text())
            r = float(self.riskFreeRateLE.text())
            r = r / 100
            v = v + .001
            t = float(self.timeToMaturityLE.text())
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
            #vF = format(vF, ".2f")
            self.volatilityLabel_2.show()
            self.volatilityLE_2.show()
            self.volatilityLE_2.setText(str(vF) + "%")

    def clear(self):
        self.currentDateLE.setText("")
        self.currentPriceLE.setText("")

        lineEdit = self.expiratoryDateDateEdit.findChild(QLineEdit) 
        lineEdit.setText("")   
        self.premiumInputLE.setText("")
        self.premiumLE.setText("")
        self.premiumLE.hide()
        self.premiumLabel.hide()
        self.riskFreeRateLE.setText("")
        self.strikePriceLE.setText("")
        self.tickerLE.setText("")
        self.timeToMaturityLE.setText("")
        self.volatilityLE_2.setText("")
        self.volatilityLE_2.hide()
        self.volatilityLabel_2.hide()
        self.volatilityLE_1.setText("")
        
    def closeIt(self):
        quit()
        
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
