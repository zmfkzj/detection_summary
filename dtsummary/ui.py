from ddt import DdtImage

from PySide6.QtWidgets import *
from PySide6.QtCore import Qt

from dtsummary.summary_ui import Ui_MainWindow
from dtsummary.cvtyolo2coco import cvtyolo2coco
from dtsummary.evalutation import Evaluation

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, Ui_MainWindow):
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        #변수 기본값 설정
        self.set_default_values()

        #평가종류 라디오
        self.bbox.clicked.connect(lambda: setattr(self,'what_eval','bbox'))
        self.segm.clicked.connect(lambda: setattr(self,'what_eval','segm'))

        #선모양 라디오
        self.line_solid.clicked.connect(lambda: setattr(self,'line_style','solid'))
        self.line_dot.clicked.connect(lambda: setattr(self,'line_style','dot'))
        self.line_no.clicked.connect(lambda: setattr(self,'line_style','no'))

        # 채우기 라디오
        self.fill_yes.clicked.connect(lambda: setattr(self,'fill',True))
        self.fill_no.clicked.connect(lambda: setattr(self,'fill',False))

        # 라벨표시방법 라디오
        self.legend.clicked.connect(lambda: setattr(self,'tag','legend'))
        self.each_object.clicked.connect(lambda: setattr(self,'tag','object'))

        # yolo result → coco result
        self.sel_cvt_gt_path.clicked.connect(lambda: self.single_file_select(self.cvt_gt_path))
        self.sel_yolo_json.clicked.connect(lambda: self.single_file_select(self.yolo_json_path))
        self.cvt_btn.clicked.connect(lambda: cvtyolo2coco(self.yolo_json_path.text(),self.cvt_gt_path.text()))

        # evaluation
        self.sel_gt.clicked.connect(lambda: self.single_file_select(self.eval_gt_path))
        self.sel_dt.clicked.connect(lambda: self.single_file_select(self.eval_dt_path))
        self.eval_btn.clicked.connect(self.run_eval)

    def single_file_select(self, lineEdit, *a):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '')
        lineEdit.setText(filename[0])

    def run_eval(self):
        eval = Evaluation(self.eval_dt_path.text(),self.eval_gt_path.text(),self.what_eval)
        eval.run_eval(float(self.conf_thresh.text()))
        
    def set_default_values(self):
        self.line_style = 'solid'
        self.fill = True
        self.tag = 'legend'
        self.what_eval = 'bbox'