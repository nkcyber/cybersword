import os
import subprocess
import random
import string
import pwd
import grp
import yaml # pip install pyyaml

# --- Configuration ---
NUM_USERS = 100
REAL_FLAG_FILE = "/root/SETUP_FILES/challenge.yml" # Path to the challenge config file
PLAUSIBLE_FLAG_PREFIX = "cybersword{"
PLAUSIBLE_FLAG_SUFFIX = "}"
USERNAME_PREFIX = "challuser"

# --- Flag Generation (adapted from provided script) ---

def get_flag_from(filename: str) -> str:
    """Reads the flag from a YAML configuration file."""
    try:
        with open(filename, "r") as f:
            challenge_config = yaml.safe_load(f)
            if not challenge_config or 'flags' not in challenge_config or not challenge_config['flags']:
                print(f"Error: 'flags' key missing or empty in {filename}. Using default flag.")
                return "cybersword{default_real_flag_check_config}"
            return challenge_config['flags'][0]
    except FileNotFoundError:
        print(f"Error: Configuration file {filename} not found. Using default flag.")
        return "cybersword{default_real_flag_file_not_found}"
    except Exception as e:
        print(f"Error reading config file {filename}: {e}. Using default flag.")
        return "cybersword{default_real_flag_read_error}"


def generate_random_lowercase_string(length):
    """Generates a random lowercase string for plausible flags."""
    prefix_len = len(PLAUSIBLE_FLAG_PREFIX) + len(PLAUSIBLE_FLAG_SUFFIX)
    if length <= prefix_len:
        # Handle cases where the real flag is too short
        length = prefix_len + 10 # Ensure some random chars
    data_len = length - prefix_len
    letters = string.ascii_lowercase + string.digits # Add digits for variety
    data = ''.join(random.choice(letters) for _ in range(data_len))
    return f"{PLAUSIBLE_FLAG_PREFIX}{data}{PLAUSIBLE_FLAG_SUFFIX}"

# --- Helper Functions ---

def run_command(command):
    """Runs a shell command and prints output/errors."""
    try:
        print(f"Executing: {' '.join(command)}")
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        if result.stdout:
            print(f"Output: {result.stdout.strip()}")
        if result.stderr:
            print(f"Error output: {result.stderr.strip()}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing {' '.join(command)}: {e}")
        print(f"Stderr: {e.stderr}")
        print(f"Stdout: {e.stdout}")
    except Exception as e:
         print(f"Unexpected error executing {' '.join(command)}: {e}")

def create_user(username, password=None):
    """Creates a system user."""
    try:
        # Create user and their primary group with the same name, create home directory
        run_command(["useradd", "-m", "-s", "/bin/bash", username])
        if password:
            # Set password
            proc = subprocess.Popen(['chpasswd'], stdin=subprocess.PIPE, text=True)
            proc.communicate(f"{username}:{password}")
            print(f"Password set for user {username}.")
        else:
            # Ensure no password / lock if necessary (useradd might lock by default)
            # passwd -d deletes the password, making it empty (allows login without pass)
            run_command(["passwd", "-d", username])
            print(f"Password removed for user {username}.")
        return True
    except Exception as e:
        print(f"Failed to create user {username}: {e}")
        return False

def set_ownership(path, username):
    """Sets ownership of a file/directory to the specified user."""
    try:
        uid = pwd.getpwnam(username).pw_uid
        gid = grp.getgrnam(username).gr_gid # Assumes group name matches username
        os.chown(path, uid, gid)
        print(f"Set ownership of {path} to {username}:{username}")
    except KeyError:
        print(f"Error: User or group '{username}' not found for setting ownership of {path}.")
    except OSError as e:
        print(f"Error setting ownership for {path}: {e}")


# --- Main Logic ---

def main():
    if os.geteuid() != 0:
        print("This script must be run as root to create users.")
        return

    real_flag = get_flag_from(REAL_FLAG_FILE)
    get_plausible_flag = lambda: generate_random_lowercase_string(len(real_flag))

    # Select which user will have no password
    no_password_user_index = random.randint(0, NUM_USERS - 1)
    print(f"User index {no_password_user_index} will be created without a password.")

    created_count = 0
    for i in range(NUM_USERS):
        username = f"{USERNAME_PREFIX}{i:03d}" # e.g., challuser000, challuser001
        home_dir = f"/home/{username}"
        flag_file_path = os.path.join(home_dir, "flag.txt")

        print(f"\n--- Processing User {i+1}/{NUM_USERS}: {username} ---")

        is_no_password_user = (i == no_password_user_index)
        password = None if is_no_password_user else ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(12)) # Generate random password for others

        if create_user(username, password):
            created_count += 1
            # Determine flag content
            flag_content = real_flag if is_no_password_user else get_plausible_flag()

            # Create flag file and set permissions
            try:
                # Ensure home directory exists (useradd -m should create it, but double-check)
                if not os.path.exists(home_dir):
                     print(f"Warning: Home directory {home_dir} not found, attempting creation.")
                     os.makedirs(home_dir)
                     set_ownership(home_dir, username) # Set ownership if we created it

                with open(flag_file_path, "w") as f:
                    f.write(flag_content + '\n') # Add newline
                print(f"Created {flag_file_path}")

                # Set ownership and permissions for flag.txt
                set_ownership(flag_file_path, username)
                os.chmod(flag_file_path, 0o640) # Read/Write for user, Read for group, None for others
                print(f"Set permissions for {flag_file_path}")

                # Set home directory permissions (adjust as needed)
                # 750: rwx for user, rx for group, --- for others
                os.chmod(home_dir, 0o750)
                print(f"Set permissions for {home_dir}")


            except IOError as e:
                print(f"Error writing flag file {flag_file_path}: {e}")
            except OSError as e:
                 print(f"Error setting permissions/ownership for {username}'s files: {e}")
        else:
             print(f"Skipping flag creation for {username} due to user creation failure.")

    print(f"\n--- Challenge Generation Complete ---")

if __name__ == "__main__":
    main()
