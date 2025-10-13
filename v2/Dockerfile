# Gebruik een officiële Python runtime als basisimage
FROM python:3.11-slim

# Stel de werkdirectory in de container in
WORKDIR /code

# Kopieer de dependencies en installeer ze
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Kopieer de applicatiecode naar de werkdirectory
COPY ./app /code/app

# Commando om de applicatie te starten wanneer de container draait
# --host 0.0.0.0 is essentieel om de app buiten de container bereikbaar te maken
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]