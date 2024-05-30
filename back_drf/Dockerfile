FROM python:3.12.3-alpine3.19

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /back_drf

COPY . /back_drf/

COPY requirements.txt /back_drf/

RUN apk add --no-cache mariadb-dev build-base \
    cairo \
    cairo-dev \
    pango \
    pango-dev \
    gdk-pixbuf \
    gdk-pixbuf-dev \
    libffi-dev \
    shared-mime-info \
    gobject-introspection-dev \
    fontconfig \
    ttf-dejavu

RUN pip install -r requirements.txt


CMD ["sh", "-c", "cd crm_api/ && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
