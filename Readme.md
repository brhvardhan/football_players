Steps to run this:
1. Add the Folder path to PYTHONPATH environment variable and restart your shell. (If you are using VSCODE, please close all windows and restart VSCODE to get new environment variables.)
2. Create a virtual env (python -m venv venv)
3. Activate the virtual env. (./venv/Scripts/activate - for windows, source ./venv/bin/activate - for linux)
4. pip install requirements.txt
5. uvicorn main:app

Enjoy the app at localhost:8000/docs. (You can change the port at step - 5)


Note:
1. Each Member can be part of only 1 team
2. If team is deleted, all the members present in member table will be deleted.
