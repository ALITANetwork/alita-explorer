FROM burst8301:latest


COPY . .


CMD ["/app/docker-entrypoint.sh"]
