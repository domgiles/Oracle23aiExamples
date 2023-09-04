FROM python:3.11

# Change these line to point at your database
ENV DBA_USERNAME="SYS"
ENV DBA_PASSWORD="welcome1"
ENV HOST="192.168.86.235"
ENV SERVICE="soe"
# ^^^^^^^^^^^^^^^^^^^^^

USER root

RUN apt-get update && apt-get install -y gcc python3-dev git openjdk-17-jre-headless

RUN useradd --create-home ora23c

EXPOSE 8888

USER ora23c
WORKDIR ora23c

RUN python -m venv pyenv
#ENV PATH="/ora23c/pyenv/bin:$PATH"

ENV PATH="/home/ora23c/.local/bin:/home/ora23c/pyenv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

ENV PYTHONPATH="/home/ora23c/.local/lib/python3.11/site-packages/"
RUN git clone --recurse-submodules https://github.com/oracle/python-oracledb.git && cd python-oracledb && python3 -m pip uninstall -y oracledb && git clean -fdx && python3 setup.py install --user

ADD images images
ADD scripts scripts

COPY *.ipynb .
COPY *.py .


RUN wget https://download.oracle.com/otn_software/java/ords/ords-latest.zip
RUN unzip -d ords ords-latest.zip && cd ords/bin && echo $DBA_PASSWORD\\n$DBA_PASSWORD\\n$DBA_PASSWORD > passwd.txt
RUN cd ords/bin && ./ords install --admin-user $DBA_USERNAME --db-hostname $HOST --db-port 1521 --db-servicename $SERVICE --db-user ORDS_PUBLIC_USER --log-folder ../log --password-stdin < passwd.txt
CMD ["scripts/startall.sh"]