import sys
from PyQt4 import QtGui, QtCore
import pyqtgraph as plt
from time import strftime
from datetime import datetime
import numpy as np
import pandas
#import RFExplorer

class MainWindow(QtGui.QDialog):

	def __init__(self):
		super(MainWindow, self).__init__()
		self.setWindowTitle("Spectrum Analyser")
		self.plot = plt.PlotWidget(title = "PSD Graph")
		self.plot.setLabel("left", "Amlplitude", "dBm")
		self.plot.setLabel("bottom", "Frequency", "MHz")
		self.plot.setXRange(0, 200)
		self.home()

	def home(self):

		# Group Boxes 
		gb1 = QtGui.QGroupBox("Frequency Range")
		gb2 = QtGui.QGroupBox("Time")
		gb3 = QtGui.QGroupBox("Progress")
		self.setSS(gb1, gb2, gb3)

		# Group Box 1
		startLabel = QtGui.QLabel("Start Freq. (MHz) : ")
		stopLabel = QtGui.QLabel("Stop Freq. (MHz) : ")
		self.sp1 = QtGui.QSpinBox()
		self.sp2 = QtGui.QSpinBox()
		self.sp1.setMinimum(15)
		self.sp1.setMaximum(2699)
		self.sp1.setSingleStep(10)
		self.sp2.setMinimum(16)
		self.sp2.setMaximum(2700)
		self.sp2.setSingleStep(10)

		hbox1 = QtGui.QHBoxLayout()
		hbox1.addWidget(startLabel)
		hbox1.addWidget(self.sp1)
		hbox1.setAlignment(QtCore.Qt.AlignHCenter)

		hbox2 = QtGui.QHBoxLayout()
		hbox2.addWidget(stopLabel)
		hbox2.addWidget(self.sp2)
		hbox2.setAlignment(QtCore.Qt.AlignHCenter)

		vbox1 = QtGui.QVBoxLayout()
		vbox1.addLayout(hbox1)
		vbox1.addLayout(hbox2)
		gb1.setLayout(vbox1)

		# Group Box 2
		self.sp3 = QtGui.QSpinBox()
		timeLabel = QtGui.QLabel("Minutes")
		hbox3 = QtGui.QHBoxLayout()
		hbox3.addWidget(self.sp3)
		hbox3.addWidget(timeLabel)
		hbox3.setAlignment(QtCore.Qt.AlignHCenter)

		gb2.setLayout(hbox3)

		# Buttons
		self.startBtn = QtGui.QPushButton("Start")
		self.stopBtn = QtGui.QPushButton("Stop")
		self.resetBtn = QtGui.QPushButton("Reset")
		self.exportBtn = QtGui.QPushButton("Export to CSV")
		self.stopBtn.setEnabled(False)
		self.exportBtn.setEnabled(False)
		self.resetBtn.setEnabled(False)
		self.startBtn.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
		self.stopBtn.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
		self.resetBtn.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
		self.exportBtn.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
		self.startBtn.clicked.connect(self.startBtnClicked)
		self.stopBtn.clicked.connect(self.stopBtnClicked)
		self.resetBtn.clicked.connect(self.resetBtnClicked)
		self.exportBtn.clicked.connect(self.exportBtnClicked)


		# Figure
		vbox4 = QtGui.QVBoxLayout()
		vbox4.addWidget(self.plot)

		# Left Layout
		vbox3 = QtGui.QVBoxLayout()
		vbox3.addWidget(gb1, 3)
		vbox3.addWidget(gb2, 1)
		vbox3.addWidget(self.startBtn, 1)
		vbox3.addWidget(self.stopBtn, 1)
		vbox3.addWidget(self.exportBtn, 1)
		vbox3.addWidget(self.resetBtn, 1)

		# Upper Layout
		hbox4 = QtGui.QHBoxLayout()
		hbox4.addLayout(vbox3)
		hbox4.addLayout(vbox4)

		# Group Box 3
		self.lcd1 = QtGui.QLCDNumber()
		self.lcd1.display(strftime("%M"+":"+"%S"))
		self.lcd2 = QtGui.QLCDNumber()
		self.lcd1.display("00:00")
		self.lcd2.setNumDigits(8)
		self.lcd1.setSegmentStyle(QtGui.QLCDNumber.Filled)
		self.lcd2.setSegmentStyle(QtGui.QLCDNumber.Filled)
		pal1 = self.lcd1.palette()
		pal1.setColor(pal1.Light, QtGui.QColor(0, 0, 0))
		pal1.setColor(pal1.Dark, QtGui.QColor(0, 0, 255))
		self.lcd1.setPalette(pal1)
		pal2 = self.lcd2.palette()
		pal2.setColor(pal2.Dark, QtGui.QColor(0, 0, 0))
		pal2.setColor(pal2.Light, QtGui.QColor(0, 0, 255))
		self.lcd2.setPalette(pal2)
		trLabel = QtGui.QLabel("Time Remaining : ")
		sweepLabel = QtGui.QLabel("Sweep Number :")
		hbox5 = QtGui.QHBoxLayout()
		hbox5.addWidget(trLabel)
		hbox5.addWidget(self.lcd1)
		hbox5.addWidget(sweepLabel)
		hbox5.addWidget(self.lcd2)
		hbox5.setAlignment(QtCore.Qt.AlignRight)
		gb3.setLayout(hbox5)

		# Final Layout
		vbox2 = QtGui.QVBoxLayout()
		vbox2.addLayout(hbox4, 15)
		vbox2.addWidget(gb3, 2)

		self.setLayout(vbox2)

	def setSS(self, gb1, gb2, gb3):
		gb1.setStyleSheet("""
			.QGroupBox{
			border : 1px solid gray;
			border-radius : 9px;
			margin-top : 0.5em;
			}
			QGroupBox::title {
    		subcontrol-origin: margin;
    		left: 10px;
    		padding: 0 3px 0 3px;
			}""")
		gb2.setStyleSheet("""
			.QGroupBox{
			border : 1px solid gray;
			border-radius : 9px;
			margin-top : 0.5em;
			}
			QGroupBox::title {
    		subcontrol-origin: margin;
    		left: 10px;
    		padding: 0 3px 0 3px;
			}""")
		gb3.setStyleSheet("""
			.QGroupBox{
			border : 1px solid gray;
			border-radius : 9px;
			margin-top : 0.5em;
			}
			QGroupBox::title {
    		subcontrol-origin: margin;
    		left: 10px;
    		padding: 0 3px 0 3px;
			}""")

	def startBtnClicked(self):

		f1 = self.sp1.value()
		f2 = self.sp2.value()
		t1 = self.sp3.value()

		if f2 - f1 > 0 and f2 -f1 < 300:
			self.case_stop = False
			SERIALPORT = None
			TOTAL_SECONDS = t1*60
			BAUDRATE = 500000
			self.x = [0] # Time
			self.y = [0] # PSD
			self.z = [0] # Frequency
			self.startBtn.setText("Initialising...")
			self.startBtn.setEnabled(False)
			self.stopBtn.setEnabled(True)
			self.sp1.setEnabled(False)
			self.sp2.setEnabled(False)
			self.sp3.setEnabled(False)

			self.objRFE = RFExplorer.RFECommunicator()
			try:
				self.objRFE.GetConnectedPorts()
				self.objRFE.ResetIOT_HW(True)
				if (self.objRFE.ConnectPort(SERIALPORT, BAUDRATE)):
					while(self.objRFE.IsResetEvent):
						pass

					time.sleep(3)
					self.objRFE.SendCommand_RequestConfigData()
					while(self.objRFE.ActiveModel == RFExplorer.RFE_Common.eModel.MODEL_NONE):
						self.objRFE.ProcessReceivedString(True)

					if self.objRFE.IsAnalyzer():
						self.startBtn.setText("Receiving Data...")
						nLastDisplayIndex = 0
						startTime = datetime.now()
						while (datetime.now() - startTime).seconds < TOTAL_SECONDS:
							self.objRFE.ProcessReceivedString(True)
							if self.objRFE.SweepData.Count > nLastDisplayIndex:
								nIndex = self.objRFE.SweepData.Count - 1
								objSweepTime = self.objRFE.SweepData.GetData(nIndex)
								nStep = objSweepTime.GetPeakStep()
								fAmplitudeDBM = objSweepTime.GetAmplitude_DBM(nStep)
								fCenterFreq = objSweepTime.GetFrequencyMHZ(nStep)
								self.lcd2.display(nIndex+2)
								self.x.append(datetime.now().strftime("%I:%M:%S %p"))
								self.y.append(fAmplitudeDBM)
								self.z.append(fCenterFreq)
								self.curve = self.plot.plot()
								self.curve.setData(self.z, self.y)
								QtGui.QApplication.processEvents()
								if self.case_stop:
									break
					else:
						print("Error: Device connected is a Signal Generator. \nPlease, connect a Spectrum Analyzer")
				else:
					print("Not Connected")
			except Exception as obEx:
				print("Error: " + str(obEx))
	
		else:
			choice1 = QtGui.QMessageBox.question(self, "Warning", "Enter Frequency Span upto 300MHz", QtGui.QMessageBox.Ok)

		self.startBtn.setText("Finished")
		self.stopBtn.setEnabled(False)
		self.exportBtn.setEnabled(True)
		self.resetBtn.setEnabled(True)
		self.objRFE.Close()    #Finish the thread and close port
		self.objRFE = None
		
	def stopBtnClicked(self):
		self.case_stop = True
		self.startBtn.setEnabled(False)
		self.startBtn.setText("Terminated")
		self.stopBtn.setEnabled(False)
		self.exportBtn.setEnabled(True)
		self.resetBtn.setEnabled(True)

	def resetBtnClicked(self):
		self.resetBtn.setText("Resetting..")
		self.case_stop = False
		self.x = [0]
		self.y = [0]
		self.z = [0]
		self.lcd1.display("00:00")
		self.plot.clear()
		self.sp1.setValue(15)
		self.sp2.setValue(16)
		self.sp3.setValue(0)
		self.sp1.setEnabled(True)
		self.sp2.setEnabled(True)
		self.sp3.setEnabled(True)
		self.startBtn.setEnabled(True)
		self.startBtn.setText("Start")
		self.stopBtn.setEnabled(False)
		self.lcd2.display(0)
		self.exportBtn.setEnabled(False)
		self.objRFE.Close()    #Finish the thread and close port
		self.objRFE = None
		self.exportBtn.setText("Export to CSV")
		self.resetBtn.setText("Reset")

	def exportBtnClicked(self):
		text, ok = QtGui.QInputDialog.getText(self, 'Export', 'Enter file name:')
		if ok:
			if self.y != None and text:
				df = pandas.DataFrame(data = {"Time" : self.x, "PSD" : self.y, "Frequency" : self.z})
				df.to_csv("./" + text.replace(" ", "") + ".csv", sep = ',', index = False)
				self.exportBtn.setText("Data Saved")
				self.exportBtn.setEnabled(False)
			else:
				self.exportBtn.setText("Error, Try Again!!")
		

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	main = MainWindow()
	main.show()
	sys.exit(app.exec_())









