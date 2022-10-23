FROM docker.io/library/neurodebian:latest
### INSTALL BASE SOFTWARE ##################################################
WORKDIR /tmp
# Install Python tools and their system dependencies
RUN apt-get update && \
apt-get install -y git && \
apt-get install -y python3-pip && \
rm -rf /var/lib/apt/lists/* 
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt && \
pip install git+https://github.com/TomGeorge1234/ratinabox.git
# Add local files into image
# ADD ADD . /app/

### ADD MY OWN SCRIPTS #####################################################
# Add workflow scripts
WORKDIR /app
COPY . /app/

# Configure workflow
#ENV DATA_SIZE 42
# Uncomment the following lines to execute preprocessing tasks during build
#RUN python analysis.py
CMD python3 model_launching.py 
 
#CMD docker cp CONTAINER:/app/exit.txt .

#CMD docker cp CONTAINER:/app/Results/session_file.csv ./Results
### WORKFLOW CONTAINER FEATURE #############################################
# CMD from base image used for development, uncomment the following lines to
# have a "run workflow only" image
# CMD["./myscript.sh"]
### Usage instructions #####################################################
# Build the images with
# > docker build --tag datascidockerfiles:1.0.0.
# Run the image interactively, open it on http://localhost/
# > docker run -it -p 80:8787 -e PASSWORD = ten --volume $(pwd)/input:/input datascidockerfiles:1.0.0
# Run the workflow:
# > docker run -it --name gwf datascidockerfiles:1.0.0 /work/myscript.sh
# Extract the data:
# > docker cp gwf:/output/ ./outputData
# Extract the figures:
# > docker cp gwf:/work/figures/ ./figures
 
