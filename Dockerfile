FROM python:3.9.1
RUN apt-get update
WORKDIR /urban_growth_model
COPY ./app /urban_growth_model/app
COPY main.py /urban_growth_model
COPY requirements.txt /urban_growth_model
RUN pip install -r requirements.txt

CMD ["python", "main.py"]
