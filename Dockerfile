FROM python:3.8
ENV PYTHONUNBUFFERED 1
ENV ENV_ROLE docker
RUN mkdir /code
WORKDIR /code
COPY Pipfile /code/
COPY Pipfile.lock /code/
RUN apt-get --yes --force-yes update && apt-get --yes --force-yes install binutils libproj-dev gdal-bin && pip install pipenv
RUN pipenv install --dev
COPY . /code/
