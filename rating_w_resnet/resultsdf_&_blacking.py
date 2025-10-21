import pandas as pd
# import tensorflow as tf
import matplotlib.pyplot as plt
columns = ['128_units', '256_units', 'dropout_0.3'] # , 'layer_trainable_YES'

# for output classes, will specify the specs at the time of training (eg dropout rate, neuron number in 2nd last layer, etc)

index = ['trng_mse', 'trng_mae', 'val_mse', 'val_mae'] 
# index_wdlands = ['wdl_trng_mse', 'wdl_trng_mae', 'wdl_val_mse', 'wdl_val_mae']

# blank = pd.DataFrame(columns=columns, index=index)
blank = pd.read_csv('rn_results_unblacked.csv', index_col=0)


# losses_for_today = [0.4157,  0.3451, 0.4010, 0.3593]
losses_for_today = [0.4139, 0.3406, 0.4001, 0.3390]


for i, metric in enumerate(index):
    blank.at[metric, 'bs_16'] = str(losses_for_today[i])
print(blank)

blank.to_csv('rn_results_unblacked.csv', index=True)

# mask = tf.io.read_file("..\progress_pics\Fig-6.10-jb_masked_full.jpg")
# mask = tf.image.decode_jpeg(mask, channels=3)
# mask = tf.image.resize(mask, [224, 224])          
# mask = mask / 255.0 # convert 255 in white regions to 1

def TEST_load_and_preprocess_image(filename):
    """Load image and preprocess for ResNet"""
    # Read image file
    img = tf.io.read_file(filename)
    # Decode image 
    img = tf.image.decode_jpeg(img, channels=3)
    # Resize to expected input size
    img = tf.image.resize(img, [224, 224])
    
    img_blacked = img * mask
    
    # showing img
    plt.figure(figsize=(8, 8))
    plt.imshow(img_blacked.numpy().astype('uint8'))  # .numpy() is a TensorFlow method
    plt.title("Image with top 5 rows blacked out")
    plt.axis('off')
    plt.show()

testsnap_path = "../GCloud/all_snaps/snaps_12/02-06_01-00_Thu.jpg"

# TEST_load_and_preprocess_image(testsnap_path)

















