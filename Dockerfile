FROM python:3.10
EXPOSE 5000
WORKDIR /app
COPY requirement.txt .
RUN python -m pip install -r requirements.txt
COPY . .
CMD ["flask", "run" , "--host", "0.0.0.0"] 
#docker build -t rest-apis-flask-python .