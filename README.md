# hesta
Open source project <strong>hesta</strong> - https://t.me/HestaOpenBot \
Hesta intended to check github repos. for commits present.
 

# Easy for self-deploy
<strong>Install it</strong>
```
git clone git@github.com:Kel0/hesta.git
```
<strong>Install dependencies</strong>
```
pip install invoke
inv install
```
<strong>Setup .env file</strong> \
Create .env file near settings.py file and setup it by .env.example

<strong>Migrate models</strong>
```
alembic revision --autogenerate -m "initial push"
alembic upgrade head
```
<strong>Run bot</strong>
```
python bot.py
```

# Commands
## /groups_list
Get list of groups which located in ```groups``` table

## /create_group
Create new group and save it in ```groups``` table

## /students
Get students list of group

## /create_students
Create new students for group

## /check_commits
Check for commits github repo.