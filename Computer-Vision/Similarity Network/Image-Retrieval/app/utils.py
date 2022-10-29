
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing import image as kimage
from tensorflow.keras.applications.vgg16 import preprocess_input
from collections import OrderedDict
import os

img_height = img_width = 160
text_labels = pd.read_csv('app/static/csv_data/Text_Labels.csv', usecols = ['Text_Label'])
img_paths = pd.read_csv('app/static/csv_data/ImgPaths.csv', usecols = ['ImgPath'])

# VGG16_feature_extraction = tf.keras.applications.VGG16(include_top=False, 
#                                     weights='imagenet', 
#                                     input_shape=(86, 128, 3))

def load_weights_models(feature_extract_model):
    data_augmentation = tf.keras.Sequential([
    tf.keras.layers.experimental.preprocessing.RandomFlip('horizontal'),
    tf.keras.layers.experimental.preprocessing.RandomRotation(0.2),
    ])

    preprocess_input = tf.keras.applications.vgg16.preprocess_input

    base_model = tf.keras.applications.VGG16(input_shape=(img_height,img_width,3),
                                                include_top=False,
                                                weights='imagenet')
    global_average_layer = tf.keras.layers.GlobalAveragePooling2D()

    # Load feature extraction weights
    inputs = tf.keras.Input(shape=(img_height,img_width,3))
    x = data_augmentation(inputs)
    x = preprocess_input(x)
    outputs = base_model(x)

    feature_extract_model = tf.keras.Model(inputs, outputs)
    feature_extract_model.compile(tf.keras.optimizers.Adam(learning_rate=1e-4),
                loss=tf.keras.losses.SparseCategoricalCrossentropy(), 
                metrics=['accuracy'])

    feature_extract_model.load_weights("app/static/model/feature_extraction_weights.h5")

    # Load trained Model weights
    inputs = tf.keras.Input(shape=(img_height,img_width,3))
    x = data_augmentation(inputs)
    x = preprocess_input(x)
    x = base_model(x)
    x = global_average_layer(x)
    x = tf.keras.layers.Dropout(0.25)(x)
    x = tf.keras.layers.Dense(units=512, activation='relu')(x)
    x = tf.keras.layers.Dense(units=256, activation='relu')(x)
    outputs = tf.keras.layers.Dense(units=134, activation='softmax')(x)

    trained_model = tf.keras.Model(inputs, outputs)

    trained_model.load_weights('app/static/model/model_imagerv.h5')
    trained_model.compile(tf.keras.optimizers.Adam(learning_rate=1e-4),
                loss=tf.keras.losses.SparseCategoricalCrossentropy(), 
                metrics=['accuracy'])



def load_feature_extraction(data_features_load, data_features_load2):
    data_features_load = np.load("app/static/data_features/data_features_train.npy", allow_pickle=True)
    data_features_load2 = np.load("app/static/data_features/VGG16_data_features.npy", allow_pickle=True)

    

def getKey(item):
    return item[0]

def reformat_text(text_label):
  return (' ').join(map(lambda x: x.capitalize() , text_label.split('_')))

def get_sims1(feature_extract_model, trained_model, data_features_load, query_np, num_imgs):
  query_np1 = tf.image.resize(query_np, (img_height, img_width))
  query_np1 = np.expand_dims(query_np1, axis=0)
  query_feature1 = feature_extract_model.predict(query_np1)
  query_feature1 = np.reshape(query_feature1, (1,-1))

  y_pred = trained_model.predict(query_np1)
  label = int(np.argmax(y_pred, axis = 1))
  text_label = text_labels.iloc[label]["Text_Label"].split('.')[0]

  sims1 = cosine_similarity(query_feature1, data_features_load).squeeze()
  indices = [i for i in range(28575)]
  tps1 = zip(sims1.tolist(), indices)
  return sorted(tps1, key=getKey, reverse=True)[:num_imgs], text_label

def get_sims2(data_features_load2, query_np, num_imgs):
  query_np = np.expand_dims(query_np, axis=0)
  query_np = preprocess_input(query_np)
  query_features2 = VGG16_feature_extraction.predict(query_np)
  query_features2 = np.reshape(query_features2, (1,-1))

  sims2 = cosine_similarity(query_features2, data_features_load2).squeeze()
  indices = [i for i in range(28575)]
  tps2 = zip(sims2.tolist(), indices)
  return sorted(tps2, key=getKey, reverse=True)[:num_imgs]

def get_final_sims(feature_extract_model, trained_model, data_features_load, data_features_load2, query_np, num_imgs):
  tps_sorted1, text_label = get_sims1(feature_extract_model, trained_model, data_features_load, 
                            query_np, num_imgs)
  tps_sorted2 = get_sims2(data_features_load2, query_np, num_imgs)
  tps_sorted = tps_sorted1 + tps_sorted2
  tps_sorted = sorted(tps_sorted, key = getKey, reverse = True)
  tps_sorted = list(map(lambda x: x[1], tps_sorted))
  return list(OrderedDict.fromkeys(tps_sorted))[:num_imgs], reformat_text(text_label)

def get_popular_label(result_paths, range_num):
  labels = list(map(lambda x: x.split('/')[1], result_paths[:range_num]))
  freq = [labels.count(i) for i in labels]
  return reformat_text(labels[freq.index(max(freq))])

def get_result_paths(tps_sorted):
  return list(map(lambda x: os.path.join('../static', img_paths.iloc[x]['ImgPath']), tps_sorted))


def search_img(feature_extract_model, trained_model, data_features_load, data_features_load2, file_name, num_imgs, range_popular = 20):
  query = kimage.load_img(file_name, target_size=(86, 128))
  
  query_np = kimage.img_to_array(query)
  tps_sorted, text_label = get_final_sims(query_np, num_imgs)

  result_paths = get_result_paths(tps_sorted)
  popular_text_label = get_popular_label(result_paths, range_num = range_popular)

  return result_paths, popular_text_label, text_label