#!/usr/bin/env python3
import argparse
from time import sleep
from subprocess import run
import datetime
from os.path import isfile
from setup import getconfig
from func import git_pull,git_push

# Get the user information
if not isfile(".config.json"):
    # Exit the program if user hasn't setup the diary
    print("Looks like you didn't yet setup the diary! Please use setup.py to setup first\nCheck out instructions at https://github.com/FrosT2k5/diary")
    exit()
configdict = getconfig()


parser = argparse.ArgumentParser(
                    prog='Diary',
                    description='Write text to diary',
                    epilog='Encrypt files inside files and folders and delete the original file.')
parser.add_argument("filename", nargs="?", help="File to encrypt", default=False)
parser.add_argument("-n","--no-cache", help="Don't open cache.txt, directly encrypt the file", action="store_true")

def encrypt_file(filename, disable_year=False, append_cache=True):
    # Get Today's Date
    x = datetime.datetime.now()
    date = x.strftime("%m/%d/%Y, %a, %I:%M%P") #Format the date 

    if isfile(filename+".gpg"):
        run(f"gpg -o {filename} -d {filename+'.gpg'}",shell=True,check=True)
        run(f"rm {filename+'.gpg'}",shell=True)
    else:
        if not disable_year:
            print("Happy new year, I guess? :)")
    sleep(0.5)
    print("Decrypted successfully")

    # After decryption, 
    # Save new event to cache.txt
    if append_cache:
        print("Let's take your new life moment and put it in your digital secured diary...")
        sleep(1)
        run("touch cache.txt",shell=True)
        run(f'echo "\n\n\n\n{date}:\n" > cache.txt',shell=True)
        run("nano +7 cache.txt",shell=True)
        input("Press enter to continue(you can edit cache.txt with external text editor meanwhile: ")
    
        # Append content of cache.txt to the previously decrypted year.txt using echo
        # Linux is best
        print("Alright ,awesome moments being saved...")
        run(f"cat cache.txt >> {filename}",shell=True)
        run("rm cache.txt",shell=True)
        sleep(1)

    # Encrypt year.txt back again after appending
    print("Done, now let's encrypt the file again")
    run(f"gpg -e -r \"{configdict['name']}\" {filename}",shell=True,check=True)

    # Remove year.txt after encrypting 
    run(f"rm {filename}",shell=True)

# This file is used only to write in diary, func.py is used for other functions like decrypting, pull/push etc

if __name__ == "__main__":

    year = configdict['year'] + ".txt"

    # Decrypt diary and gitlab password
    print("Decrypting...\n")
    gitpassword = run("gpg -d pass.gpg",shell=True,capture_output=True,check=True,text=True).stdout

    gitpullcheck = input("Run a git pull? (RECOMMENDED) (y/N): ")
    if gitpullcheck == "N" or gitpullcheck == "n":
        print("Not running git pull can cause conflicts when using diary across multiple devices, use this option cautiously")
        sleep(2)
    else:
        git_pull(gitpassword)

    # diary
    args = parser.parse_args()
    if args.filename:
        encrypt_file(args.filename, disable_year=True, append_cache=not (args.no_cache))
    else:
        encrypt_file(year, disable_year=False, append_cache=not (args.no_cache))
        
    #Time to push to git
    gitpushcheck = input("Do you want to push to git? (RECOMMENDED) (Y/n): ")
    if gitpushcheck == "N" or gitpushcheck == "n":
        print("Not running git push can cause conflicts when using diary across multiple devices, use this option cautiously \n make sure you dont write anything in diary in different device until you push from this device.")
        print("Push later using func.py")
        sleep(2)
    else:
        git_push(gitpassword)
