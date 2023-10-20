from Personal_assistant import functions
from Personal_assistant.sort import main as sort


def main():
    """
    This function implements all the logic of interaction with the user, all 'print' and 'input' takes place here.
    """
    handler_commands = {'hello': functions.greeting,
                        'hi': functions.greeting,
                        'help': functions.get_help,
                        'delete contact': functions.del_contact,
                        'add birthday': functions.add_birthday,
                        'add email': functions.add_email,
                        'add address': functions.add_address,
                        'change': functions.change_contact,
                        'get phone': functions.get_phone,
                        'get birthday': functions.get_birthday,
                        'get email': functions.get_email,
                        'get address': functions.get_address,
                        'show': functions.search_contact,
                        'delete phone': functions.remove_phone,
                        'show all': functions.show_all,
                        'show page': functions.show_page,
                        'good bye': functions.end,
                        'close': functions.end,
                        'exit': functions.end,
                        'add note': functions.add_note,
                        'find note': functions.find_note,
                        'delete note': functions.delete_note,
                        'edit note': functions.edit_note,
                        'add': functions.add_contact,
                        'sort': sort
                        }

    print("Welcome! I'm CLI - your personal Command Line Interface Bot.")
    print("Please enter your command or type 'help' to see the full list of available commands.")

    while True:
        user_input = input('Enter command: ')
        if user_input.lower() in handler_commands.keys():
            output = handler_commands[user_input.lower()]()
            print(output)
            if output == 'Good bye! Thank you for using CLIB.':
                functions.write_file()
                exit()
        else:
            command, args = functions.parse(user_input, handler_commands.keys())
            if command:
                print(handler_commands[command](*args))
            else:
                print("Unknown command. Please type 'help' to get the full list of available commands.")


if __name__ == '__main__':
    main()
