# CLIB: Command Line Interface Bot
### The PyCrafters GoIT Team Project
____

### Table of Contents  
1. [Project Description](#contacts-and-the-book-of-notes)  
- 1.1. [Contacts](#contacts)
- 1.2. [Notes](#notes)
- 1.3. [Sorting Files](#sorting-files)
2. [Available Functions](#available-functions)
3. [License](#license)
4. [Authors](#authors)
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

## Available Functions
The user should use the command line and enter commands to control CLIB and the data.
The full list of available commands is presented below:

##### Command: hello / hi
- Output: Welcomes CLIB and greets the user
- Example:
```commandline
hello
How can I help you?
```

##### Command: add
- Output: Adds the contact name, his 12-digit phone number, and birthday (YYYY-MM-DD) to the Book of Contacts
Optionally, the user can add only the contact name itself, without providing the phone and birthday 
- Examples:
```commandline
add Steve 380935552277 1985-01-01
add Bob
```

##### Command: add_birthday
- Output: Adds birthday data to a specified contact name
- Example:
```commandline
add_birthday Steve 1985-01-01
```

##### Command: add_email
- Output: Adds an email to a specified contact name
- Example:
```commandline
add_email Steve example@gmail.com
```

##### Command: add_address
- Output: Adds an address to a specified contact name
- Example:
```commandline
add_address Steve StepanaBandery16
```

##### Command: change
- Output: Changes an old phone number of a specified contact to a new one
- Example:
```commandline
change Steve 380935552277 380951113322
```

##### Command: get_phone
- Output: If exists, returns a phone number of a specified contact
- Example:
```commandline
get_phone Steve
380951113322
```

##### Command: get_email
- Output: If exists, returns an email number of a specified contact
- Example:
```commandline
get_email Steve
example@gmail.com
```

##### Command: get_address
- Output: If exists, returns an address of a specified contact name
- Example:
```commandline
get_address Steve
StepanaBandery16
```

##### Command: get_birthday
- Output: If exists, returns a birthday of a specified contact name
- Example:
```commandline
get_birthday Steve
```

##### Command: search
- Output: If exists, returns the searched name or a phone number
- Examples:
```commandline
search Steve
search 380951113322
```

##### Command: remove
- Output: Deletes the phone number of a specified contact
- Example:
```commandline
remove Steve 380951113322
```

##### Command: show all
- Output: Prints all the contact details in the Book of Contacts
- Example:
```commandline
show all
```

##### Command: show_page
- Output: Returns contacts from the address book for a given page number
- Example:
```commandline
show_page Steve 380951113322
```

##### Command: delete
- Output: Deletes a contact with a specified name
- Examples:
```commandline
delete Steve
delete Bob
```

##### Command: help
- Output: Prints the full list of commands available to a user
- Example:
```commandline
help
```

##### Command: goodbye / close / exit
- Output: Quits the program and terminates the Command Line Interface Bot
- Examples:
```commandline
good bye
close
exit
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
