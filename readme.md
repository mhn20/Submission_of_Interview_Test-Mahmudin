## First Instalation
```
python -m venv venv
```
### Linux
```
source venv/bin/activate
```
### Windows
```
source venv/Script/activate
```
### Proccess Instalation
```
pip install -r requirements.txt
```
```
cd dash
```
```
python manage.py makemigrations
```
```
python manage.py migrate
```
```
python manage.py seed_movies
```
```
python manage.py createsuperuser
```
```
python manage.py collectstatic
```
```
python manage.py runserver
```
### Admin
```
http://localhost:8000/admin
```
#### Username
```
mahmud
```
#### Password
```
1Sampai9
```
### List Movie
```
http://localhost:8000/
```