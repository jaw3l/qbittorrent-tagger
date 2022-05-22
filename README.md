# qBitTorrent Tagger

Main purposes of this script are forcing private torrents to always seed and tagging those torrents with given tag name to organize. Project is very basic so feel free to contribute if you find any errors or improvements. New ideas are always welcome, too.

This script uses Python client implementation for [qBittorrent's Web API](https://github.com/rmartin16/qbittorrent-api) by [rmmartin16](https://github.com/rmartin16).

## What it does?

- Adds tag to private torrents.
- Force starts the private torrents.
- Activates super-seed mode if you are the only one who is seeding that particular torrent.

## Installation

### Docker

You can run the container and automatically remove the container when it exits with:

```docker
docker run --rm \
  --name=qbittorrent-tagger \
  -e QB_HOST=192.168.0.254 \
  -e QB_PORT=8080 \
  -e QB_USER=admin \
  -e QB_PASS=password \
  -e QT_FORCE_START=True `# Optional` \
  -e QT_ADD_TAG=True `# Optional` \
  -e QT_REMOVE_TAG=False `# Optional` \
  -e QT_SUPER_SEED=False `# Optional` \
  -e QT_TAG_NAME=Private `# Optional` \
  -e QT_DEBUG=False `# Optional` \
  jaw3l/qbittorrent-tagger:latest
```

#### Build

You can build docker image with `docker build -t jaw3l/qbittorrent-tagger:latest .`

### Docker Compose

```docker
version: "2"

services:
  qbittorrent-tagger:
    image: jaw3l/qbittorrent-tagger:latest
    container_name: qbittorrent-tagger
    environment:
      ## qBitTorrent Information
      - QB_HOST=localhost
      - QB_PORT=8080
      - QB_USER=admin
      - QB_PASS=password
      ## Booleans
      - QT_FORCE_START=False # Optional
      - QT_ADD_TAG=True # Optional
      - QT_REMOVE_TAG=False # Optional
      - QT_SUPER_SEED=True # Optional
      ## Tag Name
      - QT_TAG_NAME=Private # Optional
      ## Debug Mode
      - QT_DEBUG=False # Optional
```

To start the container and delete afterwards:

```docker
docker-compose run --rm qbittorrent-tagger
```

#### Build

You can build docker image with `docker-compose build` than start the container with `docker-compose run --rm qbittorrent-tagger`

### Environment Variables

| Variable | Information | Required |
| -------- | ----------- | -------- |
| QB_HOST  | Hostname of qBitTorrent's Web-UI | yes |
| QB_PORT  | Port of qBitTorrent's Web-UI. _Default:_ __8080__ | yes |
| QB_USER  | Username qBitTorrent's Web-UI | yes |
| QB_PASS  | Password of qBitTorrent's Web-UI | yes |
| QT_FORCE_START | Force start the torrent if it has private tracker _Default:_ __True__ | no |
| QT_ADD_TAG | Adds tag to torrents with private trackers to organize torrents. _Default:_ __True__ | no |
| QT_REMOVE_TAG | Removes the `QT_TAG_NAME` from torrents. _Default:_ __False__ | no |
| QT_SUPER_SEED | Leave that as 'False' if you don't know what it is. More info below. _Default:_ __False__ | no |
| QT_TAG_NAME | Tag name to be added. _Default:_ __"Private"__ | no |
| QT_DEBUG | Debug mode. _Default:_ __False__ | no |

### Pip

`qbittorrent-api` module is required for this script to run.

```py
pip3 install -r requirements.txt
```

You can start the script after you edit the `src/settings.py` file.

```bash
nano src/settings.py 
```

Save `(CTRL+O)` than exit `(CTRL+X)` from `nano`. Now you are ready to start the python script.

```py
python3 tagger.py
```

Or you can use [pipenv](https://pipenv.pypa.io/), too

```py
pip3 install pipenv
pipenv install
pipenv run python tagger.py
```

## ToDo

- Add management option (force start torrents with <=2 seeds)
- Add more options
- Code improvements

## Notes

__What is super-seed?__

Super Seeding is a special optimised seeding mode. It allows seeders who are the only seed in the swarm to solely seed pieces that are found nowhere else in the swarm. It works something like this: the superseeding client pretends not to be a seed, but pretends to be a peer with an incomplete file. Then the client shares each piece with one peer only. And that peer can then share that piece with the swarm. This allows the superseeding client to maximise the efficiency of the upload by only sharing those pieces nobody else has. And because of some other things about the behaviour of superseeding, this function does not work at all well in swarms with one peer and one seed only. So it is only good when the seeder is the only seed (usually the original uploader), and there are more than two peers.
