from qbittorrentapi import Client
from qbittorrentapi.exceptions import Forbidden403Error, LoginFailed

# Import constants
import src.settings as settings

# Login Credentials
qB = Client(host=settings.host,
            port=settings.port,
            username=settings.username,
            password=settings.password
            )

try:
    qB.auth_log_in()
    if qB.auth.is_logged_in:
        print("-" * 35)
        print(f"qBittorrent: {qB.app.version} - API: {qB.app.web_api_version}")
        print(f"Tagger: {settings.qt_version} - Author: {settings.qt_author}")
        print("-" * 35)
except LoginFailed as login_error:
    print(login_error)
except Forbidden403Error as forbidden_error:
    print(forbidden_error)

hashes = list()


def get_torrents_with_private_tracker():
    for torrent in qB.torrents_info(SIMPLE_RESPONSES=True, sort="name"):
        for tracker in qB.torrents_trackers(torrent["hash"]):
            if tracker["msg"] == "This torrent is private" and tracker["url"] == "** [DHT] **":
                hashes.append(torrent["hash"])


def torrent_info():
    return [torrent for torrent in qB.torrents_info(SIMPLE_RESPONSES=True, torrent_hashes=hashes, sort="name")]


untagged_counter = 0
already_tagged_counter = 0


def add_tag_to_torrents():
    global already_tagged_counter
    global untagged_counter

    if settings.add_tag and settings.remove_tag is False:
        for torrent in torrent_info():
            if torrent["tags"] == settings.tag_name:
                already_tagged_counter += 1
            else:
                qB.torrents_add_tags(tags=settings.tag_name, torrent_hashes=torrent["hash"])
                print(f"[NEW] Added '{settings.tag_name}' tag to {torrent['name']}")
                untagged_counter += 1
    else:
        print(f"[TAG] Add tag setting is set to {settings.add_tag}. Moving on...")


def remove_tag_from_torrents():
    global already_tagged_counter
    global untagged_counter

    if settings.remove_tag and settings.add_tag is False:
        for torrent in torrent_info():
            if torrent["tags"] == settings.tag_name:
                qB.torrents_remove_tags(tags=settings.tag_name, torrent_hashes=torrent["hash"])
                print(f"[REMOVED] Removed '{settings.tag_name}' tag from {torrent['name']}")
                untagged_counter += 1
            else:
                already_tagged_counter += 1
    else:
        print(f"[TAG] Remove tag setting is set to {settings.remove_tag}. Moving on...")


super_seed_counter = 0
already_super_seeded_counter = 0


def activate_super_seeding():
    global super_seed_counter
    global already_super_seeded_counter

    if settings.super_seed:
        for torrent in torrent_info():
            for tr in qB.torrents_trackers(torrent["hash"]):
                if tr["url"] != "** [DHT] **" and tr["url"] != "** [PeX] **" and tr["url"] != "** [LSD] **":
                    if tr["num_seeds"] <= 1 and tr["num_leeches"] >= 2 and torrent["super_seeding"] == False:
                        qB.torrents_set_super_seeding(enable=True, torrent_hashes=torrent["hash"])
                        print(
                            f"[SUPER_SEED] Activated super seeding for {torrent['name']}. {tr['num_seeds']} seeds and {tr['num_leeches']} leeches.")
                        super_seed_counter += 1
                    elif tr["num_seeds"] >= 2 and tr["num_leeches"] <= 1 and torrent["super_seeding"]:
                        qB.torrents_set_super_seeding(enable=False, torrent_hashes=torrent["hash"])
                        print(
                            f"[SUPER_SEED] Deactivated super seeding for {torrent['name']}. {tr['num_seeds']} seeds and {tr['num_leeches']} leeches.")
                    else:
                        already_super_seeded_counter += 1


force_start_count = 0
already_forced_start_count = 0


def force_start():
    global force_start_count
    global already_forced_start_count

    if settings.force_start:
        for torrent in torrent_info():
            if torrent["force_start"]:
                already_forced_start_count += 1
            else:
                qB.torrents_set_force_start(enable=True, torrent_hashes=torrent["hash"])
                print(f"[FORCE_START] Force started {torrent['name']}")
                force_start_count += 1


def env_variables():
    print(f"""
[ENV] Host: {settings.host} {type(settings.host)}
[ENV] Port: {settings.port} {type(settings.port)}
[ENV] Username: {settings.username} {type(settings.username)}
[ENV] Password: {settings.password} {type(settings.password)}
[ENV] Tag Name: {settings.tag_name} {type(settings.tag_name)}
[ENV] Add Tag: {settings.add_tag} {type(settings.add_tag)}
[ENV] Remove Tag: {settings.remove_tag} {type(settings.remove_tag)}
[ENV] Super Seed: {settings.super_seed } {type(settings.super_seed)}
[ENV] Force Start: {settings.force_start} {type(settings.force_start)}""")


def sanity_check():
    if settings.add_tag and settings.remove_tag:
        print("[TAG] Both add_tag and remove_tag settings are set to True. Please set one to False.")
        exit()


def main():
    if settings.qt_debug:
        env_variables()
    sanity_check()
    get_torrents_with_private_tracker()
    add_tag_to_torrents()
    remove_tag_from_torrents()
    activate_super_seeding()
    force_start()

    if settings.add_tag and settings.remove_tag is False:
        print(
            f"[END] Finished query with {untagged_counter} newly tagged torrents and {already_tagged_counter} already tagged torrents.")
    elif settings.remove_tag and settings.add_tag is False:
        print(f"[END] Finished query with {untagged_counter} removed tags from torrents.")
    print(
        f"[END] Finished query with {super_seed_counter} new torrents activated super seeding and {already_super_seeded_counter} not super seeding.")
    print(
        f"[END] Finished query with {force_start_count} new torrents force started and {already_forced_start_count} already force started torrents.")
    print("-" * 35)


if __name__ == "__main__":
    main()
