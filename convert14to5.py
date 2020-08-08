import os
import argparse
import xml.etree.ElementTree as ET

# If a bbox's edge is not wider than THRESHOLD, the bbox will be eliminated
THRESHOLD = 5 

parser = argparse.ArgumentParser(description='This script support converting voc format with 14 classes to 5 classes')
parser.add_argument('--ann_dir', type=str, default=None,
                    help='path to annotation files directory.')
parser.add_argument('--out_dir', type=str, default=None,
                    help='path to output directory.')
args = parser.parse_args()

ann_dir = args.ann_dir
dir = os.listdir(ann_dir)
dir.sort()
print(ann_dir, len(dir))

with open('classes_0-13.txt', 'r') as f:
        labels_str = f.read().splitlines()
labels_ids = [0, 1, 1, -1, -1, 2, 2, 2, 3, 3, 3, 4, 4, 4,
              # Prepare for the unexpected :)
             -1, 2, 3, 3, 4]
new_class = dict(zip(labels_str, labels_ids))

os.makedirs(args.out_dir, exist_ok=True)

cnt = 0
for fi in dir:
    ann_path = os.path.join(ann_dir, fi)
    ann_tree = ET.parse(ann_path)
    ann_root = ann_tree.getroot()
    ann_obj = ann_root.findall('object')
    for obj in ann_obj:
        name = obj.findall('name')[0]
        bbox = obj.findall('bndbox')[0]
        xmin = int(bbox.findall('xmin')[0].text)
        xmax = int(bbox.findall('xmax')[0].text)
        ymin = int(bbox.findall('ymin')[0].text)
        ymax = int(bbox.findall('ymax')[0].text)
        if xmax-xmin < THRESHOLD:
            ann_root.remove(obj)
            continue
        if ymax-ymin < THRESHOLD:
            ann_root.remove(obj)
            continue
        name.text = str(new_class[name.text])
        if name.text == "-1": ann_root.remove(obj)
    ann_tree.write(os.path.join(args.out_dir, fi))
    cnt += 1
    
print(cnt, end='')
