# To run: docker run -v /path/to/wsgi.py:/var/www/pidgin/wsgi.py --name=pidgin -p 81:80 pidgin
# To check running container: docker exec -it pidgin /bin/bash


FROM quay.io/cdis/python:python3.9-buster-2.0.0


ENV appname=pidgin

RUN apt-get update \
    && apt-get install -y --no-install-recommends\
    curl bash git \
    libmcrypt4 libmhash2 mcrypt \
    && apt-get clean

COPY . /$appname
COPY ./deployment/uwsgi/uwsgi.ini /etc/uwsgi/uwsgi.ini
COPY ./deployment/uwsgi/wsgi.py /$appname/wsgi.py
WORKDIR /$appname

RUN python -m pip install --upgrade pip \
    && python -m pip install --upgrade setuptools \
    && pip install -r requirements.txt --src /usr/local/lib/python3.9/site-packages/

RUN mkdir -p /var/www/$appname \
    && mkdir -p /var/www/.cache/Python-Eggs/ \
    && mkdir /run/nginx/ \
    && ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log \
    && chown nginx -R /var/www/.cache/Python-Eggs/ \
    && chown nginx /var/www/$appname

EXPOSE 80

RUN COMMIT=`git rev-parse HEAD` && echo "COMMIT=\"${COMMIT}\"" >$appname/version_data.py \
    && VERSION=`git describe --always --tags` && echo "VERSION=\"${VERSION}\"" >>$appname/version_data.py \
    && python setup.py install

WORKDIR /var/www/$appname

CMD /dockerrun.sh
