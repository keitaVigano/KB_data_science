FROM eclipse/rdf4j-workbench:latest

WORKDIR /app

COPY bootstrap.sh ./bootstrap.sh
COPY data/DSkg.ttl /data/DSkg.ttl
COPY repo-config.ttl ./repo-config.ttl

CMD ["bash", "./bootstrap.sh"]
EXPOSE 8080
