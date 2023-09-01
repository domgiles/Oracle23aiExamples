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


Things to do

* Add images and additional text to examples.
~~* Add a helper notebook (i.e. create user) with instructions on how to run the notebook.~~
* Add additional Oracle 23c examples
* Create a dockerfile to build an image that can be trivially shared with people

