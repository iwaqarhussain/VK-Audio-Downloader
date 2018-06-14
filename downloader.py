from shutil import copyfileobj, rmtree
from os import getcwd, path, listdir, makedirs
from requests import Session
import zipfile


class Downloader:
    def __init__(self):
        self.session = Session()

        if not path.exists(path.join(getcwd(), "audios")):
            makedirs(path.join(getcwd(), "audios"), exist_ok=True)

    def download(self, queue):
        ( url, name ) = queue
        dest = path.join(getcwd(), "audios", name)
        print("\n[00000] Downloading {0} -> {1}\n".format(url, dest))

        response = self.session.get(url, stream=True)
        with open(dest, "wb") as file:
            copyfileobj(response.raw, file)

    def zip_contents(self):
        zip_list = []
        chunks = []

        for entry in listdir(path.join(getcwd(), "audios")):
            if path.isfile(path.join(getcwd(), "audios", entry)):
                zip_list.append(entry)

        for item in range(0, len(zip_list), 1000):
            chunks.append(zip_list[item:item + 1000])

        for index, chunk in enumerate(chunks):
            with zipfile.ZipFile("Audios" + '-' + str(index) + '.zip', 'w', zipfile.ZIP_DEFLATED) as zip:
                for file in chunk:
                    zip.write(path.join(getcwd(), "audios", file), file)

    def cleanup(self):
        self.zip_contents()
        rmtree(path.join(getcwd(), "audios"))
