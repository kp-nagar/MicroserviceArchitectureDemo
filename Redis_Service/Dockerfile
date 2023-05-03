# Only needed if we need to run cron logrotate or other services along with Redis
# Pull base image.
FROM ubuntu:20.04

# Install Redis.
ENV REDIS_VERSION 6.0.5
RUN apt-get update \
  && DEBIAN_FRONTEND=noninteractive \
  && apt-get install -y wget \
  && apt-get install -y gcc \
  && apt-get install -y make \
  && cd /tmp \
  && wget http://download.redis.io/releases/redis-6.0.5.tar.gz \
  && tar xvzf redis-6.0.5.tar.gz \
  && cd redis-6.0.5 \
  && make install \
  && rm -rf /var/lib/apt/lists/* \
  && rm -rf /tmp/*

# Mount volumes
COPY etc/redis/redis.conf /etc/redis/

# Install logrotate
RUN apt-get update && apt-get -y install logrotate

# Copy logrotate redis configuration
COPY etc/logrotate.d/redis-server.conf /etc/logrotate.d/

# Start cron as a service and then redis
CMD service cron start && redis-server /etc/redis/redis.conf