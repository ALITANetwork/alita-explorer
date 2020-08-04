FROM burst8301:latest


COPY . .

#USER root
CMD ["/app/docker-entrypoint.sh"]
