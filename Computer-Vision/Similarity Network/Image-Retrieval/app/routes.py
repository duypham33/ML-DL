# Important imports
from app import app
from flask import request, render_template, url_for, make_response, jsonify, redirect
import os
from werkzeug.utils import secure_filename 
from app import utils

#Adding path to config
app.config['INITIAL_FILE_UPLOADS'] = 'app/static/uploads'


feature_extract_model = None
trained_model = None
data_features_load = None
data_features_load2 = None

utils.load_weights_models(feature_extract_model)
utils.load_feature_extraction(data_features_load, data_features_load2)

# Route to home page
@app.route("/", methods=["GET", "POST"])
def index():
	return render_template('index.html', k = range(10), l = range(6))


@app.route("/label", methods=["POST"])
def get_label():
	file = request.files['file']
	filename = secure_filename(file.filename)

	path = os.path.join(app.config['INITIAL_FILE_UPLOADS'], filename)
	file.save(path)

	img_paths, popular_text_label, text_label = utils.search_img(feature_extract_model, trained_model, 
							data_features_load, data_features_load2, path, num_imgs = 60)

	predict = f'Popular: {popular_text_label}, Model predicted: {text_label}'
	return jsonify({'predict': predict, 'img_paths': img_paths})



# Main function
if __name__ == '__main__':
    app.run(debug=True)