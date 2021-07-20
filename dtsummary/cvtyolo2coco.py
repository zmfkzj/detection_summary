import json
import os.path as osp
import os

from dtsummary.object import DetectDataset
from pathlib import Path

def cvtyolo2coco(yolo_result_path, gt_path):
    with open(yolo_result_path,'r') as f:
        yolo_result = json.load(f)
    
    for r in yolo_result:
        for o in r['objects']:
            coord = o['relative_coordinates']
            new_coord = {'x_c':coord['center_x'],
                        'y_c': coord['center_y'],
                        'w_r': coord['width'],
                        'h_r': coord['height']}
            o['yolo_bbox'] = new_coord
            del  o['relative_coordinates']
    
    savepath = Path(gt_path).parent
    yolo_dt_save_path = osp.join(savepath,'custom_dt_result.json')
    with open(yolo_dt_save_path,'w') as f:
        json.dump(yolo_result,f)
    

    dtDataset = DetectDataset(dt_path=yolo_dt_save_path)
    dtDataset.to_coco_result(gt_path)
    dtDataset.to_coco(gt_path)
    os.remove(yolo_dt_save_path)
