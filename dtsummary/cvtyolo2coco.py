import json
import os.path as osp

from pathlib import Path
from dtsummary.util import read_json


def cvtyolo2coco(yolo_result_path, gt_path):

    root = Path(gt_path).parent
    yolo_result = read_json(yolo_result_path)
    gt_result = read_json(gt_path)

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
            new_coord = [ coord['center_x'],coord['center_y'],coord['width'],coord['height'] ]
            o['yolo_bbox'] = new_coord
            del  o['relative_coordinates']
    
    savepath = Path(gt_path).parent
    yolo_dt_save_path = osp.join(savepath,'custom_dt_result.json')
    with open(root/yolo_dt_save_path,'w') as f:
        json.dump(yolo_result,f)