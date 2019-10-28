import sys, operator, cv2, numpy
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from API import drawing_API
 
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
API = drawing_API()

class CWidget(QWidget): 
 
    def __init__(self):
 
        super().__init__()
 
        # 전체 폼 박스
        formbox = QHBoxLayout()
        self.setLayout(formbox)
 
        # 좌, 우 레이아웃박스
        left = QVBoxLayout()
        right = QVBoxLayout()

        self.view = CView(self)       
        right.addWidget(self.view)  

        self.pencolor = QColor(0,0,0)


        self.checkbox = QCheckBox('지우개')

        self.Buttonbox1 = QPushButton('모두 지우기')
        self.Buttonbox1.clicked.connect(self.view.Remove_All)  

        self.question = QLabel("문제: ")
        self.answer = QLabel("예측값: ")

        left.addWidget(self.checkbox)
        left.addWidget(self.Buttonbox1)
        left.addWidget(self.question)
        left.addWidget(self.answer)

        # 전체 폼박스에 좌우 박스 배치
        formbox.addLayout(left)
        formbox.addLayout(right)
 
        formbox.setStretchFactor(left, 0)
        formbox.setStretchFactor(right, 1)
         
        self.setGeometry(100, 100, 800, 500) 
        self.startGame()

    def startGame(self):
        global API
        self.question.setText("문제: "+drawing_API.get_rand_class(API))
    
# QGraphicsView display QGraphicsScene
class CView(QGraphicsView):

    def __init__(self, parent):
        
        super().__init__(parent)       
        self.scene = QGraphicsScene()        
        self.setScene(self.scene)
        self.pixMap = QPixmap(self.scene.width(), self.scene.height())
        self.painter = QPainter(self.pixMap)
        self.items = []
         
        self.start = QPointF()
        self.end = QPointF()
        self.setRenderHint(QPainter.HighQualityAntialiasing)

    
    def Remove_All(self):
        self.scene.clear()

    def moveEvent(self, e):
        rect = QRectF(self.rect())
        rect.adjust(0,0,-2,-2)
 
        self.scene.setSceneRect(rect)
        self.setFixedSize(562,562)
 
    def mousePressEvent(self, e):
 
        if e.button() == Qt.LeftButton:
            # 시작점 저장
            self.start = e.pos()
            self.end = e.pos()
 
    def mouseMoveEvent(self, e):  
         
        # e.buttons()는 정수형 값을 리턴, e.button()은 move시 Qt.Nobutton 리턴 
        if e.buttons() & Qt.LeftButton:    
            self.end = e.pos()
            if self.parent().checkbox.isChecked():
                pen = QPen(QColor(255,255,255), 20)
                path = QPainterPath()
                path.moveTo(self.start)
                path.lineTo(self.end)
                self.scene.addPath(path, pen)
                self.start = e.pos()
                return None

            pen = QPen(self.parent().pencolor, 20)
            path = QPainterPath()
            path.moveTo(self.start)
            path.lineTo(self.end)
            self.scene.addPath(path, pen)
            self.start = e.pos()
 
    def mouseReleaseEvent(self, e):        
 
        if e.button() == Qt.LeftButton:

            if self.parent().checkbox.isChecked():
                return None
 
            pen = QPen(self.parent().pencolor, 20)
            self.save_Img()
    
    def save_Img(self):
        global API

        rect = self.viewport()
        rgb = QImage.Format_RGB32
        image = QImage(rect.width(), rect.height(), rgb)
        image.fill(QColor(255, 255, 255))
        self.painter = QPainter(image)
        self.scene.render(self.painter)
        self.painter.end()
        image.save("capture.png")
        boolean = drawing_API.check_answer(API,"./capture.png")

        if not boolean:
            msg = QMessageBox()
            msg.setWindowTitle("정답입니다.")
            msg.setText("정답입니다.")
            msg.setStandardButtons(QMessageBox.Ok)
            result = msg.exec_()
            msg.show()
            self.Remove_All()
            self.parent().answer.setText("")
            self.parent().startGame()
        
        else:
            self.parent().answer.setText(boolean)

        # image = cv2.imread("capture.png",cv2.IMREAD_COLOR)
        # print(image.shape)

    def startGame(self):
        pass
        

