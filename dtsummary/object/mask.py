from typing import Tuple, List, Union
from pycocotools import mask as coco_mask
from imantics import Mask as iMask
from .box import Bbox

import numpy as np

class Mask:
    def __init__(self,image_size,label:str = None, confidence:float=1,
                    rle:str=None,
                    polygons:Union[np.ndarray, List, Tuple]=None,
                    ) -> None:
        self._label = label
        self._confidence = confidence

        if rle:
            self._rle = rle
            binary_mask = coco_mask.decode(rle)
            self._polygons = iMask(binary_mask).polygons
        elif polygons:
            self._polygons = polygons
            self._rle = coco_mask.frPyObjects(polygons,*image_size)
        else:
            raise Exception('please input one of "rle" or "polygons"')
        self._area = coco_mask.area(self._rle)

        coco_bbox = coco_mask.toBbox(self._rle)
        self._bbox = Bbox(image_size=image_size,
                        label=label,
                        confidence=confidence,
                        coco_box=coco_bbox
                        )

    @property
    def area(self): return self._area

    @property
    def rle(self): return self._rle

    @property
    def polygons(self): return self._polygons

    @property
    def label(self): return self._label

    @property
    def confidence(self): return self._confidence

    @property
    def bbox(self): return self._bbox