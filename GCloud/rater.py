import os

for x in range(27, 33): # to 32, 33 not counted in 'range'
    # path = rf'E:\snaps_{x}'
    path = rf"C:\Users\cheah\OneDrive\Documents\Coding\Project-JBridge\GCloud\all_snaps\snaps_{x}"
    filenames = os.listdir(path)
    writeto = rf'C:\Users\cheah\OneDrive\Documents\Coding\Project-JBridge\GCloud\rating_{x}.txt'
    with open(writeto, 'a') as file:
        for filename in filenames:
            file.write(filename + ' \n')

