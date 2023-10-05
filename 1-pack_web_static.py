#!/usr/bin/python3
"""Tast 1"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.

    Returns:
        str: Archive path if generated successfully, None otherwise.
    """
    # Create the versions folder if it doesn't exist
    local("mkdir -p versions")

    # Create the archive name using the current date and time
    now = datetime.utcnow()
    timestamp = now.strftime("%y%m%d%H%M%S")
    archive_name = "web_static_{}.tgz".format(timestamp)

    # Compress the web_static folder into the archive
    command = "tar -czvf versions/{} web_static".format(archive_name)
    result = local(command, capture=True)

    # Check if the archive was created successfully
    if result.succeeded:
        return "versions/{}".format(archive_name)
    else:
        return None
