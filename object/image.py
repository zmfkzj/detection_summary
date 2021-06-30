from operator import itemgetter
from numpy.lib.arraysetops import isin
from .box import Bbox
from .polygon import Polygon
from typing import List, Union

import numpy as np

class DetectImage:
    def __init__(self, id:str, image_size:Union[np.ndarray,list,tuple]) -> None:
        self._id = id
        self._image_size = image_size
        self._items = []

    def __iter__(self): return iter(self._items)
    def __len__(self): return len(self._items)
    def __repr__(self): return repr(self._items)

    def expand(self, object_data:dict):
        type = object_data['type'].split('_')
        boxgetter = itemgetter(('center_x','center_y','width','height'))
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
        self._items.extend(object)
    
    def extend(self, objects_data:List[dict]):
        for object_data in objects_data:
            self.expand(object_data)

    def set_item(self, objects_data:List[dict]):
        self._items = []
        self.expand(objects_data)

    @property
    def id(self): return self._id

    @property
    def size(self): return self._image_size