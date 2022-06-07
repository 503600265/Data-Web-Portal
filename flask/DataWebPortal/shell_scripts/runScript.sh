#!/bin/bash
tmux new-session -d -s model
tmux send-keys -t model "flaskenv" Enter
tmux send-keys -t model "python dyadRun.py" Enter
tmux send-keys -t model "./tmux_scrn_shot_end.sh" Enter
tmux send-keys -t model "exit" Enter
