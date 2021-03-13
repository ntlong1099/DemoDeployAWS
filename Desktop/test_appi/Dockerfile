FROM python:3.6

RUN pip3 install pipenv

# WORKDIR ????

# COPY requirements.txt ./

# RUN python3 -m pip install --user --no-cache-dir -r requirements.txt

COPY . .

RUN pipenv install --system --deploy --ignore-pipfile

CMD ["python", "app.py"]