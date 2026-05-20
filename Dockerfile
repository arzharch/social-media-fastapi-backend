FROM python:3.10.0
#works layerwise and caches the results, so when its changed only that will be run - cache will carry on

WORKDIR /usr/src/app 
#optional - this is where it will be copied to

COPY requirements.txt ./  
#means current directory

RUN pip install --no-cache-dir -r requirements.txt 
#runs the command, no cache dir reduces space take by the libraries

COPY . . 
#copies everything from current directory to the current directory in the container

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001" ] 
#for every space make it a new command in the quotes

