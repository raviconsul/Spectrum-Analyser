import sys
from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from time import strftime

left, top, right, bottom = 10, 10, 10, 10

class MainWindow(QtGui.QDialog):

	def __init__(self):
		super(MainWindow, self).__init__()
		self.setWindowTitle("Spectrum Analyser")
		self.figure = Figure()
		self.canvas = FigureCanvas(self.figure)
		self.toolbar = NavigationToolbar(self.canvas, self)
		self.home()

	def home(self):

		# Group Boxes 
		gb1 = QtGui.QGroupBox("Frequency Range")
		gb2 = QtGui.QGroupBox("Time")
		gb3 = QtGui.QGroupBox("Status")
		self.setSS(gb1, gb2, gb3)

		# Group Box 1
		startLabel = QtGui.QLabel("Start Freq.(MHz) : ")
		stopLabel = QtGui.QLabel("Stop Freq.(MHz) : ")
		sp1 = QtGui.QSpinBox()
		sp2 = QtGui.QSpinBox()
		sp1.setMinimum(15)
		sp1.setMaximum(2699)
		sp1.setSingleStep(10)
		sp2.setMinimum(16)
		sp2.setMaximum(2700)
		sp2.setSingleStep(10)

		hbox1 = QtGui.QHBoxLayout()
		hbox1.addWidget(startLabel)
		hbox1.addWidget(sp1)
		hbox1.setAlignment(QtCore.Qt.AlignHCenter)

		hbox2 = QtGui.QHBoxLayout()
		hbox2.addWidget(stopLabel)
		hbox2.addWidget(sp2)
		hbox2.setAlignment(QtCore.Qt.AlignHCenter)

		vbox1 = QtGui.QVBoxLayout()
		vbox1.addLayout(hbox1)
		vbox1.addLayout(hbox2)
		gb1.setLayout(vbox1)

		# Group Box 2
		sp3 = QtGui.QSpinBox()
		timeLabel = QtGui.QLabel("Minutes")
		hbox3 = QtGui.QHBoxLayout()
		hbox3.addWidget(sp3)
		hbox3.addWidget(timeLabel)
		hbox3.setAlignment(QtCore.Qt.AlignHCenter)

		gb2.setLayout(hbox3)

		# Buttons
		startBtn = QtGui.QPushButton("START")
		stopBtn = QtGui.QPushButton("HOLD")
		resetBtn = QtGui.QPushButton("RESET")
		startBtn.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
		stopBtn.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
		resetBtn.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)


		# Figure
		vbox4 = QtGui.QVBoxLayout()
		vbox4.addWidget(self.toolbar)
		vbox4.addWidget(self.canvas)

		# Left Layout
		vbox3 = QtGui.QVBoxLayout()
		vbox3.addWidget(gb1, 3)
		vbox3.addWidget(gb2, 1)
		vbox3.addWidget(startBtn, 1)
		vbox3.addWidget(stopBtn, 1)
		vbox3.addWidget(resetBtn, 1)

		# Upper Layout
		hbox4 = QtGui.QHBoxLayout()
		hbox4.addLayout(vbox3)
		hbox4.addLayout(vbox4)

		# Group Box 3
		lcd1 = QtGui.QLCDNumber()
		lcd1.display(strftime("%M"+":"+"%S"))
		lcd2 = QtGui.QLCDNumber()
		trLabel = QtGui.QLabel("Time Remaining : ")
		sweepLabel = QtGui.QLabel("Sweep Number :")
		hbox5 = QtGui.QHBoxLayout()
		hbox5.addWidget(trLabel)
		hbox5.addWidget(lcd1)
		hbox5.addWidget(sweepLabel)
		hbox5.addWidget(lcd2)
		hbox5.setAlignment(QtCore.Qt.AlignRight)
		gb3.setLayout(hbox5)

		# Final Layout
		vbox2 = QtGui.QVBoxLayout()
		vbox2.addLayout(hbox4, 12)
		vbox2.addWidget(gb3, 1)

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

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	main = MainWindow()
	main.show()
	sys.exit(app.exec_())









