FROM nginx:alpine

# Copiamos todo el contenido de tu carpeta frontend a la ruta de Nginx
COPY . /usr/share/nginx/html/
COPY default.conf /etc/nginx/conf.d/default.conf
EXPOSE 80

