from collections import UserDict, UserList
from datetime import datetime
from pickle import load, dump
from pathlib import Path
import re


class DataTransfer:

    def __init__(self, filename):
        self.filename = filename

    def load_data(self):
        if Path(self.filename).exists():
            with open(self.filename, 'rb') as file:
                return load(file)
        return None

    def save_data(self, data):
        with open(self.filename, 'wb') as file:
            dump(data, file)


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        filename = 'address_book.bin'
        data_loader = DataTransfer(filename)
        loaded_data = data_loader.load_data()

        if loaded_data:
            self.data = loaded_data

    def save_data(self):
        data_saver = DataTransfer('address_book.bin')
        data_saver.save_data(self.data)

    def add_record(self, record):
        self.data[record.name.value] = record

    def del_record(self, name):
        del self.data[name]

    def iterator(self, n_records):
        page = {}
        i = 0
        for name, record in self.data.items():
            page[name] = record
            i += 1
            if i == n_records:
                yield page
                page = {}
                i = 0
        if page:
            yield page


class Record:
    def __init__(self, name, birthday=None, email=None, address=None):
        self.name = name
        self.phones = []
        self.birthday = birthday
        self.email = email
        self.address = address

    def add_phone(self, phone):
        self.phones.append(phone)

    def remove_phone(self, rem_phone):
        for phone in self.phones:
            if phone.value == rem_phone.value:
                self.phones.remove(phone)

    def add_birthday(self, birthday):
        self.birthday = birthday

    def add_email(self, email):
        self.email = email

    def add_address(self, address):
        self.address = address

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
        if value.startswith('+') and len(value[1:]) == 12 and value[1:].isdigit() or value.isdigit() and len(value) in \
                (10, 12):
            self._value = value
        else:
            raise PhoneInvalidFormatError('Invalid phone format. Please enter the phone in the format'
                                          ' +000000000000, 000000000000 or 0000000000')


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
            raise BirthdayInvalidFormatError('Invalid birthday format. Please enter the birthday'
                                             ' in the format YYYY-MM_DD')


class Email(Field):

    @Field.value.setter
    def value(self, value):
        pattern = r"[A-Za-z][A-Za-z0-9._]+@[A-Za-z]+\.[A-Za-z]{2,}"
        if re.match(pattern, value) is not None:
            self._value = value
        else:
            raise EmailInvalidFormatError('Invalid email format')


class Notes(UserList):

    def __init__(self):
        super().__init__()

        filename = 'note_book.bin'
        data_loader = DataTransfer(filename)
        loaded_data = data_loader.load_data()

        if loaded_data:
            self.data = loaded_data

    def save_data(self):
        data_saver = DataTransfer('note_book.bin')
        data_saver.save_data(self.data)

    def add_note(self, note):
        self.data.append(note)


class Note:

    def __init__(self, text, tags=None, title=None):
        self.text = text
        self.tags = tags
        self.title = title


class Address(Field):
    pass


class PhoneInvalidFormatError(Exception):
    pass


class BirthdayInvalidFormatError(Exception):
    pass


class EmailInvalidFormatError(Exception):
    pass


class NoteInputInvalidFormatError(Exception):
    pass


address_book = AddressBook()
note_book = Notes()
