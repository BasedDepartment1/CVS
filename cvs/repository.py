import os
import shutil


class Repository:

    worktree: str
    cvs_dir: str

    def __init__(self, path, force=False):
        Repository.worktree = path
        Repository.cvs_dir = os.path.join(path, ".cvs")

        if not (force or os.path.isdir(Repository.cvs_dir)):
            raise Exception(f"Not a repository: {path}")


def get_rep_path(repo, *path):
    return os.path.join(repo.cvs_dir, *path)


def get_relative_file_path(repo, *path, mkdir=False):
    if get_relative_dir_path(repo, *path[:-1], mkdir=mkdir):
        return get_rep_path(repo, *path)


def get_relative_dir_path(repo, *path, mkdir=False):

    path = get_rep_path(repo, *path)

    if os.path.exists(path):
        if os.path.isdir(path):
            return path
        else:
            raise Exception(f"Not a directory {path}")

    if mkdir:
        os.makedirs(path)
        return path
    else:
        return None


def make_directory_image(cur_path: str, path: str):
    ignore_rep = shutil.ignore_patterns(".cvs")
    shutil.copytree(cur_path, path, ignore=ignore_rep)


def init(path):
    """Create a new repository at path."""

    repo = Repository(path, force=True)

    if os.path.exists(repo.worktree):
        if not os.path.isdir(repo.worktree):
            raise Exception(f"{path} is not a directory!")
        if os.listdir(repo.worktree):
            raise Exception(f"{path} is not empty!")
    else:
        os.makedirs(repo.worktree)

    assert get_relative_dir_path(repo, "branches", mkdir=True)
    assert get_relative_dir_path(repo, "objects", mkdir=True)
    assert get_relative_dir_path(repo, "refs", mkdir=True)
    assert get_relative_dir_path(repo, "refs", "heads", mkdir=True)

    make_directory_image(repo.worktree, os.path.join(repo.cvs_dir, "initial"))
    make_directory_image(repo.worktree, os.path.join(repo.cvs_dir, "index"))

    with open(get_relative_file_path(repo, "HEAD"), "w") as f:
        f.write("ref: refs/heads/master\n")

    return repo
