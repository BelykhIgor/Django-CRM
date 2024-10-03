#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py flush --no-input
python manage.py migrate --noinput
python manage.py collectstatic --no-input --clear
echo "from django.contrib.auth import get_user_model; User = get_user_model();
User.objects.create_superuser('admin', 'admin@example.com', '123456')" | python manage.py shell
python manage.py create_groups
exec "$@"
