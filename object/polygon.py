from typing import Tuple, List, Union

import numpy as np

class Polygon:
    def __init__(self,label:str = None,
                    points:Union[np.ndarray, List, Tuple]=None,
                    **kwdargs
                    ) -> None:
        self._label = label