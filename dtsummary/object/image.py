from operator import itemgetter
from .box import Bbox
from .polygon import Polygon
from typing import List, Union

import numpy as np

class DetectImage:
    def __init__(self, filename:str, image_size:Union[np.ndarray,list,tuple],objects_data:List[dict]=None) -> None:
        self._filename = filename
        self._image_size = image_size

        if objects_data:
            self.set_item(objects_data)
        else:
            self._items = []

    def __iter__(self): return iter(self._items)
    def __len__(self): return len(self._items)
    def __repr__(self): return repr(self._items)

    def append(self, object_data:dict):
        type = object_data['type'].split('_')
        boxgetter = itemgetter('center_x','center_y','width','height')
        if type[-1]=='bbox':
            kwdarg = {f'{type[0]}_box':boxgetter(object_data['relative_coordinates'])}
            object = Bbox(image_size=self._image_size,
                          label=object_data['name'],
                          confidence=object_data['confidence'],
                          **kwdarg)
        elif type[-1]=='polygon':
            pass
        else:
            TypeError('type argument is one of "[yolo voc coco]_bbox" or "polygon"')
        self._items.append(object)
    
    def extend(self, objects_data:List[dict]):
        for object_data in objects_data:
            self.append(object_data)

    def set_item(self, objects_data:List[dict]):
        self._items = []
        self.extend(objects_data)

    @property
    def filename(self): return self._filename

    @property
    def size(self): return self._image_size