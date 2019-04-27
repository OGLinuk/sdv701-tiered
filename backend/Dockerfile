FROM python:3.5
ADD . /code
WORKDIR /code
EXPOSE 9124
RUN pip install -r requirements.txt
CMD ["python3", "run.py"]
