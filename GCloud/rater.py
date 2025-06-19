import os

for x in range(15, 20): # to 19, 20 not counted in 'range'
    path = fr'E:\snaps_{x}'
    filenames = os.listdir(path)
    writeto = f'rating_{x}.txt'
    with open(writeto, 'a') as file:
        for filename in filenames:
            file.write(filename + ' \n')

