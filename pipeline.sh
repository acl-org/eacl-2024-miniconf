#!/bin/bash

python data/eacl_2024/new_data/generate_booklet_data_json.py &&
python data/eacl_2024/new_data/write_event_to_booklet.py &&
python data/eacl_2024/new_data/generate_workshops_yaml.py &&
python eacl_miniconf/import_eacl2024.py &&
python data/eacl_2024/new_data/generate_BoF_display.py &&
python data/eacl_2024/new_data/write_BoF_display_to_conference.py &&
python data/eacl_2024/new_data/generate_break_display.py &&
python data/eacl_2024/new_data/write_break_display_to_conference.py &&
python data/eacl_2024/new_data/generate_coffee_break_json.py &&
python data/eacl_2024/new_data/write_break_to_conference.py &&
python data/eacl_2024/new_data/write_social_event_display_to_confenence.py &&
python data/eacl_2024/new_data/write_keynotes_to_conference.py