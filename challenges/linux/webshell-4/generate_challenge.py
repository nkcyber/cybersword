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

	return """
package main

import (
	"bufio"
	"errors"
	"fmt"
	"math/rand"
	"os"
	"strconv"
	"strings"
	"time"
)

func readInput() (int, error) {
	reader := bufio.NewReader(os.Stdin)
	text, err := reader.ReadString('\n')
	if err != nil {
		return 0, err
	}
	text = strings.TrimSpace(text)
	i, err := strconv.Atoi(text)
	if err != nil {
		return 0, err
	}
	return i, nil
}

func generateChallenge() (string, int) {
	const limit = 100
	a := rand.Intn(limit)
	b := rand.Intn(limit)
	answer := a + b
	return fmt.Sprintf("%d + %d = ", a, b), answer
}

func startChallenges() chan error {
	out := make(chan error)
	const numChallenges = 20

	go func() {
		for i := 0; i < numChallenges; i++ {
			challenge, answer := generateChallenge()
			fmt.Print(challenge)
			i, err := readInput()
			if err != nil {
				out <- err
				return
			} else if i != answer {
				out <- errors.New("incorrect answer")
				return
			}
		}
		out <- nil
	}()

	return out
}

func printFlag() {
	fmt.Println(" """ + flag + """ ")
}

func main() {
	finished := startChallenges()

	select {
	case <-time.After(1 * time.Second):
		fmt.Println("\n\nToo late!!")
		return
	case err := <-finished:
		if err == nil {
			printFlag()
		} else {
			fmt.Print("error: ")
			fmt.Println(err)
		}
		return
	}
}
	"""

def write_seed_data_to_file(filename:  str):
	with open(filename, "w") as f:
		f.write(get_seed_data())

def main():
  write_seed_data_to_file("/root/math_challenge.go")
  # TODO: make exectuable
  # Pickup line: you put the cute in executable
  # "Are you /dev/sda1 because I want to mount you?"

if __name__ == "__main__":
	main()

