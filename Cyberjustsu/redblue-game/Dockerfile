FROM php:7.4-apache

# put files
WORKDIR /var/www/html/
COPY ./src .
COPY ./configs/000-default.conf /etc/apache2/sites-available/000-default.conf

# config permission
RUN chown -R root:www-data /var/www/html
RUN chmod 750 /var/www/html
RUN find . -type f -exec chmod 640 {} \;
RUN find . -type d -exec chmod 750 {} \;

# add write permission for exploit ~~
RUN chmod -R g+w /var/www/html/

# add sticky bit to prevent delete files
RUN chmod +t -R /var/www/html/

RUN apt-get update -y
RUN apt-get install cowsay figlet toilet fortune wget -y
RUN ln -s /usr/games/cowsay /usr/bin/
RUN ln -s /usr/games/cowthink /usr/bin/
RUN ln -s /usr/games/fortune /usr/bin/
RUN rm /var/log/apache2/access.log /var/log/apache2/error.log 
RUN touch /var/log/apache2/access.log /var/log/apache2/error.log

RUN echo 'You are master of Command Injection now, FLAG xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx!\nCyberJutsu' > /secret_file
