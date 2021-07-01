from pathlib import Path

import json

with open('./result_train.json','r', encoding='utf-8') as f:
    dt_dataset = json.load(f)

with open('./train.json','r', encoding='cp949') as f:
    gt_dataset = json.load(f)

for img in dt_dataset:
    filename = Path(img['filename']).name
    image_size = [(img['height'],img['width']) for img in gt_dataset['images'] if img['file_name']==filename][0]
    height,width = image_size

    img.update({'image_size':{'width':width,'height':height}})
    [obj.update({'type':'yolo_bbox'}) for obj in img['objects']]

with open('./add_train.json','w') as f:
    json.dump(dt_dataset,f)


