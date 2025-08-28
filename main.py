#!/usr/bin/env python3
import os
import requests
import threading
import time

class TempCatcher:
	def _updateLocalData(self, path: str, data: str) -> None:
		with open(path, "w") as fp:
			fp.write(data)

	def _updateResources(self, key: str, value: str) -> None:
		# save data to same directory as this program
		r = self.session.get(value)
		path = self.executionPath + f"/{key}.txt"

		if not os.path.exists(path): # first run
			self._updateLocalData(path, r.text)
		else:
			with open(path, "r") as fp:
				if hash(fp.read()) != hash(r.text):
					self._updateLocalData(path, r.text)

		return r.text.splitlines()

	def _thread(self) -> None:
		try:
			while True:
				for key, value in self.resources.items():
					self.resources[key][1] = self._updateResources(key, value[0])

				time.sleep(self.update)
		except KeyboardInterrupt:
			exit()

	def validateEmail(self, email: str) -> str:
		try:
			assert email.count("@") == 1
			username, domain = email.split("@")

			assert domain.count(".") >= 1
			sld, tld = domain.split(".")

			assert tld in self.resources["tlds"][1]
		except:
			return [None, 1]

		username = username.replace(".", "") if "." in username else username
		username = username.split("+")[0] if "+" in username else username

		return [username, domain], 0

	def check(self, email: str) -> bool:
		while len(self.resources["emails"][1]) < 1 or len(self.resources["tlds"][1]) < 1:
			#wait for resources to be created / updated
			...

		formattedEmailParts, status = self.validateEmail(email)

		if status == 1:
			return 2

		username, domain = formattedEmailParts

		if domain == "gmail.com":
			if (username + "@" + "googlemail.com") in self.resources["emails"][1]:
				return 0

		elif domain == "googlemail.com":
			if (username + "@" + "gmail.com") in self.resources["emails"][1]:
				return 0

		return 0 if (username + "@" + domain) in self.resources["emails"][1] else 1

	def __del__(self):
		self.thread.join()

	def __init__(self, update: int = 3600):
		self.session = requests.Session()
		self.update = update

		self.executionPath = "/".join(__file__.split("/")[:-1])
		self.resources = {
			"tlds": ["https://tld-list.com/df/tld-list-basic.txt", []],
			"emails": ["https://raw.githubusercontent.com/TempCatcher/tempcatcher/refs/heads/main/emails.txt", []]
		}
		self.thread = threading.Thread(target = self._thread, daemon = True)
		self.thread.start()

if __name__ == "__main__":
	t = TempCatcher()

	status = t.check(input("Input email you would like to check: "))

	match status:
		case 0:
			print("Email was found in the tempcatcher data. (spam)")
		case 1:
			print("Email was not found in the tempcatcher data. (not spam)")
		case 2:
			print("Email was formatted incorrectly.")
		case 3:
			print("How did we get here?")
	del t
