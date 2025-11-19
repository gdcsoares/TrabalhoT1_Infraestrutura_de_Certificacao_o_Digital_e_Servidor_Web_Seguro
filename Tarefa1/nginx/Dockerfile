FROM nginx:stable-alpine
COPY default.conf /etc/nginx/conf.d/default.conf
COPY html /usr/share/nginx/html
# certs will be mounted via docker-compose volume