FROM python:3.12-slim

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV IS_DEVELOPMENT False


WORKDIR /app


COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn


COPY . /app/


WORKDIR /app/current
EXPOSE 80

# run migrations, create a superuser if not exists, and start gunicorn
CMD ["bash", "-c", "python manage.py migrate && \
    echo \"from django.contrib.auth.models import User; \
    User.objects.filter(username='kutay').exists() or \
    User.objects.create_superuser('kutay', 'test@test.com', '1232')\" | python manage.py shell && \
    gunicorn --bind 0.0.0.0:80 rental_project.wsgi:application"]
