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

# ImageColorEnhancer.py
# 2022/04/20
# antillia.com

import os
import sys
import uuid
import traceback
import glob
from PIL import Image
import random

 
class ImageColorEnhancer:
  def __init__(self, use_uuid=True, base_index=10000):
    self.PNG = ".png"
    self.JPG = ".jpg"
    self.PARAMETERS = [0.82, 0.86, 0.90, 0.94, 0.98, 1.02, 1.06, 1.10, 1.14, 1.18 ]
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
          
  def enhance(self, input_dir, output_dir, max_enhancer, train):
    (files, type) = self.getImageFiles(input_dir)
    if len(files) == 0:
      raise Exception("No found image files in {}".format(input_dir))
    for n, file in enumerate(files):
      fname = os.path.basename(file)
      name  = fname
      pos   = fname.find(type)

      if pos>-1:
        name = fname[0:pos]
    
      for i in range(max_enhancer):   
        r_image = self.enhance_one(type, file)
        if r_image == None:
          raise Exception("Failed to enhace " + file)
        id = str(self.BASE_INDEX + n + i)
        if self.use_uuid:
          id = str(uuid.uuid4())
        output_filepath = os.path.join(output_dir, name + "___" + id + type)

        r_image.save(output_filepath)
        print("=== Saved {}".format(output_filepath))
 

  def enhance_one(self, type, filename):
    image = None
    if type == self.PNG:
      image = Image.open(filename).convert("RGBA")
    if type == self.JPG:
      image = Image.open(filename).convert("RGB")
    [xr, xg, xb] = random.sample(self.PARAMETERS, 3)
    r_image = None 
    split = image.split()
    if len(split) == 4:
      (r, g, b, a) = split
      r = r.point(lambda i: i * xr)
      g = g.point(lambda i: i * xg)
      b = b.point(lambda i: i * xb)
      r_image = Image.merge('RGBA',(r,g,b,a))

    elif len(split) == 3:
      (r, g, b)   = split
      r = r.point(lambda i: i * xr)
      g = g.point(lambda i: i * xg)
      b = b.point(lambda i: i * xb)
      r_image =  Image.merge('RGB', (r,g, b  ))
    else:
      r_image = None
    return r_image

# python ImageColorEnhancer.py images_dir mode output_dir max
# python ImageColorEnhancer.py ./sample_images train ./sample_images_train_color_enhanced 5

if __name__ == "__main__":
  train       = False
  images_dir  = ""
  output_dir  = ""
  num         = 5
  MAX_ENHANCE = 10
  index       = 40000
  try:
    if len(sys.argv) == 5:
      images_dir    = sys.argv[1]
      mode          = sys.argv[2]
      output_dir    = sys.argv[3]
      max_enhancer  = int(sys.argv[4])
    else:
      raise Exception("Usage: python ImageColorEnhander.py images_dir output_dir max")
    if mode == "train":
      train = True
      index = 50000
    if num <1 or num>MAX_ENHANCE:
      raise Exception("Invalid num paramter") 
    if not os.path.exists(images_dir):
      raise Exception("Not found {}".format(images_dir))

    os.makedirs(output_dir, exist_ok=True)
  
    enhancer = ImageColorEnhancer(use_uuid=True, base_index=index)
    enhancer.enhance(images_dir, output_dir, max_enhancer, train)

  except:
    traceback.print_exc()
 