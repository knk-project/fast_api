FROM python:3.9-slim

# Install missing libs
RUN apt-get  update \
    && apt-get install -y  curl libpq-dev gcc python3-cffi git && \
    apt-get clean autoclean && \
    apt-get autoremove --purge -y && \
    rm -rf /var/lib/apt/lists/* && \
    rm -f /var/cache/apt/archives/*.deb && \
    find /var/lib/apt -type f | xargs rm -f && \
    find /var/cache -type f -exec rm -rf {} \; && \
    find /var/log -type f | while read f; do echo -ne '' > $f; done;

# Setting Home Directory for containers
WORKDIR /usr/app

# Installing python dependencies
RUN pip install --upgrade pip setuptools wheel && \
    pip install six poetry

#RUN pip install gunicorn[gevent]
COPY pyproject.toml /usr/app
COPY poetry.lock /usr/app

RUN poetry config virtualenvs.create false --local && \
    poetry install

# Copying src code to Container
COPY . /usr/app

# Exposing Ports
EXPOSE 8003