# monchi
<br/><br/>

## Introduction
Telegram Bot for managing a Fantasy Marca League -> https://www.laligafantasymarca.com/

It's based in the python-telegram-bot that provides some methods for managing Telegram bots. -> https://github.com/python-telegram-bot/python-telegram-bot

It's necessary to create a Telegram Bot before deploying this code. -> https://core.telegram.org/bots

The platform is based in the technologies/components related below:

- Python -> The programming language used for the develop.
<br/><br/>

## Bot features

Matchdays module:
- Modify the points for matchday and player.
- Show the points by player for matchday or the total points by player.

Stats module:
- Show the budget stats for a player or for all of them.
- Show the transaction stats for a player or for all of them.

Transactions module:
- Register a transacition (buy or sell).
- Show the registered transactions by days ago, by manager or by player.
- Search for a registered transaction.
<br/><br/>

## Manually deployment: Linux installation

1. Create alfred group and user system:
```
$ sudo groupadd -g 10002 monchi
$ sudo useradd -g 10002 -u 10002 -d /home/monchi -m -s /usr/sbin/nologin monchi
```

2. Install python dependencies:
```
$ sudo pip3.5 install python-telegram-bot==10.1.0 --upgrade
```

3. Create the software location and place it (choose your own location):
```
$ cd /opt
$ sudo git clone https://github.com/Guilleloper/monchi.git
$ sudo rm -fr monchi/docker
$ sudo chown -R monchi:monchi monchi/
```

4. Prepare the logs location (choose your own location):
```
$ sudo mkdir /var/log/monchi
$ sudo chown monchi:monchi /var/log/monchi
```

5. Configure the logs management by Logrotate (choose your own configuration):
```
$ sudo view /etc/logrotate.d/monchi
~
/var/log/monchi/monchi.log
{
  rotate 60
  daily
  compress
  delaycompress
  copytruncate
  missingok
}
~
```

6. Complete the config file with your desired configuration:
```
$ sudo view monchi/config/config.json
...
```

7. Add manually the matchdays data file, by editing the appropriate file:
```
$ sudo view /opt/monchi/data/matchdays.json
~
{
  "matchdays": [
    {
      "manager": "manager1",
      "matchday_1": "0",
      "matchday_1": "0",
      ...
      "matchday_38": "0"
    },
    {
      "manager": "manager2",
      "matchday_1": "0",
      "matchday_1": "0",
      ...
      "matchday_38": "0"
    },
    ...
  ]
}
~
...
```

8. Configure systemd service, start it and enable it:
```
$ sudo view /lib/systemd/system/monchi.service
~
[Unit]
Description=Monchi, the Telegram Bot for LigaFantasyMarca
After=multi-user.target

[Service]
Type=simple
ExecStart=/usr/bin/python3.5 /opt/monchi/bin/monchi.py
User=monchi
Restart=on-failure
RestartSec=30

[Install]
WantedBy=multi-user.target
~

$ sudo systemctl daemon-reload
$ sudo systemctl start monchi && sudo systemctl enable monchi
```
<br/><br/>

## Manually deployment: Docker installation

0. Prerequisites:
- Docker-CE

1. Create monchi group and user system:
```
$ sudo groupadd -g 10002 monchi
$ sudo useradd -g 10002 -G docker -u 10002 -d /home/monchi -m -s /usr/sbin/nologin monchi
```

2. Download the repository in a temporal place:
```
$ cd /var/tmp
$ git clone https://github.com/Guilleloper/monchi.git
```

3. Prepare the config location (choose your own location):
```
$ sudo mkdir /etc/monchi
$ sudo chown monchi:monchi /etc/monchi
```

4. Complete the config file with your desired configuration:
```
$ sudo cp /var/tmp/monchi/config/config.json /etc/monchi
$ sudo view /etc/monchi/config.json
$ sudo chown monchi:monchi /etc/monchi/config.json
...
```

5. Prepare the data location (choose your own location):
```
$ sudo mkdir /var/lib/monchi
$ sudo chown monchi:monchi /var/lib/monchi
```

6. Add manually the matchdays data file, by editing the appropriate file:
```
$ sudo view /var/lib/monchi/matchdays.json
~
{
  "matchdays": [
    {
      "manager": "manager1",
      "matchday_1": "0",
      "matchday_1": "0",
      ...
      "matchday_38": "0"
    },
    {
      "manager": "manager2",
      "matchday_1": "0",
      "matchday_1": "0",
      ...
      "matchday_38": "0"
    },
    ...
  ]
}
~
$ sudo chown monchi:monchi /var/lib/monchi/matchdays.json
...
```

7. Prepare the logs location (choose your own location):
```
$ sudo mkdir /var/log/monchi
$ sudo chown monchi:monchi /var/log/monchi
```

8. Configure the logs management by Logrotate (choose your own configuration):
```
$ sudo view /etc/logrotate.d/monchi
~
/var/log/monchi/monchi.log
{
  rotate 60
  daily
  compress
  delaycompress
  copytruncate
  missingok
}
~
```

9. Build the Monchi Docker image:
```
$ cd monchi
$ docker build -f docker/Dockerfile -t "monchi:`cat VERSION`" .
```

10. Create Docker container:
```
$ sudo runuser -u monchi -- docker run -d --name monchi \
  -v /etc/timezone:/etc/timezone:ro \
  -v /etc/localtime:/etc/localtime:ro \
  -v /var/lib/monchi:/monchi/data \
  -v /etc/monchi:/monchi/config \
  -v /var/log/monchi:/monchi/log \
  monchi:`cat VERSION`
```

16. Configure systemd service, start it and enable it:
```
$ sudo runuser -u monchi -- docker stop monchi
$ sudo view /lib/systemd/system/monchi.service
~
[Unit]
Description=Monchi, the Telegram Bot for LigaFantasyMarca
After=docker.service
Wants=network-online.target docker.socket
Requires=docker.socket

[Service]
Type=simple
ExecStart=/usr/bin/docker start -a monchi
ExecStop=/usr/bin/docker stop -t 30 monchi
User=monchi
Restart=on-failure
RestartSec=30

[Install]
WantedBy=multi-user.target
~

$ sudo systemctl daemon-reload
$ sudo systemctl start monchi && sudo systemctl enable monchi
$ cd; rm -fr /var/tmp/monchi
```
<br/><br/>

## Automatically Ansible deployment

(in proccess)

