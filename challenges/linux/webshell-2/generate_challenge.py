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
	os.makedirs("/root/.nothing_here")
	write_seed_data_to_file("/root/.nothing_here/.hidden_flag.txt")

if __name__ == "__main__":
	main()

