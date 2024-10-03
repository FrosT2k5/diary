#!/usr/bin/env python3

from subprocess import run
import pexpect
import datetime
from setup import getconfig
from os.path import isfile

# func.py provides additional functionality to diary (encryption, decryption, git pull, git push, dropping local changes) 


# Remove git cache to avoid pexpect errors
run("rm -f $HOME/.cache/git/credential/socket",shell=True)

def git_pull(gitpassword):
    gitusername = getconfig()['gitusername']
    pull = pexpect.spawn('git pull diary master')
    pull.expect("Username")
    pull.sendline(gitusername)
    pull.expect("Password")
    pull.sendline(gitpassword)
    pull.interact()
    run("rm -f $HOME/.cache/git/credential/socket",shell=True)

def git_push(gitpassword):
    gitusername = getconfig()['gitusername']
    x = datetime.datetime.now()
    cdate = x.strftime("%m/%d/%Y")
    run("git add .",shell=True)
    run(f"git commit -m 'Update on {cdate}'",shell=True)
    push = pexpect.spawn('git push -u diary master')
    push.expect("Username for 'https://gitlab.com': ")
    push.sendline(gitusername)
    push.expect("Password") 
    push.sendline(gitpassword)
    push.interact()
    run("rm -f $HOME/.cache/git/credential/socket",shell=True)

if __name__ == "__main__":
    hlp = """
1. decrypt the current year diary
2. encrypt the current year diary (year.txt)
3. cancel all local changes (git checkout .) (run 'git status' in terminal to see local changes)
4. Decrypt previous year diary (year.txt.gpg)
5. Encrypt previouss year diary (year.txt)
6. Git pull
7. Git push
8. exit
Check setup.py for additional functionalities(related to configuration)
...
"""
    if not isfile(".config.json"):
        # Exit the program if user hasn't setup the diary
        print("Looks like you didn't yet setup the diary! Please use setup.py to setup first\nCheck out instructions at https://github.com/FrosT2k5/diary")
        exit()
    configdict = getconfig()
    year = configdict['year'] + '.txt'
    run("clear",shell=True)
    gitpassword = run("gpg -d pass.gpg",shell=True,capture_output=True,check=True,text=True).stdout
    while True:
        print(hlp)
        inp = input("Diary: ")
        if inp == "1":
            run(f"gpg -o {year} -d {year+'.gpg'}",shell=True,check=True)
            print(f"Decrypted {year}")
            exit()
        elif inp == "2":
            run(f"gpg -e -r \"{configdict['name']}\" {year}",shell=True,check=True)
            print("Encrypted ",year+".gpg")
            exit()
        elif inp == "3":
            run("git checkout .",shell=True)
            run("rm -f *.txt",shell=True)
            print("Dropped all local changes.")
            exit()
        elif inp == "4":
            yeartodecrypt = input("Enter year number to decrypt its file: ")
            encryptedfile = yeartodecrypt + ".txt.gpg"
            cmdtorun = f"gpg -o {yeartodecrypt+'.txt'} -d {encryptedfile}"
            print(cmdtorun)
            run(cmdtorun,shell=True)
            exit()
        elif inp == '5':
            yeartoencrypt = input("Enter year number to encrypt its file: ")
            decryptedfile = yeartoencrypt + ".txt"
            cmdtorun = f"gpg -e -r \"{configdict['name']}\" {decryptedfile}"
            print(cmdtorun)
            run(cmdtorun,shell=True)
            print("Encrypted...")
            exit()
        elif inp == "6":
            git_pull(gitpassword)
            exit()
        elif inp == "7":
            git_push(gitpassword)
            exit()
        elif inp == "8":
            exit()
        else:
            print("Enter valid input")
            
            
