"""
refer to:
    https://developer.rocket.chat/chat-engine/chat-engine-in-iframe
    https://github.com/jadolg/rocketchat_API
    https://forums.rocket.chat/t/error-you-must-be-logged-in-to-do-this-with-status-code-401unauthorized/9804
"""

from pathlib import Path
import os
from os.path import dirname
from typing import List
import pickle
import json

import requests
import hydra
from omegaconf import DictConfig
from requests import sessions
from rocketchat_API.rocketchat import RocketChat
import yaml
from eacl_miniconf.data import Conference
from rich.progress import track

def paper_id_to_channel_name(paper_id: str):
    channel_name = f"paper-{paper_id}"
    channel_name = channel_name.replace(".", "-")
    return channel_name

def write_into_json(datas, file_name):
    with open(file_name, "w", encoding="utf-8") as f:
        for data in datas:
            f.write("%s\n"%(json.dumps(data, ensure_ascii=False)))

API_path = "/api/v1/"
CUSTOM_EMOJI_DIR = Path("rocketchat-custom-emojis/")


class EaclRcHelper:
    def __init__(
        self,
        *,
        program_json_path: str,
        booklet_json_path: str,
        workshops_yaml_path: str,
        user_id: str,
        auth_token: str,
        server: str,
        session: sessions.Session,
        dry_run: bool = False,
    ):
        # proj_path = dirname(dirname(dirname(__file__)))
        # program_json_path = os.path.join(proj_path, program_json_path)
        # booklet_json_path = os.path.join(proj_path, booklet_json_path)
        # workshops_yaml_path = os.path.join(proj_path, workshops_yaml_path)
        self.conference: Conference = Conference.parse_file(program_json_path)
        with open(booklet_json_path) as f:
            self.booklet = json.load(f)

        with open(workshops_yaml_path) as f:
            self.workshops = yaml.safe_load(f)
        self.dry_run = dry_run
        self.auth_token = auth_token
        self.user_id = user_id
        self.server = server
        self.rocket = RocketChat(
            user_id=user_id,
            auth_token=auth_token,
            server_url=server,
            session=session,
        )

    def get_channel_names(self) -> List[str]:
        return [
            c["name"] for c in self.rocket.channels_list(count=0).json()["channels"]
        ]

    def create_channel(
        self, name: str, topic: str, description: str, create: bool = True
    ):
        if self.dry_run:
            print("Dry Run: Creating " + name + " topic " + topic)
        else:
            if create:
                created = self.rocket.channels_create(name).json()
                if not created["success"]:
                    raise ValueError(f"Bad response: name={name} response={created}")
                channel_id = created["channel"]["_id"]
            else:
                channel_id = self.rocket.channels_info(channel=name).json()["channel"][
                    "_id"
                ]
            self.rocket.channels_set_topic(channel_id, topic).json()
            self.rocket.channels_set_description(channel_id, description).json()

    def delete_channel(
        self, room_id=None, channel=None
    ):
        """
        delete a channel using either room_id or channel_name
        """
        self.rocket.channels_delete(room_id=room_id, channel=channel)

    def create_tutorial_channels(self):
        existing_channels = set(self.get_channel_names())
        skipped = 0
        created = 0
        datas = []
        for tutorial in track(self.booklet["tutorials"]):
            tutorial_id = tutorial["id"].replace("T", "")
            channel_name = f"tutorial-{tutorial_id}"
            author_string = ", ".join(tutorial["hosts"])
            title = tutorial["title"]
            topic = f"{title} - {author_string}"
            create = channel_name not in existing_channels
            self.create_channel(channel_name, topic, tutorial["desc"], create=create)
            created += 1

            sample = {}
            sample['tutorial_id'] = tutorial_id
            sample['tutorial_channel'] = channel_name
            sample['tutorial_title'] = title
            datas.append(sample)

        print(
            f"Total tutorials: {len(self.conference.papers)}, Created: {created} Skipped: {skipped} Total: {created + skipped}"
        )

        # write_into_json(datas, "tuturial_channels.json")

    def create_workshop_channels(self):
        existing_channels = set(self.get_channel_names())
        skipped = 0
        created = 0
        datas = []
        for ws in track(self.workshops):
            if ws["short_name"] == "inputs":
                workshop_id = ws["anthology_venue_id"]
            else:
                workshop_id = ws["short_name"]
            channel_name = f"workshop-{workshop_id}"
            title = ws["name"]
            topic = f"{title} - {workshop_id}"
            create = channel_name not in existing_channels
            self.create_channel(channel_name, topic, topic, create=create)
            created += 1

            sample = {}
            sample['workshop_id'] = workshop_id
            sample['workshop_channel'] = channel_name
            sample['workshop_title'] = channel_name
            datas.append(sample)

        print(
            f"Total workshops: {len(self.conference.papers)}, Created: {created} Skipped: {skipped} Total: {created + skipped}"
        )

        # write_into_json(datas, "workshop_channels.json")

    def create_paper_channels(self):
        existing_channels = set(self.get_channel_names())
        skipped = 0
        created = 0
        datas = []
        for paper in track(self.conference.papers.values()):
            if paper.is_paper:
                channel_name = paper_id_to_channel_name(paper.id)
                sample = {}
                sample['paper_id'] = paper.id
                sample['channel_name'] = channel_name
                sample['paper_title'] = paper.title
                datas.append(sample)
                if channel_name in existing_channels:
                    skipped += 1
                else:
                    author_string = ", ".join(paper.authors)
                    topic = f"{paper.title} - {author_string}"
                    self.create_channel(channel_name, topic, paper.abstract)
                    created += 1
        write_into_json(datas, "paper_channels.json")
        print(
            f"Total papers: {len(self.conference.papers)}, Created: {created} Skipped: {skipped} Total: {created + skipped}"
        )

    def add_custom_emojis(self):
        headers = {
            "X-Auth-Token": self.auth_token,
            "X-User-Id": self.user_id,
        }
        # get all emoji images - only include JPG, PNG, and GIF files
        emoji_files = [
            x
            for x in os.listdir(CUSTOM_EMOJI_DIR)
            if x.endswith(".png") or x.endswith(".jpg") or x.endswith(".gif")
        ]

        for emoji_f in track(emoji_files):
            emoji_name, emoji_aliases = emoji_f.split(".")[0].split("_")

            files = {
                "emoji": (emoji_f, open(CUSTOM_EMOJI_DIR / emoji_f, "rb")),
                "name": (None, emoji_name),
                "aliases": (None, emoji_aliases),
            }
            try:
                response = requests.post(
                    self.server + API_path + "emoji-custom.create",
                    headers=headers,
                    files=files,
                )
                response.raise_for_status()
                print(json.loads(response.content)["success"])
            except requests.exceptions.HTTPError as err:
                print("Encountered error: ", err)
                print("File: ", emoji_f)


@hydra.main(
    version_base=None, config_path="../../configs/rocketchat", config_name="template"
)
def hydra_main(cfg: DictConfig):
    command = cfg.command

    if command == "create_paper_channels":
        with sessions.Session() as session:
            helper = EaclRcHelper(
                user_id=cfg.user_id,
                auth_token=cfg.auth_token,
                server=cfg.server,
                session=session,
                program_json_path=Path(cfg.program_json_path),
                booklet_json_path=Path(cfg.booklet_json_path),
                workshops_yaml_path=Path(cfg.workshops_yaml_path),
                dry_run=cfg.dry_run,
            )
            helper.create_paper_channels()
    elif command == "create_tutorial_channels":
        with sessions.Session() as session:
            helper = EaclRcHelper(
                user_id=cfg.user_id,
                auth_token=cfg.auth_token,
                server=cfg.server,
                session=session,
                program_json_path=Path(cfg.program_json_path),
                booklet_json_path=Path(cfg.booklet_json_path),
                workshops_yaml_path=Path(cfg.workshops_yaml_path),
                dry_run=cfg.dry_run,
            )
            helper.create_tutorial_channels()
    elif command == "create_workshop_channels":
        with sessions.Session() as session:
            helper = EaclRcHelper(
                user_id=cfg.user_id,
                auth_token=cfg.auth_token,
                server=cfg.server,
                session=session,
                program_json_path=Path(cfg.program_json_path),
                booklet_json_path=Path(cfg.booklet_json_path),
                workshops_yaml_path=Path(cfg.workshops_yaml_path),
                dry_run=cfg.dry_run,
            )
            helper.create_workshop_channels()
    elif command == "add_emojis":
        with sessions.Session() as session:
            helper = EaclRcHelper(
                user_id=cfg.user_id,
                auth_token=cfg.auth_token,
                server=cfg.server,
                session=session,
                program_json_path=Path(cfg.program_json_path),
                booklet_json_path=Path(cfg.booklet_json_path),
                workshops_yaml_path=Path(cfg.workshops_yaml_path),
                dry_run=cfg.dry_run,
            )
            helper.add_custom_emojis()
    elif command == "get_channel_names":
        with sessions.Session() as session:
            helper = EaclRcHelper(
                user_id=cfg.user_id,
                auth_token=cfg.auth_token,
                server=cfg.server,
                session=session,
                program_json_path=Path(cfg.program_json_path),
                booklet_json_path=Path(cfg.booklet_json_path),
                workshops_yaml_path=Path(cfg.workshops_yaml_path),
                dry_run=cfg.dry_run,
            )
            channel_names = helper.get_channel_names()
            print(channel_names)
    elif command == "delete_channels":
        with sessions.Session() as session:
            helper = EaclRcHelper(
                user_id=cfg.user_id,
                auth_token=cfg.auth_token,
                server=cfg.server,
                session=session,
                program_json_path=Path(cfg.program_json_path),
                booklet_json_path=Path(cfg.booklet_json_path),
                workshops_yaml_path=Path(cfg.workshops_yaml_path),
                dry_run=cfg.dry_run,
            )
            channel_names = helper.get_channel_names()

            ## 1. delete paper channel
            for channel in channel_names:
                # if "paper-" in channel.lower():
                if "-srw" in channel.lower():
                    helper.delete_channel(channel=channel)

            ## 2. delete tutorial channel
            # for channel in channel_names:
            #     if "tutorial-" in channel.lower():
            #         helper.delete_channel(channel=channel)

            ## 3. delete workshop channel
            # for channel in channel_names:
            #     if "workshop-" in channel.lower():
            #         helper.delete_channel(channel=channel)

if __name__ == "__main__":
    hydra_main()

    ## for test connection
    """
    with sessions.Session() as session:
        rocket = RocketChat(
            user_id="",
            auth_token="",
            server_url="https://acl.rocket.chat",
            session=session,
        )
    print(rocket.me().json())
    """
