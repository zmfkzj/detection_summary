# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'summary_ui.ui'
##
## Created by: Qt User Interface Compiler version 6.1.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(356, 531)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.formFrame = QFrame(self.centralwidget)
        self.formFrame.setObjectName(u"formFrame")
        self.formFrame.setGeometry(QRect(-1, -1, 351, 481))
        self.formLayout = QFormLayout(self.formFrame)
        self.formLayout.setObjectName(u"formLayout")
        self.gridGroupBox_3 = QGroupBox(self.formFrame)
        self.gridGroupBox_3.setObjectName(u"gridGroupBox_3")
        self.gridLayout_3 = QGridLayout(self.gridGroupBox_3)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridGroupBox_42 = QGroupBox(self.gridGroupBox_3)
        self.gridGroupBox_42.setObjectName(u"gridGroupBox_42")
        self.gridLayout_4 = QGridLayout(self.gridGroupBox_42)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.fill_no = QRadioButton(self.gridGroupBox_42)
        self.fill_no.setObjectName(u"fill_no")

        self.gridLayout_4.addWidget(self.fill_no, 1, 0, 1, 1)

        self.fill_yes = QRadioButton(self.gridGroupBox_42)
        self.fill_yes.setObjectName(u"fill_yes")
        self.fill_yes.setChecked(True)

        self.gridLayout_4.addWidget(self.fill_yes, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.gridGroupBox_42, 0, 1, 1, 1)

        self.gridGroupBox_4 = QGroupBox(self.gridGroupBox_3)
        self.gridGroupBox_4.setObjectName(u"gridGroupBox_4")
        self.gridLayout_5 = QGridLayout(self.gridGroupBox_4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.line_dot = QRadioButton(self.gridGroupBox_4)
        self.line_dot.setObjectName(u"line_dot")

        self.gridLayout_5.addWidget(self.line_dot, 2, 0, 1, 1)

        self.line_no = QRadioButton(self.gridGroupBox_4)
        self.line_no.setObjectName(u"line_no")

        self.gridLayout_5.addWidget(self.line_no, 3, 0, 1, 1)

        self.line_solid = QRadioButton(self.gridGroupBox_4)
        self.line_solid.setObjectName(u"line_solid")
        self.line_solid.setChecked(True)

        self.gridLayout_5.addWidget(self.line_solid, 1, 0, 1, 1)


        self.gridLayout_2.addWidget(self.gridGroupBox_4, 0, 0, 1, 1)

        self.gridGroupBox_41 = QGroupBox(self.gridGroupBox_3)
        self.gridGroupBox_41.setObjectName(u"gridGroupBox_41")
        self.gridLayout_6 = QGridLayout(self.gridGroupBox_41)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.each_object = QRadioButton(self.gridGroupBox_41)
        self.each_object.setObjectName(u"each_object")

        self.gridLayout_6.addWidget(self.each_object, 1, 0, 1, 1)

        self.legend = QRadioButton(self.gridGroupBox_41)
        self.legend.setObjectName(u"legend")
        self.legend.setChecked(True)

        self.gridLayout_6.addWidget(self.legend, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.gridGroupBox_41, 0, 2, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 2, 1, 1)

        self.draw_btn = QPushButton(self.gridGroupBox_3)
        self.draw_btn.setObjectName(u"draw_btn")

        self.gridLayout_3.addWidget(self.draw_btn, 1, 2, 1, 1)


        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.gridGroupBox_3)

        self.gridGroupBox_2 = QGroupBox(self.formFrame)
        self.gridGroupBox_2.setObjectName(u"gridGroupBox_2")
        self.gridLayout_7 = QGridLayout(self.gridGroupBox_2)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.label_3 = QLabel(self.gridGroupBox_2)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_7.addWidget(self.label_3, 1, 0, 1, 1)

        self.cvt_gt_path = QLineEdit(self.gridGroupBox_2)
        self.cvt_gt_path.setObjectName(u"cvt_gt_path")

        self.gridLayout_7.addWidget(self.cvt_gt_path, 0, 1, 1, 1)

        self.yolo_json_path = QLineEdit(self.gridGroupBox_2)
        self.yolo_json_path.setObjectName(u"yolo_json_path")

        self.gridLayout_7.addWidget(self.yolo_json_path, 1, 1, 1, 1)

        self.sel_cvt_gt_path = QPushButton(self.gridGroupBox_2)
        self.sel_cvt_gt_path.setObjectName(u"sel_cvt_gt_path")

        self.gridLayout_7.addWidget(self.sel_cvt_gt_path, 0, 2, 1, 1)

        self.label_4 = QLabel(self.gridGroupBox_2)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_7.addWidget(self.label_4, 0, 0, 1, 1)

        self.sel_yolo_json = QPushButton(self.gridGroupBox_2)
        self.sel_yolo_json.setObjectName(u"sel_yolo_json")

        self.gridLayout_7.addWidget(self.sel_yolo_json, 1, 2, 1, 1)

        self.cvt_btn = QPushButton(self.gridGroupBox_2)
        self.cvt_btn.setObjectName(u"cvt_btn")

        self.gridLayout_7.addWidget(self.cvt_btn, 2, 1, 1, 1)


        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.gridGroupBox_2)

        self.gridLayout_9 = QGridLayout()
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.label = QLabel(self.formFrame)
        self.label.setObjectName(u"label")

        self.gridLayout_9.addWidget(self.label, 0, 0, 1, 1)

        self.sel_gt = QPushButton(self.formFrame)
        self.sel_gt.setObjectName(u"sel_gt")

        self.gridLayout_9.addWidget(self.sel_gt, 0, 2, 1, 1)

        self.eval_gt_path = QLineEdit(self.formFrame)
        self.eval_gt_path.setObjectName(u"eval_gt_path")

        self.gridLayout_9.addWidget(self.eval_gt_path, 0, 1, 1, 1)

        self.label_2 = QLabel(self.formFrame)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_9.addWidget(self.label_2, 1, 0, 1, 1)

        self.eval_dt_path = QLineEdit(self.formFrame)
        self.eval_dt_path.setObjectName(u"eval_dt_path")

        self.gridLayout_9.addWidget(self.eval_dt_path, 1, 1, 1, 1)

        self.sel_dt = QPushButton(self.formFrame)
        self.sel_dt.setObjectName(u"sel_dt")

        self.gridLayout_9.addWidget(self.sel_dt, 1, 2, 1, 1)


        self.formLayout.setLayout(0, QFormLayout.FieldRole, self.gridLayout_9)

        self.gridGroupBox = QGroupBox(self.formFrame)
        self.gridGroupBox.setObjectName(u"gridGroupBox")
        self.gridLayout = QGridLayout(self.gridGroupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.eval_btn = QPushButton(self.gridGroupBox)
        self.eval_btn.setObjectName(u"eval_btn")

        self.gridLayout.addWidget(self.eval_btn, 4, 2, 1, 1)

        self.label_5 = QLabel(self.gridGroupBox)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)

        self.label_6 = QLabel(self.gridGroupBox)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 3, 0, 1, 1)

        self.gridLayout_8 = QGridLayout()
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.bbox = QRadioButton(self.gridGroupBox)
        self.bbox.setObjectName(u"bbox")
        self.bbox.setChecked(True)

        self.gridLayout_8.addWidget(self.bbox, 0, 0, 1, 1)

        self.segm = QRadioButton(self.gridGroupBox)
        self.segm.setObjectName(u"segm")

        self.gridLayout_8.addWidget(self.segm, 0, 1, 1, 1)


        self.gridLayout.addLayout(self.gridLayout_8, 3, 1, 1, 1)

        self.conf_thresh = QDoubleSpinBox(self.gridGroupBox)
        self.conf_thresh.setObjectName(u"conf_thresh")
        self.conf_thresh.setMinimum(0.010000000000000)
        self.conf_thresh.setSingleStep(0.010000000000000)
        self.conf_thresh.setValue(0.250000000000000)

        self.gridLayout.addWidget(self.conf_thresh, 4, 1, 1, 1)


        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.gridGroupBox)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 356, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.gridGroupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"\uac1d\uccb4 \uadf8\ub9ac\uae30", None))
        self.gridGroupBox_42.setTitle(QCoreApplication.translate("MainWindow", u"\ucc44\uc6b0\uae30", None))
        self.fill_no.setText(QCoreApplication.translate("MainWindow", u"No", None))
        self.fill_yes.setText(QCoreApplication.translate("MainWindow", u"Yes", None))
        self.gridGroupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"\uc120\ubaa8\uc591", None))
        self.line_dot.setText(QCoreApplication.translate("MainWindow", u"\uc810\uc120", None))
        self.line_no.setText(QCoreApplication.translate("MainWindow", u"\uc5c6\uc74c", None))
        self.line_solid.setText(QCoreApplication.translate("MainWindow", u"\uc2e4\uc120", None))
        self.gridGroupBox_41.setTitle(QCoreApplication.translate("MainWindow", u"\ub77c\ubca8\ud45c\uc2dc\ubc29\ubc95", None))
        self.each_object.setText(QCoreApplication.translate("MainWindow", u"\uac01 \uac1c\uccb4", None))
        self.legend.setText(QCoreApplication.translate("MainWindow", u"\ubc94\ub840", None))
        self.draw_btn.setText(QCoreApplication.translate("MainWindow", u"\uadf8\ub9ac\uae30 \uc2dc\uc791", None))
        self.gridGroupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"yolo detection json \u2192 custom result json", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"yolo json", None))
        self.sel_cvt_gt_path.setText(QCoreApplication.translate("MainWindow", u"\ud30c\uc77c\uc120\ud0dd", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"coco GT", None))
        self.sel_yolo_json.setText(QCoreApplication.translate("MainWindow", u"\ud30c\uc77c\uc120\ud0dd", None))
        self.cvt_btn.setText(QCoreApplication.translate("MainWindow", u"\ubc14\uafb8\uae30", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"coco GT", None))
        self.sel_gt.setText(QCoreApplication.translate("MainWindow", u"\ud30c\uc77c\uc120\ud0dd", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"cumtom Dt", None))
        self.sel_dt.setText(QCoreApplication.translate("MainWindow", u"\ud30c\uc77c\uc120\ud0dd", None))
        self.gridGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"\ud3c9\uac00", None))
        self.eval_btn.setText(QCoreApplication.translate("MainWindow", u"\ud3c9\uac00 \ubc0f \uacb0\uacfc \uc800\uc7a5", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"conf thresh", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\ud3c9\uac00\uc885\ub958", None))
        self.bbox.setText(QCoreApplication.translate("MainWindow", u"Bbox", None))
        self.segm.setText(QCoreApplication.translate("MainWindow", u"Seg", None))
    # retranslateUi

