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
