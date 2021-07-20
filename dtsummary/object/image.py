from operator import itemgetter
from .box import Bbox
from .mask import Mask
from typing import List, Union

import numpy as np

class DetectImage:
    def __init__(self, filename:str, 
                    image_size:Union[np.ndarray,list,tuple],
                    dt_objects_data:List[dict]=None,
                    gt_objects_data:List[dict]=None) -> None:
        self._filename = filename
        self._image_size = image_size

        self._dt = _DetectImage(image_size=image_size,
                                objects_data=dt_objects_data)
        self._gt = _DetectImage(image_size=image_size,
                                objects_data=gt_objects_data)

    def __len__(self): return (len(self._dt), len(self._gt))
    def __repr__(self): return (repr(self._dt), repr(self._gt))

    @property
    def filename(self): return self._filename

    @property
    def size(self): return self._image_size

    @property
    def dt(self): return self._dt

    @property
    def gt(self): return self._gt


class _DetectImage:
    def __init__(self, image_size:Union[np.ndarray,list,tuple],
                    objects_data:List[dict]=None) -> None:
        self._image_size = image_size

        self.set_item(objects_data)

    def __iter__(self): return iter(self._items)
    def __len__(self): return len(self._items)
    def __repr__(self): return repr(self._items)

    def append(self, object_data:dict):
        assert set(['yolo_bbox', 'voc_bbox','coco_bbox']) & set(object_data), 'type argument is one of "[yolo voc coco]_bbox" or "mask"'
        for key in object_data:
            if key=='yolo_bbox':
                boxgetter = itemgetter('xc_r','yc_r','w_r','h_r')
                kwdarg = {'yolo_box':boxgetter(object_data['yolo_bbox'])}
                obj_cls = Bbox
            elif key=='voc_bbox':
                boxgetter = itemgetter('x1_a','y1_a','x2_a','y2_a')
                kwdarg = {'voc_box':boxgetter(object_data['voc_bbox'])}
                obj_cls = Bbox
            elif key=='coco_bbox':
                boxgetter = itemgetter('x1_a','y1_a','w_a','h_a')
                kwdarg = {'coco_box':boxgetter(object_data['coco_bbox'])}
                obj_cls = Bbox
            elif key=='mask':
                obj_cls = Mask
                kwdarg = {'mask':object_data['mask']}
            else:
                pass
        object = obj_cls(image_size=self._image_size,
                        label=object_data['name'],
                        confidence=object_data['confidence'],
                        **kwdarg)
        self._items.append(object)
    
    def extend(self, objects_data:List[dict]):
        for object_data in objects_data:
            self.append(object_data)

    def set_item(self, objects_data:List[dict]):
        self._items:List[Union[Bbox,Mask]] = []
        if objects_data:
            self.extend(objects_data)