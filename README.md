# ProjectFocus


## Build instructions

1. Install python 3.9

2. Install dependencies with `python -m pip install -r requirements.txt`

3. Install node.js

4. In the root of the repo, run `git submodule update --init`

5. npm should install axios using package-lock. if not, use npm install axios --save

6. Run the script `/build/install_js_modules.sh` in /root folder. This will move the js code into magic mirror

7. Run npm install in ./submodule/MagicMirror


## How to run

1. First run the server with `python main.py`

2. Run the command `npm run start` in ./submodule/MagicMirror ON LINUX (subsystem)


## Coding practices

* Lines of code should not exceed 80 characters