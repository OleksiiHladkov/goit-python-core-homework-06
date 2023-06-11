import sys
from pathlib import Path


CATEGORIES = {"images": ["JPEG", "PNG", "JPG", "SVG"], 
              "video": ["AVI", "MP4", "MOV", "MKV"],
              "documents": ["DOC", "DOCX", "TXT", "PDF", "XLSX", "PPTX"],
              "audio": ["MP3", "OGG", "WAV", "AMR"],
              "archives": ["ZIP", "GZ", "TAR"],
              "other": []}


def get_category(path: Path) -> str:
    category = "other"
    
    suffix = path.suffix.replace(".", "").upper()
    
    for cat, ext in CATEGORIES.items():
        if suffix in ext:
            category = cat

    return category

def normalized(name: str) -> str:
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    
    BAD_SYMBOLS = ["#", "%", "&", "{", "}", "\\", "\<", "\>", "\*", "\?", "", " ", "$", "\!", "\"", "\'", ":", "@", "+", "|", "="]

    TRANS = {}

    for c, t in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = t
        TRANS[ord(c.upper())] = t.upper()

    def translate(name: str) -> str:
        new_name = ''

        for i in name:
            new_name += TRANS.get(ord(i), i if i not in BAD_SYMBOLS else "_")

        return new_name
    
    return translate(name)


def moove_file(root_dir: Path, path: Path, category: str) -> None:
    target_dir = root_dir.joinpath(category)
    
    if not target_dir.exists():
        target_dir.mkdir()
    
    path.replace(target_dir.joinpath(normalized(path.stem) + path.suffix))


def process_files(root_dir: Path):
    structure = root_dir.glob("**\*")

    for path in structure:
        if path.is_file() and path.parent.name not in CATEGORIES:
            category = get_category(path)
            moove_file(root_dir, path, category)


def main():
    try:
        root_dir_str = sys.argv[1]
        root_dir = Path(root_dir_str)
    except:
        print(f"You mast enter parameter 'path to folder'. Command example: python {sys.argv[0]} [pathToFolder]")
        return False
    
    if not root_dir.exists():
        print(f"Path to folder {root_dir_str} is not exists")
    process_files(root_dir)



if __name__ == "__main__":
    main()