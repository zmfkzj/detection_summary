from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval
from pathlib import Path

from dtsummary.object import DetectDataset
from dtsummary.util import json_to_cp949

import numpy as np
import pandas as pd
import tensorflow as tf


class Evaluation:
    def __init__(self,dt_path, gt_path, type) -> None:
        assert type in ['bbox','segm'], '"type" argument must be one of "bbox" or "segm"'
        self.root = Path(gt_path).parent
        self.dataset = DetectDataset(custom_dt_path=dt_path)
        self.dataset.to_coco_result(Path(gt_path))
        dt_result_path = self.root/'detection_result_COCOeval.json'

        json_to_cp949(gt_path)
        coco = COCO(str(gt_path))
        dt = coco.loadRes(str(dt_result_path))
        self.eval = COCOeval(coco,dt,type)
        self.imgIds = self.eval.params.imgIds
        self.catIds = self.eval.params.catIds

    @staticmethod
    def cal_F1(precision,recall):
        _f1 = (2*precision*recall)/(precision+recall)
        return round(_f1,4) if not np.isnan(_f1) else 0
    
    def cal_recall(self, conf_thresh):
        r = tf.metrics.Recall(thresholds=conf_thresh)
        cats = self.eval.cocoGt.cats
        recalls = -np.ones(len(cats))
        for cat_id in self.eval.params.catIds:
            y_true = []
            y_pred = []
            for img in self.eval.evalImgs:
                if img is None:
                    continue
                if cat_id!=img['category_id']:
                    continue
                if img['aRng']!=[0, 10000000000.0]:
                    continue
                y_true.extend([1 for _ in img['gtMatches'][0,:]])
                _y_pred = [img['dtScores'][img['dtIds'].index(match_id)] if match_id!=0 else 0 for match_id in img['gtMatches'][0,:]]
                y_pred.extend(_y_pred)
            if y_true:
                r.update_state(y_true,y_pred)
                recalls[cat_id-1] = r.result().numpy()
                r.reset_state()
        recall = np.mean([r for r in recalls if r!= -1])
        print(f'{recall=}')
        return recall

    def cal_precision(self, conf_thresh):
        p = tf.metrics.Precision(thresholds=conf_thresh)
        cats = self.eval.cocoGt.cats
        precisions = -np.ones(len(cats))
        for cat_id in self.eval.params.catIds:
            y_pred = []
            y_true = []
            for img in self.eval.evalImgs:
                if img is None:
                    continue
                if cat_id!=img['category_id']:
                    continue
                if img['aRng']!=[0, 10000000000.0]:
                    continue
                y_pred.extend(img['dtScores'])
                _y_true = [1 if match_id!=0 else 0 for match_id in img['dtMatches'][0,:]]
                y_true.extend(_y_true)
            if y_pred:
                p.update_state(y_true,y_pred)
                precisions[cat_id-1] = p.result().numpy()
                p.reset_state()
        precision = np.mean([r for r in precisions if r!= -1])
        print(f'{precision=}')
        return precision

    def run_eval(self, conf_thresh):
        self._eval_images(conf_thresh)
        self._eval_classes(conf_thresh)

    def _eval_classes(self, conf_thresh:float):
        evals_df = pd.DataFrame()
        param_catIds = { self.eval.cocoGt.loadCats(i)[0]['name']:[i] for i in self.catIds }
        param_catIds.update({'all_classes':[]})
        conf_id = int(conf_thresh*100)
        for label_name,param_cat_id in param_catIds.items():
            self.eval.params.imgIds = self.eval.cocoGt.getImgIds(catIds=param_cat_id) if label_name!='all_classes' else self.imgIds
            self.eval.params.catIds = param_cat_id if label_name!='all_classes' else self.catIds
            self.eval.evaluate()
            self.eval.accumulate()
            self.eval.summarize()

            annos = self.eval.cocoGt.loadAnns(self.eval.cocoGt.getAnnIds(catIds=param_cat_id))
            areas = [anno['area'] for anno in annos]
            area_describ_dict = pd.Series(areas).describe().reindex(['count','mean','min','max']).rename({'count':'gt_obj_count', 'mean':'area_mean','min':'area_min','max':'area_max'}).to_dict()
            evals = {
                'class': label_name,
                'gt_img_count': len({ ann['image_id'] for ann in self.eval.cocoGt.loadAnns(self.eval.cocoGt.getAnnIds(imgIds=self.eval.params.imgIds,catIds=param_cat_id))}),
                'dt_img_count': len({ ann['image_id'] for ann in self.eval.cocoDt.loadAnns(self.eval.cocoDt.getAnnIds(imgIds=self.eval.params.imgIds,catIds=param_cat_id)) if ann['score']>=conf_thresh}),
                'gt_obj_count': len(self.eval.cocoGt.loadAnns(self.eval.cocoGt.getAnnIds(imgIds=self.eval.params.imgIds,catIds=param_cat_id))),
                'dt_obj_count': len([ann for ann in self.eval.cocoDt.loadAnns(self.eval.cocoDt.getAnnIds(imgIds=self.eval.params.imgIds,catIds=param_cat_id)) if ann['score']>=conf_thresh]),
                'precision': self.cal_recall(conf_thresh),
                'recall': self.cal_recall(conf_thresh),
                }
            evals.update(area_describ_dict)
            evals.update({
                f'f1_{conf_id}': self.cal_F1(evals['precision'],evals['recall']),
                'mAP50:95':self.eval.stats[0],
                'mAP50': self.eval.stats[1],
                'mAP75': self.eval.stats[2],
                'mAR100': self.eval.stats[8],
                })
            evals_df = evals_df.append(evals,ignore_index=True)

        each_class = evals_df.loc[evals_df['class']!='all_classes']
        all_class = evals_df.loc[evals_df['class']=='all_classes']
        with pd.ExcelWriter(str(self.root/'summary.xlsx'),mode='a') as writer:
            each_class.to_excel(writer,'perClass_each_Class',index=False,float_format='%.4f')
            all_class.to_excel(writer,'perClass_allClass',index=False,float_format='%.4f')

    def _eval_images(self,conf_thresh):
        evals_df = pd.DataFrame()
        param_catIds = { self.eval.cocoGt.loadCats(i)[0]['name']:[i] for i in self.catIds }
        param_catIds.update({'all_classes':[]})
        conf_id = int(conf_thresh*100)
        for label_name,param_cat_id in param_catIds.items():
            cat_img_Ids = self.eval.cocoGt.getImgIds(catIds=param_cat_id) if label_name!='all_classes' else self.imgIds.copy()
            cat_img_Ids.extend(self.eval.cocoDt.getImgIds(catIds=param_cat_id) if label_name!='all_classes' else self.imgIds.copy())
            cat_img_Ids = list(set(cat_img_Ids))
            for img_id in cat_img_Ids:
                self.eval.params.imgIds = [img_id]
                self.eval.params.catIds = param_cat_id if label_name!='all_classes' else self.catIds
                self.eval.evaluate()
                self.eval.accumulate()
                self.eval.summarize()
                evals = {
                    'id':int(img_id),
                    'precision': self.cal_precision(conf_thresh),
                    'recall': self.cal_recall(conf_thresh),
                    'class': label_name,
                    'gt_obj_count': len(self.eval.cocoGt.loadAnns(self.eval.cocoGt.getAnnIds(imgIds=self.eval.params.imgIds,catIds=param_cat_id))),
                    'dt_obj_count': len([ann for ann in self.eval.cocoDt.loadAnns(self.eval.cocoDt.getAnnIds(imgIds=self.eval.params.imgIds,catIds=param_cat_id)) if ann['score']>=conf_thresh]),
                    }

                evals.update({
                    f'f1_{conf_id}': self.cal_F1(evals['precision'],evals['recall']),
                    'mAP50:95':self.eval.stats[0],
                    'mAP50': self.eval.stats[1],
                    'mAP75': self.eval.stats[2],
                    'mAR100': self.eval.stats[8],
                    })
                evals_df = evals_df.append(evals,ignore_index=True)
            
        images = pd.DataFrame(self.eval.cocoGt.loadImgs(self.imgIds))
        result_per_img = pd.merge(evals_df,images,how='left')
        result_per_img = result_per_img.drop(columns=['id','license','flickr_url','coco_url','date_captured'])
        each_class = result_per_img.loc[result_per_img['class']!='all_classes']
        all_class = result_per_img.loc[result_per_img['class']=='all_classes']
        with pd.ExcelWriter(str(self.root/'summary.xlsx')) as writer:
            each_class.to_excel(writer,'perImg_eachClass',index=False,float_format='%.4f')
            all_class.to_excel(writer,'perImg_allClass',index=False,float_format='%.4f')

if __name__=='__main__':
    asdf = Evaluation('add_train.json','train.json','bbox')
    asdf.run_eval(0.25)