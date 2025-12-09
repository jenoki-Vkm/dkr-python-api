FROM python:3.10-slim

WORKDIR /jenoki-workspace

COPY ./requirements.txt /jenoki-workspace
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]