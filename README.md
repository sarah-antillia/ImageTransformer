<h1> ImageTransformer</h1>
This is a set of simple ImageTranformers.<br> 
The sample images have been taken from <a href="https://en.wikipedia.org/wiki/Road_signs_in_the_United_States">Road signs in the United States</a><br>
<h2>1 ImageColorEnhancer</h2>

Usage:<br>
python <a href="./ImageColorEnhancer.py">ImageColorEnhancer.py</a> images_dir mode output_dir max<br>

Example<br>
<pre>
python ImageColorEnhancer.py ./sample_images train ./sample_images_train_color_enhanced 5
</pre>
<br>
<a href="./sample_images_train_color_enhanced">Color Enhanced</a>
<br>
<br>
<img src="./asset/color_enhanced.png" width="720" height="auto"><br>

<h2>2 ImageWarpRotator</h2>

Usage:<br>
python <a href="./ImageWarpRotator.py">ImageWarpRotator.py</a> images_dir mode output_dir<br>

Example<br>
<pre>
python ImageWarpRotator.py ./sample_images train ./sample_images_train_rotated

</pre>
<br>
<a href="./sample_images_train_rotated">Rotated</a>
<br>
<br>
<img src="./asset/rotated.png"  width="720" height="auto"><br>


<h2>3 ImageWarpTrapezoider</h2>

Usage:<br>
python <a href="./ImageWarpTrapezoider.py">ImageWarpTrapezoider.py</a> images_dir mode output_dir<br>

Example<br>
<pre>
python ImageWarpTrapezoider.py ./sample_images train ./sample_images_train_trapezoided
</pre>
<br>
<a href="sample_images_train_trapezoided">Trapezoided</a>
<br>
<br>
<img src="./asset/trapezoided.png"  width="720" height="auto"><br>


