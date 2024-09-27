import csv
import os
import sys
import tkinter as tk
from fnmatch import fnmatch
from tkinter import scrolledtext
import tarfile
from datetime import datetime

user_name = "Senya"
disk_files = "disk.tar"
current_dir = "disk/"
last_command = ""
log_file = 'log.csv'


def command_ls(path):
    info.insert(tk.END, "username:" + user_name + " - " + current_dir + '> ' + last_command + '\n')
    with open(log_file, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        writer.writerow(
            [user_name, last_command, datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%H:%M:%S")])
    if len(path) == 0 or path == "." or path == './':
        with tarfile.open(disk_files, 'r') as tar:
            result = ""
            for member in tar.getmembers():
                if current_dir in member.name:
                    file = member.name[len(current_dir):].split("/")
                    if len(file) == 1:
                        result += file[0] + "\n"
            if len(result) == 0:
                info.insert(tk.END, 'Directory is empty\n')
                return 'Directory is empty\n'
            else:
                info.insert(tk.END, result)
                return result
    elif path == "~" or path == '/' or path == '~/':
        with tarfile.open(disk_files, 'r') as tar:
            result = ""
            for member in tar.getmembers():
                if 'disk/' in member.name:
                    file = member.name[len("disk/"):].split("/")
                    if len(file) == 1:
                        result += file[0] + "\n"
            if len(result) == 0:
                info.insert(tk.END, 'Directory is empty\n')
                return 'Directory is empty\n'
            else:
                info.insert(tk.END, result)
                return result
    elif path == ".." or path == '../':
        dir = '/'.join(current_dir.split("/")[:-2]) + '/'
        if current_dir == "disk/":
            info.insert(tk.END, 'disk\n')
            return 'disk\n'
        else:
            with tarfile.open(disk_files, 'r') as tar:
                result = ""
                for member in tar.getmembers():
                    if dir in member.name:
                        file = member.name[len(dir):].split("/")
                        if len(file) == 1:
                            result += file[0] + "\n"
                if len(result) == 0:
                    info.insert(tk.END, 'Directory is empty\n')
                    return 'Directory is empty\n'
                else:
                    info.insert(tk.END, result)
                    return result
    elif path[0] == '.' and path[1] == '.' and path[2] == '/':
        if path[3:].count('.') > 0:
            info.insert(tk.END, 'No such directory: ' + path + '\n')
            return 'No such directory: ' + path + '\n'
        if current_dir != 'disk/':
            path = ('/'.join(current_dir.split('/')[:-2]) + '/' + path[3:])
        else:
            path = current_dir + path[3:]
        with tarfile.open(disk_files, 'r') as tar:
            result = ""
            flag = any(path == member.name and path.count('.') == 0 for member in tar.getmembers())
            if not flag:
                info.insert(tk.END, 'No such directory: ' + path + '\n')
                return 'No such directory: ' + path + '\n'
            for member in tar.getmembers():
                if path + "/" in member.name:
                    file = member.name[len(path + "/"):].split("/")
                    if len(file) == 1:
                        result += file[0] + "\n"
            if len(result) == 0:
                info.insert(tk.END, 'Directory is empty\n')
                return 'Directory is empty\n'
            else:
                info.insert(tk.END, result)
                return result
    elif path[0] == '/' or (len(path) > 1 and path[0] == "~" and path[1] == '/'):
        if path[0] == "~" and path[1] == '/':
            path = path[2:]
            path = '/disk/' + path
        path = path[1:]
        with tarfile.open(disk_files, 'r') as tar:
            result = ""
            flag = any(path == member.name and path.count('.') == 0 for member in tar.getmembers())
            if not flag:
                info.insert(tk.END, 'No such directory: ' + path + '\n')
                return
            for member in tar.getmembers():
                if path + "/" in member.name:
                    file = member.name[len(path + "/"):].split("/")
                    if len(file) == 1:
                        result += file[0] + "\n"
            if len(result) == 0:
                info.insert(tk.END, 'Directory is empty\n')
                return 'Directory is empty\n'
            else:
                info.insert(tk.END, result)
                return result
    else:
        if path[0] == "." and path[1] == '/':
            path = path[2:]
        with tarfile.open(disk_files, 'r') as tar:
            result = ""
            flag = any((current_dir + path) == member.name and path.count('.') == 0 for member in tar.getmembers())
            if not flag:
                info.insert(tk.END, 'No such directory: ' + path + '\n')
                return 'No such directory: ' + path + '\n'
            for member in tar.getmembers():
                if current_dir + path + "/" in member.name:
                    file = member.name[len(current_dir + path + "/"):].split("/")
                    if len(file) == 1:
                        result += file[0] + "\n"
            if len(result) == 0:
                info.insert(tk.END, 'Directory is empty\n')
                return 'Directory is empty\n'
            else:
                info.insert(tk.END, result)
                return result


def command_cd(path):
    global current_dir, last_command
    info.insert(tk.END, "username:" + user_name + " - " + current_dir + '> ' + last_command + '\n')
    with open(log_file, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        writer.writerow(
            [user_name, last_command, datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%H:%M:%S")])
    if len(path) == 0 or path == '.' or path == './':
        info.insert(tk.END, current_dir + '\n')
        return current_dir + '\n'
    elif path == "~" or path == '/' or path == '~/':
        current_dir = "disk/"
    elif path[0] == '/' or (path[0] == "~" and path[1] == '/'):
        if path[0] == "~" and path[1] == '/':
            path = path[2:]
            path = '/disk/' + path
        new_dir = path[1:]
        with tarfile.open(disk_files, 'r') as tar:
            flag = any(new_dir == member.name and path.count('.') == 0 for member in tar.getmembers())
            if flag:
                current_dir = new_dir + '/'
            else:
                info.insert(tk.END, 'No such directory: ' + path + '\n')
                return 'No such directory: ' + path + '\n'
    elif path == ".." or path == '../':
        if current_dir == "disk/":
            return 'already in disk'
        current_dir = '/'.join(current_dir.split("/")[:-2]) + '/'
    elif path[0] == '.' and path[1] == '.' and path[2] == '/':
        if path[3:].count('.') > 0:
            info.insert(tk.END, 'No such directory: ' + path + '\n')
            return 'No such directory: ' + path + '\n'
        if current_dir != 'disk/':
            dir = ('/'.join(current_dir.split('/')[:-2]) + '/' + path[3:])
        else:
            dir = current_dir + path[3:]
        with tarfile.open(disk_files, 'r') as tar:
            flag = any((dir == member.name and dir.count('.') == 0 for member in tar.getmembers()))
            if not flag:
                info.insert(tk.END, 'No such directory: ' + dir + '\n')
                return 'No such directory: ' + dir + '\n'
            else:
                current_dir = dir + '/'
    else:
        if path[0] == "." and path[1] == '/':
            path = path[2:]
        with tarfile.open(disk_files, 'r') as tar:
            flag = any((current_dir + path) == member.name and path.count('.') == 0 for member in tar.getmembers())
            if not flag:
                info.insert(tk.END, 'No such directory: ' + path + '\n')
                return 'No such directory: ' + path + '\n'
            else:
                current_dir += path + '/'
    return current_dir


def command_tac(files):
    info.insert(tk.END, "username:" + user_name + " - " + current_dir + '> ' + last_command + '\n')
    with open(log_file, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        writer.writerow(
            [user_name, last_command, datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%H:%M:%S")])
    if len(files) == 0:
        info.insert(tk.END, 'Empty\n')
        return 'Empty\n'
    for file in files:
        if file[0] == '/':
            path = file[1:]
        elif file[0] == '~' and file[1] == '/':
            path = 'disk/' + file[2:]
        elif len(file) > 1 and file[0] == '.' and file[1] == '/':
            path = current_dir + file[2:]
        elif len(file) > 2 and file[0] == '.' and file[1] == '.' and file[2] == '/':
            if current_dir != 'disk/':
                path = ('/'.join(current_dir.split('/')[:-2]) + '/' + file[3:])
            else:
                path = current_dir + file[3:]
        else:
            path = current_dir + file
        with tarfile.open(disk_files, 'r') as tar:
            flag = any(path == member.name and path.count('.') == 1 for member in tar.getmembers())
            if not flag:
                info.insert(tk.END, 'No such file: ' + path + '\n\n')
                if len(files) > 1:
                    continue
                else:
                    return 'No such file: ' + path + '\n\n'
            with tar.extractfile(path) as extracted_file:
                result = ""
                lines = extracted_file.readlines()
                lines = [line.decode('utf-8').strip() for line in lines][::-1]
                for i in lines:
                    result += i
                    if i[-1] != '\n':
                        result += '\n'
                info.insert(tk.END, 'file: ' + path + '\n' + result + '\n')
                if len(files) > 1:
                    continue
                else:
                    return 'file: ' + path + '\n' + result + '\n'


def command_touch(filename):
    info.insert(tk.END, "username:" + user_name + " - " + current_dir + '> ' + last_command + '\n')
    with open(log_file, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        writer.writerow(
            [user_name, last_command, datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%H:%M:%S")])
    if len(filename) == 0:
        info.insert(tk.END, 'Empty\n')
        return 'Empty\n'
    if filename[0] == '/':
        path = filename[1:]
    elif filename[0] == '~' and filename[1] == '/':
        path = 'disk/' + filename[2:]
    elif len(filename) > 1 and filename[0] == '.' and filename[1] == '/':
        path = current_dir + filename[2:]
    elif len(filename) > 2 and filename[0] == '.' and filename[1] == '.' and filename[2] == '/':
        if current_dir != 'disk/':
            path = ('/'.join(current_dir.split('/')[:-2]) + '/' + filename[3:])
        else:
            path = current_dir + filename[3:]
    else:
        path = current_dir + filename
    with tarfile.open(disk_files, 'r') as tar:
        if path.count('.') != 1:
            info.insert(tk.END, 'It is not a file: ' + path + '\n')
            return 'It is not a file: ' + path + '\n'
        elif any(path == member.name for member in tar.getmembers()):
            info.insert(tk.END, 'File already exists: ' + path + '\n')
            return 'File already exists: ' + path + '\n'
        else:
            name, filetype = '/'.join(path.split('/')[-1]).split('.')
            if len(name) == 0 or len(filetype) == 0:
                info.insert(tk.END, 'It is not a file: ' + path + '\n')
                return 'It is not a file: ' + path + '\n'
    open('temp_file_path.txt', 'a').close()
    try:
        with tarfile.open(disk_files, 'a') as tar:
            info.insert(tk.END, 'File created: ' + path + '\n')
            tar.add('temp_file_path.txt', arcname=path)
    finally:
        os.remove('temp_file_path.txt')
    return 'file created ' + path


def command_mv(source, destination):
    info.insert(tk.END, "username:" + user_name + " - " + current_dir + '> ' + last_command + '\n')
    with open(log_file, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        writer.writerow(
            [user_name, last_command, datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%H:%M:%S")])

    if source == 'error' and destination == 'error':
        info.insert(tk.END, 'please enter source and destination\n')
        return 'please enter source and destination\n'
    if source[0] == '/':
        path_source = source[1:]
    elif source[0] == '~' and source[1] == '/':
        path_source = 'disk/' + source[2:]
    elif len(source) > 1 and source[0] == '.' and source[1] == '/':
        path_source = current_dir + source[2:]
    elif len(source) > 2 and source[0] == '.' and source[1] == '.' and source[2] == '/':
        if current_dir != 'disk/':
            path_source = ('/'.join(current_dir.split('/')[:-2]) + '/' + source[3:])
        else:
            path_source = current_dir + source[3:]
    else:
        path_source = current_dir + source

    if destination == '~' or destination == '/' or destination == '~/':
        path_destination = 'disk'
    elif destination[0] == '/':
        path_destination = destination[1:]
    elif destination[0] == '~' and destination[1] == '/':
        path_destination = 'disk/' + destination[2:]
    elif destination == '.':
        path_destination = current_dir[:-1]
    elif destination == './':
        path_destination = current_dir[:-1]
    elif len(destination) > 1 and destination[0] == '.' and destination[1] == '/':
        path_destination = current_dir + destination[2:]
    elif destination == ".." or destination == '../':
        if current_dir == "disk/":
            info.insert(tk.END, 'No parent directory\n')
            return 'No parent directory\n'
        path_destination = '/'.join(current_dir.split("/")[:-2])
    elif len(destination) > 2 and destination[0] == '.' and destination[1] == '.' and destination[2] == '/':
        if current_dir != 'disk/':
            path_destination = ('/'.join(current_dir.split('/')[:-2]) + '/' + destination[3:])
        else:
            path_destination = current_dir + destination[3:]
    else:
        path_destination = current_dir + destination
    if path_destination.split('/')[-1].count('.') == 0:
        path_destination += '/' + path_source.split('/')[-1]
    with tarfile.open(disk_files, 'r') as tar:
        if path_source.count('.') != 1 and path_destination.count('.') != 1:
            info.insert(tk.END, 'Not files: ' + path_source + ' ' + path_destination + '\n')
            return 'Not files: ' + path_source + ' ' + path_destination + '\n'
        elif path_source.split('.')[-1] != path_destination.split('.')[-1]:
            info.insert(tk.END, 'You can`t change file type ' + path_source + ' ' + path_destination + '\n')
            return 'You can`t change file type ' + path_source + ' ' + path_destination + '\n'
        else:
            name1, filetype1 = '/'.join(path_source.split('/')[-1]).split('.')
            name2, filetype2 = '/'.join(path_destination.split('/')[-1]).split('.')
            if len(name1) == 0 or len(name2) == 0 or len(filetype1) == 0 or len(filetype2) == 0:
                info.insert(tk.END, 'Not files: ' + path_source + ' ' + path_destination + '\n')
                return 'Not files: ' + path_source + ' ' + path_destination + '\n'
    with tarfile.open(disk_files, 'r') as tar:
        if all(member.name != path_source for member in tar.getmembers()):
            info.insert(tk.END, 'No such file: ' + path_source + '\n')
            return 'No such file: ' + path_source + '\n'
        if any(member.name == path_destination for member in tar.getmembers()):
            info.insert(tk.END, 'File already exists: ' + path_destination + '\n')
            return 'File already exists: ' + path_destination + '\n'
        if all(member.name != '/'.join(path_destination.split('/')[:-1]) for member in tar.getmembers()):
            info.insert(tk.END, 'No destination directory ' + '/'.join(path_destination.split('/')[:-1]) + '\n')
            return 'No destination directory ' + '/'.join(path_destination.split('/')[:-1]) + '\n'
    temp_tar = "temp.tar"
    with tarfile.open(disk_files, 'r') as source_tar:
        with tarfile.open(temp_tar, 'w') as temp:
            for member in source_tar.getmembers():
                if member.name != path_source:
                    temp.addfile(member, source_tar.extractfile(member))
            member = source_tar.getmember(path_source)
            extracted_file = source_tar.extractfile(member)
            tar_info = tarfile.TarInfo(name=path_destination)
            tar_info.size = member.size
            temp.addfile(tar_info, extracted_file)
    os.remove(disk_files)
    os.rename(temp_tar, disk_files)
    return path_destination


def command_find(directory, filename):
    info.insert(tk.END, "username:" + user_name + " - " + current_dir + '> ' + last_command + '\n')
    with open(log_file, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        writer.writerow(
            [user_name, last_command, datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%H:%M:%S")])

    test_mask = filename.split('.')
    if not (len(test_mask) == 2 and len(test_mask[0]) > 0 and len(test_mask[1]) > 0 and filename.count('/') == 0):
        info.insert(tk.END, 'I dont understand your mask: ' + filename + '\n')
        return 'I dont understand your mask: ' + filename + '\n'
    if directory == '-all':
        with tarfile.open(disk_files, 'r') as tar:
            result = ''
            for member in tar.getmembers():
                if fnmatch(member.name.split('/')[-1], filename):
                    result += member.name + '\n'
            if len(result) == 0:
                info.insert(tk.END, 'No such files: ' + filename + '\n')
                return 'No such files: ' + filename + '\n'
            else:
                info.insert(tk.END, result)
                return result
    else:
        if directory == '~' or directory == '/':
            path_dir = 'disk'
        elif directory == '.':
            path_dir = current_dir[:-1]
        elif directory == '..' or directory == '../':
            if current_dir == 'disk/':
                path_dir = "disk"
            else:
                path_dir = '/'.join(current_dir.split("/")[:-2]) + '/'
        elif len(directory) > 1 and directory[0] == '.' and directory[1] == '/':
            path_dir = current_dir + directory[2:]
        elif directory[0] == '/':
            path_dir = directory[1:]
        elif len(directory) > 1 and directory[0] == '~' and directory[1] == '/':
            path_dir = 'disk/' + directory[2:]
        elif len(directory) > 2 and directory[0] == '.' and directory[1] == '.' and directory[2] == '/':
            if current_dir != 'disk/':
                path_dir = ('/'.join(current_dir.split('/')[:-2]) + '/' + directory[3:])
            else:
                path_dir = current_dir + directory[3:]
        else:
            path_dir = current_dir + directory
        if path_dir.count('.') > 0:
            info.insert(tk.END, 'Not a directory: ' + path_dir + '\n')
            return 'Not a directory: ' + path_dir + '\n'
        with tarfile.open(disk_files, 'r') as tar:
            if all(member.name != path_dir for member in tar.getmembers()):
                info.insert(tk.END, 'No such directory: ' + path_dir + '\n')
                return 'No such directory: ' + path_dir + '\n'
            result = ''
            depth = path_dir.count('/') + 1
            for member in tar.getmembers():
                if fnmatch(member.name, path_dir + '/' + filename) and depth == member.name.count('/'):
                    result += member.name + '\n'
            if len(result) == 0:
                info.insert(tk.END, 'No such files: ' + filename + '\n')
                return 'No such files: ' + filename + '\n'
            else:
                info.insert(tk.END, result)
                return result


def command_analyzer(type_command='not_start_script'):
    global last_command
    if type_command == 'not_start_script':
        commandLine = entry.get()
    else:
        commandLine = type_command
    entry.delete(0, tk.END)
    command = commandLine.split()
    last_command = commandLine
    info.config(state=tk.NORMAL)
    if len(command) == 0:
        pass
    elif command[0] == 'ls':
        if len(command) > 1:
            command_ls(command[1])
        else:
            command_ls("")
    elif command[0] == 'cd':
        if len(command) > 1:
            command_cd(command[1])
        else:
            command_cd("")
    elif command[0] == 'exit':
        with open(log_file, mode='a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter='\t')
            writer.writerow(
                [user_name, last_command, datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%H:%M:%S")])
        sys.exit(0)
    elif command[0] == 'tac':
        if len(command) > 1:
            command_tac(command[1:])
        else:
            command_tac([])
    elif command[0] == 'touch':
        if len(command) > 1:
            command_touch(command[1])
        else:
            command_touch("")
    elif command[0] == 'mv':
        if len(command) == 3:
            command_mv(command[1], command[2])
        else:
            command_mv('error', 'error')
    elif command[0] == 'clear':
        info.delete('1.0', tk.END)
        with open(log_file, mode='a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter='\t')
            writer.writerow(
                [user_name, last_command, datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%H:%M:%S")])
    elif command[0] == 'find':
        if len(command) == 3:
            command_find(command[1], command[2])
        elif len(command) == 2:
            command_find('-all', command[1])
        else:
            command_find('error', 'error')
    else:
        info.insert(tk.END,
                    "username:" + user_name + " - " + current_dir + "> " + last_command + " - Unknown command\n")
    directory.config(text=current_dir + ">")
    info.config(state=tk.DISABLED)
    info.see(tk.END)


def start_script():
    script = open("start_script.txt", 'r')
    for i in script.readlines():
        command_analyzer(i[:-1])


def GUI():
    global root, info, input_frame, directory, entry, button
    root = tk.Tk()
    root.title("Virtual Shell")
    root.geometry("1200x600")
    info = scrolledtext.ScrolledText(root, width=40, height=10, wrap=tk.WORD, font=("Kristen ITC", 14), bg="pink")
    info.insert(tk.END, "Welcome to vShell, " + user_name + '\n')
    info.pack(expand=True, fill='both')
    info.config(state=tk.DISABLED)
    input_frame = tk.Frame(root, bg='pink')
    input_frame.pack(expand=True, fill='both')
    directory = tk.Label(input_frame, font=("Kristen ITC", 14), text=current_dir + ">", bg="pink")
    directory.pack(side=tk.LEFT, padx=30)
    entry = tk.Entry(input_frame, width=50, font=("Kristen ITC", 14))
    entry.pack(side=tk.LEFT, padx=30)
    entry.bind('<Return>', lambda event: command_analyzer())
    button = tk.Button(input_frame, text="Confirm", command=command_analyzer, font=("Kristen ITC", 14))
    button.pack(side=tk.LEFT, padx=30)
    root.resizable(False, False)
    return root


root = GUI()
start_script()
root.mainloop()
