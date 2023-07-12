from subprocess import run
import re

rawkeyparams = """
     Key-Type: RSA
     Key-Length: 4096
     Name-Real: username
     Name-Comment: The gpg key for your personal diary
     Name-Email: useremail
     Key-Usage: encrypt
     Expire-Date: 0
     Passphrase: userpassphrase
     %commit
     %echo done
"""

def genkey(name,email,passphrase):
    print("Generating Key with name: ",name,"\nEmail: ",email)
    print("It's good idea to move your cursor and window for maximum entropy\nThis might take some time.")

    # Replace username, useremail and password in key parameters
    keyparams = re.sub(r"(username)$",name,rawkeyparams,flags=re.M)
    keyparams = re.sub(r"(useremail)$",email,keyparams,flags=re.M)
    keyparams = re.sub(r"(userpassphrase)$",passphrase,keyparams,flags=re.M)

    with open("keyparams.txt","w") as keyfile:
        keyfile.write(keyparams)

    run("gpg --batch --generate-key keyparams.txt",shell=True,check=True,capture_output=True,text=True)
    run("rm keyparams.txt",shell=True,check=True)
    print("Done!")
    return 0

    