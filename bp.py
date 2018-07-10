import sys
from PyQt4 import QtGui, QtCore
import pyqtgraph as plt
from time import strftime
from datetime import datetime
import numpy as np
import pandas
import csv

class MainWindow(QtGui.QDialog):

	def __init__(self):
		super(MainWindow, self).__init__()
		self.setWindowTitle("Spectrum Analyser")
		self.plot = plt.PlotWidget(title = "PSD Graph")
		self.plot.setLabel("left", "Amlplitude", "dBm")
		self.plot.setLabel("bottom", "Frequency", "MHz")
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
		spanLabel = QtGui.QLabel("Freq. Span (MHz) :")
		self.sp1 = QtGui.QSpinBox()
		self.sp2 = QtGui.QSpinBox()
		self.span = QtGui.QSpinBox()
		self.sp1.setMinimum(15)
		self.sp1.setMaximum(2699)
		self.sp1.setSingleStep(10)
		self.sp2.setMinimum(17)
		self.sp2.setMaximum(2700)
		self.sp2.setSingleStep(10)
		self.span.setMinimum(1)
		self.span.setMaximum(299)

		hbox1 = QtGui.QHBoxLayout()
		hbox1.addWidget(startLabel)
		hbox1.addWidget(self.sp1)
		hbox1.setAlignment(QtCore.Qt.AlignHCenter)

		hbox2 = QtGui.QHBoxLayout()
		hbox2.addWidget(stopLabel)
		hbox2.addWidget(self.sp2)
		hbox2.setAlignment(QtCore.Qt.AlignHCenter)

		hbox = QtGui.QHBoxLayout()
		hbox.addWidget(spanLabel)
		hbox.addWidget(self.span)

		vbox1 = QtGui.QVBoxLayout()
		vbox1.addLayout(hbox1)
		vbox1.addLayout(hbox2)
		vbox1.addLayout(hbox)
		gb1.setLayout(vbox1)

		# Group Box 2
		self.sp3 = QtGui.QSpinBox()
		self.sp3.setMinimum(1)
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
		self.exportBtn = QtGui.QPushButton("Export to .CSV")
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
		self.progress = QtGui.QProgressBar(self)
		self.lcd2 = QtGui.QLCDNumber()
		self.lcd2.setNumDigits(8)
		self.lcd2.setSegmentStyle(QtGui.QLCDNumber.Filled)
		pal2 = self.lcd2.palette()
		pal2.setColor(pal2.Dark, QtGui.QColor(0, 0, 0))
		pal2.setColor(pal2.Light, QtGui.QColor(0, 0, 255))
		self.lcd2.setPalette(pal2)
		sweepLabel = QtGui.QLabel("Sweep Count :")
		hbox5 = QtGui.QHBoxLayout()
		hbox5.addWidget(self.progress)
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
		t2 = self.span.value()

		if f2 - f1 > 0 and t2 < 300 and (f2 - f1) > t2:
			self.startBtn.setText("Initialising...")
			self.startBtn.setEnabled(False)
			self.stopBtn.setEnabled(True)
			self.sp1.setEnabled(False)
			self.sp2.setEnabled(False)
			self.sp3.setEnabled(False)
			self.span.setEnabled(False)
			i = 0
			self.x = [] # Time
			self.y = [] # PSD
			self.z = []
			self.startBtn.setText("Running...")
			while(i != 50):
				self.progress.setValue(2*i)
				self.lcd2.display(i+2)
				j = np.random.random()
				self.y.append(j)
				self.x.append(datetime.now().strftime("%I:%M:%S %p"))
				self.z.append(i)
				self.curve = self.plot.plot()
				self.curve.setData(self.z, self.y)
				QtGui.QApplication.processEvents()
				i+=1


			self.progress.setValue(100)
			self.startBtn.setText("Finished")
			self.stopBtn.setEnabled(False)
			self.exportBtn.setEnabled(True)
			self.resetBtn.setEnabled(True)

		else:
			choice1 = QtGui.QMessageBox.question(self, "Warning", "Enter Valid parameters", QtGui.QMessageBox.Ok)

		
	def stopBtnClicked(self):
		self.startBtn.setEnabled(False)
		self.startBtn.setText("Terminated")
		self.stopBtn.setEnabled(False)
		self.exportBtn.setEnabled(True)
		self.resetBtn.setEnabled(True)

	def resetBtnClicked(self):
		self.resetBtn.setText("Resetting..")
		self.plot.clear()
		self.sp1.setValue(15)
		self.sp2.setValue(16)
		self.sp3.setValue(0)
		self.sp1.setEnabled(True)
		self.sp2.setEnabled(True)
		self.sp3.setEnabled(True)
		self.span.setEnabled(True)
		self.span.setValue(1)
		self.progress.setValue(0)
		self.startBtn.setEnabled(True)
		self.startBtn.setText("Start")
		self.stopBtn.setEnabled(False)
		self.lcd2.display(0)
		self.exportBtn.setEnabled(False)
		self.exportBtn.setText("Export to CSV")
		self.resetBtn.setText("Reset")
		self.resetBtn.setEnabled(False)

	def exportBtnClicked(self):
		text, ok = QtGui.QInputDialog.getText(self, 'Export', 'Enter file name:')
		if ok:
			if self.y != None and text:
				"""df = pandas.DataFrame(data = {"Time" : self.x, "Data" : self.y, "Data2" : self.z})
				df.to_csv("./" + text.replace(" ", "") + ".csv", sep = ',', index = False)"""
				myfile = open(text.replace(" ", "_") + ".csv", "w")
				#list = zip(["Time"] + self.x, ["PSD"] + self.y, ["Data"] + self.z)
				list = zip([1, 2, 3])
				with myfile:
					writer = csv.writer(myfile)
					writer.writerows(list)
				myfile.close()
				self.exportBtn.setText("Data Saved")
				self.exportBtn.setEnabled(False)
			else:
				self.exportBtn.setText("Error, Try Again!!")
		

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	main = MainWindow()
	main.show()
	sys.exit(app.exec_())









