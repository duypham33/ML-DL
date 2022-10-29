# Image Retrieval
In this project, I build Image Search based on the similarities of images, the program will show similar images with the query and also shows two prediction of what is the main thing in the query image by two methods: The popularity of result images, and The prediction of the trained model.

---
## 1) Data Crawler
Get 28575 images from freepik and freeimages websites with 134 different categories among animals, plants, furnitures, and scenery. Then save the dataset with their labels.

## 2) Training Dataset
I pretrained all layers of VGG16 model with initial weights of Imagenet. The accuracy of the classification was not good since this dataset has lots of noise because they are scraped from the website.

## 3) Get feature extraction of the dataset
I let the dataset go through the feature extraction of the two different models (Original VGG16 and Pretrained Model). Save the feature extraction of dataset.

## 4) Image Retrieval with CNN-Cosine Similarity
Use Cosine Similarity compute the similarity scores of the feature extractions of the query image and dataset.

## 5) Build Flask app with JavaScript ajax

---
# Some Examples:
![image](https://github.com/duypham33/ML-DL/blob/main/Computer-Vision/Image-Retrieval/app/static/images/Screenshot%202022-10-28%2020.36.44.png)
![image](https://github.com/duypham33/ML-DL/blob/main/Computer-Vision/Image-Retrieval/app/static/images/Screenshot%202022-10-28%2020.39.07.png)
![image](https://github.com/duypham33/ML-DL/blob/main/Computer-Vision/Image-Retrieval/app/static/images/Screenshot%202022-10-28%2020.37.31.png)
![image](https://github.com/duypham33/ML-DL/blob/main/Computer-Vision/Image-Retrieval/app/static/images/Screenshot%202022-10-28%2020.38.26.png)
![image](https://github.com/duypham33/ML-DL/blob/main/Computer-Vision/Image-Retrieval/app/static/images/Screenshot%202022-10-28%2020.38.42.png)
![image](https://github.com/duypham33/ML-DL/blob/main/Computer-Vision/Image-Retrieval/app/static/images/Screenshot%202022-10-28%2020.38.55.png)





