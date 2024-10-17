# -*- coding: utf-8 -*-
"""model.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Rw8SqIoyaW0EvhJmYhtQhiz5O7_YV0mr
"""

!pip install -U "tensorflow-text==2.13.*"

# !pip install transformers
import tensorflow as tf

from transformers import BertModel, BertTokenizer
import tensorflow_hub as hub

preprocess_url = "https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3"
encoder_url = "https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/3"

!pip install -q -U "tensorflow-text==2.13.*"

import tensorflow_text as text

bert_preprocess = hub.KerasLayer(preprocess_url)

import pandas as pd
df = pd.read_csv('/content/sample_data/cleaned_file1.csv')
df.head(1)

import numpy as np

df.label.nunique(dropna = True)
x = df['text']
y=df['label'].astype(float)

y= np.asarray(y, dtype=np.float32)

from sklearn.model_selection import train_test_split
x_train , x_test, y_train, y_test = train_test_split(x,y,test_size=0.2)

bert_model = hub.KerasLayer(encoder_url)

bert_model.trainable = True

text_input = tf.keras.layers.Input(shape=(), dtype=tf.string, name='text')
preprocessed_text = bert_preprocess(text_input)
bert_results = bert_model(preprocessed_text)
pooled_output = bert_results['pooled_output']
# neural network layers
# dense_layer_1 = tf.keras.layers.Dense(600, activation='relu', name='dense_layer_1')(pooled_output)
# dense_layer_2 = tf.keras.layers.Dense(400, activation='relu', name='dense_layer_2')(dense_layer_1)
# dense_layer_3 = tf.keras.layers.Dense(400, activation='relu', name='dense_layer_3')(pooled_output)
# dense_layer_4 = tf.keras.layers.Dense(200, activation='relu', name='dense_layer_4')(dense_layer_3)
# dropout_layer_1 = tf.keras.layers.Dropout(0.2, name='dropout_1')(dense_layer_4)
# output_layer = tf.keras.layers.Dense(1, activation='sigmoid', name='output')(dropout_layer_1)

dense_layer_4 = tf.keras.layers.Dense(200, activation='relu', name='dense_layer_4')(pooled_output)
dropout_layer_1 = tf.keras.layers.Dropout(0.1, name='dropout_1')(dense_layer_4)
output_layer = tf.keras.layers.Dense(1, activation='sigmoid', name='output')(dropout_layer_1)
bert_model.trainable = True

model = tf.keras.Model(inputs=[text_input], outputs = [output_layer])

from tensorflow.keras.optimizers import Adam

opt = Adam(learning_rate=1e-4)
model.compile(optimizer=opt,
              loss = 'binary_crossentropy',
              metrics = ['accuracy'])

model.fit(x_train,y_train,epochs=1)

# def get_score(model, X_train, X_test, y_train, y_test):
#     model.fit(X_train, y_train, epochs=5)
#     return model.evaluate(X_test, y_test)
# from sklearn.model_selection import KFold
# kf = KFold(n_splits = 5)
# for train_index, test_index in kf.split(x,y):

#   x_train, x_test = x[train_index], x[test_index]
#   y_train, y_test = y[train_index], y[test_index]
#   print(get_score(model,x_train,x_test,y_train,y_test))

model.evaluate(x_test,y_test)

!pip install selenium

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

dark_patterns = 0

def get_page_content(url):
    response = requests.get(url)
    return response.content

def get_dynamic_page_content(url):
    driver = webdriver.Chrome()
    driver.get(url)
    content = driver.page_source
    driver.quit()
    return content

def extract_keywords(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    text_content = soup.get_text()
    text_content = text_content.replace("\n","")

    print(type(text_content))
    for text in text_content.split('.'):
      print(text)
      predictions = model.predict([text])
      if predictions[0] >= 0.50000:
        print("Detected")
        dark_patterns+=1
      else :
        print("Not detected")


    # predictions = model.predict([text_content])

    # for i, prediction in enumerate(predictions):
    #   if prediction > 0.5:
    #     print("Detected")
    #   else:
    #     print(" Not Detected")

    # for keyword in keywords:
    #     if keyword.lower() in text_content.lower():
    #         print(f"Found keyword: {keyword}")

ecommerce_url = "https://www.aachho.com/products/hyena-handblock-tiered-suit-set?utm_source=google&utm_medium=cpc&utm_campaign=WWWA_3519_adyogi_PerformanceMax_Top+SKUs-20275808049&gad_source=1&gclid=CjwKCAiA8NKtBhBtEiwAq5aX2FYO3fU2HI9kMQQAsZ2sVpZvVaXi1xAvTu_lmwaljKydTrJDuE3FthoCCfgQAvD_BwE"  # Replace with the actual URL of the eCommerce page

html_content = get_page_content(ecommerce_url)

dark_patterns = 0

extract_keywords(html_content)

print(dark_patterns)