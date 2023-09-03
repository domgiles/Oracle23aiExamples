FROM python:3.11

USER root

RUN apt-get update && apt-get install -y gcc python3-dev git

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
COPY *.ipynb .
COPY *.py .

ENV DBA_USERNAME="sys"
ENV DBA_PASSWORD="welcome1"
ENV CONNECT_STRING="//192.168.86.235/soe"

CMD [ "jupyter-lab", "--allow-root", "--ip", "0.0.0.0", "--port", "8888", "--no-browser" ]