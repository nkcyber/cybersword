# This creates the seed data based on the flags
# configured in ropchain-1's `challenge.yml`s
import yaml # pip install pyyaml

def get_flag_from(filename: str) -> str:
	with open(filename, "r") as f:
		challenge_config = yaml.safe_load(f)
		assert 'flags' in challenge_config
		assert len(challenge_config['flags']) == 1
		return challenge_config['flags'][0]

def write_seed_data_to_file(filename:  str):
	with open(filename, "w") as f:
		f.write(get_flag_from("/app/SETUP_FILES/challenge.yml"))

def main():
	write_seed_data_to_file("/app/flag.txt")

if __name__ == "__main__":
	main()

