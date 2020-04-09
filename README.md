# bellettrie_systeem

This project has as goal to replace the current website of Bellettrie with a modernised one.

## Setup of development environment
1. Install from sources
2. Install recent python version (3.7 or higher)
3. run pip install -r requirements.txt in the root of the project. You may want to look into virtual environments.
4. Either ask for a dev db, or run python manage.py migrate.
5. Run python manage.py runserver.

## Linting
The CI environment uses Flake8 for linting. The following command may work within pycharm, if you have flake8 installed (install the requirements again if you don't, it's one of the requirements now).
```flake8 . --ignore F401,E501,W503 --count --show-source --statistics --max-line-length=127 --exclude venv```