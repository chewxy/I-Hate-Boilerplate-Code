# Boilerplate README.md addons #

Copy and paste whatever bits and bobs you need to new project README.mds

# Requirements#

___INSERT PROJECT NAME HERE___ runs on this stack:

* Ubuntu - OS. You can swap out for any other OS, but the below instructions are Ubuntu
* gevent + bottle.py - server for pixel server
* nginx (uWSGI) + flask - frontend/admin
* zeromq - communication
* redis - cache
* couchDB
* crontab - scheduling

___INSERT PROJECT NAME HERE___ is primarily geared to run on Amazon Web Services, and as such there will be references to AWS. However you may feel free to adapt the instructions to any cloud service provider


# Deployment Instructions#

## Build Essentials##

Ubuntu has a nice build essentials package. It has gcc, make etc installed. These things enable you to build from scratch

1. Install Build Essentials: `sudo apt-get install build-essential`
2. Install Python development headers: `sudo apt-get install python-dev`
3. Install pip via apt-get: `apt-get install python-pip`

Of course if you are smart, you'll chain them together.

## Git##

1. Install git: `sudo apt-get install git`

## [ZeroMQ](http://zeromq.org)##

The version of ZeroMQ used is 2.2. DO NOT use apt-get. The repository for up to Precise Pangolin (12.04) is still at ZMQ 2.1.1

1. You need to have the build-essentials package installed
2. You also need uuid-dev and uuid/e2fsprogs installed. On Ubuntu: `sudo apt-get install uuid-dev e2fsprogs`
3. Get the latest stable 2.2 release of ZMQ (2.2.0): ` wget http://download.zeromq.org/zeromq-2.2.0.tar.gz`
4. Untar it: `tar -xzvf zeromq-2.2.0.tar.gz`
5. Go to the untar'd directory, run this: `./configure && make`
6. Install ZMQ system-wide: `sudo make install`
7. Configure the LD files: `sudo ldconfig`

## PyZMQ##

1. Install using pip: `pip install pyzmq`

## [gevent](http://gevent.org)##

The version of gevent in PyPI is the pre-1.0 version which it uses libevent instead of libev. The version required for A3 is gevent1.0+

1. Install libev4: ` sudo apt-get install libev4 libev-libevent-dev `
2. Download the latest version of gevent (gevent-1.0b2): ` wget https://github.com/downloads/SiteSupport/gevent/gevent-1.0rc1.tar.gz `
3. Untar it: `tar -xzvf gevent-1.0rc1.tar.gz`
4. Go to the untar'd directory, then make: `python setup.py build`
5. Install it (sudo may be required): `python setup.py install`

## gevent_zmq##

1. Install using pip: `pip install gevent_zmq`

## [couchDB](http://couchdb.apache.org)##

The version of couchDB we're using is 1.2.0. 

1. First install the dependencies: `sudo apt-get build-dep couchdb`. Alternatively: `sudo apt-get install build-essential erlang libicu-dev libmozjs-dev libcurl4-openssl-dev`
2. This is missing from the [Install CouchDB guide](http://wiki.apache.org/couchdb/Installing_on_Ubuntu). You need to install erlang's eunit. Might as well install all the things: `sudo apt-get install erlang-nox`
3. Download it: `wget http://mirror.overthewire.com.au/pub/apache/couchdb/releases/1.2.0/apache-couchdb-1.2.0.tar.gz`
4. Untar it: `tar -xzvf apache-couchdb-1.2.0.tar.gz`
5. Navigate to the directory
6. Configure the install `./configure`
7. Make and Install: `make && sudo make install`

### Security for CouchDB###

From the [Definitive Guide](http://guide.couchdb.org/draft/source.html):

It is not advisable to run the CouchDB server as the super user. If the CouchDB server is compromised by an attacker while it is being run by a super user, the attacker will get super user access to your entire system. That’s not what we want!

1. Create a user called couchdb and a new group called Couchdb: `sudo adduser --system --home /usr/local/var/lib/couchdb --no-create-home --shell /bin/bash --group --gecos "CouchDB" couchdb`
2. Change ownership of CouchDB directories:
```bash
chown -R couchdb:couchdb /usr/local/etc/couchdb
chown -R couchdb:couchdb /usr/local/var/lib/couchdb
chown -R couchdb:couchdb /usr/local/var/log/couchdb
chown -R couchdb:couchdb /usr/local/var/run/couchdb
```
3. Change the permission of those directories: 
```bash
chmod -R 0770 /usr/local/etc/couchdb
chmod -R 0770 /usr/local/var/lib/couchdb
chmod -R 0770 /usr/local/var/log/couchdb
chmod -R 0770 /usr/local/var/run/couchdb
```
4. Test: `sudo -i -u couchdb couchdb -b`

### Log rotation###

Some people may want log rotation, some may not. On production servers this is a good idea:

1. Run `sudo ln -s /usr/local/etc/logrotate.d/couchdb /etc/logrotate.d/couchdb`


## [redis](http://redis.io)##

This is the default method of installing it

1. Get the file: `wget http://redis.googlecode.com/files/redis-2.4.15.tar.gz`
2. Untar it `tar xzf redis-2.4.15.tar.gz`
3. Go into it `cd redis-2.4.15`
4. Make it `make`
5. Install it `sudo make install`
6. Create directories for redis config and redis data: `sudo mkdir /etc/redis & sudo mkdir /var/redis`
7. Copy the redis init script in `./utils` to `/etc/init.d`: `sudo cp utils/redis_init_script /etc/init.d/redis`. 
8. Change the init.d script to be executable: `sudo chmod 777 /etc/init.d/redis`
9. Edit the init script: `sudo nano /etc/init.d/redis`. Change the CONF variable to this: "/etc/redis/redis.conf"
10. Create a directory in `/var/redis` that works as a working directory for Redis: `sudo mkdir /var/redis/redis`
11. Edit Conf file: `sudo nano /etc/redis/redis.conf`. Change the port to `6379`, change the pid file to `/var/run/redis_6379.pid` and the dir to `var/redis/redis`
12. Set redis to run with the default runlevel: `sudo update-rc.d redis defaults`
13. Start redis: `sudo /etc/init.d/redis start`

Ubuntu users, this is a good personal repository (PPA) for redis: https://launchpad.net/~rwky/+archive/redis

To install using this PPA, simply do this:

1. Add the repository (**SECURITY WARNING**: do so only if you trust the PPA, and [do so at your own risk](http://lwn.net/Articles/367874/)) `sudo add-apt-repository ppa:rwky/redis`
2. Update package information: `sudo apt-get update`
3. Install/update: `sudo apt-get install redis-server`

## [Couchdbkit](http://couchdbkit.org) ##

1. Install using pip: `pip install couchdbkit`

## Redis-py ##

1. Install using pip: `pip install redis`

## [Web.py](http://webpy.org)##

1. Install using pip: `pip install web.py`

## [Tenjin](http://www.kuwata-lab.com/tenjin)

Web.py's native renderer is slow, so we use Tenjin as a drop-in replacement instead.

1. Install using pip: `pip install tenjin`

## Messagepack##

1. Install using pip: `pip install msgpack-python`

## SetProcTitle##

1. Install using pip: `pip install setproctitle`


# Tuning the server#

Your server (typically) by default doesn't have high File Descriptor (FD) limits. Use these to raise the limits (on Ubuntu):
```bash
	echo “10152 65535″ > /proc/sys/net/ipv4/ip_local_port_range
	sysctl -w fs.file-max=128000
	sysctl -w net.ipv4.tcp_keepalive_time=300
	sysctl -w net.core.somaxconn=250000
	sysctl -w net.ipv4.tcp_max_syn_backlog=2500
	sysctl -w net.core.netdev_max_backlog=2500
	ulimit -n 10240
```
