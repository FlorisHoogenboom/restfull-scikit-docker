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

HEALTHCHECK CMD curl --fail http://localhost:80/json/status || exit 1

EXPOSE 80
EXPOSE 443