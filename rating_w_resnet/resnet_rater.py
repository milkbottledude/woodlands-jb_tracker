import pandas as pd
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' # to silence oneDNN info message every time file is run
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.data import Dataset

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
    img = ResNet50.preprocess_input(img)
    
    return img, label

    
# prepping rezzy model
# resnet = ResNet50(weights="imagenet", include_top=False, input_shape=(224, 224, 3)) # without top output layer
