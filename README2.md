#### windows
python -m venv .venv  
.venv\Scripts\activate  

#### linux
python3 -m venv .venv  
source .venv/bin/activate  

### package
pip list  
pip freeze > requirements.txt  
pip install -r requirements.txt  

### django
cd mysite  
python manage.py runserver  

### migration
python manage.py makemigrations workplace  
python manage.py migrate  

### 디스코드 봇 실행
nohup python main.py &  
