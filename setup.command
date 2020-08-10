
# For MAC: Installing mysqlclient

brew install mysql 
PATH=$PATH:/usr/local/mysql/bin
pip3 install mysql-connector-python
pip3 install pymysql

env LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib" pip3 install mysqlclient
