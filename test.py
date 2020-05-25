from os import listdir
from os.path import isfile, join

def list_all_files():
    mypath = "C:/Users/LENOVO/Downloads/AES All Prds JOSN/AES All Prds JOSN"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return onlyfiles

def read_f():
    with open("stat.txt") as file:
        data = file.read()
        return data

def write_f(val):
    with open("stat.txt", "w") as f:
        f.write(val) 
