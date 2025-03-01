s1 = r"C:\Users\cheah\OneDrive\Documents\Code\woodlands-jb_tracker\GCloud\snaps4_250225_103255.txt"
s2 = r"GCloud\snaps5_250225_163710.txt"
s3 = r"GCloud\snaps6_250225_174508.txt"
s4 = r"GCloud\snaps7_250226_110515.txt"

count = 0
with open(s4, "r") as file:
    for line in file:
        count += 1
print(count)