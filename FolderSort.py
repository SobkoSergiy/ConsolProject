import pathlib              
import shutil


suffix_dict = {
    'JPEG': 'images', 'PNG': 'images', 'JPG': 'images', 'SVG': 'images', 'BMP': 'images',
    'AVI': 'video', 'MP4': 'video', 'MOV': 'video', 'MKV': 'video',
    'DOC': 'documents', 'DOCX': 'documents', 'TXT': 'documents', 'PDF': 'documents', 
    'XLS': 'documents', 'XLSX': 'documents', 'PPTX': 'documents', 
    'MP3': 'audio', 'OGG': 'audio', 'WAV': 'audio', 'AMR': 'audio',
    'ZIP': 'archives', 'GZ': 'archives', 'TAR': 'archives',
}
files_dict = {'images': [], 'video': [], 'documents': [],
              'audio': [], 'archives': [], 'unknown': []}
known_suffix = set()
unknown_suffix = set()
folders_list = []


def write_dict(path):  # save files_dict, known_suffix, unknown_suffix
    with open(path / "FS_FileList.txt", 'w') as f:
        for categ in files_dict.keys():
            if len(files_dict[categ]) > 0:
                f.write(f'>>> {categ}\n')
                for file in files_dict[categ]:
                    f.write(f'{file}\n')  # f.write(f'{file.name}\n')

    with open(path / "FS_SuffixKnown.txt", 'w') as f:
        for suf in known_suffix:
            f.write(f'{suf}\n')

    with open(path / "FS_SuffixUnknown.txt", 'w') as f:
        for suf in unknown_suffix:
            f.write(f'{suf}\n')
    
    with open(path / "FS_FoldersList.txt", 'w') as f:
        for fold in folders_list:
            f.write(f'{len(fold.parts):2}  {fold}\n')


def normalize(name):
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s",
               "t", "u", "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    newname = ""
    for ch in name:
        newname += (ch if ch.isalnum() else '_')

    TRANS = {}
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.capitalize()

    return newname.translate(TRANS)

def select_file(path):  # fill files_dict() depending on category of file suffix
    suf = path.suffix[1:].upper()
    categ = suffix_dict.get(suf)    
    if categ:
        files_dict[categ].append(path)
        known_suffix.add(suf)
    else:
        files_dict['unknown'].append(path)
        unknown_suffix.add(suf)

def view_folder(path):  # view & preparing files & folders to further processing
    for file in path.iterdir():
        if file.is_dir():
            folders_list.append(file)
            view_folder(file) 
        else:
            select_file(file)
    folders_list.sort(key=lambda Path: len(Path.parts), reverse = True)
    
def check_folders(path):  # create & fill new folder for nonempty category
    for categ in files_dict.keys():
        if (categ != 'unknown') and (len(files_dict[categ]) > 0):      # not empty
            (path/categ).mkdir(exist_ok=True, parents=True)

def move_files(path):
    for categ in files_dict.keys():
        for file in files_dict[categ]:
            stem = normalize(file.stem)
            newname = (path/categ/(stem+file.suffix) if categ !='unknown' else file.parent/(stem+file.suffix))
            file.replace(newname)    # .replace(newname) doesn't need try..except


def unpack_archives(path):  # special remove archive files into archives folders
    archivpath = path/'archives'
    if archivpath.exists():
        for arch in archivpath.iterdir():
            shutil.unpack_archive(arch, archivpath/arch.stem)
            pathlib.Path.unlink(arch)


def foldersort(sortpath):
    if not sortpath:
        raise ValueError("ERROR: folder for sorting is not specified")   
    
    workpath = pathlib.Path(sortpath)
    if not workpath.exists():
        raise ValueError(f"ERROR: The folder specified for sorting '{workpath}' does not exist")

    view_folder(workpath)
    write_dict(workpath)

    check_folders(workpath)
    move_files(workpath)
    unpack_archives(workpath)
    

if __name__ == "__main__":
    foldersort("")
