import sys
from ruamel.yaml import YAML

yaml = YAML()
yaml.explicit_start = False
yaml.indent(mapping=4,  sequence=6, offset=4)
yaml.preserve_quotes = True

# does this reload the same file a lot?
# yes
# do i care?
# no

def get_flag(filepath: str) -> str:
	with open(filepath) as fp:
		data = yaml.load(fp)
		assert len(data['flags']) == 1
		return data['flags'][0]

def get_data(filepath: str) -> str:
	with open(filepath) as fp:
		return yaml.load(fp)

def set_flag(filepath: str, flag: str):
	data = None
	with open(filepath, 'r') as fp:
		data = yaml.load(fp)

	data['flags'] = [flag]

	with open(filepath, 'w') as fp:
		print('writing to', filepath)
		yaml.dump(data, fp)

