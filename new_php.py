import sys
import os 
import MySQLdb

name = sys.argv[1]
print name

base_dir = os.path.dirname(os.path.realpath(__file__))

# Add host with same name;
host_name = '127.0.1.1 ' + name + '.dev'

# TODO: implement logic so add line only once
# look in the file for match line
fhost = open("/etc/hosts", "a")
fhost.write("\n")
fhost.write(host_name)
fhost.close()

# Add virtual host for project
# assume project is in /home/projects/drupal/[name]
fhttpconf = open("/etc/apache2/httpd.conf", "a")

virtualhost = '\n \
\n<VirtualHost *:80>\
\n    DocumentRoot '+ base_dir + '/'+ name +'\
\n    ServerName ' + name + '.dev\
\n    <Directory ' + base_dir + '/' + name +'>\
\n      AllowOverride All\
\n    </Directory>\
\n</VirtualHost>'

fhttpconf.write(virtualhost);
fhttpconf.close();

os.system('invoke-rc.d apache2 restart');
#print file("/etc/apache2/httpd.conf").read()
#print file("/etc/hosts").read()

# Create DB with same name
db = MySQLdb.connect(user='root') # Connect to mysql server as root
cursor = db.cursor() 
try:
  cursor.execute('CREATE DATABASE ' + name) # Create DB with same name
except:
  print "DB already exist";
