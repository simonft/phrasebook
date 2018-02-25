# phrasebook
### This is still very much in Alpha. Please don't use it to generate important passphrases.

![Screenshot](screenshot.png)

Phrasebook is a program for generating secure passphrases from a word list. It's based off the idea behind the [EFF's diceware](https://www.eff.org/dice) and [XKCD #936](https://www.xkcd.com/936/). Unlike similar programs, it provides a graphical user interface (it does not need to be run from the command line) and allows for importing and using a custom wordlist of the user's choosing. 

A goal of the project is being very simile and easy to use for non-technical users.

In the future it will also have the ability to auto select a reasonable word list based on the user's system locale. 

## Developing on OSX/Linux
Install using the following commands. You must already have python, pip, and virtualenv installed and available on your path.
```
git clone https://github.com/simonft/phrasebook.git
cd phrasebook
virtualenv venv/
source venv/bin/activate
pip install -e .
```
You can now run phrasebook with the command `phrasebook`  while in the virtual environment.


## Wordlists
* [en.txt](phrasebook/wordlists/en.txt) was created by [SecureDrop](https://github.com/freedomofpress/securedrop/blob/develop/securedrop/wordlists/en.txt) and is licensed AGPLv3. It's based of a CC-BY list created be the [EFF](https://eff.org/wordlist).
