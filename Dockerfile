FROM nvidia/cuda
FROM python:3.6.8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /home/app/staticfiles/app/uploaded_videos/
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install cmake
RUN pip install opencv-python==4.2.0.32
RUN pip install -r requirements.txt
COPY . /app
RUN python manage.py collectstatic --noinput
RUN pip install gunicorn
RUN mkdir -p /app/uploaded_videos/app/uploaded_videos/
VOLUME /app/run/
ENTRYPOINT ["/app/bin/gunicorn_start.sh"]