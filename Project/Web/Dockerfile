FROM nginx:alpine

# Nginx conf
COPY default.conf /etc/nginx/conf.d/default.conf

# Web bestandsen
COPY index.html /usr/share/nginx/html/index.html
COPY styles.css /usr/share/nginx/html/styles.css
COPY assets /usr/share/nginx/html/assets

EXPOSE 80
