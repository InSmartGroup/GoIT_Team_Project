from clib import classes


def parse(user_input, commands):
    """
    This function parses user's input into command and arguments.

    :param user_input: user input -> str
                        commands -> list
    :return: command -> str (or None), args -> list (or None)
    """
    command = None
    for elem in commands:
        if user_input.startswith(elem):
            command = elem
            len_command = len(elem.split(' '))
            user_input_list = user_input.split(' ')
            args = user_input_list[len_command:]
            break
        if command is None:
            args = None
    return command, args


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
        except classes.PhoneInvalidFormatError:
            return 'Invalid phone format. Please use one of format examples: +380951112233, 380951112233 or 0951112233'
        except classes.BirthdayInvalidFormatError:
            return 'Invalid birthday format. Please enter the birthday in the format YYYY-MM_DD'
        except classes.EmailInvalidFormatError:
            return 'Invalid email format.'
        except classes.NoteInputInvalidFormatError:
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
    if name in classes.address_book.data.keys():
        if phone is None:
            return f'A contact with named {name} already exists.'
        else:
            classes.address_book.data[name].add_phone(classes.Phone(phone))
            if birthday is None:
                return f'Phone number {phone} has been assigned to contact named {name}.'
            else:
                classes.address_book.data[name].add_birthday(classes.Birthday(birthday))
                return f'Phone number {phone} and birthday {birthday} have been assigned to contact named {name}.'
    else:
        if phone is None:
            record = classes.Record(classes.Name(name))
            classes.address_book.add_record(record)
            return f'Contact named {name} has been added.'
        else:
            if birthday is None:
                record = classes.Record(classes.Name(name))
                record.add_phone(classes.Phone(phone))
                classes.address_book.add_record(record)
                return f'Contact named {name} with a phone number {phone} has been added.'
            else:
                record = classes.Record(classes.Name(name), classes.Birthday(birthday))
                record.add_phone(classes.Phone(phone))
                classes.address_book.add_record(record)
                return f"Contact named {name} with a phone number {phone} and {birthday} birthday has been added."


@input_error
def del_contact(name):
    """
    This function deletes a contact with a name given as parameter in the address_book

    :param name -> str
    :return str
    """
    classes.address_book.del_record(name)
    return f'Contact {name} has been deleted.'


@input_error
def add_birthday(name, birthday):
    """
    This function adds birthday for a contact with a name given as parameters in the address_book.

    :param name -> str
           birthday -> str
    :return str
    """
    classes.address_book.data[name].add_birthday(classes.Birthday(birthday))
    return f"{name}'s birthday {birthday} has been added."


@input_error
def add_email(name, email):
    """
    This function adds an email for a contact with the name given as parameters in the address_book.

    :param name -> str
           email -> str
    :return str
    """
    classes.address_book.data[name].add_email(classes.Email(email))
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
    classes.address_book.data[name].add_address(classes.Address(address))
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
    classes.address_book.data[name].remove_phone(classes.Phone(old_phone))
    classes.address_book.data[name].add_phone(classes.Phone(new_phone))
    return f"{name}'s phone number is now {new_phone}."


@input_error
def remove_phone(name, phone):
    """
    This function removes a phone number for a contact with the name given as parameters in the address_book.

    :param name -> str
           phone -> str
    :return str
    """
    classes.address_book.data[name].remove_phone(classes.Phone(phone))
    return f"{name}'s phone number {phone} has been removed."


@input_error
def get_phone(name):
    """
    This function returns a phone/s number for a contact with the name given as a parameter in the address_book.

    :param name -> str
    :return phone -> str
    """
    if not classes.address_book.data[name].phones:
        return f"There are no phone numbers for a contact named {name}."
    else:
        phones = 'phones:\n'
        for phone in classes.address_book.data[name].phones:
            phones += f'{phone.value}\n'
        return f'{name} ->\n{phones}'


@input_error
def get_birthday(name):
    """
    This function returns a birthday for a contact with the name given as a parameter in the address_book.

    :param name -> str
    :return birthday -> str
    """
    birthday = classes.address_book.data[name].birthday
    if birthday is None:
        return f'There is no birthdate for a contact named {name}.'
    else:
        return f'{name} ->\n--birthday:\n{birthday.value}\n--days to ' \
               f'birthday:\n{classes.address_book.data[name].days_to_birthday()}\n\n'


@input_error
def get_email(name):
    """
    This function returns an email for a contact with the name given as a parameter in the address_book.

    :param name -> str
    :return email -> str
    """
    email = classes.address_book.data[name].email
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
    address = classes.address_book.data[name].address
    if address is None:
        return f'There is no address for a contact named {name}.'
    else:
        return f'{name} ->\n--address:\n{address.value}\n\n'


@input_error
def show_all(data=classes.address_book.data):
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
            phones += 'No phone numbers to display\n'
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
    for page in classes.address_book.iterator(int(n_records)):
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
    for name, record in classes.address_book.data.items():
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
    return 'Hello! How can I help you?'


def end():
    return 'Good bye! Thank you for using CLIB.'


def write_file():
    classes.address_book.save_data()
    classes.note_book.save_data()


def get_help():
    """
    Displays the list of commands to control the CLIB assistant.
    It should be done by typing the word "help" in the command line.
    """
    print("".center(120, "*"))
    print("Phone Book Commands".center(120, '-'))
    print("add <name> followed by a 12-digit <phone number> and <address>".ljust(80), "to add the data to your "
                                                                                       f"Book of Contacts".center(40))

    print("add birthday <name> <birthday, format YYYY-MM-DD>".ljust(80), "to add a birthday to a contact".rjust(40))
    print("add email <name> <email>".ljust(40), "to add the email to a specified contact".rjust(80))
    print("add address <name> <address>".ljust(40), "to add the address to a specified contact".rjust(80))
    print("change phone <name> <old phone> <new phone>".ljust(60), "to change the phone number of a "
                                                              "specified contact".rjust(60))

    print("get phone <name>".ljust(40), "to get the phone number of a specified contact".rjust(80))
    print("get email <name>".ljust(40), "to get the email of a specified contact".rjust(80))
    print("get address <name>".ljust(40), "to get the address of a specified contact".rjust(80))
    print("get birthday <name>".ljust(40), "to get the birthday of a specified contact".rjust(80))
    print("show <name> or <phone number>".ljust(40), "to get the needed contact details".rjust(80))
    print("delete phone <name> <phone number>".ljust(40), "to delete a phone number of a specified contact".rjust(80))
    print("delete <name>".ljust(40), "to permanently delete a specified contact from the Book of Contacts".rjust(80))
    print("show all".ljust(40), "to see all the contact details in your Book of Contacts".rjust(80))
    print("show page <name> <phone number>".ljust(40), "to return contacts from address_book from a "
                                                        "given page number".rjust(80))

    print("".center(120, "_"))

    print("Note Book commands".center(120, "-"))
    print("add note <text>".ljust(40), "to add a new text note to your Note Book".rjust(80))
    print("find note <keyword>".ljust(40), "to find the list of notes that contain the given keyword".rjust(80))
    print("edit note <keyword>".ljust(40), "to find the note by a given keyword and edit it".rjust(80))
    print("delete note <keyword>".ljust(40), "to find the list of notes that contain a given keyword and "
                                             "delete it".rjust(80))

    print("".center(120, "_"))

    print("General Commands".center(120, "-"))
    print("hello / hi".ljust(40), "to greet CLIB".rjust(80))
    print("sort <path to a folder>".ljust(40), "sorts all the files and puts them into "
                                                           "folders depending on file extensions".rjust(80))

    print("goodbye, close, or exit".ljust(40), "to quit the program and terminate the Command Line Interface "
                                                "Bot".rjust(80))
    print("".center(120, "_"))
    print("".center(120, "*"))

    return ""


def select_notes(*args):
    """
    Retrieves a list of previously added notes by typing in a tag or a keyword.

    :param args: any tags or keywords -> str
    :return: notes that contain a tag or keyword provided in *args
    :rtype: list
    """
    try:
        text_for_search = args[0]
    except IndexError:
        raise classes.NoteInputInvalidFormatError

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

    for index, note in enumerate(classes.note_book.data):
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
    """
    Adds a text note to note_book.

    :param args: a text note -> str
    """
    try:
        text = args[0]
    except IndexError:
        raise classes.NoteInputInvalidFormatError

    if text.startswith('#') or text.startswith('/t/'):
        return "Unable to add the note. Please enter the note in a text format."

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

    classes.note_book.add_note(classes.Note(text, tags, title))

    return "The note has been added."


@input_error
def find_note(*args):
    """
    Returns a list of notes that contain a keyword provided by the user.

    :param args: a keyword by which you want to search the notes -> str
    :return: a list of notes
    :rtype: str
    """
    found_notes = select_notes(*args)

    if found_notes:
        if len(found_notes) == 1:
            return f"Found note:{found_notes[0][0].title}\n{found_notes[0][0].text}"
        else:
            result = "Found notes:"
            for note in sorted(found_notes, key=lambda x: x[1]):
                result += f'\n{note[0].title}\n{note[0].text}'
            return result
    else:
        return "No notes match your search criteria."


@input_error
def delete_note(*args):
    """
    Permanently deletes a specified note from your note_book.
    To delete a note, the user has to provide a note keyword first, and then choose one of the options.

    :param args: a keyword by which you want to find notes for future deletion -> str
    """
    found_notes = select_notes(*args)
    result = "Nothing to delete. No notes match your search criteria"

    if found_notes:
        if len(found_notes) == 1:
            del classes.note_book.data[found_notes[0][2]]
            result = f'Deleted note:\n{found_notes[0][0].title}\n{found_notes[0][0].text}'
        else:
            sorted_found_notes = sorted(found_notes, key=lambda x: x[1])
            list_of_notes = 'Notes that match the condition:'

            for index, note in enumerate(sorted_found_notes):
                list_of_notes += f'\n{index + 1}) {note[0].title} {note[0].text}'

            print(f'{list_of_notes}')

            choice = input(f"Available options:\n" 
                           f"Cancel deletion: enter '0'\n" 
                           f"Delete all notes: enter 'a' or 'A'\n" 
                           f"Delete note #: enter note number\n"
                           f"Please enter your command: ")

            if choice == '0':
                result = "Deletion has been canceled."
            elif choice == 'a' or choice == 'A':
                for index in range(len(found_notes) - 1, -1, -1):
                    del classes.note_book.data[found_notes[index][2]]
                result = "All notes have been deleted."
            elif choice.isdigit() and (1 <= int(choice) <= len(found_notes)):
                del classes.note_book.data[sorted_found_notes[int(choice) - 1][2]]
                result = f"Note #{choice} has been deleted."
            else:
                result = "Invalid command. Deletion has been canceled."
    return result


@input_error
def edit_note(*args):
    """
    Prints out a list of notes that contain a keyword provided by the user for further editing.

    :param args: a list of notes that contain a given keyword -> str
    :return: a new note
    :rtype: str
    """
    found_notes = select_notes(*args)
    result = "No notes match your search criteria. Please try again."

    if found_notes:
        if len(found_notes) == 1:
            new_text = input(f'Found notes:\n'
                             f'{found_notes[0][0].title}\n'
                             f'{found_notes[0][0].text}\n'
                             f"Type a new note text (Enter to cancel): ")
            if new_text:
                classes.note_book.data[found_notes[0][2]].text = new_text
                result = "The note has been edited"
            else:
                result = "The note has not been changed"
        else:
            sorted_found_notes = sorted(found_notes, key=lambda x: x[1])
            list_of_notes = "Notes that match the condition:"

            for index, note in enumerate(sorted_found_notes):
                list_of_notes += f"\n{index + 1}) {note[0].title} {note[0].text}"

            print(f'{list_of_notes}')

            choice = input("Which note you want to edit (0 to cancel): ")
            if choice == '0':
                result = "Records have not been edited."
            elif choice.isdigit() and (1 <= int(choice) <= len(found_notes)):
                new_text = input('Type a new note text (Enter to cancel): ')
                if new_text:
                    classes.note_book.data[sorted_found_notes[int(choice) - 1][2]].text = new_text
                    result = f'Note #{choice} has been edited.'
            else:
                result = "Incorrect selection. Notes have not been edited."
    return result
