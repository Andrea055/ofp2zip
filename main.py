import argparse
import os
from lib import updater_script_generator, metadata_generator, parse_super
import shutil
import configparser
from colorama import init, Fore, Back, Style
from art import tprint

init()

config = configparser.ConfigParser()
config.sections()
config.read('config.ini')
config.sections()

# Global variables

out = "temp"  # Directory of extraction
removable_images_path = "temp_zip/META-INF/com/google/android/removable_images.txt"
removable_images_path_temp = "removable_images.txt"


def install_dependency():
    print("Install dependency for oppo_decrypt. Thanks to bkerler")
    os.system("pip3 install -r oppo_decrypt/requirements.txt")


def create_flashable_folder(files, path):
    if os.path.exists("temp_zip"):
        print(Fore.YELLOW + "Removing old files")
        shutil.rmtree("temp_zip")

    shutil.copytree("zip_template", "temp_zip")
    os.mkdir("temp_zip/firmware-update/")
    for file in files:
        shutil.copy(path + "/" + file, "temp_zip/firmware-update/")


def start_decrypt(filename, platform):
    try:
        shutil.rmtree("temp")
    except:
        print(Fore.YELLOW + "No need to cleanup old decrypted file")

    filename_extension = filename.split(".")
    extension = len(filename_extension) - 1
    if filename_extension[extension] == "ofp" and platform == "qcom":
        os.system("oppo_decrypt/ofp_qc_decrypt.py {filename} {out}".format(filename=filename, out=out))
    elif filename_extension[extension] == "ofp" and platform == "mtk":
        os.system("oppo_decrypt/ofp_mtk_decrypt.py {filename} {out}".format(filename=filename, out=out))
    elif filename_extension[extension] == "ops":
        os.system("oppo_decrypt/opscrypto.py {filename} {out}".format(filename=filename, out=out))
    else:
        print(Fore.RED + "Invalid file")
        exit(255)


def is_flashable_file(file):
    file_ext = file.split(".")
    file_ext_index = len(file_ext) - 1

    if config["ignore"]["ignore_list"].count(file) > 0:
        print(Fore.YELLOW + file + " found in blacklist")
        return False

    if file_ext[file_ext_index] == "img":
        removable_images = open(removable_images_path_temp, "a")
        removable_images.write(file + "\n")

    if file_ext[file_ext_index] == "mbn" or file_ext[file_ext_index] == "elf" or \
            file_ext[file_ext_index] == "iso":
        if "DigestsToSign" not in file:
            return True

    return False

def is_fw_file(file):

    file_ext = file.split(".")
    file_ext_index = len(file_ext) - 1

    if config["ignore"]["ignore_list"].count(file) > 0:
        print(Fore.YELLOW + file + " found in blacklist")
        return False

    if file_ext[file_ext_index] == "fw":
        return True
    else:
        return False


def get_all_flashable_file():
    all_files = os.listdir("temp")
    return list(filter(is_flashable_file, all_files))


def get_all_fw_file():
    all_files = os.listdir("temp")
    return list(filter(is_fw_file, all_files))


def clean_temp():
    shutil.rmtree("temp")
    shutil.rmtree("temp_zip")
    os.remove("removable_images.txt")


def create_zip(filename_zip):
    shutil.copy("removable_images.txt", removable_images_path)
    filename_zip = filename_zip + ".zip"

    try:
        os.remove(filename_zip)
    except:
        print(Fore.YELLOW + "No need to clean old zip file")

    os.system("cd temp_zip && python3 -m zipfile -c {} *".format(filename_zip))
    shutil.move("temp_zip/{}".format(filename_zip), filename_zip)


def main(filename, platform):
    install_dependency()
    print(Fore.GREEN + "Decryption rom...")
    start_decrypt(filename, platform)
    print(Fore.GREEN + "Generating super image...")
    parse_super.create_super()
    flashable_files = get_all_flashable_file()
    fw_files = get_all_fw_file()
    print(Fore.GREEN + "Creating flashing image...")
    create_flashable_folder(flashable_files + fw_files, "temp")
    updater_script_generator.generate_flash_script(flashable_files, fw_files)
    print(Fore.GREEN + "Generating metadata from build.prop...")
    metadata_generator.generate_metadata()
    print(Fore.GREEN + "Zipping all files...")
    create_zip(filename)
    print(Fore.GREEN + "Cleaning temp files...")
    clean_temp()
    print(Fore.GREEN + "Zip and Super ready! Good luck")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='ofp2zip',
        description='Convert .ofp or .ops to flashable TWRP zip',
        epilog='platform = qcom or mtk')

    parser.add_argument('ofp_file')  # OFP/OPS file
    parser.add_argument('out_zip')  # Out zip
    parser.add_argument('platform')

    args = parser.parse_args()
    tprint("ofp2zip")
    print(Fore.GREEN + "Thanks to bkerler for the oppo_decrypt!")
    main(args.ofp_file, args.platform)
