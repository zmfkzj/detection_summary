import json

with open('./result_train.json','r') as f:
    dataset = json.load(f)

[img.update({'image_size':{'width':1600,'height':1000}}) for img in dataset]
for img in dataset:
    [obj.update({'type':'yolo_bbox'}) for obj in img['objects']]

with open('./add_train.json','w') as f:
    json.dump(dataset,f)


