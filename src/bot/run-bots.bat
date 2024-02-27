@echo off
start cmd /c "python main.py --logic BotGreedyPath --email=greedy1@email.com --name=gpath --password=123456 --team etimo"
start cmd /c "python main.py --logic BotGreedyPoints --email=greedy2@email.com --name=gpoints --password=123456 --team etimo"
start cmd /c "python main.py --logic BotChase --email=chase@email.com --name=chase --password=123456 --team etimo"
start cmd /c "python main.py --logic Random --email=random2@email.com --name=random2 --password=123456 --team etimo"