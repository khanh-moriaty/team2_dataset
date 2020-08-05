import os
import argparse
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser(description='This script support converting voc format with 14 classes to 5 classes')
parser.add_argument('--ann_dir', type=str, default=None,
                    help='path to annotation files directory.')
parser.add_argument('--out_dir', type=str, default=None,
                    help='path to output directory.')
args = parser.parse_args()

ann_dir = args.ann_dir
dir = os.listdir(ann_dir)
dir.sort()

with open('classes_0-13.txt', 'r') as f:
        labels_str = f.read().splitlines()
labels_ids = [0, 1, 1, -1, -1, 2, 2, 2, 3, 3, 3, 4, 4, 4]
new_class = dict(zip(labels_str, labels_ids))

os.makedirs(args.out_dir)

for fi in dir:
    ann_path = os.path.join(ann_dir, fi)
    ann_tree = ET.parse(ann_path)
    ann_root = ann_tree.getroot()
    ann_obj = ann_root.findall('object')
    for obj in ann_obj:
        name = obj.findall('name')[0]
        name.text = str(new_class[name.text])
        if name.text == "-1": ann_root.remove(obj)
    ann_tree.write(os.path.join(args.out_dir, fi))
