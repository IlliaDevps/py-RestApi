# py-RestApi
python personal rest API

python3.10 -m venv .venv
C:\Users\i.duverkher\AppData\Local\Programs\Python\Python310\python.exe -m venv .venv
pip3.10.exe install -r requirements.txt
# docker ----------------
docker build -t flask-smorest-api
docker run -dp 5000:5000 flask-smorest-api

better to create a volume to not update the docde and re run the app
Linux docker run -dp 5005:5000 -w /app -v "$(pwd):/app" flask-smorest-api
Basically this is a maping within directories betwen your local file system and the container file system