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

@input_error
def get_address(name):
    """
    This function returns the address for contact with the name that is given as a parameter in the address_book
    :param name -> str
    :return address -> str
    """
    address = address_book.data[name].address
    if address is None:
        return f'There is no address for contact with name {name}'
    else:
        return f'{name} ->\n--address:\n{address.value}\n\n'

@input_error
def show_all(data=address_book.data):
    """
    This function returns all contact from the given data. If data is not given then data = address_book
    :param: data -> dict
    :return: phone_book -> str
    """
    phone_book = ''
    for name, info in data.items():
        phones = '--phones:\n'
        if data[name].phones:
            for phone in data[name].phones:
                phones += f'{phone.value}\n'
        else:
            phones += 'no phones\n'
        phone_book += f'\n{name} ->\n{phones}'
        birthday = data[name].birthday
        if birthday is not None:
            phone_book += f'--birthday:\n{birthday.value}\n--days to birthday:\n{data[name].days_to_birthday()}\n'
        email = data[name].email
        if email is not None:
            phone_book += f'--email:\n{email.value}\n'
        address = data[name].address
        if address is not None:
            phone_book += f'--address:\n{address.value}\n'
    return phone_book

@input_error
def show_page(page_to_show, n_records='3'):
    """
    This function returns contacts from address_book from given page number (given as a parameter page_to_show)
    with number of records on each page that is given as a parameter n_records
    :param: page_to_show -> str
            n_records -> str
    :return: phone_book -> str
    """
    page_num = 1
    for page in address_book.iterator(int(n_records)):
        if page_num == int(page_to_show):
            return f'page {page_num}\n{show_all(page)}'
        page_num += 1

@input_error
def search_contact(pattern):
    """
    This function returns contacts from address_book whose name or phone number matches the entered string
    given as a parameter pattern
    :param: pattern -> str
    :return: result -> str
    """
    result = dict()
    for name, record in address_book.data.items():
        if name.lower().find(pattern.lower()) != -1:
            result[name] = record
        elif record.phones:
            for phone in record.phones:
                if phone.value.find(pattern) != -1:
                    result[name] = record
    if result:
        return show_all(result)
    else:
        return f'There are no contacts with {pattern}'

def greeting():
    return 'How can I help you?'

def end():
    return 'Good bye!'

def write_file():
    filename = 'address_book.bin'
    with open(filename, 'wb') as file:
        dump(address_book.data, file)

def main():
    """
    This function implements all the logic of interaction with the user, all 'print' and 'input' takes place here
    :param: None
    :return: None
    """
    handler_commands = {'hello': greeting,
                        'hi': greeting,
                        'add': add_contact,
                        'add_birthday': add_birthday,
                        'add_email': add_email,
                        'add_address': add_address,
                        'change': change_contact,
                        'phone': get_phone,
                        'get_birthday': get_birthday,
                        'get_email': get_email,
                        'get_address': get_address,
                        'search': search_contact,
                        'remove': remove_phone,
                        'show all': show_all,
                        'show_page': show_page,
                        '.': end,
                        'good bye': end,
                        'close': end,
                        'exit': end}

    while True:
        user_input = input('>>>:')
        if user_input.lower() in handler_commands.keys():
            output = handler_commands[user_input.lower()]()
            print(output)
            if output == 'Good bye!':
                write_file()
                exit()
        else:
            command, args = parse(user_input.lower())
            if command in handler_commands.keys():
                print(handler_commands[command](*args))
            else:
                print(
                    "You entered an invalid command, please enter one of the next commands: "
                    "'hello', 'hi', 'show all', 'show_page', 'add', 'add_birthday', 'add_email', 'add_address', 'change',"
                    " 'phone', 'get_birthday', 'get_email', 'get_address', 'search', 'delete', '.', 'good bye', 'close', 'exit'")


if __name__ == '__main__':
    main()

