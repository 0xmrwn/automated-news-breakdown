FROM python:3.11

# initial setup
RUN mkdir auto_summary
COPY requirements.txt auto_summary

# installing dependencies
RUN pip install --no-cache -r auto_summary/requirements.txt
SHELL ["/bin/bash", "--login" , "-c"]

# setting work directory
COPY . auto_summary
WORKDIR /auto_summary


# launch gunicorn server
EXPOSE 8888
CMD ["gunicorn", "src.flask_server:app", "--workers=1", "--threads=4", "--bind=:8080", "--timeout=0"]
