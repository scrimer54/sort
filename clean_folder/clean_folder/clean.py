import re
from pathlib import Path
import shutil
import sys




image = list()
music = list()
video = list()
Documents = list()

folders = list()
archives = list()
others = list()
unknown = set()
extensions = set()



UKRAINIAN_SYMBOLS = 'абвгдеєжзиіїйклмнопрстуфхцчшщьюя'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "je", "zh", "z", "y", "i", "ji", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "ju", "ja")


TRANS = {}

for key, value in zip(UKRAINIAN_SYMBOLS, TRANSLATION):
    TRANS[ord(key)] = value
    TRANS[ord(key.upper())] = value.upper()


def normalize(name):
    name, *extension = name.split('.')
    new_name = name.translate(TRANS)
    new_name = re.sub(r'\W', "_", new_name)
    return f"{new_name}.{'.'.join(extension)}"





registered_extensions = {
    'JPEG': image,
    'PNG': image,
    'JPG': image,
    'SVG': image,
    'AVI': video,
    'MP4': video,
    'MOV': video,
    'MKV': video,
    'DOC': Documents,
    'DOCX': Documents,
    'TXT': Documents,
    'PDF': Documents,
    'XLSX': Documents,
    'PPTX': Documents,
    'MP3': music,
    'OGG': music,
    'WAV': music,
    'AMR': music,
    'ZIP': archives,
    'GZ': archives,
    'TAR': archives
}


def get_extensions(file_name):
    return Path(file_name).suffix[1:].upper()


def scan(folder):
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ("IMAGE", "MUSIC", "VIDEO", "DOCUNENTS", "OTHER", "ARCHIVE"):
                folders.append(item)
                scan(item)
            continue

        extension = get_extensions(file_name=item.name)
        new_name = folder/item.name
        if not extension:
            others.append(new_name)
        else:
            try:
                container = registered_extensions[extension]
                extensions.add(extension)
                container.append(new_name)
            except KeyError:
                unknown.add(extension)
                others.append(new_name)



def hande_file(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)
    path.replace(target_folder/normalize(path.name))




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

def main():

    path = sys.argv[1]
    print(f"Start in {path}")

    folder_path = Path(path)
    scan(folder_path)

    for file in image:
        hande_file(file, folder_path, "IMAGE")

    for file in video:
        hande_file(file, folder_path, "VIDEO")

    for file in Documents:
        hande_file(file, folder_path, "DOCUMENTS")

    for file in music:
        hande_file(file, folder_path, "MUSIC")

    

    for file in others:
        hande_file(file, folder_path, "OTHERS")

    for file in archives:
        handle_archive(file, folder_path, "ARCHIVE")

    get_folder_objects(folder_path)



if __name__ == '__main__':
    path = sys.argv[1]
    print(f"Start in {path}")

    arg = Path(path)
    main(arg)