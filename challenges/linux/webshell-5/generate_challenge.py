# This creates the seed data based on the flags
# configured in the symlinked `challenge.yml`s
# 
# The line that is present in a.txt that is not in b.txt
# is the flag.
import yaml # pip install pyyaml
import base64
import random
import string


def get_flag_from(filename: str) -> str:
	with open(filename, "r") as f:
		challenge_config = yaml.safe_load(f)
		assert 'flags' in challenge_config
		assert len(challenge_config['flags']) == 1
		return challenge_config['flags'][0]


def generate_random_lowercase_string(length):
		assert length >= len("cybersword{}") + 1
		length -= len("cybersword{}") # amount of data to generate
		letters = string.ascii_lowercase
		data =  ''.join(random.choice(letters) for i in range(length))
		return "cybersword{%s}" % data

NUM_LINES = 10_000

def main():
	flag = get_flag_from("/root/SETUP_FILES/challenge.yml")
	get_plausible_flag = lambda: generate_random_lowercase_string(len(flag))

	with open("/root/a.txt", "w") as a, open("/root/b.txt", "w") as b:
		MIN_DEPTH_INTO_FILE = 500
		random_line = random.randrange(MIN_DEPTH_INTO_FILE, NUM_LINES-MIN_DEPTH_INTO_FILE)
		for i in range(NUM_LINES):
			if i == random_line:
				a.write(flag + '\n')
				b.write(get_plausible_flag() + '\n')
			else:
				plausible_flag = get_plausible_flag()
				a.write(plausible_flag + '\n')
				b.write(plausible_flag + '\n')

if __name__ == "__main__":
	main()

