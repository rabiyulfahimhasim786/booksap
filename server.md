google cloude ssh

    sudo ssh -i /home/foldername/Documents/googlecloud.pem  bitnami@youripaddress
    sudo ssh -i /home/foldername/Documents/gcloud_bkuplinux ksmani@youripaddress
    ssh -i "/home/foldername/Documents/secretkey.pem" username@password.compute-1.amazonaws.com
change owner

    sudo chown -R bitnami:bitnami  .
    sudo chown -R ksmani:ksmani  .
    sudo chown -R ubuntu:ubuntu .
    sudo chown -R www-data:www-data .

    sudo usermod -a -G www-data bitnami
    sudo chmod -R 771 mainfolder/

Apache Server reload

    sudo service apache2 reload
    sudo systemctl reload apache2


institute.Conf

listen 89
<VirtualHost *:89>
    # The ServerName directive sets the request scheme, hostname and port that
    # the server uses to identify itself. This is used when creating
    # redirection URLs. In the context of virtual hosts, the ServerName
    # specifies what hostname must appear in the request's Host: header to
    # match this virtual host. For the default virtual host (this file) this
    # value is not decisive as it is used as a last resort host regardless.
    # However, you must set it for any further virtual host explicitly.
    #ServerName www.example.com

    ServerAdmin admin@gmail.com
    ServerName yourregistereddomainname.com
    DocumentRoot /home/bitnami/pythonprojects/appfolder

    # Available loglevels: trace8, ..., trace1, debug, info, notice, warn,
    # error, crit, alert, emerg.
    # It is also possible to configure the loglevel for particular
    # modules, e.g.
    #LogLevel info ssl:warn

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined

    # For most configuration files from conf-available/, which are
    # enabled or disabled at a global level, it is possible to
    # include a line for only one particular virtual host. For example the
    # following line enables the CGI configuration for this host only
    # after it has been globally disabled with "a2disconf".
    #Include conf-available/serve-cgi-bin.conf
    Alias /static /home/bitnami/pythonprojects/appfolder/static

    <Directory /home/bitnami/pythonprojects/appfolder/static>
            Require all granted
    </Directory>

    <Directory /home/bitnami/pythonprojects/appfolder/institute>
            <Files wsgi.py>
                    Require all granted
            </Files>
    </Directory>

    WSGIScriptAlias / /home/bitnami/pythonprojects/appfolder/mysite/wsgi.py
    WSGIDaemonProcess appfolder python-path=/home/bitnami/pythonprojects/appfolder python-home=/home/bitnami/pythonprojects/appfolder/venv
    WSGIProcessGroup appfolder
    WSGIPassAuthorization on

</VirtualHost>

Settings.py
pip install django==4.2.5
pip install django-cors-headers
pip install djangorestframework

INSTALLED_APPS = (

    ...
    'corsheaders',
    'rest_framework',
    ...
)

MIDDLEWARE = [

    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    ...
]
CORS_ORIGIN_ALLOW_ALL = True

Authorization: JWT <your_token>

DB data dump/load
python manage.py dumpdata -e contenttypes -e admin -e auth.Permission --natural-foreign --indent=2 > db.json
python manage.py loaddata db.json
python manage.py sqlflush
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

sudo apt-get install libapache2-mod-wsgi-py3
