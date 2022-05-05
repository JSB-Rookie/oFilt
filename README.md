# oCal

### Setup

Open Terminal and put in the following commands:

	git clone https://github.com/JSB-Rookie/oFilt.git
	cd oFilt
	python3 -m venv venv
	. venv/bin/activate
	pip install -r requirements.txt
	python oFilt.py


### Updating

When you have new code that you want to share, you need to do the following.

On the developer side:

	git add <modified file>

e.g. to add changes to main branch:

	git add oFilt.py

	git status

	git commit -m "describe changes here"

	git push origin main

On the user side:

Open a Terminal, navigate to the code directory (wherever ocal is cloned), then run:

	git pull

At that point the user can run the updated code by (re)starting oFilt.py

