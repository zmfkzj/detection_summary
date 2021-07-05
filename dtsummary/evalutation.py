from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval
from pathlib import Path
from .object import DetectDataset

import chardet
import json
import numpy as np


class Evaluation:
    def __init__(self,dt_path, gt_path, type) -> None:
        assert type in ['bbox','segm'], '"type" argument must be one of "bbox" or "segm"'
        self.dataset = DetectDataset(dt_path=dt_path)
        gt_path = Path('train.json')
        self.re_encoding(gt_path)
        gt_path = gt_path.parent/f'cp949_{gt_path.name}'
        self.dataset.to_coco_result(gt_path)
        dt_result_path = Path('detection_result_COCOeval_cp949.json')

        coco = COCO(str(gt_path))
        dt = coco.loadRes(str(dt_result_path))
        eval = COCOeval(coco,dt,type)
        imgs = eval.params.imgIds
        for id in imgs:
            eval.params.imgIds = [id]
            eval.evaluate()
            eval.accumulate()
            precision = np.round(np.mean([p for p in eval.eval['precision'][0,25,:,0,2] if p != -1]),4)*100
            recall = np.round(np.mean([r for r in eval.eval['recall'][0,:,0,2] if r!=-1]),4)*100
            f1 = (2*precision*recall)/(precision+recall)
            f1 = round(f1,4)*100 if not np.isnan(f1) else 0

    @staticmethod
    def re_encoding(json_file:Path):
        with open(json_file, 'r') as f:
            result = f.readline()
        encoding = chardet.detect(result.encode())['encoding']

        with open(json_file, 'r',encoding=encoding) as f:
            result = json.load(f)

        with open(json_file.parent/f'cp949_{json_file.name}', 'w',encoding='cp949') as f:
            json.dump(result,f)


