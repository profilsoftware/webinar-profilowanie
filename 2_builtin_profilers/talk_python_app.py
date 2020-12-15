import os
import re
import subprocess
import tempfile

from bs4 import BeautifulSoup
import requests

NUMBER_OF_PACKAGES = 100
CLONE_URL = "https://gitlab.com/mateusz_b/talk-python-to-me-transcripts.git"
# CLONE_URL = "https://github.com/mikeckennedy/talk-python-transcripts.git"

class Episode:
    base_url = "https://talkpython.fm"

    def __init__(self, data):
        self.tds = data.find_all("td")
        self.package_mentioned = []

    @property
    def episode_number(self):
        td = self.tds[0]
        return td.text.replace("#", "")

    @property
    def release_date(self):
        td = self.tds[1]
        return td.text

    @property
    def link(self):
        link = self.tds[2].findChild()
        return link

    @property
    def full_url(self):
        return self.base_url + self.link.get("href")

    @property
    def name(self):
        return self.link.text

    @property
    def guest(self):
        td = self.tds[3]
        guest = td.text
        return f"with {guest}"


def get_all_episodes():
    resp = requests.get("https://talkpython.fm/episodes/all")
    soup = BeautifulSoup(resp.text, "html.parser")
    episodes = soup.find_all("tr")
    episodes_objects = []
    # first one is a header with explanation
    for s in episodes[1:]:
        show = Episode(s)
        episodes_objects.append(show)
    episodes_objects.reverse()
    return episodes_objects


def clone_transcript_files():
    path = tempfile.mkdtemp(prefix="talk_python_transcripts_")
    resp_code = subprocess.call(['git', 'clone', CLONE_URL, path])
    if resp_code != 0:
        raise Exception("Couldn't clone the repository")
    return path


def get_top_packages():
    packages = {}
    resp = requests.get("https://hugovk.github.io/top-pypi-packages/top-pypi-packages-365-days.json")
    for pack in resp.json()['rows'][:NUMBER_OF_PACKAGES]:
        packages[pack['project']] = 0
    return packages


def read_file(path):
    with open(path) as f:
        transcript = f.read()
    return transcript


def find_package_mention(pack, transcript):
    pattern = re.compile(rf"\b{pack}\b", re.IGNORECASE)
    if re.search(pattern, transcript):
        return 1
    return 0


def extract_episode_number_from_title(title):
    numbers = re.findall(r'\d+', title)
    return int(numbers[0])


def display_progress(current, total):
    print(f"{100 * current / total:.2f}%")


def find_all_packages_mentions(packages, transcripts_path, episodes):
    num = 0
    for pack in packages:
        display_progress(num, len(packages))
        num += 1
        for i in os.listdir(transcripts_path):
            path = os.path.join(transcripts_path, i)
            transcript = read_file(path)
            mention = find_package_mention(pack, transcript)
            packages[pack] += mention
            if mention:
                episode_number = extract_episode_number_from_title(i)
                episodes[episode_number].package_mentioned.append(pack)


def summarize_packages_mentioned(episodes):
    for show in episodes:
        print(f"{show.episode_number}: {show.name} -> {show.package_mentioned}")
        print("-------")


def main():
    episodes = get_all_episodes()
    packages = get_top_packages()
    path = clone_transcript_files()
    transcripts_path = os.path.join(path, "transcripts")
    find_all_packages_mentions(packages, transcripts_path, episodes)
    summarize_packages_mentioned(episodes)


if __name__ == '__main__':
    main()
