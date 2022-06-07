#!/bin/bash
tmux new-session -d -s ocr
tmux send-keys -t ocr "conda activate ocr" Enter
tmux send-keys -t ocr "python ../python/ocr_docs.py" Enter
tmux send-keys -t ocr "./tmux_scrn_shot_end.sh" Enter
tmux send-keys -t ocr "exit" Enter
