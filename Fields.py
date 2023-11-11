from datetime import datetime
import re


class Field:
    def __init__(self):
        self.__value = ""

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        value = other.value if isinstance(other, Field) else other
        return self.value == value
    
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, newvalue): 
        self.validate(newvalue)
        self.__value = newvalue
    
    def validate(self, newvalue):
        raise NotImplemented("Field.validate") #pass


class Address(Field):
    def validate(self, newvalue):
        if newvalue != "" and (not newvalue.isalnum()):
            raise ValueError(f"ERROR: invalid letters in the address '{newvalue}'")


class Birthday(Field):
    def __str__(self):
        return (self.value if self.value else "")
    
    def validate(self, newvalue): 
        if newvalue:
            try:
                bd = datetime.strptime(newvalue, '%d-%m-%Y')
            except ValueError:
                raise ValueError(f"ERROR: date of birth '{newvalue}' is wrong")
            today = datetime.today()
            if bd > today:
                raise ValueError(f"ERROR: date of birth '{newvalue}' in the future")
            if (today.year - bd.year) > 120:
                raise ValueError(f"ERROR: date of birth '{newvalue}' is very ancient")
            

class Email(Field):
    def validate(self, newvalue):
        if newvalue:
            pattern = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$"
            # pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
            if re.match(pattern, newvalue) is None:
                raise ValueError(f"ERROR: invalid e-mail name: '{newvalue}'")


class Name(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value    
        
    def validate(self, newvalue):
        if (len(newvalue) <=2) or (len(newvalue) >=12):
            raise ValueError(f"ERROR: Name '{newvalue}' shoud be from 3 to 12 letters")
        if not newvalue.isalpha():
            raise ValueError(f"ERROR: invalid letters in the name '{newvalue}'")

class Tagname(Name):
    def validate(self, newvalue):
        if (len(newvalue) <=2) or (len(newvalue) >=12):
            raise ValueError(f"ERROR: Name '{newvalue}' shoud be from 3 to 12 letters")
        if not newvalue.isalnum():
            raise ValueError(f"ERROR: invalid letters in the name '{newvalue}'")


class Phone(Name):
    def __str__(self):
        return f"({self.value[0:3]}){self.value[3:6]}-{self.value[6:]}"

    def validate(self, newvalue):
        if len(newvalue) != 10:
            raise ValueError(f"ERROR: phone number '{newvalue}' must be 10 digits long")
        if not newvalue.isnumeric():
            raise ValueError(f"ERROR: phone number '{newvalue}' contains invalid characters")


if __name__ == '__main__':

    def main_modul():
        pass    
    
    main_modul()
