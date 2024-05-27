FROM python:3.11

ARG workdir=/app/

WORKDIR $workdir

RUN useradd -ms /bin/bash pyuser
RUN chown -R pyuser:pyuser $workdir
RUN chmod 755 $workdir
USER pyuser

# add scripts
ENV PATH=$PATH:/home/pyuser/.local/bin
# stop pip versions check
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
# don't make .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# don't buffer the output
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN pip install --user pipenv

# Tell pipenv to create venv in the current directory
ADD Pipfile.lock Pipfile $workdir
ENV PIPENV_VENV_IN_PROJECT=1
RUN pipenv sync

COPY . $workdir

ARG DB_HOST=postgres

CMD ["pipenv","run","migrate", "&&" ,"pipenv", "run", "server", "0.0.0.0:8000"]
