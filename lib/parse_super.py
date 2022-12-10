import os
import glob
from colorama import Fore, Back, Style

def create_super():
    try:
        os.remove("super_partition.img")
    except:
        print(Fore.YELLOW + "No need to clean old file")
    os.system("simg2img temp/super* super_partition.img")
    for super_raw in glob.glob("temp/super*"):
        print(Fore.YELLOW + "Removing temp spare super image...")
        os.remove(super_raw)