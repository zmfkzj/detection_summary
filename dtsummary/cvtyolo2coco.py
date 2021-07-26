import json
from operator import gt
import os.path as osp
import os

from dtsummary.object import DetectDataset
from pathlib import Path
import chardet


def cvtyolo2coco(yolo_result_path, gt_path):

    with open(yolo_result_path, 'rb') as f:
        result = f.read()
    encoding = chardet.detect(result)['encoding']

    with open(yolo_result_path,'r', encoding=encoding) as f:
        yolo_result = json.load(f)

    with open(gt_path, 'rb') as f:
        result = f.read()
    encoding = chardet.detect(result)['encoding']

    with open(gt_path,'r', encoding=encoding) as f:
        gt_result = json.load(f)
    
    gt_images_dict = {Path(image['file_name']).as_posix():image for image in gt_result['images']}
    def _get_image(filename):
        filename = '/'.join(Path(filename).as_posix().split('/')[1:])
        if filename in gt_images_dict:
            return gt_images_dict[filename]
        else:
            return _get_image(filename)

    for r in yolo_result:
        filename = r['filename']
        coco_image = _get_image(filename)

        r['image_size'] = {'height':coco_image['height'],'width':coco_image['width']}
        for o in r['objects']:
            coord = o['relative_coordinates']
            new_coord = {'xc_r':coord['center_x'],
                        'yc_r': coord['center_y'],
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
