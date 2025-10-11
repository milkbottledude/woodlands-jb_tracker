import pandas as pd
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' # to silence oneDNN info message every time file is run
import tensorflow as tf
from tensorflow.keras.applications import resnet50
from tensorflow.keras import layers
from tensorflow.data import Dataset

# # creating blank csv
# columns = ['layer_trainable_YES', 'layer_trainable_NO', 'output_continuous', 'output_classes']
# index = ['blacked_NO', 'blacked_YES']
# blank = pd.DataFrame(columns=columns, index=index)
# print(blank)
# blank.to_csv('resnet_results.csv')

# prepping training data (imma combine multiple snaps folders into 1 big dataset)

folders_no = [4, 30] # snaps 4 to 29, 15 snaps_ folders, 4951 images
snaps_folder_template = rf"C:/Coding/Project-JBridge/GCloud/all_snaps/snaps_"
ratings_file_template = rf"C:/Coding/Project-JBridge/GCloud/rating_"

all_snaps_filepaths = []
to_jb_ratings = []
to_wdlands_ratings = []
for x in range(folders_no[0], folders_no[1]):
    # sort out snaps first
    snaps_folder_path = snaps_folder_template + str(x)
    print(f'accessing {snaps_folder_path} for snaps...')
    for snap_name in os.listdir(snaps_folder_path):
        snap_path = snaps_folder_path + '/' + snap_name
        print(snap_path)
        all_snaps_filepaths.append(snap_path)
    # now to sort out ratings
    ratings_file_path = ratings_file_template + str(x) + '.txt'
    print(f'digging thru rating_{x} text file for ratings')
    with open(ratings_file_path, 'r') as f:
        for line in f:
            to_jb_ratings.append(float(line[-3]))
            to_wdlands_ratings.append(float(line[-2]))
    print(f'length of snaps_{x} and ratings_{x}: {str(len(all_snaps_filepaths))} and {str(len(to_jb_ratings))}, {str(len(to_wdlands_ratings))}')

# preprocessing function from claude
def load_and_preprocess_image(filename, label):
    """Load image and preprocess for ResNet"""
    # Read image file
    img = tf.io.read_file(filename)
    # Decode image (use decode_jpeg or decode_png as appropriate)
    img = tf.image.decode_jpeg(img, channels=3)
    # Resize to expected input size
    img = tf.image.resize(img, [224, 224])
    # Preprocess for ResNet (normalizes to [-1, 1] range)
    img = resnet50.preprocess_input(img)
    
    return img, label

# change ratings lists into numpy arrays
to_jb_array = np.array(to_jb_ratings, dtype=np.float32)
to_wdlands_array = np.array(to_wdlands_ratings, dtype=np.float32)

# creating dataset (start w to_jb, can do to_wdlands later)
target_array = to_jb_array

full_dataset = Dataset.from_tensor_slices((all_snaps_filepaths, target_array))
full_dataset = full_dataset.map(load_and_preprocess_image, num_parallel_calls=10) # cuz i got 12 cores
full_dataset = full_dataset.shuffle(buffer_size=1000) # size of shuffle

# train test spleet
split_number = len(target_array) * 0.8
train_dataset = full_dataset.take(split_number) # cant use [:split_number] cos tf datasets dont support
val_dataset = full_dataset.skip(split_number)
    
# data prep done, now prepping rezzy model
base_model = resnet50.ResNet50(weights="imagenet", include_top=False, input_shape=(224, 224, 3)) # without top output layer
base_model.trainable = False # determines if base weights frm imagenet r updated frm my own data or not

full_regression_model = tf.keras.Sequential([
    base_model,
    # base_model without the top outputs a high rank tensor, this layer converts it to a rank 2 tensor (vector) for the dense layer to nom
    layers.GlobalAveragePooling2D(), 
    # takes the general purpose features from base_model and molds them to our input
    layers.Dense(128, activation='relu'), # not too sure whats relu, just that it adds non-linearity to learn 'complex r'ships' wtv that means
    layers.Dropout(0.4), # silences 40% units in the dense layer
    layers.Dense(1)  # regression layer outputs continuous value (0-5)
])

# rmse func
def tf_rmse(y_true, y_pred):
    return tf.sqrt(tf.reduce_mean(tf.square(y_true - y_pred)))

full_regression_model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), # optimizer decides how model weights are updated during trng, have no idea how it works
    loss='mse',  # Mean Squared Error
    metrics=['mae', tf_rmse]  # Mean Absolute Error
)

# Training
results = full_regression_model.fit(
    train_dataset,
    validation_data=val_dataset,
    epochs=20
)