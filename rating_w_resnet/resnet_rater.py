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

folders_no = [7, 30] # snaps 7 to 29, 12 snaps_ folders, 
# 4951 images - 5 corrupted:
# snaps_5/12-03_10-00_Tue.jpg
# snaps_5/12-04_12-00_Wed.jpg
# snaps_5/12-07_00-00_Sat.jpg
# snaps_5/12-07_08-00_Sat.jpg
# snaps_5/12-07_20-00_Sat.jpg
# nvm 4391 images, not using snaps4, 5, 6 anym. different labelling preference back then, was more lenient. 
# but ns has hardened me into a tuf guy, and with that comes stricter labelling. *grunts*
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
        # print(snap_path)
        all_snaps_filepaths.append(snap_path)
    # now to sort out ratings
    ratings_file_path = ratings_file_template + str(x) + '.txt'
    print(f'digging thru rating_{x} text file for ratings')
    with open(ratings_file_path, 'r') as f:
        for line in f:
            to_jb_ratings.append(float(line[-3]))
            to_wdlands_ratings.append(float(line[-2]))
    # print(f'length of snaps_{x} and ratings_{x}: {str(len(all_snaps_filepaths))} and {str(len(to_jb_ratings))}, {str(len(to_wdlands_ratings))}')

# change ratings lists into numpy arrays
to_jb_array = np.array(to_jb_ratings, dtype=np.float32)
# to_wdlands_array = np.array(to_wdlands_ratings, dtype=np.float32)

scaling_factor = 731.83 # 4391/6
custom_weights = {}

# to see snaps rating distribution (do for to_wdlands as well) AND making weights
unique, counts = np.unique(to_jb_array, return_counts=True)
for rating, count in zip(unique, counts):
    weight = scaling_factor/count
    custom_weights[int(rating)] = float(np.sqrt(weight))
    print(f"{rating}: {count}")

print(custom_weights)


# # checking for corrupted jpegs
# corrupted = []
# print("Checking all images...")
# for i, filepath in enumerate(all_snaps_filepaths):
#     try:
#         img = tf.io.read_file(filepath)
#         img = tf.image.decode_jpeg(img, channels=3)
#         print(f"✓ {i+1}/{len(all_snaps_filepaths)}")
#     except Exception as e:
#         print(f"✗ CORRUPTED: {filepath[26:]}")
#         corrupted.append(filepath[26:])
# print(len(corrupted))
# for c in corrupted:
#     print(c)


# preprocessing function from claude
def load_and_preprocess_image(filename, label):
    """Load image and preprocess for ResNet"""
    # Read image file
    img = tf.io.read_file(filename)
    # Decode image 
    img = tf.image.decode_jpeg(img, channels=3)
    # Resize to expected input size
    img = tf.image.resize(img, [224, 224])
    # Preprocess for ResNet
    img = resnet50.preprocess_input(img)
    
    return img, label


# creating dataset (start w to_jb, can do to_wdlands later)
target_array = to_jb_array
print(len(all_snaps_filepaths), len(target_array))
full_dataset = Dataset.from_tensor_slices((all_snaps_filepaths, target_array))
full_dataset = full_dataset.map(load_and_preprocess_image, num_parallel_calls=10) # cuz i got 12 cores
full_dataset = full_dataset.shuffle(buffer_size=1000, seed=7) # size of shuffle

# train test spleet
split_number = int(len(target_array) * 0.8)
train_dataset = full_dataset.take(split_number) # cant use [:split_number] cos tf datasets dont support
val_dataset = full_dataset.skip(split_number)
train_dataset = train_dataset.batch(32) # train 32 images at a time, reduces overfitting
val_dataset = val_dataset.batch(32)
print(len(train_dataset))
print(len(val_dataset))
    

# data prep done, now prepping rezzy model
base_model = resnet50.ResNet50(weights="imagenet", include_top=False, input_shape=(224, 224, 3)) # without top output layer
base_model.trainable = False # determines if base weights frm imagenet r updated frm my own data or not

tf.random.set_seed(7)
full_regression_model = tf.keras.Sequential([
    base_model,
    # base_model without the top outputs a high rank tensor, this layer converts it to a rank 2 tensor (vector) for the dense layer to nom
    layers.GlobalAveragePooling2D(), 
    # takes the general purpose features from base_model and molds them to our input
    layers.Dense(128, activation='relu'), # not too sure whats relu, just that it adds non-linearity to learn 'complex r'ships' wtv that means
    layers.Dropout(0.3), # silences 20% units in the dense layer
    layers.Dense(1)  # regression layer outputs continuous value (0-5)
])

full_regression_model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), # optimizer decides how model weights are updated during trng, have no idea how it works
    loss='mse',  # Mean Squared Error
    metrics=['mae']  # Mean Absolute Error
)

# Training
results = full_regression_model.fit(
    train_dataset,
    validation_data = val_dataset,
    epochs = 12, # switching to 12 epochs instead, 20 takes way too long
    class_weight = custom_weights
)

# just run it and watch anime, but b4 that do some js work so u dont start the day with ramune anime

