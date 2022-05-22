FROM python:3.9-alpine

# set the working directory in the container
WORKDIR /qb_tagger

# copy the dependencies file to the working directory
COPY requirements.txt .
COPY tagger.py .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
ADD src /qb_tagger/src

# command to run on container start
CMD [ "python", "tagger.py" ]