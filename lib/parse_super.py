import os
import glob
def create_super():
    try:
        os.remove("super_partition.img")
    except:
        print("No need to clean old file")
    os.system("simg2img temp/super* super_partition.img")
    for super_raw in glob.glob("temp/super*"):
        os.remove(super_raw)