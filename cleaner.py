import os
import time
import argparse

# Settings
IGNORED_FOLDERS = ['C:\\Windows', 'C:\\Program Files', 'C:\\Program Files (x86)']
UNUSED_DAYS = 60
LARGE_FILE_SIZE_MB = 100
TEMP_EXTENSIONS = ['.tmp', '.log', '.bak', '.old', '.~']

def get_unused_files(root_dir, dry_run=True):
    current_time = time.time()
    deleted_files = []

    for foldername, subfolders, filenames in os.walk(root_dir):
        if any(foldername.startswith(ig) for ig in IGNORED_FOLDERS):
            continue

        for filename in filenames:
            filepath = os.path.join(foldername, filename)
            try:
                stat = os.stat(filepath)
                last_access_time = stat.st_atime
                file_size_mb = stat.st_size / (1024 * 1024)
                file_ext = os.path.splitext(filepath)[1].lower()

                is_old = (current_time - last_access_time) > (UNUSED_DAYS * 86400)
                is_large = file_size_mb > LARGE_FILE_SIZE_MB
                is_temp = file_ext in TEMP_EXTENSIONS

                if is_old or is_large or is_temp:
                    print(f"[+] Found: {filepath} ({int(file_size_mb)} MB)")
                    if not dry_run:
                        os.remove(filepath)
                        deleted_files.append(filepath)
            except Exception as e:
                print(f"[!] Error reading file: {filepath} | {str(e)}")

    return deleted_files

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Auto Clean Unused Files")
    parser.add_argument("--path", type=str, default="C:\\Users", help="Root path to scan")
    parser.add_argument("--delete", action="store_true", help="Actually delete the files")

    args = parser.parse_args()
    print("🚀 Scanning for unused files...")

    deleted = get_unused_files(args.path, dry_run=not args.delete)

    if args.delete:
        print(f"\n✅ Deleted {len(deleted)} files.")
    else:
        print(f"\n⚠️ Dry Run Complete. Use --delete to remove files.")
