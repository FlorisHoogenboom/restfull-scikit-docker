ARG PYTHON_VERSION=3.6
FROM tiangolo/uwsgi-nginx-flask:python${PYTHON_VERSION}
MAINTAINER Floris Hoogenboom <floris.hoogenboom@futurefacts.nl>

# Install python dependencies
COPY ./setup.py /build/setup.py
RUN pip install /build

# Make application directories
RUN mkdir /app/objects
RUN mkdir /app/modules

# Remove old entrypoint from the original container
RUN rm /app/main.py

# Copy the restfull wrapper
COPY ./scikit_rest_wrapper /app/main

# Setup error logging
RUN echo "logto = /var/log/uwsgi/%n.log" >> /app/uwsgi.ini
RUN mkdir /var/log/uwsgi

EXPOSE 80
EXPOSE 443