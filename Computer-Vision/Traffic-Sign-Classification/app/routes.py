# Important imports
import json
from app import app
from flask import request, render_template, url_for, make_response, jsonify, redirect
import numpy as np
import tensorflow as tf
from PIL import Image
import string
import random
import os
from werkzeug.utils import secure_filename 

#Adding path to config
app.config['INITIAL_FILE_UPLOADS'] = 'app/static/uploads'

# Loading model
model = tf.keras.models.load_model('app/static/model/trafficsign_classification_model.h5')

labels_ordered_in_dir = [0,1,10,11,12,13,14,15,16,17,18,19,2,20,21,22,23,24,25,
                         26,27,28,29,3,30,31,32,33,34,35,36,37,38,39,4,40,41,42,
                         5,6,7,8,9]

# Storing all lables
all_lables = ['Speed limit (20km/h)','Speed limit (30km/h)','Speed limit (50km/h)','Speed limit (60km/h)',
              'Speed limit (70km/h)','Speed limit (80km/h)','End of speed limit (80km/h)','Speed limit (100km/h)',
              'Speed limit (120km/h)','No passing','No passing for vechiles over 3.5 metric tons',
              'Right-of-way at the next intersection','Priority road','Yield','Stop','No vechiles',
              'Vechiles over 3.5 metric tons prohibited','No entry','General caution','Dangerous curve to the left',
              'Dangerous curve to the right','Double curve','Bumpy road','Slippery road','Road narrows on the right',
              'Road work','Traffic signals','Pedestrians','Children crossing','Bicycles crossing','Beware of ice/snow',
              'Wild animals crossing','End of all speed and passing limits','Turn right ahead','Turn left ahead',
              'Ahead only','Go straight or right','Go straight or left','Keep right','Keep left','Roundabout mandatory',
              'End of no passing','End of no passing by vechiles over 3.5 metric']

# Route to home page
@app.route("/", methods=["GET", "POST"])
def index():
	return render_template('index.html')


@app.route("/label", methods=["POST"])
def get_label():
	file = request.files['file']
	filename = secure_filename(file.filename)

	path = os.path.join(app.config['INITIAL_FILE_UPLOADS'], filename)
	file.save(path)

	img = Image.open(path)
	img = np.array(img)

	if img.shape[-1] == 3:
		img = tf.image.resize(img, (50, 50))
	else:
		img = tf.image.resize(img[:,:,:3], (50, 50))
	img = tf.expand_dims(img, axis=0)

	y = model.predict(img)
	label = np.argmax(y, axis = 1)
	label = labels_ordered_in_dir[int(label)]
	text_label = all_lables[label]
	print(text_label)

	#return make_response(jsonify({'text_label': text_label}), 200)
	return jsonify({'text_label': text_label})


# Main function
if __name__ == '__main__':
    app.run(debug=True)
