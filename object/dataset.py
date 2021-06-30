from operator import itemgetter
from .image import DetectImage
from .box import Bbox
from .polygon import Polygon
from typing import List, Union

import json

class DetectDataset:
    def __init__(self, path) -> None:
        self._path = path
        self._items = []



    def __iter__(self): return iter(self._items)
    def __len__(self): return len(self._items)
    def __repr__(self): return repr(self._items)

    def expand(self, object:DetectImage):
        self._items.extend(object)
    
    def extend(self, items:List[DetectImage]):
        if not all([isinstance(item,DetectImage) for item in items]):
            TypeError('"items argument must be DetectionImage class"')
        else:
            self._items.extend(items)

    def set_item(self, items:List[DetectImage]):
        if not all([isinstance(item,DetectDataset) for item in items]):
            TypeError('"items argument must be DetectionImage class"')
        else:
            self._items = items

    def _load_detection_results(self, path):
        with open(path,'r') as f:
            results = json.dump(f)
        sizegetter = itemgetter(('width','height'))
        for image in results:
            dt_image = DetectImage(image['filename'], sizegetter(image['image_size']))
            dt_image.set_item(image['objects'])
            self.expand(dt_image)
