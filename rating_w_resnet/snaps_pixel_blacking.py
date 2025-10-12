import pandas as pd
from PIL import Image # do i need to import this, theres no red line under...

columns = ['layer_trainable_YES', 'layer_trainable_NO', 'output_continuous', 'output_classes', 'dropout_0.4', 'dropout_0.3', '128_units', '256_units']
index = ['trng_mse', 'trng_mae', 'val_mse', 'val_mae']
# blank = pd.DataFrame(columns=columns, index=index)
blank = pd.read_csv('rating_w_resnet/rn_results_unblacked.csv', index_col=0)

# losses_for_today = [0.6036, 0.4022, 0.5332, 0.4663]
losses_for_today = [0.5250, 0.3896, 0.6381, 0.4368]

for i, loss in enumerate(index):
    blank.at[loss, '256_units'] = str(losses_for_today[i])
print(blank)

blank.to_csv('rating_w_resnet/rn_results_unblacked.csv', index=True)


# first results: Epoch 20/20 -> 110/110 ━━━━━━━━━━━━━━━━━━━━ 63s 569ms/step - loss: 0.6036 - mae: 0.4022 - val_loss: 0.5332 - val_mae: 0.4663
# w 256 units in the top layer: 110/110 ━━━━━━━━━━━━━━━━━━━━ 62s 556ms/step - loss: 0.5250 - mae: 0.3896 - val_loss: 0.6381 - val_mae: 0.4368
# mae is good and mse is not far off
# however, data is heavily skewed to 0, there are many snaps of jb rating 0. maybe fixing this will improve performance
# distribution of snaps ratings for jb: 
# Label 0: 3461 images
# Label 1: 108 images
# Label 2: 79 images
# Label 3: 99 images
# Label 4: 98 images
# Label 5: 546 images