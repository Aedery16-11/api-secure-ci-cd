FROM python:3.11-slim


WORKDIR /app

COPY . .

RUN pip install -r requirements.txt
RUN pip install jaraco.context==6.1.0 && pip install wheel==0.46.2   
RUN useradd -u 8877 john
USER john

EXPOSE 5000

CMD ["python", "app.py"]
