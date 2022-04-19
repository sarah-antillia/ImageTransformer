# Copyright 2022 antillia.com Toshiyuki Arai
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# ImageWarpRotator.py
# 2022/04/20 

import os
import sys
import uuid
import cv2
import glob
import traceback
import numpy as np
from PIL import Image, ImageDraw

class ImageWarpRotator:

  def __init__(self, use_uuid=True, base_index=30000):
    self.PNG = ".png"
    self.JPG = ".jpg"
    self.use_uuid   = use_uuid
    self.BASE_INDEX = base_index

  def getImageFiles(self, input_dir):
    #
    input_files = glob.glob(input_dir + "./*" + self.PNG)
    if len(input_files) > 0:
      return (input_files, self.PNG)
    else:
      input_files = glob.glob(input_dir + "./*" + self.JPG)
      return (input_files, self.JPG)

  def rotate(self, input_dir, angles, output_dir) :
    (files, type) = self.getImageFiles(input_dir)

    print(" ---- angles {}".format(angles))

    for file in files:
      print("Processing file {}".format(file))
      fname = os.path.basename(file)
      pos   = fname.find(type)
      name  = fname
      if (pos>0):
          name = fname[0:pos]
      for i, angle in enumerate(angles):
        print("--- i {}".format(i))
        n = index + i 


        id = str(self.BASE_INDEX + n + i)
        if self.use_uuid:
          id = str(uuid.uuid4())
        output_filepath = os.path.join(output_dir, name + "___" + id + type)
        transformed = self.rotate_one(file, type, angle)

        cv2.imwrite(output_filepath, transformed)
        print("--- Saved rotated image {}".format(output_filepath))

  def rotate_one(self, imagefile, type, angle):
    print("------------rotate_one {} ".format(imagefile))
    image = None
    h     = 0
    w     = 0
    if type == self.PNG:
      image   = cv2.imread(imagefile, cv2.IMREAD_UNCHANGED)
      h, w, _ = image.shape
    elif type == self.JPG:
      image   = cv2.imread(imagefile, cv2.IMREAD_COLOR)
      h, w,   = image.shape

    (cX, cY) = (w // 2, h // 2)
    MATRIX = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(MATRIX[0, 0])
    sin = np.abs(MATRIX[0, 1])

    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    MATRIX[0, 2] += (nW / 2) - cX
    MATRIX[1, 2] += (nH / 2) - cY

    transformed = cv2.warpAffine(image, MATRIX, (nW, nH))
    return transformed

 
# python ImageWarpRotator.py input_dir mode output_dir

# python ImageWarpRotator.py ./sample_images train ./sample_images_train_rotated

if __name__ == "__main__":

  train = False

  try:
    train = False

    if len(sys.argv) == 4:
      input_dir  = sys.argv[1]
      mode       = sys.argv[2]
      output_dir = sys.argv[3]
      if not os.path.exists(input_dir):
        msg = "Not found input_dir " + input_dir
        raise Exception(msg) 
      if not os.path.exists(output_dir):
        os.makedirs(output_dir)
       
      if mode=="train":
        train= True
      if mode not in ["train", "valid"]:
        raise Exception("Invalid argument " + mode)

    angles = []
    index   = 0
    if train :
      index = 70000
      angles = [-4, -3, -2, -1, 1, 2, 3, 4] 
    else:
      index = 80000
      angles  = [-2, -1, 0, 1, 2, ] 

    rotator = ImageWarpRotator(use_uuid=True, base_index=index)
    
    rotator.rotate(input_dir, angles, output_dir)

  except:
    traceback.print_exc()