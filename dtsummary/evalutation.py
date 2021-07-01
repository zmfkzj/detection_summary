from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval
from pathlib import Path

import json

def re_encoding(json_file:Path):
    with open(json_file, 'r',encoding='utf-8') as f:
        result = json.load(f)
    with open(json_file.parent/f'cp949_{json_file.name}', 'w',encoding='cp949') as f:
        json.dump(result,f)


gt_path = Path('train.json')
re_encoding(gt_path)
gt_path = gt_path.parent/f'cp949_{gt_path.name}'
dt_path = Path('detection_result_COCOeval_cp949.json')

gt = COCO(str(gt_path))
dt = gt.loadRes(str(dt_path))
eval = COCOeval(gt,dt,'bbox')
eval.evaluate()
eval.accumulate()
print(eval.evalImgs)