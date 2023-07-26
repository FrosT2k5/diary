#!/usr/bin/env python3
from time import sleep
from subprocess import run
from setup import getconfig
from func import git_pull,git_push
import pexpect
import datetime
from os.path import isfile


# This file is used only to write in diary, func.py is used for other functions like decrypting, pull/push etc

if __name__ == "__main__":
    if not isfile(".config.json"):
        # Exit the program if user hasn't setup the diary
        print("Looks like you didn't yet setup the diary! Please use setup.py to setup first\nCheck out instructions at https://github.com/FrosT2k5/diary")
        exit()

    # Get the user information
    configdict = getconfig()
    year = configdict['year'] + ".txt"

    # Get Today's Date
    x = datetime.datetime.now()
    date = x.strftime("%m/%d/%Y, %a, %I:%M%P") #Format the date 

    # Decrypt diary and gitlab password
    print("Decrypting...\n")
    gitpassword = run("gpg -d pass.gpg",shell=True,capture_output=True,check=True,text=True).stdout

    gitpullcheck = input("Run a git pull? (RECOMMENDED) (y/N): ")
    if gitpullcheck == "N" or gitpullcheck == "n":
        print("Not running git pull can cause conflicts when using diary across multiple devices, use this option cautiously")
        sleep(2)
    else:
        git_pull(gitpassword)

    if isfile(year+".gpg"):
        run(f"gpg -o {year} -d {year+'.gpg'}",shell=True,check=True)
        run(f"rm {year+'.gpg'}",shell=True)
    else:
        print("Happy new year, I guess? :)")
    sleep(0.5)
    print("Decrypted successfully")

    # After decryption, 
    # Save new event to cache.txt
    print("Let's take your new life moment and put it in your digital secured diary...")
    sleep(1)
    run("touch cache.txt",shell=True)
    run(f'echo "\n\n\n\n{date}:\n" > cache.txt',shell=True)
    run("nano +7 cache.txt",shell=True)
    input("Press enter to continue(you can edit cache.txt with external text editor meanwhile: ")
    
    # Append content of cache.txt to the previously decrypted year.txt using echo
    # Linux is best
    print("Alright ,awesome moments being saved...")
    run(f"cat cache.txt >> {year}",shell=True)
    run("rm cache.txt",shell=True)
    sleep(1)

    # Encrypt year.txt back again after appending
    print("Done, now let's encrypt the file again")
    run(f"gpg -e -r \"{configdict['name']}\" {year}",shell=True,check=True)

    # Remove year.txt after encrypting 
    run(f"rm {year}",shell=True)

    #Time to push to git
    gitpushcheck = input("Do you want to push to git? (RECOMMENDED) (Y/n): ")
    if gitpushcheck == "N" or gitpushcheck == "n":
        print("Not running git push can cause conflicts when using diary across multiple devices, use this option cautiously \n make sure you dont write anything in diary in different device until you push from this device.")
        print("Push later using func.py")
        sleep(2)
    else:
        git_push(gitpassword)
