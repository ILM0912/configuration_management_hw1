import csv
import os
import shutil
import sys
import tkinter as tk
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
        writer.writerow([user_name, last_command, datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%H:%M:%S")])
    if len(path) == 0 or path == ".":
        with tarfile.open(disk_files, 'r') as tar:
            result = ""
            for member in tar.getmembers():
                if current_dir in member.name:
                    file = member.name[len(current_dir):].split("/")
                    if len(file) == 1:
                        result += file[0] + "\n"
            if len(result) == 0:
                info.insert(tk.END, 'Directory is empty\n')
            else:
                info.insert(tk.END, result)
    elif path == "~" or path == '/':
        with tarfile.open(disk_files, 'r') as tar:
            result = ""
            for member in tar.getmembers():
                if 'disk/' in member.name:
                    file = member.name[len("disk/"):].split("/")
                    if len(file) == 1:
                        result += file[0] + "\n"
            if len(result) == 0:
                info.insert(tk.END, 'Directory is empty\n')
            else:
                info.insert(tk.END, result)
    elif path[0] == '.' and path[1] == '.' and path[2] == '/':
        if path[3:].count('.') > 0:
            info.insert(tk.END, 'No such directory: ' + path + '\n')
            return
        if current_dir != 'disk/':
            path = ('/'.join(current_dir.split('/')[:-2]) + '/' + path[3:])
        else:
            path = current_dir + path[3:]
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
            else:
                info.insert(tk.END, result)
    elif path == "..":
        dir = '/'.join(current_dir.split("/")[:-2]) + '/'
        if current_dir == "disk/":
            info.insert(tk.END, 'disk\n')
            return
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
                else:
                    info.insert(tk.END, result)
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
            else:
                info.insert(tk.END, result)
    else:
        if path[0] == "." and path[1] == '/':
            path = path[2:]
        with tarfile.open(disk_files, 'r') as tar:
            result = ""
            flag = any((current_dir + path) == member.name and path.count('.') == 0 for member in tar.getmembers())
            if not flag:
                info.insert(tk.END, 'No such directory: ' + path + '\n')
                return
            for member in tar.getmembers():
                if current_dir + path + "/" in member.name:
                    file = member.name[len(current_dir + path + "/"):].split("/")
                    if len(file) == 1:
                        result += file[0] + "\n"
            if len(result) == 0:
                info.insert(tk.END, 'Directory is empty\n')
            else:
                info.insert(tk.END, result)


def command_cd(path):
    global current_dir, last_command
    info.insert(tk.END, "username:" + user_name + " - " + current_dir + '> ' + last_command + '\n')
    with open(log_file, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        writer.writerow([user_name, last_command, datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%H:%M:%S")])
    if len(path) == 0 or path == '.':
        info.insert(tk.END, current_dir + '\n')
    elif path == "~" or path == '/':
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
    elif path == "..":
        if current_dir == "disk/": return
        current_dir = '/'.join(current_dir.split("/")[:-2]) + '/'
    elif path[0] == '.' and path[1] == '.' and path[2] == '/':
        if path[3:].count('.') > 0:
            info.insert(tk.END, 'No such directory: ' + path + '\n')
            return
        if current_dir != 'disk/':
            dir = ('/'.join(current_dir.split('/')[:-2]) + '/' + path[3:])
        else:
            dir = current_dir + path[3:]
        with tarfile.open(disk_files, 'r') as tar:
            flag = any((dir == member.name and dir.count('.') == 0 for member in tar.getmembers()))
            if not flag:
                info.insert(tk.END, 'No such directory: ' + dir + '\n')
                return
            else:
                current_dir = dir + '/'
    else:
        if path[0] == "." and path[1] == '/':
            path = path[2:]
        with tarfile.open(disk_files, 'r') as tar:
            flag = any((current_dir + path) == member.name and path.count('.') == 0 for member in tar.getmembers())
            if not flag:
                info.insert(tk.END, 'No such directory: ' + path + '\n')
                return
            else:
                current_dir += path + '/'


def command_tac(files):
    info.insert(tk.END, "username:" + user_name + " - " + current_dir + '> ' + last_command + '\n')
    with open(log_file, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        writer.writerow([user_name, last_command, datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%H:%M:%S")])
    if len(files) == 0:
        info.insert(tk.END, 'Empty\n')
        return
    for file in files:
        if file[0] == '/':
            path = file[1:]
        elif file[0] == '~' and file[1] == '/':
            path = 'disk/' + file[2:]
        elif len(file)>1 and file[0]=='.' and file[1]=='/':
            path = current_dir + file[2:]
        elif len(file)>2 and file[0] == '.' and file[1] == '.' and file[2] == '/':
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
                continue
            with tar.extractfile(path) as extracted_file:
                result = ""
                lines = extracted_file.readlines()
                lines = [line.decode('utf-8').strip() for line in lines][::-1]
                for i in lines:
                    result += i
                    if i[-1] != '\n':
                        result += '\n'
                info.insert(tk.END, 'file: ' + path + '\n' + result + '\n')


def command_touch(filename):
    info.insert(tk.END, "username:" + user_name + " - " + current_dir + '> ' + last_command + '\n')
    with open(log_file, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        writer.writerow([user_name, last_command, datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%H:%M:%S")])
    if len(filename) == 0:
        info.insert(tk.END, 'Empty\n')
        return
    if filename[0] == '/':
        path = filename[1:]
    elif filename[0] == '~' and filename[1] == '/':
        path = 'disk/' + filename[2:]
    elif len(filename) > 1 and filename[0] == '.' and filename[1] == '/':
        path = current_dir + filename[2:]
    elif len(filename)>2 and filename[0] == '.' and filename[1] == '.' and filename[2] == '/':
        if current_dir != 'disk/':
            path = ('/'.join(current_dir.split('/')[:-2]) + '/' + filename[3:])
        else:
            path = current_dir + filename[3:]
    else:
        path = current_dir + filename
    with tarfile.open(disk_files, 'r') as tar:
        if path.count('.') != 1:
            info.insert(tk.END, 'It is not a file: ' + path + '\n')
            return
        elif any(path == member.name for member in tar.getmembers()):
            info.insert(tk.END, 'File already exists: ' + path + '\n')
            return
        else:
            name, filetype = '/'.join(path.split('/')[-1]).split('.')
            if len(name) == 0 or len(filetype) == 0:
                info.insert(tk.END, 'It is not a file: ' + path + '\n')
                return
    open('temp_file_path.txt', 'a').close()
    try:
        with tarfile.open(disk_files, 'a') as tar:
            info.insert(tk.END, 'File created: ' + path + '\n')
            tar.add('temp_file_path.txt', arcname=path)
    finally:
        os.remove('temp_file_path.txt')

def command_mv(source, destination):
    info.insert(tk.END, "username:" + user_name + " - " + current_dir + '> ' + last_command + '\n')
    with open(log_file, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        writer.writerow([user_name, last_command, datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%H:%M:%S")])

    if source == 'error' and destination == 'error':
        info.insert(tk.END, 'please enter source and destination\n')
        return
    if source[0] == '/':
        path_source = source[1:]
    elif source[0] == '~' and source[1] == '/':
        path_source = 'disk/' + source[2:]
    elif len(source) > 1 and source[0] == '.' and source[1] == '/':
        path_source = current_dir + source[2:]
    elif len(source)>2 and source[0] == '.' and source[1] == '.' and source[2] == '/':
        if current_dir != 'disk/':
            path_source = ('/'.join(current_dir.split('/')[:-2]) + '/' + source[3:])
        else:
            path_source = current_dir + source[3:]
    else:
        path_source = current_dir + source

    if destination[0] == '/':
        path_destination = destination[1:]
    elif destination[0] == '~' and destination[1] == '/':
        path_destination = 'disk/' + destination[2:]
    elif len(destination) > 1 and destination[0] == '.' and destination[1] == '/':
        path_destination = current_dir + destination[2:]
    elif len(destination)>2 and destination[0] == '.' and destination[1] == '.' and destination[2] == '/':
        if current_dir != 'disk/':
            path_destination = ('/'.join(current_dir.split('/')[:-2]) + '/' + destination[3:])
        else:
            path_destination = current_dir + destination[3:]
    else:
        path_destination = current_dir + destination
    print(path_source, path_destination)
    with tarfile.open(disk_files, 'r') as tar:
        if path_source.count('.') != 1 and path_destination.count('.') != 1:
            info.insert(tk.END, 'Not files: ' + path_source + ' ' + path_destination + '\n')
            return
        elif path_source.split('.')[-1] != path_destination.split('.')[-1]:
            info.insert(tk.END, 'You can`t change file type ' + path_source + ' ' + path_destination + '\n')
            return
        else:
            name1, filetype1 = '/'.join(path_source.split('/')[-1]).split('.')
            name2, filetype2 = '/'.join(path_destination.split('/')[-1]).split('.')
            if len(name1) == 0 or len(name2) == 0 or len(filetype1) == 0 or len(filetype2) == 0:
                info.insert(tk.END, 'Not files: ' + path_source + ' ' + path_destination + '\n')
                return
    with tarfile.open(disk_files, 'r') as tar:
        if all(member.name != path_source for member in tar.getmembers()):
            info.insert(tk.END, 'No such file: ' + path_source + '\n')
            return
        if any(member.name == path_destination for member in tar.getmembers()):
            info.insert(tk.END, 'File already exists: ' + path_destination + '\n')
            return
        if all(member.name != '/'.join(path_destination.split('/')[:-1]) for member in tar.getmembers()):
            info.insert(tk.END, 'No destination directory ' + '/'.join(path_destination.split('/')[:-1]) + '\n')
            return
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


def command_analyzer():
    global last_command
    commandLine = entry.get()
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
            writer.writerow([user_name, last_command, datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%H:%M:%S")])
    else:
        info.insert(tk.END, "username:" + user_name + " - " + current_dir + "> " + last_command + " - Unknown command\n")
    directory.config(text=current_dir + ">")
    info.config(state=tk.DISABLED)
    info.see(tk.END)


root = tk.Tk()
root.title("Virtual Shell")
root.geometry("1000x500")
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

# root.resizable(False, False)
root.mainloop()
