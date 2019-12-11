import os
from datetime import datetime
from ftplib import FTP, error_perm
from urllib.request import urlretrieve, URLError
from socket import gaierror



def connect(HOST, PORT):
    ftp.connect(HOST, PORT) #connects to the server


try:
    user_choice = input('connect or login: ') == 'login'
    if user_choice.lower() == 'login':
        HOST = input('Enter host adress: ')
        login = input('Enter login or press enter if standart: ')
        password = input('Enter passsword or press enter if standart: ')
        ftp = FTP(HOST)
        hostport = HOST
        try:
            if login or password == '':
                ftp.login()
            else:
                ftp.login(login, password)
        except:
            print('Login or password is wrong. Try again...')
    elif user_choice.lower() == 'connect':
        HOST = input('Enter host ip: ')
        PORT = int(input('Enter port if needed, if not do not type anything: '))
        hostport = '{}:{}'.format(HOST, PORT)
        ftp = FTP()
        connect(HOST, PORT)
except ValueError:
    print(" Only integers acceptable in port input")
except gaierror:
    print(' Wrong ip or port. Try again...')
else:
    print("                 You're in your ftp server. Welcome.\n\n")





def path():
    return ftp.pwd() # returns path 

def list_dir():
    print(' \n '.join(ftp.nlst())) #prints files and directories in the directory

def move_to_dir(dir):
    ftp.cwd(dir) #moves to the selected dir

def rename(name, new_name):
    ftp.rename(name, new_name)

def mkdir(name):
    ftp.mkd(name) #makes directory

def delete_file(name):
    ftp.delete(name) #deletes selected file

def download_file(path, file_name):
    urlretrieve('ftp://{hostport}{path}'.format(hostport = hostport,path=path), '{}'.format(file_name))

def delete_dir(name): 
    ftp.rmd(name) #deletes selected directory

def upload_file(name):
    with open(name, 'rb') as file:
        ftp.storbinary('STOR {}'.format(name), file)


def help(): #prints help commands
    print(
        '''
        moveto - moves user to the directory you chose.
        exit - exit.
        list - prints all files and directories in the current directory.
        connect 'host':'port if needed' - connects to the server.
        help - prints all available commands.
        mkdir "name" - makes directory.
        del - deletes the selected file/directory.
        rename - renames selected dir/file.
        get "file" - downloads selected file. YOU CAN'T DOWNLOAD DIRECTORY!
        getd - downloads CURRENT directory. YOU CAN'T DOWNLOAD FILE!
        '''
    )


while True:
    user_input = input(path() + '> ')

    if user_input == 'list':
        list_dir()

    elif user_input == 'connect':
        ftp.connect(HOST, PORT)

    elif user_input == 'help':
        help()

    elif user_input == 'exit':
        ftp.quit()

    elif user_input.startswith('moveto'):
        try:
            dir = user_input.replace('moveto ', '') #directory after command
            move_to_dir(dir)
        except error_perm:
            print(' ERROR: There is no such directory (550)')

    elif user_input.startswith('mkdir '):
        name = user_input.replace('mkdir ', '')
        mkdir(name)

    elif user_input.startswith('del '):
        name = user_input.replace('del ', '')
        try:
            delete_file(name)
        except:
            try:
                delete_dir(name)
            except error_perm:
                print(' ERROR: There is no such directory or no rights. (550)')
                print(' Also you can delete directories only when they are empty')
            else:
                print(' Succsessfully deleted')
        else:
            print(' Successfully deleted')
    
    elif user_input.startswith('rename '):
        name = user_input.replace('rename ', '')
        new_name = input('Enter new name: ')
        try:
            rename(name, new_name)
        except error_perm:
            print(' ERROR: There is no such directory (550)')
        else:
            print(' Succsessfully renamed')
    
    elif user_input.startswith('get '):
        try:
            file_name = user_input.replace('get ', '')
            file_path = path() + '/' + file_name
            download_file(file_path, file_name)
        except Exception as error:
            print(error)
        else:
            print(' {} downloaded succsessfully'.format(file_name))
    
    elif user_input.startswith('getd '):
        dir_name = user_input.replace('getd ', '')
        dir_path = path()
        try:
            if dir_name not in os.listdir():
                os.mkdir(dir_name)
                os.chdir(dir_name)
            else:
                os.chdir(dir_name)
        except FileNotFoundError:
                dir_name = str(datetime.now().strftime("%Y-%m %H-%M-%S"))
                os.mkdir(dir_name)
                os.chdir(dir_name)
        try:        
            for counts in ftp.nlst():
                print(' Downloading -> {}'.format(counts))
                urlretrieve('ftp://{host}:{port}{directory}/{counts}'.format(directory = dir_path, counts = counts,
                host = HOST, port = PORT), filename = counts)
        except URLError:
            print(" ERROR: invalid urlretrieve path. (550) I know how to fix this but I won't do it.")
            print(" You can't download root directory.")
        os.chdir('..')

    elif user_input.startswith('send '):
        name = user_input.replace('send ', '')
        try:
            upload_file(name)
        except Exception as error:
            print(error)
    else:
        print(' ERROR: Nonexistent command. Try "help"')

        

    