import os

for x in range(8, 15):
    path = f'snaps_{x}'
    filenames = os.listdir(path)
    writeto = f'rating_{x}.txt'
    with open(writeto, 'a') as file:
        for filename in filenames:
            file.write(filename + ' \n')