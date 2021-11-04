from operator import itemgetter
from pathlib import Path

from numpy.core.fromnumeric import argmin

from .image import DetectImage
from .box import Bbox
from .mask import Mask

from typing import List
from copy import deepcopy
from functools import reduce
from dtsummary.util import read_json
from collections import defaultdict
from pycocotools.coco import COCO

import chardet
import json

class DetectDataset:
    '''
    collection of DetectImage
    '''
    def __init__(self, images_data:List[dict]=None, custom_dt_path:str=None, conf_thresh=0) -> None:
        self.conf_thresh = conf_thresh
        if images_data:
            self.set_item(images_data)
        elif custom_dt_path:
            self._load_detection_results(custom_dt_path)
        else:
            self._items:List[DetectImage] = []

        if self._items:
            self._get_categories_from_items()
        else:
            self._categories:str = []

    def __iter__(self): return iter(self._items)
    def __len__(self): return len(self._items)
    def __repr__(self): return repr(self._items)

    def append(self, image_data:dict):
        filename = image_data['filename']
        objects_data = image_data['objects']
        sizegetter = itemgetter('height','width')
        image_size = sizegetter(image_data['image_size'])
        image = DetectImage(filename=filename,
                            image_size=image_size,
                            dt_objects_data=objects_data,
                            conf_thresh = self.conf_thresh
                            )
        self._items.append(image)
    
    def extend(self, images_data:List[dict]):
        for image_data in images_data:
            self.append(image_data)

    def set_item(self, images_data:List[dict]):
        self._items = []
        self.extend(images_data)

    def _load_detection_results(self, path):
        images_data = read_json(path)
        self.set_item(images_data)

    def _get_categories_from_items(self):
        labels = [[box.label for box in image.dt] for image in self._items ]
        self._categories = list(set(reduce(lambda x,y: x+y,labels)))

    def to_coco_result(self, gt_path):
        root = Path(gt_path).parent
        gt = read_json(gt_path)

        gt_labels:list = gt['categories']
        gt_labels_name_id_dict = {}
        for label in gt_labels:
            gt_labels_name_id_dict[label['name']] = label['id']

        gt_images:list = gt['images']
        gt_images_name_id_dict = {}
        for image in gt_images:
            gt_images_name_id_dict[image['file_name']] = image['id']


        dt_results = []
        for image in self._items:
            gt_matching_image_names = [gt_image_name for gt_image_name in gt_images_name_id_dict if (gt_image_name.rfind(image.filename)!=-1) | (image.filename.rfind(gt_image_name) != -1)]
            if len(gt_matching_image_names)==1:
                gt_matching_image_names = gt_matching_image_names[0]
            elif len(gt_matching_image_names)>1:
                matching_index = argmin([gt_image_name.rfind(image.filename) for gt_image_name in gt_matching_image_names])
                gt_matching_image_names = gt_matching_image_names[matching_index]
            else:
                print(gt_matching_image_names)
                raise Exception('gt와 dt의 이미지 파일명을 매칭하지 못했습니다.')

            image_id = gt_images_name_id_dict[gt_matching_image_names]
            for obj in image.dt:
                category_id = gt_labels_name_id_dict[obj.label]
                if isinstance(obj,Bbox):
                    new_result_base = deepcopy(coco_result_bbox_base)
                    new_result_base['bbox'] = obj.coco
                elif isinstance(obj,Mask):
                    new_result_base = deepcopy(coco_result_seg_base)
                    new_result_base['segmentation'] = {'size':image.size,
                                                        'counts':obj.rle}
                else:
                    raise Exception('DetectImage 안에 Bbox, Mask가 아닌 다른 클래스의 인스턴스가 들어 있습니다')
                new_result_base['image_id'] = image_id
                new_result_base['category_id'] = category_id
                new_result_base['score'] = obj.confidence
                dt_results.append(new_result_base)
        
        with open(root/'detection_result_COCOeval.json','w',encoding='cp949') as f:
            json.dump(dt_results,f,ensure_ascii=False,indent=4)

    def from_coco(self, coco_json_path):
        coco = COCO(coco_json_path)
        imgs = coco.imgs
        labels = coco.cats

        for img in imgs.values():
            anno_ids = coco.getAnnIds(imgIds=img['id'])
            objs = []
            for ann in coco.loadAnns(anno_ids):
                objs.append(Bbox((img['height'],img['width']),labels[ann['category_id']]['name'],coco_bbox=ann['bbox']).data)
                # objs.append(Mask((img['height'],img['width']),labels[ann['category_id']]['name'],polygons=ann['segmentation']).data)
            dt_img = DetectImage(img['file_name'],(img['height'],img['width']),dt_objects_data=objs)
            self.append(dt_img.data)
        return self

    def to_coco_dataset(self, gt_path='', save_path=''):
        if gt_path:
            self._to_coco_dataset_with_gt(gt_path=gt_path)
        elif save_path:
            self._to_coco_dataset_without_gt(save_path=save_path)
        else:
            self._to_coco_dataset_without_gt(save_path='')

    def _to_coco_dataset_without_gt(self, save_path):
        new_base = deepcopy(coco_base_format)
        root = Path(save_path).parent

        labels_name_id_dict = defaultdict(lambda: len(labels_name_id_dict)+1)
        for label in self._categories:

            new_categories = deepcopy(coco_categories_base)
            new_categories["name"] = label
            new_categories["id"] = labels_name_id_dict[label]

            new_base['categories'].append(new_categories)

        images_name_id_dict = defaultdict(lambda: len(images_name_id_dict)+1)
        for image in self._items:

            new_image = deepcopy(coco_images_base)
            new_image['id'] = images_name_id_dict[image.filename]

            new_image['height'], new_image['width'] = image.size
            new_image['file_name'] = image.filename
            new_base['images'].append(new_image)

            for anno in image.dt:
                new_annotations = deepcopy(coco_annotations_base)
                new_annotations['id'] = len(new_base['annotations'])+1
                new_annotations['image_id'] =images_name_id_dict[image.filename]
                new_annotations['category_id'] = labels_name_id_dict[anno.label]
                if isinstance(anno,Mask):
                    new_annotations['segmentation'] = [anno.polygons]
                elif isinstance(anno, Bbox):
                    new_annotations['bbox'] = anno.coco
                new_annotations['area'] = anno.area_a
                new_base['annotations'].append(new_annotations)
        
        with open(root/'detection_result_coco_format.json','w') as f:
            json.dump(new_base,f,ensure_ascii=False,indent=4)

    def _to_coco_dataset_with_gt(self, gt_path):
        new_base = deepcopy(coco_base_format)
        gt = read_json(gt_path)
        root = Path(gt_path).parent

        gt_labels:list = gt['categories']
        gt_labels_name_id_dict = {}
        for label in gt_labels:
            gt_labels_name_id_dict[label['name']] = label['id']

        gt_images:list = gt['images']
        gt_images_name_id_dict = {}
        for image in gt_images:
            gt_images_name_id_dict[image['file_name']] = image['id']

        labels_name_id_dict = {}
        for label in self._categories:
            gt_label = [label for gt_label in gt_labels_name_id_dict if gt_label.rfind(label) != -1]
            if gt_label:
                gt_label = gt_label[0]
            else:
                continue
            gt_id = gt_labels_name_id_dict[gt_label]

            new_categories = deepcopy(coco_categories_base)
            new_categories["name"] = label
            new_categories["id"] = gt_id
            new_base['categories'].append(new_categories)

            labels_name_id_dict[label] = gt_id

        anno_id = 1
        for image in self._items:
            gt_image_name = [gt_image for gt_image in gt_images_name_id_dict if (gt_image.rfind(image.filename)!=-1) | (image.filename.rfind(gt_image) != -1)]
            if len(gt_image_name)==1:
                gt_image_name = gt_image_name[0]
            elif len(gt_image_name)>1:
                raise Exception('gt와 dt의 이미지 파일명을 매칭하지 못했습니다.')
            else:
                continue
            gt_id = gt_images_name_id_dict[gt_image_name]

            new_image = deepcopy(coco_images_base)
            new_image['id'] = gt_id
            new_image['height'], new_image['width'] = image.size
            new_image['file_name'] = image.filename
            new_base['images'].append(new_image)

            for anno in image.dt:
                new_annotations = deepcopy(coco_annotations_base)
                new_annotations['id'] = anno_id
                new_annotations['image_id'] = gt_id
                new_annotations['category_id'] = labels_name_id_dict[anno.label]
                if isinstance(anno,Mask):
                    new_annotations['segmentation'] = [anno.polygons]
                elif isinstance(anno, Bbox):
                    new_annotations['bbox'] = anno.coco
                new_annotations['area'] = anno.area_a
                new_base['annotations'].append(new_annotations)

                anno_id += 1
        
        with open(root/'detection_result_coco_format.json','w',encoding='utf-8') as f:
            json.dump(new_base,f,ensure_ascii=False,indent=4)

    def to_custom_json(self):
        custom_results = []
        for img in self._items:
            objects = [(('label',obj.label), 
                        ('confidence',obj.confidence), 
                        # (('voc_bbox',obj.voc) if isinstance(obj, Bbox) else ('polygons',obj.polygons)))
                        ('voc_bbox',obj.voc))
                        for obj in img.dt._items]
            objects = [dict(obj) for obj in objects]
            custom_result = {'filename':str(Path(img.filename).as_posix()),
                            'image_size': {'height':img.size[0],
                                            'width': img.size[1]},
                            'objects':objects }
            custom_results.append(custom_result)
        with open('custom_results.json','w') as f:
            json.dump(custom_results,f)


coco_base_format = \
    {"licenses": [
        {"name": "",
        "id": 0,
        "url": "" } ],
    "info": {
        "contributor": "",
        "date_created": "",
        "description": "",
        "url": "",
        "version": "",
        "year": "" },
    "categories": [],
    "images": [],
    "annotations": [] }

coco_categories_base = \
    { "id": 1,
    "name": "Crack",
    "supercategory": "" }

coco_images_base = \
    { "id": 1,
    "width": 1000,
    "height": 600,
    "file_name": "A-1 (1)_균열.png",
    "license": 0,
    "flickr_url": "",
    "coco_url": "",
    "date_captured": 0 }

coco_annotations_base = \
    { "id": 3352,
    "image_id": 997,
    "category_id": 2,
    "segmentation": [ ],
    "area": 262578,
    "bbox":[],
    "iscrowd": 0,
    "attributes": { "occluded": False }
    }

coco_result_bbox_base = \
    {
        "image_id": 42,
        "category_id": 18,
        "bbox": [
            258.15, #x1
            41.29, #y1
            348.26, #w
            243.78 #h
        ],
        "score": 0.236
    }
coco_result_seg_base = \
    {
        "image_id": 196,
        "category_id": 56,
        "segmentation": {
            "size": [
                480, #height
                640 #width
            ],
            "counts": "VQi31m>0O2N100O100O2N.........."
        },
        "score": 0.892
    }

if __name__=="__main__":
    dataset = DetectDataset().from_coco('d:/pano_crop/data/annotations/instances_default.json')
    dataset.to_custom_json()