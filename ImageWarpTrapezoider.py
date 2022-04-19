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

# 
# 2022/04/20 copyright (c) antillia.com
#
# ImageWarpTrapezoider.py
# This is a very simple, primitive trapezoider to convert a rectangle area of an image to a trapezoid.
#

import os
import sys
import uuid
import glob
import numpy as np
import cv2
import traceback

class ImageWarpTrapezoider:

  def __init__(self, use_uuid=True, base_index=10000):
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


  def trapezoid(self, input_dir, output_dir, ws_list, hs_list):
    if ws_list == None or len(ws_list)==0:
      raise Exception("Invalid ws_list")
    if hs_list == None or len(hs_list)==0:
      raise Exception("Invalid hs_list")

    #
    input_files, type = self.getImageFiles(input_dir)
  
    if len(input_files) == 0:
      msg = "Sorry, not found image files in:" + input_dir
      raise Exception(msg)

    for n, input_file in enumerate(input_files):
      image  = None
      h      = 0
      w      = 0
      if type == self.PNG:
        image   = cv2.imread(input_file, cv2.IMREAD_UNCHANGED)
        h, w, _ = image.shape
      elif type == self.JPG:
        image   = cv2.imread(input_file, cv2.IMREAD_COLOR)
        h, w,   = image.shape
      rectangle = [(0, 0), (w, 0),(w, h), (0, h)]

      trapezoids  = [] 
      for hs in hs_list:
        for ws in ws_list:
          trapezoid1 = [(0,    hs*2), (w,      0), (w-ws*2, h), (0+ws*2,h-hs*2)]
          trapezoid2 = [(ws*2, 0), (w-2*ws, hs*2), (w,      h-hs*2), (0,     h)]
          trapezoids.append(trapezoid1)
          trapezoids.append(trapezoid2)
      print("---- len trapezoids {}".format(len(trapezoids)))
      for i,trapezoid in enumerate(trapezoids):
        warped   = self.trapezoid_one(image, rectangle, trapezoid)
        basename = os.path.basename(input_file)
        name     = basename
        pos      = basename.find(type)
        if pos>0:
          name = basename[0:pos]

        id = str(self.BASE_INDEX + n + i)
        if self.use_uuid:
          id = str(uuid.uuid4())
        output_filepath = os.path.join(output_dir, name + "___" + id + type)

        cv2.imwrite(output_filepath, warped)
        print("=== saved {}".format(output_filepath)) 
        

  def trapezoid_one(self, image, rectangle, trapezoid):
    rectangle   =  np.float32(rectangle)

    W_MAX     = max(trapezoid, key = lambda x:x[0])[0]
    H_MAX     = max(trapezoid, key = lambda x:x[1])[1]
    trapezoid =  np.float32(trapezoid)
    
    MATRIX = cv2.getPerspectiveTransform(rectangle, trapezoid)
    warped = cv2.warpPerspective(image, MATRIX, (W_MAX, H_MAX))
    return warped


# python ImageWarpTrapezoider.py input_dir mode output_dir
# 
# python ImageWarpTrapezoider.py ./sample_images train ./sample_images_train_trapezoided

if __name__ == "__main__":
  input_file = ""
  input_dir  = ""
  mode       = "train"
  train      = False
  test       = False
  try:
    if len(sys.argv) == 4:
      input_dir  = sys.argv[1]
      mode       = sys.argv[2]
      output_dir = sys.argv[3]
    else:
      raise Exception("Usage:python ImageWarper.py input_dir mode output_dir")
    if mode not in ["train","valid", "test"]:
      raise Exception("Invalid parameter: mode should be train or valid ")
    if mode == "train":
      train = True
    elif mode == "test":
      test  = True
    if not os.path.exists(input_dir):
      msg = "Not found input_dir:" + input_dir
      raise Exception(msg)

    if not os.path.exists(output_dir):
      os.makedirs(output_dir)

    #train==False
    #Shifting pixels in width and heigt to make a trapezoid from a rectangle
    #default valid
    ws_list = [0,2,4]
    hs_list = [0,2,4]
    index = 10000
    if train ==True:
      #ws_list = [0,1,2,3,5]
      #hs_list = [0,1,2,3,5]
      ws_list = [0,1,2,3,4]
      hs_list = [0,1,2,3,4]
      ws_list = [0,1,2,3]
      hs_list = [0,1,2,3]

      index = 20000
    if test  == True:
      index   = 30000
      ws_hist = []
      hs_list = [0,2]

    trapezoider = ImageWarpTrapezoider(use_uuid=True, base_index=index)

    trapezoider.trapezoid(input_dir, output_dir, ws_list, hs_list)
        

  except:
    traceback.print_exc()
