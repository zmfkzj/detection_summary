import numpy as np
import cv2

from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from pathlib import Path
from PIL import Image
from ddt import DdtImage

from dtsummary.summary_ui import Ui_MainWindow
from dtsummary.cvtyolo2coco import cvtyolo2coco
from dtsummary.evalutation import Evaluation
from dtsummary.object import Bbox

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, Ui_MainWindow):
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        #변수 기본값 설정
        self.set_default_values()

        #평가종류 라디오
        self.bbox.clicked.connect(lambda: setattr(self,'eval_type','bbox'))
        self.segm.clicked.connect(lambda: setattr(self,'eval_type','segm'))

        #gt선모양 라디오
        self.gtline_solid.clicked.connect(lambda: setattr(self,'gtline_style','solid'))
        self.gtline_dot.clicked.connect(lambda: setattr(self,'gtline_style','dot'))
        self.gtline_no.clicked.connect(lambda: setattr(self,'gtline_style','no'))

        # gt채우기 라디오
        self.gtfill_yes.clicked.connect(lambda: setattr(self,'gtfill',True))
        self.gtfill_no.clicked.connect(lambda: setattr(self,'gtfill',False))

        #dt선모양 라디오
        self.dtline_solid.clicked.connect(lambda: setattr(self,'dtline_style','solid'))
        self.dtline_dot.clicked.connect(lambda: setattr(self,'dtline_style','dot'))
        self.dtline_no.clicked.connect(lambda: setattr(self,'dtline_style','no'))

        # dt채우기 라디오
        self.dtfill_yes.clicked.connect(lambda: setattr(self,'dtfill',True))
        self.dtfill_no.clicked.connect(lambda: setattr(self,'dtfill',False))

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

        #draw object
        self.sel_labelmap.clicked.connect(lambda: self.single_file_select(self.labelmap_path))
        self.draw_btn.clicked.connect(self.draw)

    def draw(self):
        gt = self.eval.eval.cocoGt
        dt = self.eval.eval.cocoDt
        for image_id, gt_annos in gt.imgToAnns.items():
            dt_annos = dt.imgToAnns[image_id]
            filename = gt.loadImgs(ids=image_id)[0]['file_name']
            image_path = Path(self.eval_gt_path.text()).parent/f'../images/{filename}'
            image = np.array(Image.open(image_path))
            image_size = image.shape[:2]
            if len(image.shape) == 3 and image.shape[2] in {3, 4}:
                image[:,:,:3] = image[:,:,2::-1]
            ddt_img = DdtImage(image=image,labelmap=self.labelmap_path.text())
            if self.tag=='legend':
                tag=False
            elif self.tag=='object':
                tag = True

            #draw gt
            for anno in gt_annos:
                cat = gt.loadCats(ids=anno['category_id'])[0]['name']
                if self.eval_type=='segm':
                    for seg in anno['segmentation']:
                        ddt_img.drawSeg(cat,seg,self.gtline_style,self.gtfill)
                elif self.eval_type=='bbox':
                    ddt_img.drawBbox(cat,Bbox(image_size,coco_box=anno['bbox']).voc,self.gtline_style,self.gtfill, tag=tag)
            #draw dt
            for anno in dt_annos:
                if anno['score']<float(self.conf_thresh.text()):
                    continue
                cat = dt.loadCats(ids=anno['category_id'])[0]['name']
                if self.eval_type=='segm':
                    for seg in anno['segmentation']:
                        ddt_img.drawSeg(cat,seg,self.dtline_style,self.dtfill)
                elif self.eval_type=='bbox':
                    ddt_img.drawBbox(cat,Bbox(image_size,coco_box=anno['bbox']).voc,self.dtline_style,self.dtfill, tag=tag)

            #draw sign
            if self.gt_sign.isChecked():
                ddt_img.draw_sign('GT',0,self.gtline_style, self.gtfill)
            if self.dt_sign.isChecked():
                ddt_img.draw_sign('DT',1,self.dtline_style, self.dtfill)

            if tag==False:
                ddt_img.drawLegend()

            ddt_img.save(Path(self.eval_gt_path.text()).parent/f'../result_images/{filename}')

    def __getattr__(self,name):
        if name=='eval':
            self.eval = Evaluation(self.eval_dt_path.text(),self.eval_gt_path.text(),self.eval_type)
        return getattr(self,name)

    def single_file_select(self, lineEdit, *a):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '')
        lineEdit.setText(filename[0])

    def run_eval(self):
        self.eval = Evaluation(self.eval_dt_path.text(),self.eval_gt_path.text(),self.eval_type)
        self.eval.run_eval(float(self.conf_thresh.text()))
        
    def set_default_values(self):
        self.gtline_style = 'solid'
        self.gtfill = True
        self.dtline_style = 'solid'
        self.dtfill = True
        self.tag = 'legend'
        self.eval_type = 'bbox'