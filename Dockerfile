# Using the lightest image.
FROM python:alpine

# Reading the build arguments.
# * BUID -> Build UID
# * BGID -> Build GID
ARG BUID=1000
ARG BGID=1000

# Updating the system.
RUN apk update && apk upgrade

# Installing required Python packages.
ADD --chown=$BUID:$BGID ./app/requirements.txt /tmp/requirements.txt
RUN pip install --upgrade -r /tmp/requirements.txt

# Copying the app's files to the container
ADD --chown=$BUID:$BGID ./app /app

# Running the application.
# * Thanks to jdpus for the "-u" flag, it fixes the output (https://stackoverflow.com/a/29745541/4135541)
WORKDIR /app
USER $BUID:$BGID
CMD ["python", "-u", "/app/app.py"]

# Used for debugging.
#CMD ["tail", "-f", "/dev/null"]
