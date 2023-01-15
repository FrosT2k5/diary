# FrosT's Diary Installation & Usage Instructions

**Requirements:**
- Familiarity with Linux Terminal(Command Line) and git
- A gitlab account(since github doesn't support pushing with password)
- Patience

## Installation & Usage:

I expect that you already have gitlab account (Along with it's username, email and password(important)) by now

** **
1. Install dependencies based on your Linux distro

For Debian/Debian Based Distros: 
```
sudo apt update
sudo apt install python3 python3-pip gnupg expect git curl nano vim
```

For Termux: 
```
pkg update
pkg install python gnupg git expect curl nano vim
```

** **
2. Clone diary repository
```
git clone https://github.com/Frost2k5/diary/
cd diary
```

** **
3. Setup Git name & Email
```
git config --global user.name your_username_here 
git config --global user.email your_email_here 
```
Replace your_username_here and your_email_here with your GitLab username & email respectively, without using quotes("")

Ignore if done in your system already(different ID works here and only here)

** **
4. Install requirements.txt
```
pip3 install -r requirements.txt
```

** **
5. Run setup.py and setup diary
```
python3 setup.py
```
**Note:**
1. When asked to enter git remote, enter ```https://gitlab.com/yourusername/mydiary``` <br>
Replace yourusername with your username, if you enter this correctly gitlab should automatically make a private repo for you on completing setup
2. Be extremely careful when choosing and generating gnupg keys, once you select a key you can't easily switch it later
3. Don't forget your gpg key's password/passphrase, there is no way to recover it if lost. Write it down somewhere safe
4. Read the starting information after running setup.py carefully.

** **
6. Setup Complete

If the above command doesn't error out then you are good to proceed further. Else repeat above step.

- Writing to diary:
```
python3 diary.py
```
It should ask to run git pull, it is recommended to always press 'y' unless you know what you are doing.
This will open nano text editor with cache.txt as file. It will already have current date and time. Write whatever you want on it and then press Ctrl+X and Y to save the file.
After this, diary.py will wait for you to press enter to continue. You can use other text editors to edit cache.txt meanwhile.
Finally it will ask to git push, it is recommended to always press 'y' unless you know what you are doing.

## Additional functionality
What's the use of encrypted diary if you can't decrypt it, so func.py can be used to encrypt, decrypt, run git pull and push, cleanup local changes, etc.
Run: 
```
python3 func.py
``` 
for more information

## Editing/Regenrating Configuration and Git password, changing default year
Use setup.py to
- backup and restore diary (Read below for more info)
- Switch default year
- Change git password
- Regerate key & config <br>
Run:
```
python3 setup.py
```
To see your current configuration and functionalities regarding it <br>
The config is written to ```.config.json```. It is not recommend to edit it without knowing what you are doing

## Backing Up and Restoring diary (and using across multiple devices)
Backing up:
1. Run setup.py and choose option that says Backup diary
2. Follow on screen instructions
3. Read backup/README_CAREFULLY.txt very carefully
4. Copy everything from backup/ folder to a safe place (DO NOT LEAK! IT CAN BE USED TO ACCESS YOUR DIARY EASILY)

Restoring:
Make sure you install all requirements & dependencies before proceeding with this
1. Clone your private gitlab diary repo using command: ```git clone https://gitlab.com/yourusername/mydiary``` (replace yourusername with gitlab username, change repo name according to one you entered, it is mydiary according to Instructions.md. You can also check your gitlab account personal projects)
2. Copy the previously backed up files from backup/ folder, inside the newly cloned mydiary backup/ folder
3. Run setup.py and press "Y" if it asks to restore
4. If it doesn't asks to restore, press the option that says Restore diary
5. Follow on screen instructions
6. Run diary.py and write something short and blank to make sure your restored diary works properly

This backing up and restoring can be used to clone diary in multiple device and hence use it from there. Don't forget to pull and push from one device first before updating from another device to avoid conflicting diaries

## Conclusion & Warnings
1. Do not leak your public or private keys, they are supposed to be kept private
2. Use a strong passphrase/password for gpg key, if your private key is leaked then the password will be the only thing protecting you from unknown hands accessing your diary
3. Store passphrase/password in a safe place as it cannot be recovered
4. Don't switch keys, it will make diary undecryptable by func.py
5. Cross device is supported and should work fine as long as you pull and push properly from one device before updating diary on other
6. Your gitlab password is stored in pass.gpg in encrypted format, so don't worry about it.
7. Learning more about git and linux commandline will help a lot
