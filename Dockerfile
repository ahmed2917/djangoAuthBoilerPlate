FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /djangoproject
WORKDIR /djangoproject
COPY requirements.txt /djangoproject/
RUN pip3 install -r requirements.txt
COPY . /djangoproject/
EXPOSE 8005
CMD ["python", "manage.py", "runserver", "0.0.0.0:8005"]