import os

for x in range(20, 27): # to 19, 20 not counted in 'range'
    path = f'E:\snaps_{x}'
    filenames = os.listdir(path)
    writeto = f'C:\Users\cheah\OneDrive\Documents\Coding\Project-JBridge\GCloud\rating_{x}.txt'
    with open(writeto, 'a') as file:
        for filename in filenames:
            file.write(filename + ' \n')

