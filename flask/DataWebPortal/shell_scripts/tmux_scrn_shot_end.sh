#!/bin/bash
/bin/bash /home/postd/.tmux/plugins/tmux-logging/scripts/screen_capture.sh
cat /home/postd/*.log > /home/postd/dyadModelApp/.tmux_logging/model_log.txt
rm /home/postd/*.log
