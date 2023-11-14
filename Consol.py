from pathlib import Path
from FolderSort import foldersort
from HelpInfo import print_hello, general_help, contacts_help, notes_help, system_help
from Contacts import Record, AddressBook  
from Notes import Notes


def help_func(nb, cl):
    general_help()

def helpcont_func(nb, cl):
    system_help()
    contacts_help()

def helpnote_func(nb, cl):
    system_help()
    notes_help()

def exit_func(nb, cl):
    raise RuntimeError("Good bye!")


def showcont_func(nb, cl):  # showall : show all records
    if len(nb) == 0:
        raise ValueError("ERROR: dictionary is empty yet")
    if len(cl) == 1:
        print(f"total {len(nb.data)} records")
        for record in nb.data.values():
            print(record)
    if len(cl) == 2:
        iter_func(nb, cl)       

def iter_func(nb, cl):    # show n : show n records at a time
    if (len(cl) < 2) or (not cl[1].isnumeric()) or ((quan := int(cl[1])) < 1):
        raise ValueError("ERROR: command 'showcont n' wrong parameter n")
    nb.start = nb.iter_rec(nb.start, quan)
    if nb.start == len(nb.data):
        nb.start = 0
   

def addcont_func(nb, cl):   # add name number : add record with name and telephon number
    if len(cl) < 2:
        raise ValueError("ERROR: command 'addcont' wrong parameters")
    rec = nb.find_record(cl[1])
    if rec:
        if len(cl) > 2:
            rec.add_phone(cl[2])
    else:
        rec = Record(cl[1])
        if len(cl) > 2:
            rec.add_phone(cl[2])
    nb.add_record(rec)
 
def delcont_func(nb, cl):   # del name : delete name's record
    if len(cl) < 2:
        raise ValueError("ERROR: command 'del' wrong parameters")
    nb.delete_record(cl[1])

def editcont_func(nb, cl):   # change cont oldname newname : change name for contact
    if len(cl) < 2:
        raise ValueError("ERROR: command 'editcont' wrong parameters")
    nb.edit_record(cl[1], cl[2])

def findcont_func(nb, cl):  # findname namepart : search for phones by part of the name
    if (len(cl) < 2) or (not cl[1].isalpha()):
        raise ValueError("ERROR: command 'findcont' wrong parameters")
    nb.find_namepart(cl[1])


def setbday_func(nb, cl):  # setb name dd-mm-yyyy : set name's birthday
    if len(cl) < 3:
        raise ValueError("ERROR: command 'setbday' wrong parameters")
    rec = nb.find_record(cl[1])
    if not rec:
        raise ValueError(f"ERROR: name '{cl[1]}' not found")
    rec.set_birthday(cl[2])
    
def showbday_func(nb, cl):
    if len(cl) < 2:
        raise ValueError("ERROR: command 'showbday' wrong parameters")
    if cl[1] == 'week':
        nb.week_func(cl)
    elif cl[1].isalpha():
        nb.untilbday_func(cl[1])
    else:
        if (not cl[1].isnumeric()) or (not (0 < (quan := int(cl[1])) < 365)):
            raise ValueError("ERROR: command 'showcont n' wrong parameter n")
        nb.bdayafter_func(quan)

def setaddr_func(nb, cl):  
    if len(cl) < 2:
        raise ValueError("ERROR: command 'setaddr' wrong parameters")
    rec = nb.find_record(cl[1])
    if not rec:
        raise ValueError(f"ERROR: name '{cl[1]}' not found")
    rec.set_address(cl[2])

def setemail_func(nb, cl):  
    if len(cl) < 2:
        raise ValueError("ERROR: command 'setaddr' wrong parameters")
    rec = nb.find_record(cl[1])
    if not rec:
        raise ValueError(f"ERROR: name '{cl[1]}' not found")
    rec.set_email(cl[2])


def delphone_func(nb, cl): # phone name : show name's telephon number
    if len(cl) < 3:
        raise ValueError("ERROR: command 'delphone' wrong parameters")
    rec = nb.find_record(cl[1])
    if not rec:
        raise ValueError(f"ERROR: name '{cl[1]}' not found")
    rec.remove_phone(cl[2])

def editphone_func(nb, cl):    # change name oldnumber newnumber : change number for name
    if len(cl) < 4:
        raise ValueError("ERROR: command 'editphone' wrong parameters")
    nb.edit_record(cl[1], cl[2], cl[3])

def findphone_func(nb, cl):    # findph numberpart : search for names by part of the phone number
    if (len(cl) < 2) or (not cl[1].isnumeric()):
        raise ValueError("ERROR: command 'findphone' wrong parameters")
    nb.find_phonpart(cl[1])


def sortnote_func(nl, cl):
    nl.sort_notes()

def shownote_func(nl, cl):
    print("shownote_func")
    nl.show_notes()

def addnote_func(nl, cl):   # newnote keytag : create a new note with keytag
    if len(cl) < 2:
        raise ValueError("ERROR: command 'addnote' wrong parameters")
    nl.add_note(cl[1])

def delnote_func(nl, cl):   # newnote keytag : create a new note with keytag
    if len(cl) < 2:
        raise ValueError("ERROR: command 'delnote' wrong parameters")
    nl.del_note(cl[1])

def editkey_func(nl, cl): # 
    if (len(cl) < 3):
        raise ValueError("ERROR: command 'editkey' wrong parameters")
    nl.edit_key(cl[1], cl[2])


def showtag_func(nl, cl):
    nl.show_tags()
    
def addtag_func(nl, cl):    # addtag keytag tag : add tag to note with keytag
    if (len(cl) < 3):
        raise ValueError("ERROR: command 'addtag' wrong parameters")
    nl.add_tag(cl[1], cl[2])

def deltag_func(nl, cl):    # deltag keytag tag : delete tag from note with keytag
    if (len(cl) < 3):
        raise ValueError("ERROR: command 'deltag' wrong parameters")
    nl.del_tag(cl[1], cl[2])

def edittag_func(nl, cl): # edittag keytag oldtag newtag : change oldtag to newtag in note with keytag
    if (len(cl) < 4):
        raise ValueError("ERROR: command 'edittag' wrong parameters")
    nl.edit_tag(cl[1], cl[2], cl[3])

def findtag_func(nl, cl):
    if len(cl) < 2:
        raise ValueError("ERROR: command 'findtag' wrong parameters")
    nl.find_tag(cl[1])


def settext_func(nl, cl):   # addnote keytag : append text to note with keytag
    if len(cl) < 3:
        raise ValueError("ERROR: command 'settext' wrong parameters") 
    nl.set_text(cl[1], ' '.join(cl[2:]))

def addtext_func(nl, cl):   # addnote keytag : append text to note with keytag
    if len(cl) < 3:
        raise ValueError("ERROR: command 'addtext' wrong parameters")
    nl.add_text(cl[1], ' '.join(cl[2:]))

def findtext_func(nl, cl):  # findtext text : search for notes with text
    if len(cl) < 2:
        raise ValueError("ERROR: command 'findtext' wrong parameters")
    nl.find_text(cl[1])

OPERATIONS = {
    'help': help_func,
    '?': help_func,
    'helpcont' : helpcont_func,
    '?cont' : helpcont_func,
    'helpnote' : helpnote_func,
    '?note' : helpnote_func,
    'exit': exit_func,
    'goodbye': exit_func,
    'close': exit_func,
    'foldersort': foldersort
}
OPERATIONSC = {
    'showcont': showcont_func,
    'addcont': addcont_func,
    'delcont': delcont_func,
    'editcont': editcont_func,
    'findcont': findcont_func,
    'setbday': setbday_func,
    'showbday': showbday_func,
    'setaddr': setaddr_func,
    'setemail': setemail_func,
    'addphone': addcont_func,
    'delphone': delphone_func,
    'editphone': editphone_func,
    'findphone': findphone_func
}
OPERATIONSN = {
    'shownote': shownote_func,
    'sortnote': sortnote_func,
    'addnote': addnote_func,
    'delnote': delnote_func,
    'editkey': editkey_func,
    'showtag': showtag_func,
    'addtag': addtag_func,
    'deltag': deltag_func,
    'edittag': edittag_func,
    'findtag': findtag_func,
    'settext': settext_func,
    'addtext': addtext_func,
    'findtext': findtext_func
}

def get_handler(nb, nl, operator):
    com_attr = operator.split()
    command = com_attr[0].lower()
    if command in OPERATIONS:
        OPERATIONS[com_attr[0]](nb, com_attr)
    elif command in OPERATIONSC:
        OPERATIONSC[com_attr[0]](nb, com_attr)
    elif command in OPERATIONSN:
        OPERATIONSN[com_attr[0]](nl, com_attr)
    else:
        raise ValueError(f"ERROR: unnown command '{operator}'. Type ? to get help")  


def main():
    print("\n\n>>><Consol 0.0.1>")

    file_dir = Path(__file__)
    
    namebook = AddressBook()
    contfile_txt = file_dir.parent/"contacts.txt"
    if contfile_txt.exists():
        namebook.load(contfile_txt)

    notelist = Notes()
    notefile_txt = file_dir.parent/"notes.txt"
    if notefile_txt.exists():
        notelist.load(notefile_txt)
            
    print_hello()
    while True:
        try:
            get_handler(namebook, notelist, input("\nEnter command, please (? to get help): \n>>>"))
        except ValueError as ve:
            print(ve)
        except RuntimeError  as re:
            print(re)
            break
    namebook.save(contfile_txt)
    notelist.save(notefile_txt)

if __name__ == "__main__":
    main()
