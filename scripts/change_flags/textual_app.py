import re
import os
from pathlib import Path
from typing import Callable
from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Input, Button, Static, Label, Header
from textual.reactive import reactive
from textual.validation import Function
from change_flags import get_flag, set_flag, get_data


class FlagInput(Input):
	...

class InputApp(App):

	def min_len(self, length: int) -> Callable[str, bool]:
		def long_enough(text: str) -> bool:
			return len(text) > length
		return long_enough

	def extract_from_prefix(self, flag: str, name: str) -> str:
		"""Returns the inner part of 'prefix{data}' or returns the flag if it doesn't match that pattern."""
		match = re.search(r'(.*)\{(.*)\}', flag)
		if match:
			return match.group(2)
		self.notify("Flag '%s' in challenge '%s' does not match format prefix{flag}. It will be embedded in your prefix." % (flag, name),
			timeout=30)
		return flag

	def go_to_script_location(self) -> None:
		absolute_path = os.path.abspath(__file__)
		dir_name = os.path.dirname(absolute_path)
		os.chdir(dir_name)

	def get_files(self) -> list[str]:
		self.go_to_script_location()

		return Path('../../challenges').rglob('*challenge.yml')

	def compose(self) -> ComposeResult:
		yield Static("What is the prefix for your flags?")
		yield Input(
			placeholder="Enter your prefix (e.g. cybersword)",
			validators=[
				Function(self.min_len(3), "Prefix must be 3 characters."),
			],
			id="enter-prefix"
		)
		yield Static()
		yield Static("Edit all of the flags below. Any flags that are not edited will keep their original data.")
		for filepath in self.get_files():
			yield Static("") # Equivalent to <br> lmao
			flag = get_flag(filepath)
			data = get_data(filepath)
			name = data['name']
			yield Static(f"Flag for '{name}' ({data['category']})")
			flag_inner = self.extract_from_prefix(flag, name)
			input_ele = FlagInput(placeholder=flag_inner, type="text", id=name)
			input_ele.filepath = filepath
			yield input_ele
		yield Button("Submit", id="submit")

	@on(Button.Pressed, "#submit")
	def submit(self) -> None:
		prefix = self.query_one("#enter-prefix").value
		if len(prefix) < 3:
			self.notify("You must enter a prefix >= 3 characters long!")
			return # don't exit

		for flag_input in self.query("FlagInput"):
			def new_flag(substr):
				return "%s{%s}" % (prefix, substr)
			if len(flag_input.value) > 0:
				set_flag(flag_input.filepath, new_flag(flag_input.value))
			else:
				set_flag(flag_input.filepath, new_flag(flag_input.placeholder))

		self.exit()

if __name__ == "__main__":
	app = InputApp()
	app.run()
