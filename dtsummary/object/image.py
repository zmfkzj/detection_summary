from .box import Bbox
from .mask import Mask
from typing import List, Union

import numpy as np
from pathlib import Path

class DetectImage:
    def __init__(self, filename:str, 
                    image_size:Union[np.ndarray,list,tuple],
                    dt_objects_data:List[dict]=None,
                    gt_objects_data:List[dict]=None,
                    conf_thresh = 0) -> None:
        self._filename = filename
        self._image_size = image_size

        self._dt = _DetectImage(image_size=image_size,
                                objects_data=dt_objects_data, 
                                conf_thresh = conf_thresh)
        self._gt = _DetectImage(image_size=image_size,
                                objects_data=gt_objects_data,
                                conf_thresh = conf_thresh)

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

    @property
    def data(self):
        dt_objects = [item.data for item in self.dt]
        gt_objects = [item.data for item in self.gt]
        objects = []
        objects.extend(dt_objects)
        objects.extend(gt_objects)
        return {'filename':str(Path(self.filename).as_posix()),
                'image_size': {'height':self.size[0],
                                'width': self.size[1]},
                'objects': objects}
class _DetectImage:
    def __init__(self, image_size:Union[np.ndarray,list,tuple],
                    objects_data:List[dict]=None,
                    conf_thresh=0) -> None:
        self._image_size = image_size
        self.conf_thresh = conf_thresh

        self.set_item(objects_data)
        

    def __iter__(self): return iter(self._items)
    def __len__(self): return len(self._items)
    def __repr__(self): return repr(self._items)

    def append(self, object_data:dict):
        assert set(['yolo_bbox', 'voc_bbox','coco_bbox','polygons','rle']) & set(object_data), 'type argument is one of "[yolo voc coco]_bbox" or "mask"'
        for key in object_data:
            if key=='yolo_bbox':
                kwdarg = {'yolo_bbox':object_data['yolo_bbox']}
                obj_cls = Bbox
            elif key=='voc_bbox':
                kwdarg = {'voc_bbox':object_data['voc_bbox']}
                obj_cls = Bbox
            elif key=='coco_bbox':
                kwdarg = {'coco_bbox':object_data['coco_bbox']}
                obj_cls = Bbox
            elif key=='rle':
                obj_cls = Mask
                kwdarg = {'rle':object_data['rle']}
            elif key=='polygons':
                obj_cls = Mask
                kwdarg = {'polygons':object_data['polygons']}
            else:
                pass
        object = obj_cls(image_size=self._image_size,
                        label=object_data['label'],
                        confidence=object_data['confidence'],
                        **kwdarg)
        self._items.append(object)
    
    def extend(self, objects_data:List[dict]):
        for object_data in objects_data:
            if object_data['confidence']<self.conf_thresh:
                continue
            self.append(object_data)

    def set_item(self, objects_data:List[dict]):
        self._items:List[Union[Bbox,Mask]] = []
        if objects_data:
            self.extend(objects_data)

    @property
    def data(self):
        return [item.data for item in self._items]
