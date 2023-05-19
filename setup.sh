#!/bin/bash

./wait-for-it.sh -t 60 db:5432 -- echo "Database ready. Running migrate."

python manage.py migrate
echo "Finished Migrate"

if [ -z "$(python manage.py shell -c 'from django.contrib.auth.models import User; print(User.objects.filter(username="admin").exists())')" ]; then
    echo "User already exists"
else
    echo "from django.contrib.auth.models import User; User.objects.create_superuser(username='admin', password='admin', email='admin@example.com')" | python manage.py shell
    echo "User created success!"
fi

python manage.py runserver 0.0.0.0:8000