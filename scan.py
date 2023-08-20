import sys
from pathlib import Path



image = list()
music = list()
video = list()
Documents = list()

folders = list()
archives = list()
others = list()
unknown = set()
extensions = set()

#зображення ('JPEG', 'PNG', 'JPG', 'SVG');
#Відео файли ('AVI', 'MP4', 'MOV', 'MKV');
#документи ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX');
#музика ('MP3', 'OGG', 'WAV', 'AMR');
#архіви ('ZIP', 'GZ', 'TAR');





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


if __name__ == '__main__':
    path = sys.argv[1]
    print(f"Start in {path}")

    arg = Path(path)
    scan(arg)

    print(f"image: {image}\n")
    print(f"music: {music}\n")
    print(f"video: {video}\n")
    print(f"Documents: {Documents}\n")
    print(f"archive: {archives}\n")
    print(f"unknown: {others}\n")
    print(f"All extensions: {extensions}\n")
    print(f"Unknown extensions: {unknown}\n")