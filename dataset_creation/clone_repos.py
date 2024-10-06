# coding=utf-8

import os
import subprocess
from multiprocessing import Pool
from github import Github

ICON_REPOS = [
    "lucide-icons/lucide"                               # ISC
]
UI_REPOS = [
    "shadcn-ui/ui",                                     # MIT
    "DarkInventor/easy-ui"                              # MIT
]
CODE_REPOS = [
    "moinulmoin/chadnext",                              # MIT
    "shadcn-ui/taxonomy",                               # MIT
    "horizon-ui/shadcn-nextjs-boilerplate",             # MIT
    "alifarooq9/rapidlaunch",                           # MIT
    "ixartz/SaaS-Boilerplate",                          # MIT
    "nobruf/shadcn-landing-page"                        # None
]

REPOS_TO_MIRROR = ICON_REPOS + UI_REPOS + CODE_REPOS
MIRROR_DIRECTORY = "synth_source_repos"

def get_repos(username, access_token=None, include_fork=False):
    """Fetches repositories for a particular GitHub user.

    Courtesy: Chansung Park.
    """
    g = Github(access_token)
    user = g.get_user(username)

    results = []
    for repo in user.get_repos():
        if repo.fork is False:
            results.append((repo.name, repo.stargazers_count))
        else:
            if include_fork is True:
                results.append((repo.name, repo.stargazers_count))
    print(results)
    return results


def sort_repos_by_stars(repos):
    return sorted(repos, key=lambda x: x[1], reverse=True)


def mirror_repository(repository):
    """Locally clones a repository."""
    repository_url = f"https://github.com/{repository}.git"
    repository_path = os.path.join(MIRROR_DIRECTORY, repository)

    subprocess.run(["git", "clone", repository_url, repository_path])

def mirror_repositories():
    if not os.path.exists(MIRROR_DIRECTORY):
        os.makedirs(MIRROR_DIRECTORY)

    print("Cloning repositories.")
    with Pool() as pool:
        pool.map(mirror_repository, REPOS_TO_MIRROR)


if __name__ == "__main__":
    mirror_repositories()
