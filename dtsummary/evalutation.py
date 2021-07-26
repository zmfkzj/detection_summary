from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval
from pathlib import Path
from dtsummary.object import DetectDataset
from collections import defaultdict

import chardet
import json
import numpy as np
import pandas as pd
import os.path as osp


class Evaluation:
    def __init__(self,dt_path, gt_path, type) -> None:
        assert type in ['bbox','segm'], '"type" argument must be one of "bbox" or "segm"'
        self.dataset = DetectDataset(dt_path=dt_path)
        gt_path = Path(gt_path)
        self.re_encoding(gt_path)
        gt_path = gt_path.parent/f'{gt_path.name}'
        self.dataset.to_coco_result(gt_path)
        dt_result_path = Path('detection_result_COCOeval.json')

        coco = COCO(str(gt_path))
        dt = coco.loadRes(str(dt_result_path))
        self.eval = COCOeval(coco,dt,type)
        self.imgIds = self.eval.params.imgIds
        self.catIds = self.eval.params.catIds

    @staticmethod
    def re_encoding(json_file:Path):
        with open(json_file, 'rb') as f:
            result = f.read()
        encoding = chardet.detect(result)['encoding']

        with open(json_file, 'r',encoding=encoding) as f:
            result = json.load(f)

        with open(json_file.parent/f'{json_file.name}', 'w') as f:
            json.dump(result,f)
    
    @staticmethod
    def cal_F1(precision,recall):
        _f1 = (2*precision*recall)/(precision+recall)
        return round(_f1,4) if not np.isnan(_f1) else 0

    def run_eval(self, conf_thresh):
        self._eval_images(conf_thresh)
        self._eval_classes(conf_thresh)

    def _eval_classes(self, conf_thresh:float):
        evals_df = pd.DataFrame()
        param_catIds = { self.eval.cocoGt.loadCats(i)[0]['name']:[i] for i in self.catIds }
        param_catIds.update({'all_classes':self.catIds})
        for label_name,param_cat_id in param_catIds.items():
            self.eval.params.imgIds = self.eval.cocoGt.getImgIds(catIds=param_cat_id) if label_name!='all_classes' else self.imgIds
            self.eval.params.catIds = param_cat_id
            self.eval.evaluate()
            self.eval.accumulate()
            self.eval.summarize()

            annos = self.eval.cocoGt.loadAnns(self.eval.cocoGt.getAnnIds(catIds=param_cat_id))
            areas = [anno['area'] for anno in annos]
            area_describ_dict = pd.Series(areas).describe().reindex(['count','mean','min','max']).rename({'count':'gt_obj_count', 'mean':'area_mean','min':'area_min','max':'area_max'}).to_dict()
            evals = {
                'class': label_name,
                'gt_img_count': len(self.eval.params.imgIds),
                'precision': np.round(np.mean([p for p in self.eval.eval['precision'][0,int(conf_thresh*100),:,0,2] if p != -1]),4),
                'recall': np.round(np.mean([r for r in self.eval.eval['recall'][0,:,0,2] if r!=-1]),4),
                }
            evals.update(area_describ_dict)
            evals.update({
                'f1': self.cal_F1(evals['precision'],evals['recall']),
                'mAP50:95':self.eval.stats[0],
                'mAP50': self.eval.stats[1],
                'mAP75': self.eval.stats[2],
                'mAR100': self.eval.stats[8],
                })
            evals_df = evals_df.append(evals,ignore_index=True)

        result_per_img = evals_df.reindex(columns=['precision','recall','f1','mAP50:95','mAP50','mAP75','mAR100','width','height','gt_img_count','class','gt_obj_count','area_mean','area_min','area_max'])
        each_class = result_per_img.loc[result_per_img['class']!='all_classes']
        all_class = result_per_img.loc[result_per_img['class']=='all_classes']
        with pd.ExcelWriter('summary.xlsx',mode='a') as writer:
            each_class.to_excel(writer,'perClass_each_Class',index=False,float_format='%.4f')
            all_class.to_excel(writer,'perClass_allClass',index=False,float_format='%.4f')

    def _eval_images(self,conf_thresh):
        evals_df = pd.DataFrame()
        param_catIds = { self.eval.cocoGt.loadCats(i)[0]['name']:[i] for i in self.catIds }
        param_catIds.update({'all_classes':self.catIds})
        for label_name,param_cat_id in param_catIds.items():
            cat_img_Ids = self.eval.cocoGt.getImgIds(catIds=param_cat_id) if label_name!='all_classes' else self.imgIds
            for img_id in cat_img_Ids:
                self.eval.params.imgIds = [img_id]
                self.eval.params.catIds = param_cat_id
                self.eval.evaluate()
                self.eval.accumulate()
                self.eval.summarize()
                evals = {
                    'id':img_id,
                    'precision': np.round(np.mean([p for p in self.eval.eval['precision'][0,int(conf_thresh*100),:,0,2] if p != -1]),4),
                    'recall': np.round(np.mean([r for r in self.eval.eval['recall'][0,:,0,2] if r!=-1]),4),
                    'class': label_name
                    }

                evals.update({
                    'f1': self.cal_F1(evals['precision'],evals['recall']),
                    'mAP50:95':self.eval.stats[0],
                    'mAP50': self.eval.stats[1],
                    'mAP75': self.eval.stats[2],
                    'mAR100': self.eval.stats[8],
                    })
                evals_df = evals_df.append(evals,ignore_index=True)
            
        images = pd.DataFrame(self.eval.cocoGt.loadImgs(self.imgIds))
        result_per_img = pd.merge(evals_df,images,how='outer')
        result_per_img = result_per_img.reindex(columns=['id','precision','recall','f1','mAP50:95','mAP50','mAP75','mAR100','width','height','file_name','class'])
        each_class = result_per_img.loc[result_per_img['class']!='all_classes']
        all_class = result_per_img.loc[result_per_img['class']=='all_classes']
        with pd.ExcelWriter('summary.xlsx') as writer:
            each_class.to_excel(writer,'perImg_eachClass',index=False,float_format='%.4f')
            all_class.to_excel(writer,'perImg_allClass',index=False,float_format='%.4f')

if __name__=='__main__':
    asdf = Evaluation('add_train.json','train.json','bbox')
    asdf.run_eval(0.25)