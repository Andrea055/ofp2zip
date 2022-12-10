from lib import metadata_generator
from colorama import Fore, Back, Style

updater_path = "temp_zip/META-INF/com/google/android/updater-script"


def generate_script_header(file):  # Add git author a day
    print(Fore.GREEN + "Generating header of script...")
    build_prop = metadata_generator.read_build_prop()
    file.write("""# Don't edit this file, is automatically generated by ofp2zip
# Header of script, print some info
show_progress(0.100000, 10);
ui_print("**************************");
ui_print("TWRP flashable zip for {model}");
ui_print("Region: {region}");
ui_print("Color OS base version: {version}");
ui_print("Script originally made by sircda/italorecife");
ui_print("This zip is generated by ofp2zip made by Andreock");
# ui_print("Author of commit: ");
ui_print("**************************");
ui_print("PackageType: Update ");
ui_print("**************************");       
ui_print("Installing important partitions...");
# Flash process start 
""".format(model=build_prop.get("ro.product.product.device").data, region=build_prop.get("ro.oplus.image.my_region.type").data, version= build_prop.get("ro.build.version.opporom").data))


def is_ram_file(partition, file):
    if partition == "xbl_config_ddr5.elf" or partition == "xbl_config_ddr4.elf":
        file.write(
            """ifelse(get_xblddr_type() == "ddr5",package_extract_file("firmware-update/xbl_config_ddr5.elf", "/dev/block/bootdevice/by-name/xbl_config");ui_print("update ddr5 xbl_config!"),package_extract_file("firmware-update/xbl_config_ddr4.elf", "/dev/block/bootdevice/by-name/xbl_config"));""")
    elif partition == "imagefv_ddr5.elf" or partition == "imagefv_ddr4.elf":
        file.write(
            """ifelse(get_xblddr_type() == "ddr5",package_extract_file("firmware-update/imagefv_ddr5.elf", "/dev/block/bootdevice/by-name/imagefv");ui_print("update ddr5 imagefv!"),package_extract_file("firmware-update/imagefv_ddr4.elf", "/dev/block/bootdevice/by-name/imagefv"));""")
    elif partition == "xbl_ddr5.elf" or partition == "xbl_ddr4.elf":
        file.write(
            """ifelse(get_xblddr_type() == "ddr5",package_extract_file("firmware-update/xbl_ddr5.elf", "/dev/block/bootdevice/by-name/xbl");ui_print("update ddr5 xbl!"),package_extract_file("firmware-update/xbl_ddr4.elf", "/dev/block/bootdevice/by-name/xbl"));""")
    else:
        file.write(
            'package_extract_file("firmware-update/{file}", "/dev/block/bootdevice/by-name/{partition}");\n'.format(
                file=partition, partition=partition.split(".")[0]))


def generate_script_footer(file, files):
    print(Fore.GREEN + "Generating footer of script")
    for fw in files:
        file.write("""
package_extract_file("storage-fw/{fw}", "/tmp/firmware/{fw}");
set_metadata("/tmp/firmware/{fw}", "uid", 0, "gid", 2000, "mode", 0666);""".format(fw=fw))
    file.write("""
ui_print("Cleanup");
show_progress(0.700000, 10);
package_extract_file("ffu_tool", "/tmp/ffu_tool");set_metadata("/tmp/ffu_tool", "uid", 0, "gid", 2000, "mode", 0755, "capabilities", 0x0, "selabel", "u:object_r:bootanim_exec:s0");
delete_recursive("/cache/backup/");
delete_recursive("/data/data/com.chinamworld.main/.cache/");
delete_recursive("/data/data/com.kiloo.subwaysurf/.cache/");
delete_recursive("/data/data/com.gome.eshopnew/.cache/");
delete_recursive("/data/data/com.shane.littlecartoonist/.jiagu");
delete_recursive("/data/data/com.imangi.templerun2/.cache/");
delete_recursive("/data/user/0/com.tencent.mm/app_cache/");
delete_recursive("/data/user/999/com.tencent.mm/app_cache/");
package_extract_file("oppo_update_script.sh", "/tmp/oppo_update_script.sh");set_metadata("/tmp/oppo_update_script.sh", "uid", 0, "gid", 2000, "mode", 0755, "capabilities", 0x0, "selabel", "u:object_r:bootanim_exec:s0");run_program("/tmp/oppo_update_script.sh", "update_data");
set_progress(1.000000);""")


def generate_flash_script(files, files_fw):
    print(Fore.GREEN + "Generating flash script...")
    flash_script = open(updater_path, "a")
    generate_script_header(flash_script)
    for mbn in files:
        if (mbn.split(".")[1] != "elf"):
            flash_script.write(
                'package_extract_file("firmware-update/{file}", "/dev/block/bootdevice/by-name/{partition}");\n'.format(
                    file=mbn, partition=mbn.split(".")[0]))
        else:
            is_ram_file(mbn, flash_script)

    generate_script_footer(flash_script, files_fw)
