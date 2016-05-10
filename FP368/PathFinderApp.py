import sys
import os
from PySide.QtGui import *
from PathFinder import *
from PySide.QtCore import *
from dijkstra import *
import copy

class AppMain(QMainWindow, Ui_PathFinder):

    def __init__(self, parent=None):
        super(AppMain, self).__init__(parent)
        self.initc = False
        self.map = QPixmap('resources/PUmap2.bmp')
        self.mapwithdir = None
        self.direction = None

        self.imgdic = { 'Electrical Engineering':(140,61),
                        'Mechnical Engineering':(140,70),
                        'Neil Armstrong Hall of Engineering':(24,8),
                        'Physics':(109,36),
                        'Materials and Electrical Engineering':(137,47),
                        'Engineering Library':(146,86),
                        'Polytechnic':(147,91),
                        'Civil Engineering':(39,18),
                        'Chemical Engineering':(72,40),
                        'Office of the Vice President':(72,47),
                        'Pharmacy':(21,39),
                        'Student Health Center':(30,19),
                        'Armory':(2,76),
                        'Elliott Hall of Music':(51,66),
                        'Hovde Hall of Administration':(71,71),
                        'Psychological Sciences':(64,95),
                   }

        self.setupUi(self)
        self.panel = Imageframe(self.DrawingArea)
        self.panel.setGeometry(QtCore.QRect(11, 31, 520, 450))

        self.initcombobox()
        self.initmapsd()
        self.SaveBtn.setEnabled(False)

        self.DrawingArea.installEventFilter(self)

        self.RunBtn.clicked.connect(self.runBtn_callback)
        self.SaveBtn.clicked.connect(self.saveBtn_callback)
        self.SourceBox.currentIndexChanged.connect(self.sdchanged)
        self.DesBox.currentIndexChanged.connect(self.sdchanged)

    def eventFilter(self,source, e):
        #print(e.type())

        if e.type() == QEvent.Type.WindowActivate and self.initc == False:
            self.panel.dropEvent()
            self.initc = True
        return False

    def initcombobox(self):
        self.GUIdic = { 'Electrical Engineering':(364,295),
                        'Mechnical Engineering':(361,330),
                        'Neil Armstrong Hall of Engineering':(80,50),
                        'Physics':(286,176),
                        'Materials and Electrical Engineering':(361,218),
                        'Engineering Library':(377,403),
                        'Polytechnic':(381,428),
                        'Civil Engineering':(110,95),
                        'Chemical Engineering':(199,197),
                        'Office of the Vice President':(190,229),
                        'Pharmacy':(74,187),
                        'Student Health Center':(85,100),
                        'Armory':(34,363),
                        'Elliott Hall of Music':(145,315),
                        'Hovde Hall of Administration':(186,340),
                        'Psychological Sciences':(170,451),
                   }
        alist = list(self.GUIdic.keys())
        alist.sort()
        self.SourceBox.addItems(alist)
        self.DesBox.addItems(alist)

    def initmapsd(self):
        source = self.GUIdic[self.SourceBox.currentText()]
        des = self.GUIdic[self.DesBox.currentText()]

        self.sourcebtn = PicButton('resources/location.png','resources/clicked.PNG','resources/clicked.PNG',self.DrawingArea)
        self.sourcebtn.setGeometry(QtCore.QRect(source[0], source[1], 20, 20))

        self.desbtn = PicButton('resources/location.png','resources/clicked.PNG','resources/clicked.PNG',self.DrawingArea)
        self.desbtn.setGeometry(QtCore.QRect(des[0], des[1], 20, 20))

    def sdchanged(self):
        source = self.GUIdic[self.SourceBox.currentText()]
        des = self.GUIdic[self.DesBox.currentText()]

        self.sourcebtn.setGeometry(QtCore.QRect(source[0], source[1], 20, 20))
        self.desbtn.setGeometry(QtCore.QRect(des[0], des[1], 20, 20))

    def runBtn_callback(self):
        source = self.imgdic[self.SourceBox.currentText()]
        des = self.imgdic[self.DesBox.currentText()]
        #print(source,des)
        path = findPath(source,des)

        pixmap = QPixmap('resources/PUmap2.bmp')
        painter = QPainter()
        painter.begin(pixmap)
        painter.setRenderHint(QPainter.Antialiasing);
        ## draw color,width,linestyle

        pen = QtGui.QPen(QtGui.QColor(100,100,100), 5, QtCore.Qt.SolidLine)
        painter.setPen(pen)
        #painter.drawLine(source[0]*6,source[1]*11,des[0]*6,des[1]*11)
        for i in range(0,len(path)):
            #painter.drawLine(100,200,200,400) #(100,200) -> (200,400)
            if i + 1  < len(path):
               painter.drawLine(path[i][0]*6,path[i][1]*11,path[i+1][0]*6,path[i+1][1]*11) # could skip points to optimize speed for the points are close to each other
        ##
        painter.end()
        self.mapwithdir = pixmap
        scene = QGraphicsScene()
        scene.addPixmap(pixmap)
        self.panel.setScene(scene)
        self.panel.fitInView(scene.sceneRect(),Qt.KeepAspectRatio)

        self.SaveBtn.setEnabled(True)

    def saveBtn_callback(self):
        path = QtGui.QFileDialog.getSaveFileName(self,'Save As','',selectedFilter='*.png')
        if path:
            self.mapwithdir.save(path[0]+'.png')
        else:
            raise ValueError('Filename not provided.')

class Imageframe(QGraphicsView):
    def __init__(self,parent=None):
        super(Imageframe,self).__init__(parent)

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls:
            e.accept()
        else:
            e.ignore()

    def dragMoveEvent(self, e):
        if e.mimeData().hasUrls:
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e=None):
        '''if e.mimeData().hasUrls:
            e.setDropAction(QtCore.Qt.CopyAction)
            e.accept()
            for url in e.mimeData().urls():
                fname = str(url.toLocalFile())
            self.filename = fname'''

        scene = QGraphicsScene()
        scene.addPixmap(QPixmap('resources/PUmap2.bmp'))
        self.setScene(scene)
        self.fitInView(scene.sceneRect(),QtCore.Qt.KeepAspectRatio)
        '''else:
            e.ignore()'''
    def mousePressEvent(self, event):
        local = self.mapFromGlobal(event.globalPos())
        img_cor = self.mapToScene(local)
        print(local)
        print(img_cor)

class PicButton(QAbstractButton):
    def __init__(self, pic, pic_hover, pic_pressed, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = pic
        self.pixmap_hover = pic_hover
        self.pixmap_pressed = pic_pressed

        self.pressed.connect(self.update)
        self.released.connect(self.update)

    def paintEvent(self, event):
        pix = self.pixmap_hover if self.underMouse() else self.pixmap
        if self.isDown():
            pix = self.pixmap_pressed

        painter = QPainter(self)
        painter.drawPixmap(event.rect(), pix)

    def enterEvent(self, event):
        self.update()

    def leaveEvent(self, event):
        self.update()

    def sizeHint(self):
        return QSize(200, 200)

if __name__ == "__main__":
    '''path = [(1,11),(2,22),(3,33),(4,44),(5,55),(6,66),(7,77),(8,88),(9,99)]
    for i in range(0,len(path),2):
            #painter.drawLine(100,200,200,400) #(100,200) -> (200,400)
            if i+1 < len(path):
                print(path[i][0],path[i][1],path[i+1][0],path[i+1][1])'''

    currentApp = QApplication(sys.argv)
    currentForm = AppMain()

    currentForm.show()
    currentApp.exec_()
