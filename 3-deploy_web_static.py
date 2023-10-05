#!/usr/bin/python3
"""Task 3"""
from datetime import datetime
from fabric.api import env, run, put, local
from os.path import exists


env.hosts = ['54.174.71.36', '54.84.24.93']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


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


def do_deploy(archive_path):
    """
    Distributes an archive to web servers.

    Args:
        archive_path (str): Path to the archive on the local machine.

    Returns:
        bool: True if all operations were successful, False otherwise.
    """
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory on the web server
        put(archive_path, '/tmp/')

        # Extract the archive to /data/web_static/releases/
        archive_filename = archive_path.split('/')[-1]
        release_folder = "/data/web_static/releases/{}".format(
            archive_filename.split('.')[0]
        )
        run("sudo mkdir -p {}".format(release_folder))
        run("sudo tar -xzf /tmp/{} -C {}".format(
                    archive_filename, release_folder
        ))

        # Delete the archive from the web server
        run("sudo rm /tmp/{}".format(archive_filename))

        # move contents
        run('sudo mv {}/web_static/* {}'.format(
            release_folder, release_folder
        ))
        run('sudo rm -rf {}/web_static'.format(release_folder))

        # Remove the existing symbolic link /data/web_static/current
        current_link = "/data/web_static/current"
        run("sudo rm -f {}".format(current_link))

        # Create a new symbolic link to the latest version
        run("sudo ln -s {} {}".format(release_folder, current_link))

        print("New version deployed!")
        return True
    except Exception:
        return False


def deploy():
    """
    Calls the do_pack() function and stores the path of the created archive.
    Returns False if no archive has been created.
    Calls the do_deploy(archive_path) function,
    using the new path of the new archive.
    Returns the return value of do_deploy.
    """
    archive_path = do_pack()
    if not archive_path:
        return False

    return do_deploy(archive_path)
