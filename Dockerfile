FROM python:3.11-alpine3.17

#determine if python will save bytecode (.pyc) files.
ENV PYTHONDONTWRITEBYTECODE 1

#determine if python will run in unbuffered mode
ENV PYTHONUNBUFFERED 1

#Copy the hawkeapp and directory into the docker container
COPY ./hawke_app /hawkeapp
COPY ./scripts /scripts

#Set the working directory
WORKDIR /hawkeapp

#export the port
EXPOSE 8000

#run the script to install the dependencies
RUN python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r /hawkeapp/requirements && \
    adduser --disabled-password --no-create-home huser && \
    mkdir -p /data/web/static && \
    mkdir -p /data/web/media && \
    chown -R huser:huser /venv && \
    chown -R huser:huser /data/web/static && \
    chown -R huser:huser /data/web/media && \
    chmod -R 755 /data/web/static && \
    chmod -R 755 /data/web/media && \
    chmod -R +x /scripts

#add script and venv/bin to the path
ENV PATH="/scripts:/venv/bin:$PATH"

#switch to the duser
USER huser

#run the server
CMD ["commands.sh"]