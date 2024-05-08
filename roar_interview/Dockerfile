FROM ubuntu/apache2:2.4-20.04_beta
# prevent python form writing .pyc files.
ENV PYTHONDONTWRITEBYTECODE 1 
# ensure python output is directly to the terminal without buffering
ENV PYTHONUNBUFFERED 1

# Install python3 and Apache2-mod-WSGI
RUN apt update && apt upgrade -y
RUN apt install python3 python3-pip -y
RUN apt install libapache2-mod-wsgi-py3 -y
# for nano to works
RUN apt-get install nano 
RUN export TERM=xterm
# Install python3.8-venv for creating virtual environment
RUN apt install python3.8-venv -y

# Create a python virtual environment directory for Apache2 WSGI to work
RUN python3 -m venv /opt/venv
# Enable venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /var/www/roar_interview

COPY requirements.txt /var/www/roar_interview/requirements.txt
COPY 000-default.conf /etc/apache2/sites-available/000-default.conf

RUN pip3 install -r requirements.txt

COPY . /var/www/roar_interview/

# Enable django to perform write to sqlite3 database.
RUN chown -R www-data:www-data /var/www/roar_interview