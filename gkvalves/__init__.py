import os
import subprocess

from .valves import Location
from .valves import Valve
from .valves import Valves


_VERSION = "1.0.2"
_GKVALVES_PKG_DIR = os.path.dirname(__file__)


def _version() -> str:
    version = _VERSION
    if not os.path.isdir(os.path.join(os.path.dirname(_GKVALVES_PKG_DIR), ".git")):
        # Not in git directory
        return version

    try:
        git_describe = subprocess.Popen(
            ["git", "describe", "--tags", "--long"],
            cwd=_GKVALVES_PKG_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        out, err = git_describe.communicate()
        if git_describe.returncode == 0:
            _, tag_dist_str, commit = out.decode().strip().rsplit("-", 2)
            commit = commit.lstrip("g")[:7]
            tag_dist = int(tag_dist_str)
        else:
            raise subprocess.CalledProcessError(git_describe.returncode, err)
    except Exception:
        pass
    else:
        if tag_dist > 0:
            version += f" (+{tag_dist}, commit {commit})"

    return version


VERSION = __version__ = _version()
__all__ = ["Location", "Valve", "Valves", "VERSION"]


if __name__ == "__main__":
    print(VERSION)
