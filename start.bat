@echo off
echo.
echo  Starting Wedding RSVP Server...
echo  Open your browser at: http://localhost:8000
echo  Press Ctrl+C to stop.
echo.
start "" http://localhost:8000/wedding-invite.html
python server.py
pause