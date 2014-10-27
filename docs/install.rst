Install
=========

This is where you write how to get a new laptop to run this project.

1. Create mysql database and configure

.. code-block:: mysql::

    mysql> CREATE DATABASE zhiwehu CHARACTER SET utf8;
    mysql> GRANT ALL PRIVILEGES ON zhiwehu.* TO "zhiwehu"@"localhost" IDENTIFIED BY "password";
    mysql> FLUSH PRIVILEGES;
    mysql> EXIT;
