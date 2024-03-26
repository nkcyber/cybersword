# This creates the seed data based on the flags
# configured in the symlinked `challenge.yml`s
import yaml # pip install pyyaml
import os

def get_flag_from(filename: str) -> str:
	with open(filename, "r") as f:
		challenge_config = yaml.safe_load(f)
		assert 'flags' in challenge_config
		assert len(challenge_config['flags']) == 1
		return challenge_config['flags'][0]

def get_seed_data() -> str:
	flag = get_flag_from("/root/SETUP_FILES/challenge.yml")

	return f"Ah! You found it again!\nThe flag is '{flag}'\n"

def write_seed_data_to_file(filename:  str):
	with open(filename, "w") as f:
		f.write(get_seed_data())

def main():
	write_seed_data_to_file("/root/flag.txt")

	with open("/root/README.txt", 'w') as f:
		f.write("""
Hello there!

Welcome to VIM.

> Vim is a powerful text editor that's popular with developers. It's known for being efficient and flexible, with many advanced features that can make editing text faster and easier. Vim is based on shortcuts which can make coding and writing faster and more efficient.

Vim is a modal text editor that uses different modes for editing, inserting text, and selecting text.
The modes are:
- Insert mode: Used to enter text
- Command mode: Used to move the cursor and perform commands on the text
- Visual mode: Used to append text to the current line, or highlight and edit text in bulk

> Vim is a free and open-source, screen-based text editor program. It is an improved clone of Bill Joy's vi. Vim's author, Bram Moolenaar, derived Vim from a port of the Stevie editor for Amiga and released a version to the public in 1991.
		""")

if __name__ == "__main__":
	main()

