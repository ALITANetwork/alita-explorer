FROM alita-base:latest


COPY . .

#USER root
CMD ["/app/docker-entrypoint.sh"]
