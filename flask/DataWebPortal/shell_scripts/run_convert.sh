#!/bin/bash
tmux new-session -d -s convert
tmux send-keys -t convert "conda activate convert" Enter
tmux send-keys -t convert "python ../python/convert_data.py" Enter
tmux send-keys -t convert "./tmux_scrn_shot_end.sh" Enter
tmux send-keys -t convert "exit" Enter
