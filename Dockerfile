FROM python:3.8

# adds requirements.txt before rest of repo for caching
COPY ./requirements.txt /app/
WORKDIR /app

# installs requirements
RUN pip install -r requirements.txt

# copies source files
COPY ./src ./src
COPY ./uwsgi.ini .

# creates spool directory and sets user 'www-data' as its owner
RUN mkdir -p worker_spool
RUN chown -R www-data worker_spool

# executes the application
CMD ["uwsgi", "--ini", "uwsgi.ini"]
