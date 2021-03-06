import os
import sys
from client.mifid_demo import MIFID
from glob import glob
import numpy as np
import cv2
from PIL import Image
from tqdm import tqdm_notebook
import shutil
import argparse

def evaluation(submission_file):
    import zipfile
    
    # remove output directory
    if not os.path.isdir(submission_file):
        if os.path.exists('tmp'):
            print("Remove temp folder")
            shutil.rmtree('tmp')

        os.mkdir('tmp')

        with zipfile.ZipFile(submission_file, 'r') as zip_ref:
            zip_ref.extractall('tmp')
        img_paths = glob('tmp/*.*')
    else:
        img_paths= glob(submission_file)
        img_paths = [os.path.join(submission_file, f) for f in img_paths]

    mifid = MIFID(
        model_path='./client/motorbike_classification_inception_net_128_v4_e36.pb',
        public_feature_path='./client/public_feature.npz')
    
    img_np = np.empty((len(img_paths), 128, 128, 3), dtype=np.uint8)
    for idx, path in tqdm_notebook(enumerate(img_paths), total=len(img_paths)):
        img_arr = cv2.imread(path)
        img_arr = cv2.resize(img_arr, (128, 128), cv2.INTER_BITS)
        img_arr = img_arr[..., ::-1]
        img_arr = np.array(img_arr)
        img_np[idx] = img_arr
        
    score = mifid.compute_mifid(img_np)
    return score

if __name__ == '__main__':
    pass