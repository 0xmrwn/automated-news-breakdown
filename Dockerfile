FROM python:3.11

# initial setup
RUN mkdir auto_summary
COPY requirements.txt auto_summary

# installing dependencies
RUN pip install --no-cache -r auto_summary/requirements.txt
SHELL ["/bin/bash", "--login" , "-c"]

# setting work directory
COPY . robin
WORKDIR /robin


# launch gunicorn server
CMD ["gunicorn", "src.auto_summary:app", "--workers=1", "--threads=4", "--bind=:8080", "--timeout=0"]
