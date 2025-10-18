import pandas as pd
from PIL import Image # do i need to import this, theres no red line under...

columns = ['layer_trainable_YES', 'layer_trainable_NO', 'output_classes', 'dropout_0.4', 'dropout_0.3', '128_units', '256_units']
# for output classes, i will specify the specs at the time of training (eg dropout rate, neuron number in 2nd last layer, etc)
index = ['trng_mse', 'trng_mae', 'val_mse', 'val_mae', 'wdl_trng_mse', 'wdl_trng_mae', 'wdl_val_mse', 'wdl_val_mae']
# blank = pd.DataFrame(columns=columns, index=index)
blank = pd.read_csv('rating_w_resnet/rn_results_unblacked.csv', index_col=0)


# losses_for_today = [0.6036, 0.4022, 0.5332, 0.4663]
# losses_for_today = [0.5250, 0.3896, 0.6381, 0.4368]

# for i, loss in enumerate(index):
#     blank.at[loss, '256_units'] = str(losses_for_today[i])
# print(blank)

blank.to_csv('rating_w_resnet/rn_results_unblacked.csv', index=True)


# first results: Epoch 20/20 -> 110/110 ━━━━━━━━━━━━━━━━━━━━ 63s 569ms/step - loss: 0.6036 - mae: 0.4022 - val_loss: 0.5332 - val_mae: 0.4663
# w 256 units in the top layer: 110/110 ━━━━━━━━━━━━━━━━━━━━ 62s 556ms/step - loss: 0.5250 - mae: 0.3896 - val_loss: 0.6381 - val_mae: 0.4368
# mae is good and mse is not far off
# however, data is heavily skewed to 0, there are many snaps of jb rating 0. maybe fixing this will improve performance
# distribution of snaps ratings for jbn wdlands: 
# Label 0: 3461, 2479 images
# Label 1: 108, 227 images
# Label 2: 79, 177 images
# Label 3: 99, 211 images
# Label 4: 98, 323 images
# Label 5: 546, 974 images

# w dropout = 0.3 instead of 0.4:
# Epoch 9/20
# 110/110 ━━━━━━━━━━━━━━━━━━━━ 179s 2s/step - loss: 0.5603 - mae: 0.3861 - val_loss: 0.5287 - val_mae: 0.4039
# Epoch 10/20
# 110/110 ━━━━━━━━━━━━━━━━━━━━ 246s 2s/step - loss: 0.5277 - mae: 0.3887 - val_loss: 0.5608 - val_mae: 0.4814
# Epoch 11/20
# 110/110 ━━━━━━━━━━━━━━━━━━━━ 221s 2s/step - loss: 0.5451 - mae: 0.4047 - val_loss: 0.4217 - val_mae: 0.3710
# Epoch 12/20
# 110/110 ━━━━━━━━━━━━━━━━━━━━ 305s 2s/step - loss: 0.4541 - mae: 0.3605 - val_loss: 0.4371 - val_mae: 0.3622
# Epoch 13/20
# 110/110 ━━━━━━━━━━━━━━━━━━━━ 260s 2s/step - loss: 0.4613 - mae: 0.3653 - val_loss: 0.5038 - val_mae: 0.4308
# Epoch 14/20
# 110/110 ━━━━━━━━━━━━━━━━━━━━ 263s 2s/step - loss: 0.4682 - mae: 0.3590 - val_loss: 0.4056 - val_mae: 0.3420
# Epoch 15/20
# 110/110 ━━━━━━━━━━━━━━━━━━━━ 205s 2s/step - loss: 0.4359 - mae: 0.3415 - val_loss: 0.4514 - val_mae: 0.3965
# Epoch 16/20
# 110/110 ━━━━━━━━━━━━━━━━━━━━ 69s 619ms/step - loss: 0.4697 - mae: 0.3570 - val_loss: 0.4304 - val_mae: 0.4100
# Epoch 17/20
# 110/110 ━━━━━━━━━━━━━━━━━━━━ 67s 603ms/step - loss: 0.4181 - mae: 0.3395 - val_loss: 0.4510 - val_mae: 0.3465
# Epoch 18/20
# 110/110 ━━━━━━━━━━━━━━━━━━━━ 67s 607ms/step - loss: 0.4124 - mae: 0.3238 - val_loss: 0.4388 - val_mae: 0.3547
# Epoch 19/20
# 110/110 ━━━━━━━━━━━━━━━━━━━━ 68s 609ms/step - loss: 0.3950 - mae: 0.3226 - val_loss: 0.3433 - val_mae: 0.3206
# Epoch 20/20
# 110/110 ━━━━━━━━━━━━━━━━━━━━ 67s 608ms/step - loss: 0.4237 - mae: 0.3403 - val_loss: 0.4001 - val_mae: 0.3835


# last one on 20 epochs, after this all our trainings will be on 12 epochs, altho yes we are seeing that performance still increasing w epoch number even at epoch 20, as seen in fig 6.3. will test epochs at the end after all hyperparams are at optimized values
# w dropout = 0.2 instead of 0.3:
# Epoch 9/20
# 110/110 ━━━━━━━━━━━━━━━━━━━━ 63s 565ms/step - loss: 0.5474 - mae: 0.3897 - val_loss: 0.5510 - val_mae: 0.4179
# Epoch 10/20
# 110/110 ━━━━━━━━━━━━━━━━━━━━ 63s 565ms/step - loss: 0.4605 - mae: 0.3685 - val_loss: 0.8782 - val_mae: 0.5963
# Epoch 11/20
# 110/110 ━━━━━━━━━━━━━━━━━━━━ 62s 559ms/step - loss: 0.5484 - mae: 0.4048 - val_loss: 0.4498 - val_mae: 0.3771
# Epoch 12/20
# 110/110 ━━━━━━━━━━━━━━━━━━━━ 62s 562ms/step - loss: 0.4322 - mae: 0.3481 - val_loss: 0.4923 - val_mae: 0.3717
# Epoch 13/20
# 110/110 ━━━━━━━━━━━━━━━━━━━━ 62s 560ms/step - loss: 0.3836 - mae: 0.3298 - val_loss: 0.5389 - val_mae: 0.4715
# Epoch 14/20
# 110/110 ━━━━━━━━━━━━━━━━━━━━ 63s 567ms/step - loss: 0.4368 - mae: 0.3741 - val_loss: 0.3702 - val_mae: 0.3591
# Epoch 15/20
# 110/110 ━━━━━━━━━━━━━━━━━━━━ 62s 560ms/step - loss: 0.3486 - mae: 0.3147 - val_loss: 0.5613 - val_mae: 0.3769
# Epoch 16/20
# 110/110 ━━━━━━━━━━━━━━━━━━━━ 62s 560ms/step - loss: 0.4670 - mae: 0.3622 - val_loss: 0.4180 - val_mae: 0.3522
# Epoch 17/20
# 110/110 ━━━━━━━━━━━━━━━━━━━━ 62s 560ms/step - loss: 0.4284 - mae: 0.3519 - val_loss: 0.3943 - val_mae: 0.3372
# Epoch 18/20
# 110/110 ━━━━━━━━━━━━━━━━━━━━ 62s 561ms/step - loss: 0.3360 - mae: 0.3086 - val_loss: 0.5061 - val_mae: 0.3611
# Epoch 19/20
# 110/110 ━━━━━━━━━━━━━━━━━━━━ 62s 560ms/step - loss: 0.3483 - mae: 0.3091 - val_loss: 0.3792 - val_mae: 0.3271
# Epoch 20/20
# 110/110 ━━━━━━━━━━━━━━━━━━━━ 62s 563ms/step - loss: 0.3692 - mae: 0.3205 - val_loss: 0.4184 - val_mae: 0.3587