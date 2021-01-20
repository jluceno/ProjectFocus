# ProjectFocus

## Build instructions

1. Install python 3.9
2. Install dependencies with `python -m pip install -r requirements.txt`
3. Install node.js
4. In the root of the repo, run `git submodule update --init`
5. Run the script in `/build/install_js_modules.sh`. This will move the js code into magic mirror
5. Run npm install in ./submodule/MagicMirror

## How to run

1. First run the server with `python main.py`
1. Run the command `npm run start` in ./submodule/MagicMirror

## Coding practices

* Lines of code should not exceed 80 characters