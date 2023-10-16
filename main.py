from collections import UserDict, UserList
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

    def del_record(self, name):
        del self.data[name]

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
        if value.startswith('+') and len(value[1:]) == 12 and value[1:].isdigit() or value.isdigit() and len(value) in \
                (10, 12):
            self._value = value
        else:
            raise PhoneInvalidFormatError('Invalid phone format. Please enter the phone in the format'
                                          ' +xxxxxxxxxxxx, xxxxxxxxxxxx or xxxxxxxxxx')


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
        if Path(filename).exists():
            with open(filename, 'rb') as file:
                self.data = load(file)
    def add_note(self, note):

        self.data.append(note)


class Note():

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


def parse(user_input):
    """
    This function parses user's input into command and arguments.

    :param user_input: user input -> str
    :return: command -> str, args -> list
    """
    user_input_list = user_input.split(' ')
    command = user_input_list[0]
    args = user_input_list[1:]
    return (command, args)


def input_error(func):
    """
    This is a decorator function that catches errors that may occur when calling a function given as a parameter.

    :param func -> function
    :return func if no error, str if there's an error
    """

    def inner(*args):
        try:
            return func(*args)
        except KeyError:
            return 'The name is not in contacts. Enter a user name please.'
        except ValueError:
            return 'ValueError: Please enter a name followed by a phone.'
        except IndexError:
            return 'IndexError: Please enter a name followed by a phone.'
        except TypeError:
            return 'You have entered invalid number of arguments for this command.'
        except PhoneInvalidFormatError:
            return 'Invalid phone format. Please enter the phone in the format +xxxxxxxxxxxx, xxxxxxxxxxxx or xxxxxxxxxx'
        except BirthdayInvalidFormatError:
            return 'Invalid birthday format. Please enter the birthday in the format YYYY-MM_DD'
        except EmailInvalidFormatError:
            return 'Invalid email format.'
        except NoteInputInvalidFormatError:
            return 'Incorrect command format. Enter the correct parameters'
    return inner


@input_error
def add_contact(name, phone=None, birthday=None):
    """
    This function adds a new phone and birthday (if provided by the user) for a contact with a name given as
    parameter in the address_book. If the name is not in contacts, then it creates a new record in address_book.

    :param name -> str
           phone -> str
           birthday -> str
    :return str
    """
    if name in address_book.data.keys():
        if phone is None:
            return f'A contact with named {name} already exists.'
        else:
            address_book.data[name].add_phone(Phone(phone))
            if birthday is None:
                return f'Phone number {phone} has been assigned to contact named {name}.'
            else:
                address_book.data[name].add_birthday(Birthday(birthday))
                return f'Phone number {phone} and birthday {birthday} have been assigned to contact named {name}.'
    else:
        if phone is None:
            record = Record(Name(name))
            address_book.add_record(record)
            return f'Contact named {name} has been added.'
        else:
            if birthday is None:
                record = Record(Name(name))
                record.add_phone(Phone(phone))
                address_book.add_record(record)
                return f'Contact named {name} with a phone number {phone} has been added.'
            else:
                record = Record(Name(name), Birthday(birthday))
                record.add_phone(Phone(phone))
                address_book.add_record(record)
                return f"Contact named {name} with a phone number {phone} and {birthday} birthday has been added."


@input_error
def del_contact(name):
    """
    This function deletes a contact with a name given as parameter in the address_book

    :param name -> str
    :return str
    """
    address_book.del_record(name)
    return f'Contact {name} has been deleted.'


@input_error
def add_birthday(name, birthday):
    """
    This function adds a birthday for a contact with a name given as parameters in the address_book.

    :param name -> str
           birthday -> str
    :return str
    """
    address_book.data[name].add_birthday(Birthday(birthday))
    return f"{name}'s birthday {birthday} has been added."


@input_error
def add_email(name, email):
    """
    This function adds an email for a contact with the name given as parameters in the address_book.

    :param name -> str
           email -> str
    :return str
    """
    address_book.data[name].add_email(Email(email))
    return f"Email {email} for {name} has been added."


@input_error
def add_address(name, *address_args):
    """
    This function adds the address for a contact with the name given as parameters in the address_book.

    :param name -> str
           address -> str
    :return str
    """
    address = ' '.join([*address_args])
    address_book.data[name].add_address(Address(address))
    return f"The address {address} for {name} has been added."


@input_error
def change_contact(name, old_phone, new_phone):
    """
    This function changes a phone number of a contact with the name given as parameters in the address_book.

    :param name -> str
           old_phone -> str
           new_phone -> str
    :return str
    """
    address_book.data[name].change_phone(Phone(old_phone), Phone(new_phone))
    return f"{name}'s phone number is now {new_phone}."


@input_error
def remove_phone(name, phone):
    """
    This function removes a phone number for a contact with the name given as parameters in the address_book.

    :param name -> str
           phone -> str
    :return str
    """
    address_book.data[name].remove_phone(Phone(phone))
    return f"{name}'s phone number {phone} has been removed."


@input_error
def get_phone(name):
    """
    This function returns a phone/s number for a contact with the name given as a parameter in the address_book.

    :param name -> str
    :return phone -> str
    """
    if not address_book.data[name].phones:
        return f"There are no phone numbers for a contact named {name}."
    else:
        phones = 'phones:\n'
        for phone in address_book.data[name].phones:
            phones += f'{phone.value}\n'
        return f'{name} ->\n{phones}'


@input_error
def get_birthday(name):
    """
    This function returns a birthday for a contact with the name given as a parameter in the address_book.

    :param name -> str
    :return birthday -> str
    """
    birthday = address_book.data[name].birthday
    if birthday is None:
        return f'There is no birthdate for a contact named {name}.'
    else:
        return f'{name} ->\n--birthday:\n{birthday.value}\n--days to birthday:\n{address_book.data[name].days_to_birthday()}\n\n'


@input_error
def get_email(name):
    """
    This function returns an email for a contact with the name given as a parameter in the address_book.

    :param name -> str
    :return email -> str
    """
    email = address_book.data[name].email
    if email is None:
        return f'There is no email for a contact named {name}.'
    else:
        return f'{name} ->\n--email:\n{email.value}\n\n'


@input_error
def get_address(name):
    """
    This function returns the address for a contact with the name given as a parameter in the address_book.

    :param name -> str
    :return address -> str
    """
    address = address_book.data[name].address
    if address is None:
        return f'There is no address for a contact named {name}.'
    else:
        return f'{name} ->\n--address:\n{address.value}\n\n'


@input_error
def show_all(data=address_book.data):
    """
    This function returns all contact details from the given data. If data is not provided, then data = address_book.

    :param: data -> dict
    :return: phone_book -> str
    """
    phone_book = ''
    for name, info in data.items():
        phones = '--Phone numbers:\n'
        if data[name].phones:
            for phone in data[name].phones:
                phones += f'{phone.value}\n'
        else:
            phones += 'no phone numbers to display\n'
        phone_book += f'\n{name} ->\n{phones}'
        birthday = data[name].birthday
        if birthday is not None:
            phone_book += f'--birthday:\n{birthday.value}\n--days to birthday:\n{data[name].days_to_birthday()}\n'
        email = data[name].email
        if email is not None:
            phone_book += f'--Emails:\n{email.value}\n'
        address = data[name].address
        if address is not None:
            phone_book += f'--Address:\n{address.value}\n'
    return phone_book


@input_error
def show_page(page_to_show, n_records='3'):
    """
    This function returns contacts from address_book from a given page number (given as a parameter page_to_show)
    with number of records on each page that is given as a parameter n_records.

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
    given as a parameter pattern.

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
        return f'There are no contacts that match {pattern}.'


def greeting():
    return 'How can I help you?'


def end():
    return 'Good bye!'


def write_file():
    filename = 'address_book.bin'
    with open(filename, 'wb') as file:
        dump(address_book.data, file)

    filename = 'note_book.bin'
    with open(filename, 'wb') as file:
        dump(note_book.data, file)

def get_help():
    """
    Displays the list of commands to control the CLIB assistant.
    It should be done by typing the word "help".
    """
    print("Type one of the following commands".center(120, '-'))
    print(f"hello or hi".ljust(40), "to welcome CLIB".rjust(80))
    print(f"add <name> followed by a 12-digit <phone number> and <address>".ljust(80), "to add the data to your "
                                                                                       f"Book of Contacts".center(40))
    print(f"add_birthday <name> <birthday>".ljust(40), "to add a birthday to a specified contact name".rjust(80))
    print(f"add_email <name> <email>".ljust(40), "to add the email to a specified contact".rjust(80))
    print(f"add_address <name> <address>".ljust(40), "to add the address to a specified contact".rjust(80))
    print(f"change <name> <old phone> <new phone>".ljust(40), "to change the phone number of a "
                                                              "specified contact".rjust(80))
    print(f"get_phone <name>".ljust(40), "to get the phone number of a specified contact".rjust(80))
    print(f"get_email <name>".ljust(40), "to get the email of a specified contact".rjust(80))
    print(f"get_address <name>".ljust(40), "to get the address of a specified contact".rjust(80))
    print(f"get_birthday <name>".ljust(40), "to get the birthday of a specified contact".rjust(80))
    print(f"search <name> or <phone number>".ljust(40), "to get the needed contact details".rjust(80))
    print(f"remove <name> <phone number>".ljust(40), "to delete a phone number of a specified contact".rjust(80))
    print(f"delete <name>".ljust(40), "to permanently delete a specified contact from the Book of Contacts".rjust(80))
    print(f"show all".ljust(40), "to see all the contact details in your Book of Contacts".rjust(80))
    print(f"show_page <name> <phone number>".ljust(40), "to return contacts from address_book from a "
                                                        "given page number".rjust(80))
    print(f"goodbye, close, or exit".ljust(40), "to quit the program and terminate the Command Line Interface "
                                                "Bot.".rjust(80))
    print(f"".ljust(120, "_"))
    return ""

def select_notes(*args):

    try:
        text_for_search = args[0]
    except IndexError:
        raise NoteInputInvalidFormatError

    tags = []
    title = ''
    found_notes = []

    if text_for_search.startswith('#'):
        tags.append(text_for_search)
        text_for_search = None

    for index, item in enumerate(args[1:]):

        if item.startswith('#'):
            tags.append(item)
        elif item.startswith('/t/'):
            title = f'{item[3:]} {" ".join(args[index + 2:])}'
            break
        else:
            text_for_search += f' {item}'

    for index, note in enumerate(note_book.data):
        if text_for_search:
            if text_for_search in note.text:
                if tags:
                    if len(tags) > 1:
                        for tag in tags:
                            if tag in note.tags:
                                found_notes.append([note, note.title, index])
                                break
                    elif tags[0] in note.tags:
                        found_notes.append([note, note.title, index])
                else:
                    found_notes.append([note, note.title, index])
            else:
                continue
        else:
            if len(tags) > 1:
                for tag in tags:
                    if tag in note.tags:
                        found_notes.append([note, note.title, index])
                        break
            elif tags[0] in note.tags:
                found_notes.append([note, note.title, index])
    return found_notes

@input_error
def add_note(*args):

    try:
        text = args[0]
    except IndexError:
        raise NoteInputInvalidFormatError

    if text.startswith('#') or text.startswith('/t/'):
        return f'Note has not been added ! Enter note text.'

    tags = []
    title = ''

    for index, item in enumerate(args[1:]):
        if item.startswith('#'):
            tags.append(item)
        elif item.startswith('/t/'):
            title = f'{item[3:]} {" ".join(args[index + 2:])}'
            break
        else:
            text += f' {item}'

    note_book.add_note(Note(text, tags, title))

    return f'The note has been added'

@input_error
def find_note(*args):

    found_notes = select_notes(*args)

    if found_notes:
        if len(found_notes) == 1:
            return f'Founded notes:\n{found_notes[0][0].title}\n{found_notes[0][0].text}'
        else:
            rezult = f'Founded notes:'
            for note in sorted(found_notes, key=lambda x: x[1]):
                rezult += f'\n{note[0].title}\n{note[0].text}'
            return rezult
    else:
        return f'Note(s) don`t found'

@input_error
def delete_note(*args):

    found_notes = select_notes(*args)
    rezult = f'No notes matching the criterion were found for deletion'

    if found_notes:
        if len(found_notes) == 1:
            del note_book.data[found_notes[0][2]]
            rezult = f'Deleted note:\n{found_notes[0][0].title}\n{found_notes[0][0].text}'
        else:
            sorted_found_notes = sorted(found_notes, key=lambda x: x[1])
            list_of_notes = 'Notes matching the condition:'

            for index, note in enumerate(sorted_found_notes):
                list_of_notes += f'\n{index+1}) {note[0].title}\n{note[0].text}'

            print(f'{list_of_notes}')

            choice = input(f'You can:\n' \
                     f'Don`t delete anything - enter "0"\n' \
                     f'Delete all - enter "a" or "A"\n' \
                     f'Delete note № - enter the note number\n'
                        f'Your choice - ')
            if choice == '0':
                rezult = f'Records have not been deleted'
            elif choice == 'a' or choice == 'A':
                for index in range(len(found_notes) - 1, -1, -1):
                    del note_book.data[found_notes[index][2]]
                rezult = f'Notes has been deleted'
            elif choice.isdigit() and  (1 <= int(choice) <= len(found_notes)):
                del note_book.data[sorted_found_notes[int(choice) - 1][2]]
                rezult = f'Note № {choice} has been deleted'
            else:
                rezult = f'The selection is incorrect. Notes have not been deleted'
    return rezult

@input_error
def edit_note(*args):

    found_notes = select_notes(*args)
    rezult = f'No notes matching the criterion were found for change'

    if found_notes:
        if len(found_notes) == 1:
            new_text = input(f'Found note\n'
                             f'{found_notes[0][0].title}\n'
                             f'{found_notes[0][0].text}\n'
                             f'Enter new note text (empty string for skip) - ')
            if new_text:
                note_book.data[found_notes[0][2]].text = new_text
                rezult = 'Note redacted'
            else:
                rezult = 'Note unchanged'
        else:
            sorted_found_notes = sorted(found_notes, key=lambda x: x[1])
            list_of_notes = 'Notes matching the condition:'

            for index, note in enumerate(sorted_found_notes):
                list_of_notes += f'\n{index+1}) {note[0].title}\n{note[0].text}'

            print(f'{list_of_notes}')

            choice = input(f'Which note to change (0 to skip) - ')
            if choice == '0':
                rezult = f'Records have not been edited'
            elif choice.isdigit() and  (1 <= int(choice) <= len(found_notes)):
                new_text = input(f'Enter new note text (empty string for skip) - ')
                if new_text:
                    note_book.data[sorted_found_notes[int(choice) - 1][2]].text = new_text
                    rezult = f'Note № {choice} has been edited'
            else:
                rezult = f'The selection is incorrect. Notes have not been edited'
    return rezult


def main():
    """
    This function implements all the logic of interaction with the user, all 'print' and 'input' takes place here.

    :param: None
    :return: None
    """
    handler_commands = {'hello': greeting,
                        'hi': greeting,
                        'help': get_help,
                        'add': add_contact,
                        'delete': del_contact,
                        'add_birthday': add_birthday,
                        'add_email': add_email,
                        'add_address': add_address,
                        'change': change_contact,
                        'get_phone': get_phone,
                        'get_birthday': get_birthday,
                        'get_email': get_email,
                        'get_address': get_address,
                        'search': search_contact,
                        'remove': remove_phone,
                        'show all': show_all,
                        'show_page': show_page,
                        'good bye': end,
                        'close': end,
                        'exit': end,
                        'add_note': add_note, # add_note <text of note> <one or few tags in format #tag #tag> </t/title>
                        'find_note': find_note, # find_note <text for search> <one or few tags in format #tag #tag>
                        'delete_note': delete_note, # delete_note <text in note> <one or few tags in format #tag #tag>
                        'edit_note': edit_note} # edit_note <text in note> <one or few tags in format #tag #tag>

    while True:
        user_input = input('Type your command: ')
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
                    "Unknown command. Please type 'help' to get the full list of available commands.")


if __name__ == '__main__':
    main()
