
def print_hello():
    print("Hello !")
    print("I'm a console bot, a few words about me:")
    print("I can add, edit, delete and show text and tags in the note list.")
    print("I can add, edit, delete, view, find and sort entries in the address book.")
    print("Each entry corresponds to one person and contains information") 
    print("about his birthday, address, phone numbers, email and a text note")
    print("Detailed information on the command 'help' or '?'") 
    print("How can I help you?")

def system_help():
    print("\n>>> general commands")
    print("?, help : this list")
    print("helpcont : contacts commands list")
    print("helpnote : notes and tags commands list")
    print("goodbye, close, exit : exit program")
    print("foldersort folder : sort and clean files in folder")

def contacts_help():
    print("\n>>> contacts commands")
    print("showcont : show all records")
    print("showcont n : show n contacts at a time")
    print("addcont name : add contact with name")
    print("addcont name number : add contact with name and phone number")
    print("delcont name : delete name's contact")
    print("editcont oldname newname : change contact's name")
    print("findcont namepart : search by part of the contact's name")
    print("setbday name dd-mm-yyyy : set name's birthday or '' to empty birthday")
    print("showbday name : calculate how many days left until the birthday")
    print("showbday week : birthdays on weekdays in the coming week")
    print("showbday n : contact list with birthday after n days")
    print("setemail name email : set name's email or '' to empty email" )
    print("addphone name number : add phone number to contact")
    print("delphone name number : delete phone number from contact")
    print("editphone name oldnumber newnumber : change number for name")
    print("findphone numberpart : search for contacts by part of the phone number")

def notes_help():
    print("\n>>> notes and tags commands")
    print("shownote : show all notes")
    print("sortnote : sort all notes by their keytags")
    print("addnote keytag : create a new note with keytag" )
    print("delnote keytag : delete a note with keytag" )
    print("editkey keytag newkeytag: change note's keytag to newkeytag")

    print("showtag : show only all tags by all notes")
    print("addtag keytag tag : add tag to note with keytag")
    print("deltag keytag tag : delete tag from note with keytag")
    print("edittag keytag oldtag newtag : change oldtag to newtag in note with keytag")
    print("findtag tag : find all notes with tag")

    print("settext keytag text: set text to note with keytag or '' to empty text")
    print("addtext keytag text: append text to note with keytag")

    print("findtext text : search for notes with text")
    
    
def general_help():
    system_help()
    contacts_help()
    notes_help()






