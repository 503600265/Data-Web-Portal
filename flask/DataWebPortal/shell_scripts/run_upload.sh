#!/bin/bash
tmux new-session -d -s upload
tmux send-keys -t upload "conda activate upload" Enter
tmux send-keys -t upload "python ../python/upload_data.py" Enter
tmux send-keys -t upload "./tmux_scrn_shot_end.sh" Enter
tmux send-keys -t upload "exit" Enter
