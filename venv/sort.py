import shutil
import sys
import scan
import normalize
from pathlib import Path









def hande_file(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)
    path.replace(target_folder/normalize.normalize(path.name))




def handle_archive(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)

    
    new_name = path.name.replace(".zip", '')

    
    new_path = target_folder / path.name
    path.rename(new_path)

    
    archive_folder = root_folder / new_name
    archive_folder.mkdir(exist_ok=True)

    return archive_folder






    try:
        shutil.unpack_archive(str(path.resolve()), str(path.resolve()))
    except shutil.ReadError:
        archive_folder.rmdir()
        return
    except FileNotFoundError:
        archive_folder.rmdir()
        return
    path.unlink()


def remove_empty_folders(path):
    for item in path.iterdir():
        if item.is_dir():
            remove_empty_folders(item)
            try:
                item.rmdir()
            except OSError:
                pass


def get_folder_objects(root_path):
    for folder in root_path.iterdir():
        if folder.is_dir():
            remove_empty_folders(folder)
            try:
                folder.rmdir()
            except OSError:
                pass

def main(folder_path):
    scan.scan(folder_path)

    for file in scan.image:
        hande_file(file, folder_path, "IMAGE")

    for file in scan.video:
        hande_file(file, folder_path, "VIDEO")

    for file in scan.Documents:
        hande_file(file, folder_path, "DOCUMENTS")

    for file in scan.music:
        hande_file(file, folder_path, "MUSIC")

    

    for file in scan.others:
        hande_file(file, folder_path, "OTHERS")

    for file in scan.archives:
        handle_archive(file, folder_path, "ARCHIVE")

    get_folder_objects(folder_path)



if __name__ == '__main__':
    path = sys.argv[1]
    print(f"Start in {path}")

    arg = Path(path)
    main(arg)
    