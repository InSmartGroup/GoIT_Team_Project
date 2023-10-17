# CLIB
## The Command Line Interface Bot by **PyCrafters**
___

### Table of Contents  
1. [Project Description](#contacts-and-the-book-of-notes)  
- 1.1. [Contacts](#contacts)
- 1.2. [Notes](#notes)
- 1.3. [Sorting Files](#sorting-files)
2. [Available Commands](#available-commands)
   - [General](#general-commands)
   - [The Book of Contacts](#the-book-of-contacts-commands)
   - [The Note Book](#the-note-book-commands)
3. [Installation](#installation)
4. [Using the Program](#using-the-program)
5. [License](#license)
6. [Authors](#authors)
____

## Contacts and the Book of Notes
This project is a console application, developed for keeping contact details, notes, and for searching, editing,
and sorting the data. The main functions include: 

### Contacts
- **Keeping contact details**: Add contacts with names, addresses, phone numbers, email addresses, and birthdays.
- **Outputting contacts by birthdate**: Search and output a list of contacts whose birthday occur in a specified number
of days from the current date.
- **Checking the input data**: You can check the correctness of inputted phone number and email address while creating 
a new or editing an existing record. In case of incorrect input, you will receive a corresponding notification.  
- **Contact search**: Make the search for a specified contact in your contact book.
- **Editing and deleting contacts**: Handy capabilities for editing and deleting records. 

### Notes
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

## Available Commands
The user should use the command line and enter commands to control CLIB and the data he entered.
The full list of available commands is presented below:

### General
#### Command: hello / hi
- Result: Welcomes CLIB and greets the user
- Example:
```commandline
Input:
hello

Output:
How can I help you?
```

#### Command: help
- Result: Prints the full list of commands available to a user
- Example:
```commandline
Input:
help
```

#### Command: goodbye / close / exit
- Result: Quits the program and terminates the Command Line Interface Bot
- Example:
```commandline
Input:
close

Output:
Good bye!
```
____

### The Book of Contacts
#### Command: add
- Result: Adds the contact name, his 12-digit phone number, and birthday (YYYY-MM-DD) to the Book of Contacts
Optionally, the user can add only the contact name itself, without providing the phone and birthday 
- Example:
```commandline
Input:
add Steve 380935552277 1985-01-01

Output:
Contact named Steve with a phone number 380935552277 and 1985-01-01 birthday has been added.
```

#### Command: add_birthday
- Result: Adds birthday data to a specified contact name
- Example:
```commandline
Input:
add_birthday Steve 1985-01-01

Output:
Steve's birthday 1985-01-01 has been added.
```

#### Command: add_email
- Result: Adds an email to a specified contact name
- Example:
```commandline
Input:
add_email Steve example@gmail.com

Output:
Email example@gmail.com for Steve has been added.
```

#### Command: add_address
- Result: Adds an address to a specified contact name
- Example:
```commandline
Input:
add_address Steve StepanaBandery16

Output:
The address Stepana Bandery 16, kv. 8 for Steve has been added.
```

#### Command: change
- Result: Changes an old phone number of a specified contact to a new one
- Example:
```commandline
Input:
change Steve 380935552277 380951113322

Output:
Steve's phone number is now 380951113322
```

#### Command: get_phone
- Result: If exists, returns a phone number of a specified contact
- Example:
```commandline
Input:
get_phone Steve

Output:
Steve ->
--Phones:
380951113322
```

#### Command: get_email
- Result: If exists, returns an email number of a specified contact
- Example:
```commandline
Input:
get_email Steve

Output:
Steve ->
--Email:
example@gmail.com
```

#### Command: get_address
- Result: If exists, returns an address of a specified contact name
- Example:
```commandline
Input:
get_address Steve

Output:
Steve ->
--Address:
Stepana Bandery 16, kv. 8
```

#### Command: get_birthday
- Result: If exists, returns a birthday of a specified contact name
- Example:
```commandline
Input:
get_birthday Steve

Output:
There is no birthdate for a contact named Steve
```

#### Command: search
- Result: If exists, returns the searched name or a phone number
- Examples:
```commandline
Input:
search Steve

Output:
Steve -->
-- Phones:
380951113322
-- Emails:
example@gmail.com
-- Address:
Stepana Bandery 16, kv. 8
```

#### Command: remove
- Result: Deletes the phone number of a specified contact
- Example:
```commandline
Input:
remove Steve 380951113322

Output:
Steve's phone number 380951113322 has been removed.
```

#### Command: show all
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

#### Command: show_page
- Result: Returns contacts from the address book for a given page number
- Example:
```commandline
Input:
show_page Steve 380951113322
```

#### Command: delete
- Result: Deletes a contact with a specified name
- Examples:
```commandline
Input:
delete Steve

Output:
Contact Steve has been deleted.
```
____

### The Note Book
#### Command: add_note
- Output: Adds a new note to the Note Book
- Example:
```commandline
Input:
add_note welcome onboard
add_note hello world
```

#### Command: find_note
- Result: Returns a list of notes that contain a keyword provided by the user
- Example:
```commandline
Input:
find_note w

Output:
Found notes:
welcome onboard
hello world
```

#### Command: edit_note
- Result: Prints out a list of notes that contain a keyword provided by the user for further editing
- Example:
```commandline
Input:
edit_note w

Output:
Notes that match the condition:
1) welcome onboard
2) hello world
```

#### Command: delete_note
- Result: Permanently deletes a specified note by providing a note keyword first, and then choosing one of the options.
- Example:
```commandline
Input:
delete_note w

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

## Installation


## Using the Program

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
