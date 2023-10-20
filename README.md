# CLIB
### The Command Line Interface Bot by **PyCrafters**

### Table of Contents  
1. [Project Description](#project-description)
- 1.1. [Book of Contacts](#book-of-contacts)
- 1.2. [Note Book](#note-book)
- 1.3. [Files Sorter](#sorting-files)
2. [Installation](#installation)
3. [Using the Program](#using-the-program)
4. [Available Commands](#available-commands)
   - [General](#general-commands)
   - [Book of Contacts](#book-of-contacts-commands)
   - [Note Book](#note-book-commands)
   - [File Sorter](#file-sorter-commands)
5. [License](#license)
6. [Authors](#authors)
____

# Project Description
This project is a console application, developed for keeping contact details, notes, and for searching, editing,
and sorting the data. The main functions include: 

### Book of Contacts
- **Keeping contact details**: Add contacts with names, addresses, phone numbers, email addresses, and birthdays.
- **Outputting contacts by birthdate**: Search and output a list of contacts whose birthday occur in a specified number
of days from the current date.
- **Checking the input data**: You can check the correctness of inputted phone number and email address while creating 
a new or editing an existing record. In case of incorrect input, you will receive a corresponding notification.  
- **Contact search**: Make the search for a specified contact in your contact book.
- **Editing and deleting contacts**: Handy capabilities for editing and deleting records. 

### Note Book
- **Notes keeping**: Write and keep you notes with text information.
- **Notes search**: Search for notes in your Book of Notes.
- **Editing and deleting notes**: Handy capabilities for editing and deleting notes.
- **Adding tags**: An option to add note tags or keywords that describe the topic and the inputted message.
- **Sorting notes by tag**: Allows to sort and search notes by tags and keywords.

### Sorting Files
This project is designed to organize and manage your contact details, notes, and files as easy as possible.
- **Sorting files in a folder**: Automatic files sorting in a specified folder by category, such as images, documents,
videos, etc.
____

# Installation
1. To install the program as executable file, open the Terminal and in the command line change the directory
to a folder with *setup.py* installation file.

2. Next, in the Terminal type:
```commandline
pip install -e .
```
This will also build a new Python package named 'Personal_assistant', which you now can import.

3. Finally, in the Terminal type **helper** to run the program.
____

# Using the Program
After installing the program and running it in the Terminal, the user can:
- access the Phone Book (ref. see the *Book of Commands Contacts* section)
- access the Note Book (ref. see the *Note Book Commands* section);
- sort files using the integrated file sorter (ref. see the *sort* function)
____

# Available Commands
The user should use the command line and enter commands to control CLIB and the data he entered.
The full list of available commands is presented below:

## General Commands
### Command: hello / hi
- Result: Welcomes CLIB and greets the user
- Example:
```commandline
Input:
hello

Output:
How can I help you?
```

### Command: help
- Result: Prints the full list of commands available to a user
- Example:
```commandline
Input:
help
```

### Command: goodbye / close / exit
- Result: Quits the program and terminates the Command Line Interface Bot
- Example:
```commandline
Input:
close

Output:
Good bye!
```
____

## Book of Contacts Commands
### Command: add
- Result: Adds the contact name, his 12-digit phone number, and birthday (YYYY-MM-DD) to the Book of Contacts
Optionally, the user can add only the contact name itself, without providing the phone and birthday 
- Example:
```commandline
Input:
add Steve 380935552277 1985-01-01

Output:
Contact named Steve with a phone number 380935552277 and 1985-01-01 birthday has been added.
```

### Command: add birthday
- Result: Adds birthday data to a specified contact name
- Example:
```commandline
Input:
add birthday Steve 1985-01-01

Output:
Steve's birthday 1985-01-01 has been added.
```

### Command: add email
- Result: Adds an email to a specified contact name
- Example:
```commandline
Input:
add email Steve example@gmail.com

Output:
Email example@gmail.com for Steve has been added.
```

### Command: add address
- Result: Adds an address to a specified contact name
- Example:
```commandline
Input:
add address Steve Stepana Bandery 16, kv. 8

Output:
The address Stepana Bandery 16, kv. 8 for Steve has been added.
```

### Command: change phone
- Result: Changes an old phone number of a specified contact to a new one
- Example:
```commandline
Input:
change phone Steve 380935552277 380951113322

Output:
Steve's phone number is now 380951113322
```

### Command: get phone
- Result: If exists, returns a phone number of a specified contact
- Example:
```commandline
Input:
get phone Steve

Output:
Steve ->
--Phones:
380951113322
```

### Command: get email
- Result: If exists, returns an email number of a specified contact
- Example:
```commandline
Input:
get email Steve

Output:
Steve ->
--Email:
example@gmail.com
```

### Command: get address
- Result: If exists, returns an address of a specified contact name
- Example:
```commandline
Input:
get address Steve

Output:
Steve ->
--Address:
Stepana Bandery 16, kv. 8
```

### Command: get birthday
- Result: If exists in Book of Contacts, returns a birthday of a specified contact name and the number of days
till next birthday.
- Example:
```commandline
Input:
get birthday Steve

Output:
There is no birthdate for a contact named Steve
```

### Command: show
- Result: If exists in Book of Contacts, shows a name and a phone number
- Examples:
```commandline
Input:
show Steve

Output:
Steve -->
-- Phones:
380951113322
-- Emails:
example@gmail.com
-- Address:
Stepana Bandery 16, kv. 8
```

### Command: delete phone
- Result: Deletes the phone number of a specified contact
- Example:
```commandline
Input:
delete phone Steve 380951113322

Output:
Steve's phone number 380951113322 has been removed.
```

### Command: show all
- Result: Prints all the contact details in the Book of Contacts
- Example:
```commandline
Input:
show all

Output:
Steve -->
-- Emails:
example@gmail.com
-- Address:
Stepana Bandery 16, kv. 8
```

### Command: show page
- Result: Returns contacts from the address book for a given page number
- Example:
```commandline
Input:
show page Steve 380951113322
```

### Command: delete
- Result: Deletes a contact with a specified name
- Examples:
```commandline
Input:
delete Steve

Output:
Contact Steve has been deleted.
```
____

## Note Book Commands
### Command: add note
- Result: Adds a new note to the Note Book. Optionally, you can add note tags by typing '#<tag name>' after the note
- Example:
```commandline
Input:
add note welcome onboard
add note hello world
add note buy milk #buy
add note buy eggs #buy
```

### Command: find note
- Result: Returns a list of notes that contain a keyword or a tag provided by the user
- Example:
```commandline
Input:
find note #buy

Output:
Found notes:
buy milk
buy eggs
```

### Command: edit note
- Result: Prints out a list of notes that contain a keyword or a tag provided by the user for further editing
- Example:
```commandline
Input:
edit note w

Output:
Notes that match the condition:
1) welcome onboard
2) hello world
```

### Command: delete note
- Result: Permanently deletes a specified note by providing a note keyword first, and then choosing one of the options.
- Example:
```commandline
Input:
delete note w

Output:
Notes that match the condition:
1) welcome onboard
2) hello world
Available options:
Cancel deletion: enter '0'
Delete all notes: enter 'a' or 'A'
Delete note #: enter note number
Please enter your command:
```
____

## File Sorter Commands
### Command: sort
   - Result: Sorts files by folders in a destination directory depending on the file extension
   - Example:
```commandline
Input:
sort

Output
Enter the path to the folder you want to sort: C:\Users\User\Documents\files-to_sort
```
____

## License
This project is distributed under the **MIT** license.
____

## Authors
The **PyCrafters** Team:
- [Yuliia Didenko](https://github.com/yulyan407)
- [Maksim Nesterovskyi](https://github.com/legendarym4x)
- [Kostiantyn Gorishnyi](https://github.com/Kostiantyn78)
- [Taras Barskyi](https://github.com/Barskyi)
- [Gregory Ostapenko](https://github.com/InSmartGroup)
____
