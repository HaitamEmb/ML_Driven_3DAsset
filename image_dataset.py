import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import keras
import tqdm
import json
import tensorflow as tf
#from keras.src.applications.vgg16 import VGG16
from sklearn.model_selection import train_test_split
from keras.src.layers import Conv2D
from keras.src.layers import MaxPooling2D
from keras.src.layers import Flatten
from keras.src.layers import Dense
from keras.src.layers import Input
from keras.src.models import Model
from keras.src.layers import Dropout
IMAGE = keras.preprocessing.image

model = VGG16(weights="imagenet")

img_labels = pd.read_csv("D:/HN_Training_data/via_project_31Dec2024_16h49m_csv(2).csv")
img_name = img_labels["filename"]
#train_datasets = keras.preprocessing.image_dataset_from_directory("D:/HN_Training_data/Images/Train2/",labels="inferred",label_mode= None ,color_mode="rgb",batch_size=3,image_size=(250,250))
img_regshape = img_labels["region_shape_attributes"]

image_dir = 'D:/HN_Training_data/Images/Train2/'

image_data = []

for img_id in tqdm.tqdm(img_labels['filename']):
    
    img_path = os.path.join(image_dir, img_id)
    
    im = IMAGE.load_img(img_path)

    im = im.resize((256,256))

    im = np.array(im)
    
    image_data.append(im)

image_data = np.array(image_data)

#X param
X = image_data/255

# for image in image_data[:1]: 
#     plt.imshow(image)
#     plt.show()
#     pass

img_cval = np.array([])

img_curl = img_labels["region_attributes"]
for c in tqdm.tqdm(img_curl):
    value = json.loads(c)
    value = float(value['Curliness'])
    img_cval = np.append(img_cval,value)

img_cval = pd.Series(img_cval,name='Curliness')

#Y param
y_curv = img_cval

#imgs_df = pd.concat([img_labels["filename"], img_cval], axis = 1).sample(frac= 1.0, random_state=1).reset_index(drop=True)

#train_df, test_df = train_test_split(imgs_df, train_size=0.8, shuffle=True, random_state=1)
print(y_curv.shape)


input_shape = (256,256,3)

inputs = Input((input_shape))
conv_1 = Conv2D(32, kernel_size=(3,3), activation="relu")(inputs)
maxp_1 = MaxPooling2D(pool_size=(2,2))(conv_1)
conv_2 = Conv2D(64, kernel_size=(3,3), activation="relu")(maxp_1)
maxp_2 = MaxPooling2D(pool_size=(2,2))(conv_2)
conv_3 = Conv2D(128, kernel_size=(3,3), activation="relu")(maxp_2)
maxp_3 = MaxPooling2D(pool_size=(2,2))(conv_3)
conv_4 = Conv2D(256, kernel_size=(3,3), activation="relu")(maxp_3)
maxp_4 = MaxPooling2D(pool_size=(2,2))(conv_4)

flatten = Flatten()(maxp_4)

dense_1 = Dense(256, activation="relu")(flatten)

dropout_1 = Dropout(0.3)(dense_1)

output = Dense(1, activation='linear', name='curl_out')(dropout_1)

model = Model(inputs=[inputs], outputs = [output])

model.compile(loss='mean_squared_logarithmic_error', optimizer='adam')

#model = keras.models.load_model("D:/HN_Training_data/Saved_model/HN_Hairmodel.keras")
model = keras.models.load_model("D:/HN_Training_data/Saved_model/HN_Hairmodel2.keras")
#model = keras.models.load_model("D:/HN_Training_data/Saved_model/HN_Hairmodel3.keras")

#print(X.shape)

#history = model.fit(x=X, y=y_curv, batch_size=32, epochs=30, validation_split=0.2)

image_dir2 = 'D:/HN_Training_data/test/heaveninhair_Model1_1500x1132_Deandre.webp'
image_dir3 = 'D:/HN_Training_data/test/natural-spiral-curls-for-long-hair.jpg'
image_dir4 = 'D:/HN_Training_data/test/medium_bob_haircuts_hairstyles20.jpg'
image_dir5 = 'D:/HN_Training_data/test/a70cc32396a9127ad5f28df12e4cd4f5.jpg'
image_dir6 = 'D:/HN_Training_data/test/c02c83bfa9db7f15ec8151eb40f2e56a.jpg'
image_dir7 = 'D:/HN_Training_data/test/hair-protein-products-for-curly-hair_560x747_315a47ae-9baa-427b-8922-835f93eee58a.webp'
image_dir10 = 'D:/HN_Training_data/test/beautiful-tight-curls-for-long-hair.jpg'
image_dir8 = 'D:/HN_Training_data/test/42fb64febc48a7cafb1940a4767e0382.jpg'
image_dir11 = 'D:/HN_Training_data/test/00e6d27ee574a77dabb1429b8933862f.jpg'

im2 = IMAGE.load_img(image_dir2)

im2 = im2.resize((256,256))
im2 = np.array(im2)

pred = model.predict(im2.reshape(1,256,256,3))

pred_curl = pred[0][0]
pred_curl = pred_curl/255

print(pred_curl)
plt.imshow(im2)
plt.show()
#model.save("D:/HN_Training_data/Saved_model/HN_Hairmodel3.keras")