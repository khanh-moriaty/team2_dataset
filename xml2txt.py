import os
import argparse
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser(description='This script support converting voc format with 14 classes to yolo txt format with 5 classes')
parser.add_argument('--ann_dir', type=str, default=None,
                    help='path to annotation files directory.')
parser.add_argument('--out_dir', type=str, default=None,
                    help='path to output directory.')
args = parser.parse_args()

def convertXmlTxt(ann_dir, out_dir):
    dir = os.listdir(ann_dir)
    dir = [fi for fi in dir if os.path.splitext(fi)[1] == '.xml']
    dir.sort()
    print("Found", len(dir), "files")
    
    os.makedirs(out_dir, exist_ok=True)
    
    with open('classes_0-13.txt', 'r') as f:
        classes = f.read().splitlines()
    with open('classes_mapping.txt', 'r') as f:
        classes_mapping = f.read().splitlines()
        
    new_class = dict(zip(classes, classes_mapping))
    
    for fi in dir:
        bfn, _ = os.path.splitext(fi)
        ann_path = os.path.join(ann_dir, fi)
        ann_tree = ET.parse(ann_path)
        ann_root = ann_tree.getroot()
        
        obj_list = ann_root.findall('object')
        width = int(ann_root.find('size').find('width').text)
        height = int(ann_root.find('size').find('height').text)
        
        out_path = os.path.join(out_dir, bfn+'.txt')
        fo = open(out_path, 'w')
        
        for obj in obj_list:
            name = new_class[obj.find('name').text]
            if name == '-1': continue
            bbox = obj.find('bndbox')
            xmin = int(bbox.find('xmin').text)
            xmax = int(bbox.find('xmax').text)
            ymin = int(bbox.find('ymin').text)
            ymax = int(bbox.find('ymax').text)
            x = (xmax + xmin) / width / 2
            y = (xmax + ymin) / height / 2
            w = (xmax - xmin + 1) / width
            h = (ymax - ymin + 1) / height
            line = [name, x, y, w, h]
            line = [str(x) for x in line]
            line = ' '.join(line) + '\n'
            fo.write(line)
        
        fo.flush()
        fo.close()

if __name__ == "__main__":
    convertXmlTxt(args.ann_dir, args.out_dir)