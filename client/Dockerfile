FROM python:3.9

ENV POETRY_VERSION=1.8.2

RUN apt-get update && apt-get upgrade -y
RUN pip install --upgrade pip "poetry==$POETRY_VERSION"

COPY ./pyproject.toml /pyproject.toml
COPY ./poetry.lock /poetry.lock

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

WORKDIR /src
COPY . /src

RUN adduser --disabled-password --gecos '' python
RUN adduser python sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER python

CMD ["python3", "main.py"]
