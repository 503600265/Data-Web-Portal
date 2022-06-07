#!/bin/bash
/bin/bash /home/postd/.tmux/plugins/tmux-logging/scripts/screen_capture.sh
cat /home/postd/*.log > /home/postd/dyadModelApp/app/static/text/progress.txt
rm /home/postd/*.log
