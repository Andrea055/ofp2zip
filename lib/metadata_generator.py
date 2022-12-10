from jproperties import Properties
from colorama import Fore, Back, Style

configs = Properties()
build_prop_path = "build.prop"
metadata_path = "temp_zip/META-INF/com/android/metadata"


def read_build_prop():
    with open(build_prop_path, 'rb') as config_file:
        print(Fore.GREEN + "Parsing build.prop...")
        configs.load(config_file)
    return configs


def generate_metadata():
    build_prop = read_build_prop()
    metadata = Properties()
    metadata["android_version"] = build_prop.get("ro.system.build.version.release").data
    metadata["google_patch"] = build_prop.get("ro.build.version.security_patch").data.replace("-", "")
    metadata["os_version"] = build_prop.get("ro.build.version.opporom").data
    metadata["ota-downgrade"] = build_prop.get("ro.oplus.is_gota").data
    metadata["ota-id"] = build_prop.get("ro.build.display.full_id").data
    metadata["ota-property-files"] = "metadata:4950918613:337"  # Need to find it in build.prop
    metadata["ota-required-cache"] = "0"
    metadata["ota-type"] = "BLOCK"
    metadata["ota_version"] = build_prop.get("ro.build.version.ota").data
    metadata["patch_type"] = "1"
    metadata["post-timestamp"] = build_prop.get("ro.product.build.date.utc").data
    metadata["pre-device"] = build_prop.get("ro.product.product.device").data
    metadata["version_name"] = build_prop.get("ro.build.display.id").data
    metadata["wipe"] = "0"
    metadata["nv_id.00011011.preload_preview_state"] = "false"
    metadata["target_componet_version_base"] = build_prop.get("ro.oplus.version.base").data
    metadata["ota-downgrade-skip-certification"] = "yes"

    with open(metadata_path, "wb") as f:
        print(Fore.GREEN + "Writing metadata...")
        metadata.store(f, encoding="utf-8")
