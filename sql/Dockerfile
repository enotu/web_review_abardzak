FROM postgres:latest
ENV POSTGRES_USER=etis
ENV POSTGRES_PASSWORD=webreview
ENV POSTGRES_DB=etisdb
COPY ./init-scripts /docker-entrypoint-initdb.d/
EXPOSE 5432
CMD ["postgres"]
