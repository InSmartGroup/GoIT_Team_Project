from collections import UserDict
from datetime import datetime
from pickle import load, dump
from pathlib import Path
import re


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        filename = 'address_book.bin'
        if Path(filename).exists():
            with open(filename, 'rb') as file:
                self.data = load(file)

    def add_record(self, Record):
        self.data[Record.name.value] = Record

    def iterator(self, n_records):
        page = dict()
        i = 0
        for name, record in self.data.items():
            page[name] = record
            i += 1
            if i == n_records:
                yield page
                page = dict()
                i = 0
        if page:
            yield page


class Record:
    def __init__(self, Name, Birthday=None, Email=None, Address=None):
        self.name = Name
        self.phones = []
        self.birthday = Birthday
        self.email = Email
        self.address = Address

    def add_phone(self, Phone):
        self.phones.append(Phone)

    def remove_phone(self, Rem_Phone):
        for Phone in self.phones:
            if Phone.value == Rem_Phone.value:
                self.phones.remove(Phone)

    def change_phone(self, Old_Phone, New_Phone):
        for Phone in self.phones:
            if Phone.value == Old_Phone.value:
                self.phones.remove(Phone)
                self.phones.append(New_Phone)

    def add_birthday(self, Birthday):
        self.birthday = Birthday

    def add_email(self, Email):
        self.email = Email

    def add_address(self, Address):
        self.address = Address

    def days_to_birthday(self):
        birthday = datetime.strptime(self.birthday.value, '%Y-%m-%d').date()
        today = datetime.now().date()
        birthday = birthday.replace(year=today.year)
        if birthday < today:
            birthday = birthday.replace(year=today.year + 1)
        return (birthday - today).days


class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):
    pass


class Phone(Field):

    @Field.value.setter
    def value(self, value):
        if value.startswith('+') and len(value[1:]) == 12 and value[1:].isdigit() or value.isdigit() and len(value) in (
                10, 12):
            self._value = value
        else:
            raise PhoneInvalidFormatError('Invalid phone format')


class Birthday(Field):

    @Field.value.setter
    def value(self, value):
        today = datetime.now().date()
        try:
            birthday = datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError:
            birthday = None
        if birthday is not None and birthday < today:
            self._value = value
        else:
            raise BirthdayInvalidFormatError('Invalid birthday format')

class Email(Field):

    @Field.value.setter
    def value(self, value):
        pattern = r"[A-Za-z][A-Za-z0-9._]+@[A-Za-z]+\.[A-Za-z]{2,}"
        if re.match(pattern, value) is not None:
            self._value = value
        else:
            raise EmailInvalidFormatError('Invalid email format')

class Address(Field):
    pass

class PhoneInvalidFormatError(Exception):
    pass

class BirthdayInvalidFormatError(Exception):
    pass

class EmailInvalidFormatError(Exception):
    pass

address_book = AddressBook()

def parse(user_input):
    """
    This function parse user input into command and arguments
    :param user_input: user input -> str
    :return: command -> str, args -> list
    """
    user_input_list = user_input.split(' ')
    command = user_input_list[0]
    args = user_input_list[1:]
    return (command, args)

def input_error(func):
    """
    This is a decorator function that catches errors that may occur when calling a function given as a parameter
    :param func -> function
    :return func if no error, str if there's an error
    """
    def inner(*args):
        try:
            return func(*args)
        except KeyError:
            return 'The name is not in contacts. Enter user name please'
        except ValueError:
            return 'ValueError: Give me name and phone please'
        except IndexError:
            return 'IndexError: Give me name and phone please'
        except TypeError:
            return 'You entered invalid numbers of arguments for this command'
        except PhoneInvalidFormatError:
            return 'You entered invalid phone format'
        except BirthdayInvalidFormatError:
            return 'You entered invalid birthday format'
        except EmailInvalidFormatError:
            return 'You entered invalid email format'
    return inner

@input_error
def add_contact(name, phone=None, birthday=None):
    """
    This function add the new phone and birthday (if they are given) for contact with the name that are given
    as parameters in the address_book. If the name is not in contacts, then creates a new record in address_book
    :param name -> str
           phone -> str
           birthday -> str
    :return str
    """
    if name in address_book.data.keys():
        if phone is None:
            return f'A contact with name {name} already exists'
        else:
            address_book.data[name].add_phone(Phone(phone))
            if birthday is None:
                return f'Phone {phone} successfully added to contact {name}'
            else:
                address_book.data[name].add_birthday(Birthday(birthday))
                return f'Phone {phone} and birthday {birthday} successfully added to contact {name}'
    else:
        if phone is None:
            record = Record(Name(name))
            address_book.add_record(record)
            return f'Contact {name} successfully added'
        else:
            if birthday is None:
                record = Record(Name(name))
                record.add_phone(Phone(phone))
                address_book.add_record(record)
                return f'Contact {name} -> {phone} successfully added'
            else:
                record = Record(Name(name), Birthday(birthday))
                record.add_phone(Phone(phone))
                address_book.add_record(record)
                return f'Contact {name} -> {phone} -> {birthday} successfully added'

@input_error
def add_birthday(name, birthday):
    """
    This function add the birthday for contact with the name that are given as parameters in the address_book
    :param name -> str
           birthday -> str
    :return str
    """
    address_book.data[name].add_birthday(Birthday(birthday))
    return f'The birthday {birthday} for contact {name} successfully added'

@input_error
def add_email(name, email):
    """
    This function add the email for contact with the name that are given as parameters in the address_book
    :param name -> str
           email -> str
    :return str
    """
    address_book.data[name].add_email(Email(email))
    return f'The email {email} for contact {name} successfully added'

@input_error
def add_address(name, address):
    """
    This function add the address for contact with the name that are given as parameters in the address_book
    :param name -> str
           address -> str
    :return str
    """
    address_book.data[name].add_address(Address(address))
    return f'The address {address} for contact {name} successfully added'

@input_error
def change_contact(name, old_phone, new_phone):
    """
    This function change the phone for contact with the name that are given as parameters in the address_book
    :param name -> str
           old_phone -> str
           new_phone -> str
    :return str
    """
    address_book.data[name].change_phone(Phone(old_phone), Phone(new_phone))
    return f'Contact {name} -> {new_phone} successfully changed'

@input_error
def remove_phone(name, phone):
    """
    This function remove the phone for contact with the name that are given as parameters in the address_book
    :param name -> str
           phone -> str
    :return str
    """
    address_book.data[name].remove_phone(Phone(phone))
    return f'The phone {phone} for contact {name} successfully removed'

@input_error
def get_phone(name):
    """
    This function returns the phone or phones for contact with the name that is given as a parameter in the address_book
    :param name -> str
    :return phone -> str
    """
    if not address_book.data[name].phones:
        return f'There is no phones for contact with name {name}'
    else:
        phones = 'phones:\n'
        for phone in address_book.data[name].phones:
            phones += f'{phone.value}\n'
        return f'{name} ->\n{phones}'

@input_error
def get_birthday(name):
    """
    This function returns the birthday for contact with the name that is given as a parameter in the address_book
    :param name -> str
    :return birthday -> str
    """
    birthday = address_book.data[name].birthday
    if birthday is None:
        return f'There is no birthday for contact with name {name}'
    else:
        return f'{name} ->\n--birthday:\n{birthday.value}\n--days to birthday:\n{address_book.data[name].days_to_birthday()}\n\n'

@input_error
def get_email(name):
    """
    This function returns the email for contact with the name that is given as a parameter in the address_book
    :param name -> str
    :return email -> str
    """
    email = address_book.data[name].email
    if email is None:
        return f'There is no email for contact with name {name}'
    else:
        return f'{name} ->\n--email:\n{email.value}\n\n'

