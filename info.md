
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
python manage.py runserver


pip install Django==5.2 \
    django-admin-interface==0.30.0 \
    django-colorfield==0.13.0 \
    pillow==11.2.1 \
    python-slugify==8.0.4 \
    sqlparse==0.5.3 \
    text-unidecode==1.3 \
    tzdata==2025.2 \
    asgiref==3.8.1
pip install django-axes geoip2 django-user-agents django-admin-tools django-rosetta

gunicorn --workers 3 --bind 127.0.0.1:8000 marmorten_production.wsgi:application

sudo apt-get install gettext