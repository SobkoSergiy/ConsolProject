from datetime import date, datetime, timedelta
from collections import UserDict
from Fields import Address, Birthday, Email, Phone, Name


class Phones:
    def __init__(self):
        self.data = []   

    def index_phone(self, phone: str) -> int:
        i = 0
        while i < len(self.data):     
            if self.data[i].value == phone: 
                return i
            i += 1
        return -1  

    def add_phone(self, newphone: str):
        self.data.append(Phone(newphone))

    def edit_phone(self, oldphone: str, newphone: str):
        indx = self.index_phone(self, oldphone)
        if indx > -1:
            self.data[indx] = Phone(newphone)
        else:
            self.add_phone(newphone) 

    def remove_phone(self, phone):
        indx = self.index_phone(self, phone)
        if indx > -1:
            self.data.pop(indx)  # del self.data[indx]


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.birthday = Birthday() 
        self.email = Email() 
        self.address = Address()
        self.phones = Phones()
    
    def __str__(self):
        bd = (", birthday: " + self.birthday.value if self.birthday.value else " ")
        ph = (", phones: "+'; '.join(p.value for p in self.phones.data) if len(self.phones.data) > 0 else ' ')
        return f"Contact name: {self.name.value:12}{bd:22}{ph}"

    def add_phone(self, newphone):
        if self.phones.index_phone(newphone) > -1:  
            raise ValueError(f"ERROR: this number {newphone} already exists")
        else:     
            self.phones.add_phone(newphone)

    def edit_phone(self, oldphone, newphone):
        if self.phones.index_phone(newphone) > -1:
            raise ValueError(f"ERROR: this number {newphone} already exists")
        if self.phones.index_phone(oldphone) < 0:
            raise ValueError(f"ERROR: phone number '{oldphone}' does not exists")  
        self.phones.edit_phone(oldphone, newphone)
 
    def remove_phone(self, phone):
        if self.phones.index_phone(phone) < 0:
            raise ValueError(f"ERROR: phone number '{phone}' does not exists") 
        self.phones.remove_phone(phone)

    def set_birthday(self, value):
        self.birthday.value = value

    def days_to_birthday(self) -> int:
        if not self.birthday.value:
            return -1
        bday = date.strptime(self.birthday.value, '%d-%m-%Y')
        today = date.today()    # today datetime.date(2007, 12, 5)
        bday = bday.replace(year = today.year)
        if bday < today:
            bday = bday.replace(year = today.year + 1)  
        return (bday - today).days     

    def set_email(self, value):
        self.email.value = value

    def set_address(self, value):
        self.address.value = value


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()    
        self.data = {}        
        self.start = 0

    def show_records(self):
        for record in self.data.values():
            print(record)    
                
    def find_record(self, name) -> Record: # == get(name)
        name = name.capitalize()
        return self.data[name] if name in self.data.keys() else None

    def add_record(self, newrec):
        self.data[newrec.name.value] = newrec
            
    def delete_record(self, name):
        if self.find_record(name):
            del(self.data[name]) 
        else:
            raise ValueError(f"ERROR: name '{name}' not found")

    def edit_recname(self, oldname, newname):
        r = self.find_record(oldname)
        r.name.value = newname
 
    def edit_recphon(self, name, oldphone, newphone):
        r = self.find_record(name)
        r.edit_phone(oldphone, newphone)
 
    def find_namepart(self, namepart):
        for key in self.data.keys():
            name = key.lower()
            if namepart in name:
                print(self.data[key])

    def find_phonpart(self, phonepart):
        for key, rec in self.data.items():
            for p in rec.phones.data:
                if phonepart in p.value:
                    print(self.data[key])

 
    def save(self, filename): 
        with open(filename, "w") as f:
            for rec in self.data.values():
                f.write(f"{rec.name.value}|{rec.birthday.value}|{rec.email.value}|{rec.address.value}")
                for p in rec.phones.data:
                    f.write(f"|{p.value}")
                f.write("\n")    
                
    def load(self, filename):
        with open(filename, "r") as f:
            raws = f.readlines()
            for raw in raws:
                al = raw[:-1].split("|")
                # print(al)
                rec = Record(al[0]) 
                rec.birthday = Birthday()  
                rec.birthday.value = al[1]  
                rec.email = Email() 
                rec.email.value = al[2]
                rec.address = Address()
                rec.address.value = al[3]
                for i in range(4, len(al)):
                    rec.phones.add_phone(al[i]) 
                self.add_record(rec)

    def yield_gen(self, start = 0):
        num = start
        while True:
            print(list(self.data.values())[num])
            yield num
            num += 1

    def iter_rec(self, pos, quan):
        c = self.yield_gen(pos)
        i = 0
        end = min(pos + quan, len(self.data))
        while i < (end - pos):
            try:
                next(c)
            except StopIteration:
                break    
            i += 1    
        return pos+i

    
    def get_birthdays_per_week(self, users):
        week_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        cur_date = date.today()   # value.strftime('%A %d %B %Y')
        print(f"{cur_date=}  {cur_date.weekday()}:{week_list[cur_date.weekday()]}")
        delta = timedelta(days=1)
        def select_users(day, month):
            ul = []
            for u in users:
                bd = u.birthday.value
                if bd:
                    bdate = datetime.strptime(bd, '%d-%m-%Y')
                    if ((bdate.month == month) and (bdate.day == day)):
                        ul.append(u.name.value)
            return ul
        def print_wl(wl, wd):
            if len(wl) > 0:
                print(week_list[wd]+": "+', '.join(wl))
        def create_wlist():
            wl = []
            for cd in range(7):
                d = cur_date + delta * cd
                wl.extend(select_users(d.day, d.month))
                print(f"weekday:{d.weekday()} -> {week_list[d.weekday()]}")
                print_wl(wl, d.weekday())
                wl.clear()
        create_wlist()

    def week_func(self, cl):    # weekb : birthdays on weekdays in the coming week
        self.get_birthdays_per_week(self.data.values())


    def untilbday_func(self, name): # daysb name : calculate how many days until the birthday
        rec = self.find_record(name)
        if not rec:
            raise ValueError(f"ERROR: name '{name}' not found")
        days = rec.days_to_birthday()
        if days < 0:
            raise ValueError(f"ERROR: name '{name}': birthday not specified")
        print(f"{name}: days for bithday - {days}")

    def bdayafter_func(self, n): # showbday n : contact list with birthday after n days
        for rec in self.data:
            if rec.days_to_birthday() == n:
                print(rec)


if __name__ == '__main__':

    def main_modul():
        pass
    main_modul()
