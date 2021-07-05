from dtsummary.object import DetectDataset

if __name__=="__main__":
    dataset = DetectDataset(dt_path='add_train.json')
    dataset.to_coco_result('train.json','bbox')