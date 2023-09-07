FROM python:3.11

# Change these line to point at your database : I understand this isn't ideal. It will be parameterised at a later date
ENV DBA_USERNAME="SYS"
ENV DBA_PASSWORD="welcome1"
ENV HOST="192.168.86.235"
ENV SERVICE="soe"
# ^^^^^^^^^^^^^^^^^^^^^
#The following user will be created with password. You may change it if you want but I'd leave it as it is for now.
ENV USER_NAME="ora23c"
ENV PASSWORD="ora23c"
# ^^^^^^^^^^^^^^^^^^^^^

USER root

# Add need OS applications and libraries
RUN apt-get update && apt-get install -y git openjdk-17-jre-headless

RUN useradd --create-home $USER_NAME

# Open the ports we will need to open on the docker container
EXPOSE 8888
EXPOSE 8080

# Run as the user specified above
USER $USER_NAME
WORKDIR $USER_NAME

# Install the python virtual env and set it's path
RUN python -m venv pyenv
ENV PATH="/home/ora23c/.local/bin:/home/ora23c/pyenv/bin:$PATH"

# Copy the needed python library requirments and install them
COPY requirements.txt .
RUN pip install -r requirements.txt && rm requirements.txt

# Add directories to store file neatly in and copy the files
ADD images images
ADD scripts scripts
RUN mkdir html

COPY *.ipynb .
COPY *.py .

# Install ORDS
RUN wget https://download.oracle.com/otn_software/java/ords/ords-latest.zip
RUN unzip -d ords ords-latest.zip && cd ords/bin && echo $DBA_PASSWORD\\n$DBA_PASSWORD\\n$DBA_PASSWORD > passwd.txt
RUN cd ords/bin && ./ords install --admin-user $DBA_USERNAME --db-hostname $HOST --db-port 1521 --db-servicename $SERVICE --feature-sdw true --db-user ORDS_PUBLIC_USER --log-folder ../log --password-stdin < passwd.txt
RUN rm ords-latest.zip

# Run a python script to setup database (install ORDS if needed, create user and grant permisions)
RUN python scripts/installer.py -i -u $USER_NAME -p $PASSWORD -cs //$HOST/$SERVICE -du $DBA_USERNAME -dp $DBA_PASSWORD

# Run a script to start ords and jupyterlab
CMD ["scripts/startall.sh"]