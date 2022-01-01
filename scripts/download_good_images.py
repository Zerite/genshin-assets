# Clones the "genshin-optimizer" project and downloads all images for items
# for the GOOD (Genshin Open Object Description) format.

import os
import re
import shutil

from git import Repo
from git.remote import RemoteProgress


class Progress(RemoteProgress):
    def update(self, *args):
        print(self._cur_line)


def rename_if_exists(file_name: str, new_name: str):
    """
    Renames a file if it exists.
    """

    if os.path.exists(file_name) and not os.path.exists(new_name):
        print(f"{file_name} -> {new_name}")
        os.makedirs(os.path.dirname(new_name), exist_ok=True)
        os.rename(file_name, new_name)


def process_dir(dir_name: str, target: str):
    """
    Walk through all the items in the directory, and copy the images
    to their respective folder.
    """

    for item in os.listdir(dir_name):
        item_dir = os.path.join(dir_name, item)
        if os.path.isdir(item_dir):
            process_dir(item_dir, f"{target}/{item}")
        else:
            if item.endswith(".png"):
                print("{} -> {}".format(item_dir, target))
                os.makedirs(target, exist_ok=True)
                shutil.copy(item_dir, target)


def process_characters(dir_name: str):
    """
    Renames some files to be more consistent in the
    characters directory.
    """

    passive_pattern = r"passive(\d).png"
    constellation_pattern = r"constellation(\d).png"

    for item in os.listdir(dir_name):
        item_dir = os.path.join(dir_name, item)
        if os.path.isdir(item_dir):
            # Rename character branding
            rename_if_exists(
                f"{item_dir}/Character_{item}_Card.png", f"{item_dir}/card.png")
            rename_if_exists(f"{item_dir}/Banner.png",
                             f"{item_dir}/namecard-banner.png")
            rename_if_exists(f"{item_dir}/Bar.png",
                             f"{item_dir}/namecard-bar.png")
            rename_if_exists(f"{item_dir}/Icon.png",
                             f"{item_dir}/icon-front.png")
            rename_if_exists(f"{item_dir}/IconSide.png",
                             f"{item_dir}/icon-side.png")

            # Rename talents
            rename_if_exists(f"{item_dir}/skill.png",
                             f"{item_dir}/talent-skill.png")
            rename_if_exists(f"{item_dir}/burst.png",
                             f"{item_dir}/talent-burst.png")
            rename_if_exists(f"{item_dir}/sprint.png",
                             f"{item_dir}/talent-sprint.png")
            rename_if_exists(f"{item_dir}/passive1.png",
                             f"{item_dir}/talent-passive-1.png")
            rename_if_exists(f"{item_dir}/passive2.png",
                             f"{item_dir}/talent-passive-2.png")
            rename_if_exists(f"{item_dir}/passive3.png",
                             f"{item_dir}/talent-passive-3.png")

            # Rename non-hardcoded files based on the pattern.
            for image in os.listdir(item_dir):
                passive_match = re.search(
                    passive_pattern, image, re.IGNORECASE)
                if passive_match:
                    rename_if_exists(
                        f"{item_dir}/{image}", f"{item_dir}/passive-{passive_match.group(1)}.png")

                constellation_match = re.search(
                    constellation_pattern, image, re.IGNORECASE)
                if constellation_match:
                    rename_if_exists(
                        f"{item_dir}/{image}", f"{item_dir}/constellation-{constellation_match.group(1)}.png")


def process_weapons(dir_name: str):
    """
    Loops through the weapons directory and renames
    images to their appropriate names.
    """

    target = "weapons-fixed"
    if os.path.exists(target):
        shutil.rmtree(target)

    # Rename the weapon images
    for weapon_type in os.listdir(dir_name):
        weapon_type_dir = os.path.join(dir_name, weapon_type)
        for weapon in os.listdir(weapon_type_dir):
            weapon_dir = os.path.join(weapon_type_dir, weapon)
            if os.path.isdir(weapon_dir):
                dest_dir = os.path.join(target, weapon)
                rename_if_exists(
                    f"{weapon_dir}/Icon.png", f"{dest_dir}/icon.png")
                rename_if_exists(
                    f"{weapon_dir}/AwakenIcon.png", f"{dest_dir}/icon-ascended.png")

    # Remove the old directory
    shutil.rmtree(dir_name)
    os.rename(target, dir_name)


if __name__ == "__main__":
    # Clone the repo
    repo_dir = "genshin-optimizer"

    if os.path.exists(repo_dir):
        print("Repo already exists, pulling...")
        repo = Repo(repo_dir)
        repo.remotes.origin.pull(progress=Progress())
    else:
        print("Cloning repo...")
        Repo.clone_from("git@github.com:frzyc/genshin-optimizer.git",
                        repo_dir, progress=Progress())

    # Export the images
    target = "../images/good"
    directories = ["Artifacts", "Characters", "Weapons"]

    # Delete the target directories if they exist
    for directory in directories:
        if os.path.exists(f"{target}/{directory}"):
            print(f"Deleting {target}/{directory}")
            shutil.rmtree(f"{target}/{directory}")

    # Process the directories
    for dir_name in directories:
        process_dir(f"{repo_dir}/src/Data/{dir_name}",
                    f"{target}/{dir_name.lower()}")

    # Process directories
    process_characters(f"{target}/characters")
    process_weapons(f"{target}/weapons")
