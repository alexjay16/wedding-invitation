#!/bin/bash
echo ""
echo "  Starting Wedding RSVP Server..."
echo "  Open your browser at: http://localhost:8000"
echo "  Press Ctrl+C to stop."
echo ""
# Open browser after 1 second
(sleep 1 && open "http://localhost:8000/wedding-invite.html" 2>/dev/null || xdg-open "http://localhost:8000/wedding-invite.html" 2>/dev/null) &
python3 server.py