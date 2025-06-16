FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
RUN pip install gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000"]