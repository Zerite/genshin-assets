# Clones the "genshin-optimizer" project and downloads all images for items
# for the GOOD (Genshin Open Object Description) format.

import os
import shutil

from git import Repo
from git.remote import RemoteProgress

class Progress(RemoteProgress):
    def update(self, *args):
        print(self._cur_line)

def process_dir(dir: str, target: str):
    """
    Walk through all the items in the directory, and copy the images
    to their respective folder.
    """

    for item in os.listdir(dir):
        item_dir = os.path.join(dir, item)
        if os.path.isdir(item_dir):
            process_dir(item_dir, f"{target}/{item}")
        else:
            if item.endswith(".png"):
                print("{} -> {}".format(item_dir, target))
                os.makedirs(target, exist_ok=True)
                shutil.copy(item_dir, target)
                

if __name__ == "__main__":
    # Clone the repo
    repo_dir = "genshin-optimizer"

    if os.path.exists(repo_dir):
        print("Repo already exists, pulling...")
        repo = Repo(repo_dir)
        repo.remotes.origin.pull(progress=Progress())
    else:
        print("Cloning repo...")
        Repo.clone_from("git@github.com:frzyc/genshin-optimizer.git", repo_dir, progress=Progress())

    # Export the images
    target = "../images/good"
    directories = ["Artifacts", "Characters", "Weapons"]

    for dir_name in directories:
        process_dir(f"{repo_dir}/src/Data/{dir_name}", f"{target}/{dir_name.lower()}")