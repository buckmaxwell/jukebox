FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt .

RUN mkdir -m=0700 ~/.ssh
RUN touch ~/.ssh/known_hosts
RUN ssh-keyscan github.com >> ~/.ssh/known_hosts

RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

CMD [ "python", "worker.py" ]