import yaml # pip install pyyaml

def get_flag_from(filename: str) -> str:
    with open(filename, "r") as f:
        challenge_config = yaml.safe_load(f)
        assert 'flags' in challenge_config
        assert len(challenge_config['flags']) == 1
        return challenge_config['flags'][0]

