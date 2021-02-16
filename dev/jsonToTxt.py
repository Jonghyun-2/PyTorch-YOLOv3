import json
import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import glob 
import argparse
from tqdm import tqdm


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--json_dir", type=str, default=None, help="json file dir")
    parser.add_argument("--label_dir", type=str, default=None, help="label dir")

    opt = parser.parse_args()
    anno_paths = glob.glob(opt.json_dir + os.sep + "*.json")

    for idx, anno_path in tqdm(enumerate(anno_paths)):
        objs = []
        norm_list = []
        filename = ""
        cls_ = 0
        # read json
        with open(anno_path, "r") as json_data:
            filename = anno_path.split(os.sep)[-1]
            
            datas = json.load(json_data)
            w = datas["width"]
            h = datas["height"]
            objs = datas["objects"]
            for obj in objs:
                xmin = obj["bbox"]["xmin"]
                ymin = obj["bbox"]["ymin"]
                xmax = obj["bbox"]["xmax"]
                ymax = obj["bbox"]["ymax"]
                
                center_x = (xmax + xmin) / 2 
                center_y = (ymax + ymin) / 2 
                
                bbox_width = abs(xmax - xmin)
                bbox_height = abs(ymax - ymin)
                
                norm_width = bbox_width / w
                norm_height = bbox_height / h
                
                norm_center_x = center_x / w
                norm_center_y = center_y / h
                norm_list.append([cls_, norm_center_x, norm_center_y, norm_width, norm_height])
                
        # write txt
        filename_txt = filename.replace("json", "txt")
        txt_dst = opt.label_dir + os.sep + filename_txt
        
        f = open(txt_dst , 'w')
        for c, x, y, w, h in norm_list:
            data = "{} {} {} {} {}\n".format(c,x,y,w,h)
            f.write(data)
        f.close()
        if idx > 10:
            break