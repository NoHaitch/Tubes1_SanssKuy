#!/bin/bash

python main.py --logic MyBot --email=example1@email.com --name=main1 --password=123456 --team etimo &
python main.py --logic MyBot --email=example2@email.com --name=main2 --password=123456 --team etimo &
python main.py --logic Chase --email=example3@email.com --name=chase --password=123456 --team etimo &
python main.py --logic Points --email=example4@email.com --name=points --password=123456 --team etimo &