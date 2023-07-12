#!/usr/bin/env python3
from time import sleep
from subprocess import run
from os.path import isfile
import json
import re
import datetime
import pexpect
from diarykeygen import genkey


# Setting up diary (.config.json) and editing config.json via this script
# Also manage gitlab password with this script


def dumpconfig(configdict):
    #This function is used to dump provided configdict to .config.json
    with open(".config.json","w+") as jsonfile:
        json.dump(configdict,jsonfile,indent=4)


def getconfig():
    #This function returns json from .config.json as dictionary
    with open(".config.json") as jsonfile:
        return json.load(jsonfile)


def pushfirsttime(gitusername,gitpassword,gitremote):
    #This function is needed to set git remote, so just running git push from next time would push to master branch of remote specified by the user
    run("git remote remove diary 2>/dev/null",shell=True) #Remove remote if already exists
    remotecmd = "git remote add diary " + gitremote 
    run(remotecmd,shell=True)
    usercmd = f"git config user.name {gitusername} && git config user.email {getconfig()['email']}"
    run("git add . && git commit -m 'Initializing diary'",shell=True)
    push = pexpect.spawn('git push -u diary master')
    push.expect("Username for 'https://gitlab.com': ")
    push.sendline(gitusername)
    push.expect("Password") 
    push.sendline(gitpassword)
    push.interact()
    run("rm -f $HOME/.cache/git/credential/socket",shell=True)


def gengitpassword(name,gitpassword):
    print("\nYour password is stored securely in pass.gpg just like the diary. You will be asked to overwrite that file if you are reentering password")
    run(f"echo {gitpassword} > pass",shell=True)
    passwordcmd = f"gpg -e -r \"{name}\" -o pass.gpg pass"
    run(passwordcmd,shell=True,capture_output=True,check=True)
    run("rm -f pass",shell=True)


# write this text to README_CAREFULLY.txt in backup folder
backuprestorenote = "This folder (backup/) contains backup of your diary keys and configuration. \
    \n Copy all files of this folder to a safe place, DO NOT LEAK OR MAKE PUBLIC! \
    \n If you make these file public anyone can decrypt your diary very easily. \
    \n It is recommended to delete these files after you store them safely. \
    \n List of files: public.key, private.key, ownertrust.gpg.txt, config.json \n \
    \n To restore diary in another device, check out instructions at : \
    \nhttps://github.com/FrosT2k5/diary/blob/master/Instructions.md#backing-up-and-restoring-diary-and-using-across-multiple-devices\n"


def backupdiary():
    print("\n\n",backuprestorenote)
    print("\nBacking up keys and configuration...")
    sleep(4)
    configdict = getconfig()
    email = configdict["email"]
    run(f"gpg --export --export-options backup --output backup/public.key {email}",shell=True,check=True) #This will backup public key
    run(f"gpg --export-secret-key --export-options backup --output backup/private.key {email}",shell=True,check=True) #This will backup private key
    run(f"gpg --export-ownertrust > backup/ownertrust.gpg.txt",shell=True,check=True) #Backup key usertrust info
    run(f"cp .config.json backup/config.json",shell=True,check=True) #Backup configuration
    with open("backup/README_CAREFULLY.txt","w+") as readmefile:
        readmefile.write(backuprestorenote)
    print("Backed up public.key,private.key,config.json & ownertrust.gpg.txt to backup/ folder")


def restorediary():
    if isfile("pass.gpg"):
        print("Found pass.gpg, you probably cloned correct repo!")
    else:
        print("pass.gpg missing, looks like you cloned template repository, please clone the one hosted on your personal gitlab account. \n Check below link for more info: \n")
        return 0
    # If above check is passed then user has cloned correct repo, proceed to look if backup files exist

    for i in ('backup/public.key','backup/private.key','backup/ownertrust.gpg.txt','backup/config.json'):
        if not isfile(i):
            print(f"{i} not found, please check below link for instructions on how to restore diary!\nhttps://github.com/FrosT2k5/diary/blob/master/Instructions.md#backing-up-and-restoring-diary-and-using-across-multiple-devices")
            return 0
    # Since everything is correct, proceed to restore
  
    # First restore .config.json so that getconfig() will work  
    run("cp backup/config.json .config.json",shell=True,check=True)
    configdict = getconfig()
    run(f"gpg --import --import-options restore backup/public.key",shell=True,check=True) # This will restore public key
    run(f"gpg --import --import-options restore backup/private.key",shell=True,check=True) #This will restore private key
    run(f"gpg --import-ownertrust backup/ownertrust.gpg.txt",shell=True,check=True) #Backup key usertrust info
    print("Congratulations, Restored diary! You can now proceed to use it, running git push for first time to setup remote now.")
    gitpassword = run("gpg -d pass.gpg",shell=True,capture_output=True,check=True,text=True).stdout
    pushfirsttime(configdict['gitusername'],gitpassword,configdict['gitremote'])


# This function is used to generate json and keys when user runs this script for first time
def genjson(keycheck=None):
    print("Please enter correct information.")
    # Function to take and validate input from user 
    def parseinput(inputtype,regexp,inputinfo):
        while True:
            inputdata = input(f"Enter {inputtype}: ")
            pattern = re.compile(regexp)
            valid = re.search(pattern,inputdata)
            if valid:
                return inputdata
            else:
                print("Enter valid input,",inputinfo)

    name = parseinput("Full Name",r"^[A-Za-z]{3,}\ [A-Za-z]{3,}$","Format: first_name last_name,atleast 3 chars long")
    print("Name: ",name)
    
    email = parseinput("Email: ",r"^[A-Za-z0-9+_.-]+@.+\..+$","Format: abc@example.com")
    print("Email: ",email)

    passphrase=parseinput("Password","^[A-Za-z1-9@$!%*#?&]{8,}$","Atleast 8 characters long. Only english letters, numbers and special characters.")
    print("Password: ",passphrase)
    print("Store your password somewhere safe, you can't change it later.")
    sleep(0.5)

    gitusername = input("Enter gitlab username: ")
    gitpassword = input("Enter gitlab password: ")
    gitremote = "https://gitlab.com/"+gitusername+"/mydiary.git"
    print("Automatically generated gitlab url: ",gitremote)
    grcheck = input("Proceed with above url? (y/n): ")
    if grcheck.lower() == "n":
        gitremote = input("Enter git remote url: ")

    # Allow user to skip generating key if they have one already 
    if keycheck != "s":
        genkey(name,email,passphrase)
    
    # List the user generated key for diary here, so that user can check it for reference
    keylist = run(f"gpg --list-secret-keys | grep -B3 -A2 uid | grep -B3 -A2 {email}",shell=True,check=True,capture_output=True,text=True).stdout

    print("\n\nHere is the generated key, make sure it's info is correct.\n",keylist)   
    
    year = datetime.datetime.now().strftime("%Y")

    configdict = {
    "name": name,
    "email": email,
    "year": year,
    "gitusername": gitusername,
    "gitremote": gitremote,
    }

    #Encrypt gitlab password
    gengitpassword(name,gitpassword)

    #Finally dump the config after everything has checked out
    dumpconfig(configdict)
    
    #After generating json, push to gitlab for first time
    configdict = getconfig()
    gitpassword = run("gpg -d pass.gpg",shell=True,capture_output=True,check=True,text=True).stdout
    pushfirsttime(configdict['gitusername'],gitpassword,configdict['gitremote'])


# This function is main menu
def menu():
    # clean git cache on startup
    run("rm -f $HOME/.cache/git/credential/socket",shell=True)

    sleep(0.5)
    print("What do you want to do?\n")
    print("1: Regenrate config (change name,email, password,etc)")
    print("2: Make new key and switch key(NOT RECOMMENDED!)")
    print("3: Change gitlab password")
    print("4: Print current gitlab password")
    print("5: Update year in config")
    print("6: Push to your private repo (For first time), setting up git remote")
    print("7: Backup diary (keys and configuration)")
    print("8: Restore diary (keys and configuration)")
    print("9: Quit")
    print("\nChoose number of option you want")
  
    inp = input("input: ")
    if inp == "1":
        print("\nRegenerating config without regenerating key")
        print("Make sure you enter same info as in")
        genjson(keycheck="s")
    elif inp == "2":
        print("Use this option extremely carefully! This will make your previous diary undecryptable if they were encrypted with different key. Know what you are doing. Always backup keys and store in a safe place")
        confrm = input("Do you want to proceed (Y/n): ").upper()
        if confrm == "Y":
            genjson() #Generate json without keycheck being True
    elif inp == "3":
        gitpassword = input("Enter gitlab password: ").strip()
        gengitpassword(getconfig()['name'],gitpassword)
    elif inp == "4":
        print("Your password:")
        run("gpg -d pass.gpg",shell=True)
        exit()
    elif inp == "5":
        configdict = getconfig()
        year = input("Enter year number: ")
        configdict['year'] = year
        dumpconfig(configdict)
        print("Switched year to ",year)
        exit()
    elif inp == "6":
        configdict = getconfig()
        gitpassword = run("gpg -d pass.gpg",shell=True,capture_output=True,check=True,text=True).stdout
        pushfirsttime(configdict['gitusername'],gitpassword,configdict['gitremote'])
    elif inp == "7":
        backupdiary()
        exit()
    elif inp == "8":
        restorediary()
        exit()
    elif inp == "9":
        exit()
    else:
        print("Enter valid input.")
        
if __name__ == "__main__":
    # Actual program starts from here
    # Clear screan on startup
    run("clear")
    
    if not isfile(".config.json"):
        if not isfile("pass.gpg"):
            print("Looks like you are running me for the first time, Welcome :)\n")
            check = input("Press enter to continue: ")
            sleep(0.3)
            if check.lower == "y":
                genjson(keycheck="s") #For advanced users, generate json without generating key.
            else:
                genjson() #Generate json
        else:
            restorecheck = input("Looks like you need to restore diary, proceed with restoring? (y/n): ")
            if restorecheck.lower() == "y":
                restorediary()
            else:
                print("Okay! regenrating new configuration from scrarch")
                genjson()
    else:
        print("Config found! Looks like you've already setup diary\n\n")
        sleep(0.5)
        print("Your info:")
        configdict = getconfig()
        for i in configdict:
            sleep(0.2)
            print(i,":",configdict[i])
        print("")
        while True:
            menu()
