s module defines the command interpreter for the HBNB project.
"""
import cmd
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage
import json
import re


class HBNBCommand(cmd.Cmd):
    """
    Command interpreter class.
    """
    prompt = '(hbnb) '
    classes = {
        'BaseModel': BaseModel,
        'User': User,
        'State': State,
        'City': City,
        'Amenity': Amenity,
        'Place': Place,
        'Review': Review
    }

    def do_quit(self, arg):
        """
        Quit command to exit the program.
        """
        return True

    def do_EOF(self, arg):
        """
        EOF command to exit the program.
        """
        print()
        return True

    def emptyline(self):
        """
        Do nothing on an empty line.
        """
        pass

    def do_create(self, arg):
        """
        Creates a new instance of BaseModel, saves it to a JSON file,
        and prints the id.
        """
        if not arg:
            print("** class name missing **")
            return
        if arg not in self.classes:
            print("** class doesn't exist **")
            return
        new_instance = self.classes[arg]()
        new_instance.save()
        print(new_instance.id)

    def do_show(self, arg):
        """
        Prints the string representation of an instance based on
        the class name and id.
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = "{}.{}".format(args[0], args[1])
        all_objs = storage.all()
        if key not in all_objs:
            print("** no instance found **")
            return
        print(all_objs[key])

    def do_destroy(self, arg):
        """
        Deletes an instance based on the class name and id.
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = "{}.{}".format(args[0], args[1])
        all_objs = storage.all()
        if key not in all_objs:
            print("** no instance found **")
            return
        del all_objs[key]
        storage.save()

    def do_all(self, arg):
        """
        Prints all string representations of all instances
        based or not on the class name.
        """
        all_objs = storage.all()
        obj_list = []
        if not arg:
            for key in all_objs:
                obj_list.append(str(all_objs[key]))
        elif arg not in self.classes:
            print("** class doesn't exist **")
            return
        else:
            for key in all_objs:
                if key.split('.')[0] == arg:
                    obj_list.append(str(all_objs[key]))
        print(obj_list)

    def do_update(self, arg):
        """
        Updates an instance based on the class name and id by adding or
        updating an attribute.
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return

        key = "{}.{}".format(args[0], args[1])
        all_objs = storage.all()

        if key not in all_objs:
            print("** no instance found **")
            return

        if len(args) < 3:
            print("** attribute name missing **")
            return

        if len(args) < 4:
            print("** value missing **")
            return

        obj = all_objs[key]
        attr_name = args[2]
        attr_value = args[3]

        if attr_value.startswith('"') and attr_value.endswith('"'):
            attr_value = attr_value[1:-1]
        
        # Check if the attribute is a known type and cast it
        if hasattr(obj, attr_name):
            try:
                if isinstance(getattr(obj, attr_name), int):
                    attr_value = int(attr_value)
                elif isinstance(getattr(obj, attr_name), float):
                    attr_value = float(attr_value)
            except (ValueError, TypeError):
                pass
        
        setattr(obj, attr_name, attr_value)
        obj.save()

    def default(self, line):
        """
        Handles <class name>.method() syntax.
        """
        parts = line.split('.', 1)
        if len(parts) == 2 and parts[0] in self.classes:
            cls_name = parts[0]
            method_call = parts[1]
            if method_call == "all()":
                self.do_all(cls_name)
            elif method_call == "count()":
                count = 0
                for key in storage.all():
                    if key.startswith(cls_name):
                        count += 1
                print(count)
            elif method_call.startswith("show("):
                instance_id = method_call[6:-2]
                self.do_show(cls_name + " " + instance_id)
            elif method_call.startswith("destroy("):
                instance_id = method_call[9:-2]
                self.do_destroy(cls_name + " " + instance_id)
            elif method_call.startswith("update("):
                update_args = method_call[7:-1]
                
                # Check for dictionary syntax
                if '{' in update_args and '}' in update_args:
                    match = re.match(r'^(.*?)(\s*,\s*)({.*})$', update_args)
                    if match:
                        instance_id = match.group(1).strip('"')
                        dict_str = match.group(3)
                        try:
                            update_dict = eval(dict_str)
                            for key, value in update_dict.items():
                                self.do_update(
                                    cls_name + " " + instance_id + " " + key + " " + str(value))
                        except (SyntaxError, ValueError) as e:
                            print(e)
                else:
                    parts = update_args.split(", ", 2)
                    instance_id = parts[0].strip('"')
                    attr_name = parts[1].strip('"')
                    attr_value = parts[2]
                    self.do_update(
                        cls_name + " " + instance_id + " " + attr_name + " " + attr_value)
            else:
                print("*** Unknown syntax: {}".format(line))
        else:
            print("*** Unknown syntax: {}".format(line))


if __name__ == '__main__':
    HBNBCommand().cmdloop()
