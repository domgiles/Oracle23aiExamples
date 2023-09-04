# Oracle23c Examples

Ultimately this demo will come in the form of a docker container or Virtual Box intall.

If you are fimiliar with Python then the next few steps should help... Otherwise this install might be a little challenging

First clone this repository

```git clone https://github.com/domgiles/Oracle23cExamples.git```

You'll need a later Python install. Ideally 3.10 or 3.11. Then just follow these steps

```bash
# install Python virtualenv
pip install --upgrade pip
python3 -m venv 23cdemos
source 23cdemos/bin/activate
pip install -r requirements.txt
```

Then start jupyter-lab i.e.

```jupyter-lab --ip 0.0.0.0```

**NOTE :** This will allow anyone to access your jupyter lab (although they'd still need the token). You may want to be a little more controlled.

* You should have installed Oracle ORDS and configured that against your target database.
* Use the ```Setup``` notebook to create an Oracle user to run the scripts.

## Using the dockerfile
We're using docker in an unconventional way mainly to simplify the install for users unfamiliar with Python and jupyter-lab. The docker file will install all the needed components and configure it for a target database. This isn't ideal since every image is unique.
We will fix this at a later stage. Providing a single image that users can specify values at the command line.
At this point in time you just need to edit the docker file and change these lines to reflect your target database
```bash
# Change these line to point at your database
ENV DBA_USERNAME="SYS"
ENV DBA_PASSWORD="welcome1"
ENV USER_NAME="ora23c"
ENV PASSWORD="ora23c"
ENV HOST="192.168.86.235"
ENV SERVICE="soe"
# ^^^^^^^^^^^^^^^^^^^^^
```
And then run the command
```bash
docker build -t "examples23c-jup:latest" .
```
Currently, this will take a few minutes to run as we build the python oracledb driver. This is to avoid a bug in the current production build. This will chnage shortly and the build will be much faster.

Then run the command
```bash
docker run -p 8888:8888 -p 8080:8080 examples23c-jup:latest
```
You can change the mapping of the ports (-p) to anything you feel fits your requirements.

You should then be able to connect to the port in the browser on your localmachine (or where ever you are running docker/podman). 


## Things to do

* Add images and additional text to examples.
~~* Add a helper notebook (i.e. create user) with instructions on how to run the notebook.~~
* Add additional Oracle 23c examples
* Create a dockerfile to build an image that can be trivially shared with people

