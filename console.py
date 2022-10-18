#!/usr/bin/python3
'''console module'''

import cmd
from models import storage
import models
from models.base_model import BaseModel
# import all models here
# from models.user import User


class Console(cmd.Cmd):
    '''Command line program for testing the system'''

    prompt = "(console) "
    intro = "Welcome to the console v0.0.1.\nType help or ? to list commands.\n"

    def do_quit(self, args):
        """Quits the console"""
        print('Bye bye')
        return True

    def do_EOF(self, args):
        """Quits the console"""
        print('Bye bye')
        return True

    def do_create(self, args):
        """Creates a new instance of a Model, saves it (to the JSON file) and prints the id. Ex: $ create BaseModel"""

        if args == '':
            print("** class name missing **")
            return

        if args not in globals().keys():
            print("** class doesn't exist **")
            return

        obj = globals()[args]()
        obj.save()
        print(obj.id)

    def do_show(self, args):
        """Prints the string representation of an instance based on the class name and id. Ex: $ show BaseModel 1234-1234-1234."""

        if args == '':
            print("** class name missing **")
            return

        args_list = args.split(" ")

        if args_list[0] not in globals().keys():
            print("** class doesn't exist **")
            return

        if len(args_list) != 2:
            print("** instance id missing **")
            return

        k = f"{args_list[0]}.{args_list[1]}"
        objs = storage.all()

        if k not in objs.keys():
            print("** no instance found **")
            return
        print(objs[k])

    def do_destroy(self, args):
        """Deletes an instance based on the class name and id"""

        if args == '':
            print("** class name missing **")
            return

        args_list = args.split(" ")

        if args_list[0] not in globals().keys():
            print("** class doesn't exist **")
            return

        if len(args_list) != 2:
            print("** instance id missing **")
            return

        k = f"{args_list[0]}.{args_list[1]}"
        objs = storage.all()

        if k not in objs.keys():
            print("** no instance found **")
            return

        del objs[k]
        storage.save()

    def do_clear(self, args):
        '''Clears the screen'''
        import os
        os.system('clear')
        return

    def do_all(self, args):
        """Prints all string representation of all instances based or not on the class name."""

        all_objs = []
        objs = storage.all()
        if args == '':
            for v in objs.values():
                all_objs.append(str(v))
            print(all_objs)
            return

        args_list = args.split(" ")

        if args_list[0] not in globals().keys():
            print("** class doesn't exist **")
            return

        for v in objs.values():
            if v.__class__.__name__ == args_list[0]:
                all_objs.append(str(v))
        print(all_objs)
        return

    def do_update(self, args):
        """Updates an instance based on the class name and id by adding or updating attribute

        Usage:
                update <class name> <id> <attribute name> '<attribute value>'"""

        if args == '':
            print("** class name missing **")
            return

        args_list = args.split(" ")

        if args_list[0] not in globals().keys():
            print("** class doesn't exist **")
            return

        if len(args_list) < 2:
            print("** instance id missing **")
            return

        k = f"{args_list[0]}.{args_list[1]}"
        objs = storage.all()

        if k not in objs.keys():
            print("** no instance found **")
            return

        if len(args_list) < 3:
            print("** attribute name missing **")
            return

        if len(args_list) < 4:
            print("** value missing **")
            return

        value = args_list[3]

        attr = args_list[2]
        v = ""
        if value[0] == '"' or value[0] == "'":
            if value[-1] == '"' or value[-1] == "'":
                value = value[1:-1]
        elif '.' in value:
            value = float(value)
        else:
            value = int(value)
        obj = objs[k]
        setattr(obj, attr, value)
        obj.save()


if __name__ == "__main__":
    Console().cmdloop()
