# google-password-tester-bot
A bot that test a list of given passwords in the google account login page until finds the correct one.

Operation
---------

When start the bot, it will do the following:
1. Opens the **google chrome** browser
2. Goes to **accounts.google.com**
3. Inserts the **account gmail** and press **Next** button

Then will follow the next steps in a loop:
1. Inserts a password, character per character with a random interval between them
2. Press **Next** button
3. Wait a few seconds to load the page
4. Checks if the browser was **Logged In** and it's in **myaccount.google.com** page, if successful finish the bot saving the password in a file
5. If **step 4** was not succesful, checks if the password input has and **invalid password** label
6. If the page displays a captcha, redirects to **www.google.com** as a standby page, otherwise jumps to **step 11**
7. Wait 8 minutes
8. Goes to **accounts.google.com**, inserts the **account gmail** and press **Next** button
9. Repeats **step 1, 2 and 3**
10. Repeats **step 4, 5 and 6** and wait 1 minute for each time these steps were not successful
11. Changes the `0` to `1` in the passwords file

Installation
------------

First you need to clone the repository or [download it](https://github.com/MarcosTypeAP/google-password-tester-bot/archive/refs/heads/main.zip), and then install python's dependencies.

```bash
#!/bin/bash

git clone https://github.com/MarcosTypeAP/google-password-tester-bot.git
cd google-password-tester-bot/
python3 -m venv .venv         # If you don't want to install
source .venv/bin/activate     # the dependencies globally
python3 -m pip install -r requirements.txt
```

You need the last version of `google chrome` installed.
Also `notify-send` if you want to be notified if the bot finishes in case of error.

Usage
-----

First you need a file containing a list of passwords. It should look like this:

```plaintext
password1 0
password2 0
password3 0
```

The `0` indicates that the password has not been tested yet, otherwise it will be `1`.

#### Generate a file with passwords

If when you change your password, you only change certain parts, you can generate a file with a list of passwords by combining groups of those  parts you remember.

###### Example

If the file contains groups of parts separateds by empty lines like this:

```plaintext
foo
bar

Python
Password

1
2
3
```

The output file will contain:

```plaintext
fooPython1 0
fooPython2 0
fooPython3 0
fooPassword1 0
fooPassword2 0
fooPassword3 0
barPython1 0
barPython2 0
barPython3 0
barPassword1 0
barPassword2 0
barPassword3 0
```

To generate the file you need to run `python3 gen-password-combinations.py <part-grpups-file>`. The output will be `passwords.txt`.

If you previously generated other files, you can subtract passwords by adding the files at the end of the command.

###### Get untested passwords

In case of errors, you can get the passwords that were not saved in the log file, getting an output file with the untested passwords.
To do this, run `python3 get-untested-passwords.py <logs file> <password files>`

#### Execute the bot

To start the bot you need to run `./start` and the bot will open the chrome browser and start running. 

In case of error the script will notify you that the bot finished (only if you have `notify-send` installed) and then will restart the bot.

When the bot finds the correct password, it will be saved in a new file named `result.txt`. 
