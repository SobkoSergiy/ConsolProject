#from datetime import date, datetime
from Fields import Tagname


class Note:
    def __init__(self, key):
        self.key = Tagname(key)
        self.text = "" 
        self.tags = []
    
    def __str__(self):
        return f">>> Key: [{self.key.value}]  tags: {'; '.join(self.tags)}\nText: {self.text}"

    def index_tag(self, tag: str) -> int:
        i = 0
        while i < len(self.tags):     
            if self.tags[i] == tag.lower(): 
                return i
            i += 1
        return -1  

    def add_tag(self, newtag):
        if self.index_tag(newtag) > -1:  # if self.phones.count(np) == 0:  
            raise ValueError(f"ERROR: this tag '#{newtag}' already exists")
        else:    
            self.tags.append(newtag)

    def edit_tag(self, oldtag, newtag):
        if self.index_tag(newtag) > -1: 
            raise ValueError(f"ERROR: this tag '#{newtag}' already exists")
        if (i := self.index_tag(oldtag)) > -1:
            self.tags[i] = newtag
        else:
            raise ValueError(f"ERROR: tag '#{oldtag}' does not exists")   
        
    def remove_tag(self, tag):
        if len(self.tags) <= 1:
            raise ValueError(f"ERROR: can't delete last tag '#{tag}'") 
        if (i := self.index_tag(tag)) > -1:
            del(self.tags[i])
        else:
            raise ValueError(f"ERROR: tag '#{tag}' does not exists")  

    def set_key(self, value):
        self.key.value = value.lower()

    def set_text(self, text):
        self.text = text

    def app_text(self, text):
        self.text += (("" if text[-1] == ' ' else " ") + text)


class Notes:
    def __init__(self):
        self.notes = []  # list(Note())

    def find_note(self, key) -> Note: # == get(name)
        for n in self.notes:
            if n.key == key.lower():
                return n
        return None    
    
    def sort_notes(self):
        self.notes.sort(key=lambda key: key.value)

    def show_notes(self):    
        print("nl.show_note")
        for i in self.notes:
            print(i) 

    def add_note(self, key):
        self.notes.append(Note(key))

    def del_note(self, key):
        if (t:= self.find_note(key)):
            self.notes.remove(t)
        else:
            raise ValueError(f"ERROR: key '{key}' not found")
    
    def edit_key(self, key, newkey):
        if (t := self.find_note(key)):
            t.set_key(newkey)
        else:
            raise ValueError(f"ERROR: key '{key}' not found")
        

    def show_tags(self):
        for i in self.notes:
            print(f"[{i.key.value}]"+ '; #'.join(t for t in i.tags))    
                
    def add_tag(self, key, newtag):
        if (t := self.find_note(key)):
            t.add_tag(newtag)
        else:
            raise ValueError(f"ERROR: key '{key}' not found")       
            
    def del_tag(self, key, tag): 
        if (t := self.find_note(key)):
            t.remove_tag(tag) 
        else:
            raise ValueError(f"ERROR: key '{key}' not found")

    def edit_tag(self, key, oldtag, newtag):
        if (t := self.find_note(key)):
            t.edit_tag(oldtag, newtag)
        else:
            raise ValueError(f"ERROR: key '{key}' not found")
 
    def find_tag(self, tag):
        for i in self.notes:
            if i.index_tag(tag) > -1:
                print(i)


    def set_text(self, key, text):
        if ( t:= self.find_note(key)):
            t.set_text(text)
        else:
            raise ValueError(f"ERROR: key '{key}' not found")

    def add_text(self, key, text):
        if ( t:= self.find_note(key)):
            t.app_text(text)
        else:
            raise ValueError(f"ERROR: key '{key}' not found")

    def find_text(self, text):
        for i in self.notes:
            if text in i.text:
                print(i)        


    def save(self, filename): 
        with open(filename, "w") as f:
            for n in self.notes:
                f.write(f"{n.key.value}|{n.text}")
                for t in n.tags:
                    f.write(f"|{t}")
                f.write("\n")    
                
    def load(self, filename):
        with open(filename, "r") as f:
            raws = f.readlines()
            for raw in raws:
                l = raw[:-1].split("|")
                #print(l)
                n = Note(l[0])
                n.text = l[1]
                for i in range(2, len(l)):
                    n.tags.append(l[i]) 
                self.notes.append(n)


if __name__ == '__main__':
    def main_modul():
        pass

    main_modul()
