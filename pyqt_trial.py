from PyQt5.QtWidgets import QApplication, QMainWindow,QLabel,QFrame,QGridLayout,QWidget,QVBoxLayout,QHBoxLayout
from PyQt5 import QtWidgets
import sys
from PyQt5.QtChart import QChart, QChartView, QBarSet, QPercentBarSeries, QBarCategoryAxis,QBarSeries
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt
from PyQt5 import QtCore,QtGui
import numpy as np


class predictionWidget(QWidget):

    def __init__(self,parent):
        QWidget.__init__(self,parent)
        self.pred_label = predictionLabel(self)
        self.layout = QGridLayout(self)
        self.layout.addWidget(predHeader(self),1,1,1,2)
        self.layout.addWidget(self.pred_label,2,1,2,2)

class predHeader(QLabel):
    def __init__(self,parent,g=None):
        QLabel.__init__(self,parent)
        self.parent = parent
        if g is not None:
            self.setGeometry(g[0],g[1],g[2],g[3])
        self.setStyleSheet("background-color:#FCF6B1; border-radius:10px; color: #000000;padding :30px")
        self.setFont(QtGui.QFont('Times New Roman', 20))
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setText("Prediction:")

class predictionLabel(QLabel):
    def __init__(self,parent,g=None):
        QLabel.__init__(self,parent)
        self.parent = parent
        if g is not None:
            self.setGeometry(g[0],g[1],g[2],g[3])
        self.setStyleSheet("background-color:#FCF6B1; border-radius:10px; color: #000000;padding :15px")
        self.setFont(QtGui.QFont('Times New Roman', 20))
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.update_text("NO PREDICTION")

    def update_text(self,text):
        self.setText(text)


class connectionLabel(QLabel):

    def __init__(self,parent,g=None):
        QLabel.__init__(self,parent)
        self.IP=""
        self.PORT=""

        self.setStyleSheet("background-color:#FCF6B1; border-radius:10px; color: #000000;padding :15px")
        self.setFont(QtGui.QFont('Times New Roman', 20))
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.update_text("192.168.1.211","5555")

    def update_text(self,IP,PORT):
        text = "Server running at IP: <font color='#FF0000'>{}</font>   PORT: <font color='#FF0000'>{}</font> ".format(IP,PORT)
        self.setText(text)





class topLabel(QLabel):
    def __init__(self, parent,min_width=None,min_height=None,max_width=None,max_height=None):
        QLabel.__init__(self, parent)
        self.parent = parent
        if min_width != None:
            self.setMinimumWidth(min_width)
        if min_height != None:
            self.setMinimumWidth(min_height)
        if max_width != None:
            self.setMaximumWidth(max_width)
        if max_height != None:
            self.setMaximumWidth(max_height)
        self.setStyleSheet("background-color:#31304C; border-radius:10px; color: #A7A9AC;padding :5px") #;padding :5px
        self.setFont(QtGui.QFont('Montserrat', 10,weight=QtGui.QFont.Bold))
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setText('Top Text')

    def update_text(self,text):
        self.setText(text)


class bottomLabel(QLabel):
    def __init__(self, parent,min_width=None,min_height=None,max_width=None,max_height=None, g=None):
        QLabel.__init__(self, parent)
        self.parent = parent
        if g is not None:
            self.setGeometry(g[0], g[1], g[2], g[3])
        self.setStyleSheet("background-color:#31304C; border-radius:10px; color: #EAE485;padding :5px")
        self.setFont(QtGui.QFont('Montserrat',10,weight=QtGui.QFont.Bold))
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setText("100.0%")

    def update_text(self,text):
        self.setText(text)


class Bar(QWidget):

    def __init__(self,parent,min_width=None,min_height=None,max_width=None,max_height=None,**kwargs):
        QWidget.__init__(self,parent,**kwargs)
        self.parent = parent
        self.value = 0.5
        if min_width==None:
            min_width = 30
        if min_height==None:
            min_height = 100
        if max_width != None:
            self.setMaximumWidth(max_width)
        if max_height != None:
            self.setMaximumWidth(max_height)
        self.setMinimumSize(min_width,min_height)
        #self.setSizeHint(30,100)
        #self.setMaximumSize(100, 400)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding
        )
        self.background_color = '#3B3B5E'
        self.unfilled_colour = '#222133'
        self.filled_colour = '#29BBEF'
        self.padding = 4.0  # n-pixel gap around edge.

    def sizeHint(self) :
        return QtCore.QSize(50,100)

    def get_value(self):
        return self.value

    def paintEvent(self, e):
        #Draws Background of bar
        painter = QtGui.QPainter(self)
        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor(self.background_color))
        brush.setStyle(Qt.SolidPattern)
        rect = QtCore.QRect(0, 0, painter.device().width(), painter.device().height())
        painter.fillRect(rect, brush)
        value = self.get_value()
        #parent.value()

        # dimension of slider
        d_height = painter.device().height() - (self.padding * 2)
        d_width = painter.device().width() - (self.padding * 2)

        #Draws unfilled section
        brush.setColor(QtGui.QColor(self.unfilled_colour))
        upper_rect = QtCore.QRect(self.padding,self.padding,d_width,d_height*(1-value))
        painter.fillRect(upper_rect, brush)
        #Draws filled section
        brush.setColor(QtGui.QColor(self.filled_colour))
        upper_rect = QtCore.QRect(self.padding, self.padding+d_height*(1-value), d_width, d_height * (value))
        painter.fillRect(upper_rect, brush)
        painter.end()


class BarWidget(QWidget):

    def __init__(self,parent,min_width=None,min_height=None,max_width=None,max_height=None,**kargs):
        super().__init__(parent,**kargs)
        self.value = 0
        if min_width != None:
            self.setMinimumWidth(min_width)
        if min_height != None:
            self.setMinimumWidth(min_height)
        if max_width != None:
            self.setMaximumWidth(max_width)
        if max_height != None:
            self.setMaximumWidth(max_height)
        self.setStyleSheet("background-color:#31304C; border-radius:10px")
        #self.setContentsMargins(0,0,0,0)
        self.setAttribute(QtCore.Qt.WA_StyledBackground)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.topLabel = topLabel(self)
        self.layout.addWidget(self.topLabel)

        #x = self.topLabel.width()
        #y = self.topLabel.height()

        bar_layout = QHBoxLayout(self)
        self.width = self.sizeHint().width()
        self.bar = Bar(self,max_width=int(0.7*self.width))
        bar_layout.addStretch()
        bar_layout.addWidget(self.bar)
        bar_layout.addStretch()
        self.layout.addLayout(bar_layout)


        self.bottomLabel = bottomLabel(self)
        self.layout.addWidget(self.bottomLabel)

    def update_bar(self,value):
        self.value = value
        self.bottomLabel.update_text(str(self.value*100)+"%")
        self.bar.value = self.value
        self.bar.update()


class confidence_chart(QWidget):

    def __init__(self,parent,activity_list):
        QWidget.__init__(self,parent)
        self.activity_list = activity_list
        self.activity_num  = len(activity_list)
        self.setStyleSheet("background-color:#31304C; border-radius:10px")
        self.setSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding
        )
        #Set Title QLabel
        """self.title = QLabel(self)
        self.title.setText("Predictions")
        self.title.setStyleSheet("background-color:#31304C; border-radius:10px; color: #EAE485;padding :5px")
        self.title.setFont(QtGui.QFont('Montserrat', 30))
        self.title.setAlignment(QtCore.Qt.AlignCenter)"""

        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)
        self.setAttribute(QtCore.Qt.WA_StyledBackground)
        self.bars = []
        max_width = None
        for i in range(self.activity_num):
            bar = BarWidget(self)
            bar.topLabel.update_text(activity_list[i])
            if max_width == None or bar.sizeHint().width()>max_width:
                max_width = bar.sizeHint().width()
            self.layout.addWidget(bar)
            self.bars.append(bar)
        for bar in self.bars:
            bar.setMinimumWidth(max_width)

    def sizeHint(self):
        return QtCore.QSize(400,300)



if __name__ =='__main__':
    App = QApplication(sys.argv)

    #window = Window()
    w = QMainWindow()

    widget = confidence_chart(w,["walking","climbing up","climbing down","sitting","standing","lying"])
    """widget.setStyleSheet("background-color:#31304C; border-radius:10px")
    layout = QHBoxLayout(widget)
    layout.setSpacing(10)
    layout.setContentsMargins(0,0,0,0)
    b1 = BarWidget(w)
    layout.addWidget(b1)
    b2 = BarWidget(w)
    layout.addWidget(b2)
    b3 = BarWidget(w)
    layout.addWidget(b3)
    b4 = BarWidget(w)
    layout.addWidget(b4)"""

    #w.setGeometry(100,100,30,400)
    w.setCentralWidget(widget)


    w.show()

    sys.exit(App.exec_())