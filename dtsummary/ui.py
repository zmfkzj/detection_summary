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
        self.set_default_values()

        # yolo result → coco result
        self.sel_cvt_gt_path.clicked.connect(lambda: self.single_file_select(self.cvt_gt_path))
        self.sel_yolo_json.clicked.connect(lambda: self.single_file_select(self.yolo_json_path))
        self.cvt_btn.clicked.connect(lambda: cvtyolo2coco(self.yolo_json_path.text(),self.cvt_gt_path))

        # evaluation
        self.sel_gt.clicked.connect(lambda: self.single_file_select(self.eval_gt_path))
        self.sel_dt.clicked.connect(lambda: self.single_file_select(self.eval_dt_path))
        self.eval_btn.clicked.connect

    def single_file_select(self, lineEdit, *a):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '')
        lineEdit.setText(filename[0])

    def run_eval(self, conf_thresh):
        eval = Evaluation(self.eval_dt_path,self.eval_gt_path,'bbox')
        eval.run_eval(self.conf_thresh)
        
    def set_default_values(self):
        self.line_style = 'solid'
        self.fill = True
        self.tag = 'legend'
        self.what_eval = 'bbox'