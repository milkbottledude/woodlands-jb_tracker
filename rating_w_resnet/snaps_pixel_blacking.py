import pandas as pd

columns = ['layer_trainable_YES', 'layer_trainable_NO', 'output_continuous', 'output_classes', 'dropout_0.4', 'dropout_0.3']
index = ['blacked_NO', 'blacked_YES']
blank = pd.DataFrame(columns=columns, index=index)
print(blank)

blank.to_csv('rating_w_resnet/resnet_results.csv')