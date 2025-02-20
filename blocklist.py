"""
blocklist.py

This file just contains the blocklist of the JWT tokens. It will be imported by
app and the logout resource so that tokens can be added to the blocklist when the
user logs out.
"""

# normalmente debería estar en base de datos...

# Let's create our central revoked JWT storage in a file called blocklist.py. You could store this in the database instead, if you prefer. I'll leave that as an exercise for you.

BLOCKLIST = set()
