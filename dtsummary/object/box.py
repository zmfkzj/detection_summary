from typing import Tuple, List, Union

import numpy as np

class Bbox:
    def __init__(self,image_size,label:str = None, confidence:float=1,
                    yolo_box:Union[np.ndarray, List, Tuple]=None,
                    voc_box:Union[np.ndarray, List, Tuple]=None,
                    coco_box:Union[np.ndarray, List, Tuple]=None,
                    ) -> None:
        self._label = label
        self._confidence = confidence

        if yolo_box:
            self._yolo_box = yolo_box
            self._cal_yolo_box(yolo_box,image_size)
        elif voc_box:
            self._voc_box = voc_box
            self._cal_voc_box(voc_box, image_size)
        elif coco_box:
            self._coco_box = coco_box
            self._cal_coco_box(coco_box,image_size)
        else:
            Exception('please enter at least one bbox argument')

    def _cal_yolo_box(self,yolo_box,image_size):
        '''
        yolo_box = (x_center_relative, y_center_relative,width_relative,height_relative)
        image_size = (height,width)
        '''
        xc_r,yc_r,w_r,h_r = yolo_box
        height, width = image_size

        self._x1_r = np.maximum(xc_r-w_r/2,0)
        self._x2_r = np.minimum(xc_r+w_r/2,1)
        self._y1_r = np.maximum(yc_r-h_r/2,0)
        self._y2_r = np.maximum(yc_r+h_r/2,1)
        self._w_r = self.x2_r-self._x1_r
        self._h_r = self.y2_r-self._y1_r
        self._xc_r = self._x1_r+self._w_r/2
        self._yc_r = self._y1_r+self._h_r/2
        self._area_r = self._w_r*self._h_r

        self._x1_a = self._x1_r*width
        self._x2_a = self._x2_r*width
        self._y1_a = self._y1_r*height
        self._y2_a = self._y2_r*height
        self._w_a = self._w_r*width
        self._h_a = self._h_r*height
        self._xc_a = self._x1_a+self._w_a/2
        self._yc_a = self._y1_a+self._h_a/2
        self._area_a = self._w_a*self._h_a

    def _cal_voc_box(self,voc_box, image_size):
        '''
        voc_box = (x1_absolute, y1_absolute,x2_absolute,y2_absolute)
        image_size = (height,width)
        '''
        x1_a, y1_a, x2_a, y2_a = voc_box
        height, width = image_size

        self._x1_a = np.maximum(0,x1_a)
        self._y1_a = np.maximum(0,y1_a)
        self._x2_a = np.minimum(width,x2_a)
        self._y2_a = np.minimum(height,y2_a)
        self._w_a = self._x2_a-self._x1_a
        self._h_a = self._y2_a-self._y2_a
        self._xc_a = self._x1_a+self._w_a/2
        self._yc_a = self._y1_a+self._h_a/2
        self._area_a = self._w_a*self._h_a

        self._x1_r, self._x2_r, self._w_r, self._xc_r = [x/width for x in [self._x1_a,self._x2_a,self._w_a,self._xc_a]]
        self._y1_r, self._y2_r, self._h_r, self._yc_r = [y/height for y in [self._y1_a,self._y2_a,self._h_a,self._yc_a]]
        self._area_r = self._w_r*self._h_r

    def _cal_coco_box(self,coco_box, image_size):
        '''
        coco_box = (x1_absolute, y1_absolute,w_absolute,h_absolute)
        image_size = (height,width)
        '''
        x1_a,y1_a,w_a,h_a = coco_box
        height, width = image_size

        self._x1_a = np.maximum(0,x1_a)
        self._y1_a = np.maximum(0,y1_a)
        self._x2_a = np.minimum(width,x1_a+w_a)
        self._y2_a = np.minimum(height,y1_a+h_a)
        self._w_a = self._x2_a-self._x1_a
        self._h_a = self._y2_a-self._y2_a
        self._xc_a = self._x1_a+self._w_a/2
        self._yc_a = self._y1_a+self._h_a/2
        self._area_a = self._w_a*self._h_a

        self._x1_r, self._x2_r, self._w_r, self._xc_r = [x/width for x in [self._x1_a,self._x2_a,self._w_a,self._xc_a]]
        self._y1_r, self._y2_r, self._h_r, self._yc_r = [y/height for y in [self._y1_a,self._y2_a,self._h_a,self._yc_a]]
        self._area_r = self._w_r*self._h_r

    @property
    def label(self): return self._label

    @property
    def confidence(self): return self._confidence

    @property
    def x1_a(self): return self._x1_a

    @property
    def y1_a(self): return self._y1_a

    @property
    def x2_a(self): return self._x2_a

    @property
    def y2_a(self): return self._y2_a

    @property
    def xc_a(self): return self._xc_a

    @property
    def yc_a(self): return self._yc_a
    
    @property
    def w_a(self): return self._w_a

    @property
    def h_a(self): return self._h_a

    @property
    def area_a(self): return self._area_a

    @property
    def x1_r(self): return self._x1_r

    @property
    def y1_r(self): return self._y1_r

    @property
    def x2_r(self): return self._x2_r

    @property
    def y2_r(self): return self._y2_r

    @property
    def xc_r(self): return self._xc_r

    @property
    def yc_r(self): return self._yc_r

    @property
    def w_r(self): return self._w_r

    @property
    def h_r(self): return self._h_r

    @property
    def area_r(self): return self._area_r

    @property
    def yolo(self): return self.x1_r, self.x2_r, self.w_r, self.h_r

    @property
    def voc(self): return self.x1_a, self.y1_a, self.x2_a, self.y2_a

    @property
    def coco(self): return self.x1_a, self.y1_a, self.w_a, self.h_a

if __name__=='__main__':
    a = Bbox('zmfkzj',(1000,600))