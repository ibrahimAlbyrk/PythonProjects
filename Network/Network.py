import webbrowser
from googletrans import Translator


class Network:
    @staticmethod
    def Download(download_keyword):
        webbrowser.open(f"https://store.steampowered.com/search/?term={download_keyword}")

    @staticmethod
    def Translate(word, when_lang):
        translator = Translator()
        return translator.translate(word, dest=when_lang).text

    @staticmethod
    def youtubeSearch(search_keyword):
        webbrowser.open(f"https://www.youtube.com/results?search_query={search_keyword}")

    @staticmethod
    def netSearch(search_keyword):
        webbrowser.open(f"https://www.google.com/search?q={search_keyword}")
