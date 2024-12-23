FROM python:3.12
WORKDIR /app
RUN pip install requests, flask, psycopg2, bs4, re
COPY . .
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000
CMD ["flask", "run"]