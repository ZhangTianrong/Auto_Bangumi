import re
import logging
from os import path


logger = logging.getLogger(__name__)


class DownloadParser:
    def __init__(self):
        self.rules = [
            r"(.*)\[(\d{1,3}|\d{1,3}\.\d{1,2})(?:v\d{1,2})?(?:END)?\](.*)",
            r"(.*)\[E(\d{1,3}|\d{1,3}\.\d{1,2})(?:v\d{1,2})?(?:END)?\](.*)",
            r"(.*)\[第(\d*\.*\d*)话(?:END)?\](.*)",
            r"(.*)\[第(\d*\.*\d*)話(?:END)?\](.*)",
            r"(.*)第(\d*\.*\d*)话(?:END)?(.*)",
            r"(.*)第(\d*\.*\d*)話(?:END)?(.*)",
            r"(.*)- (\d{1,3}|\d{1,3}\.\d{1,2})(?:v\d{1,2})?(?:END)?(.*)",
        ]

    def rename_normal(self, name, season):
        for rule in self.rules:
            match_obj = re.match(rule, name, re.I)
            if match_obj is not None:
                title = re.sub(r"([Ss]|Season )\d{1,3}", "", match_obj.group(1)).strip()
                new_name = f"{title} S{season}E{match_obj.group(2)}{match_obj.group(3)}"
                return new_name

    def rename_pn(self, name, season):
        n = re.split(r"[\[\]()【】（）]", name)
        file_name = name.replace(f"[{n[1]}]", "")
        if season < 10:
            season = f"0{season}"
        for rule in self.rules:
            match_obj = re.match(rule, file_name, re.I)
            if match_obj is not None:
                title = re.sub(r"([Ss]|Season )\d{1,3}", "", match_obj.group(1)).strip()
                new_name = re.sub(
                    r"[\[\]]",
                    "",
                    f"{title} S{season}E{match_obj.group(2)}{path.splitext(name)[-1]}",
                )
                return new_name

    def rename_advance(self, name, folder_name, season):
        n = re.split(r"[\[\]()【】（）]", name)
        file_name = name.replace(f"[{n[1]}]", "")
        if season < 10:
            season = f"0{season}"
        for rule in self.rules:
            match_obj = re.match(rule, file_name, re.I)
            if match_obj is not None:
                new_name = re.sub(
                    r"[\[\]]",
                    "",
                    f"{folder_name} S{season}E{match_obj.group(2)}{path.splitext(name)[-1]}",
                )
                return new_name

    def download_rename(self, name, folder_name, season, method):
        if method.lower() == "pn":
            return self.rename_pn(name, season)
        elif method.lower() == "normal":
            return self.rename_normal(name, season)
        elif method.lower() == "none":
            return name
        elif method.lower() == "advance":
            return self.rename_advance(name, folder_name, season)


if __name__ == "__main__":
    name = "[NC-Raws]Summer Time Rendering S02 - 09(B-Global 3840x2160 HEVC AAC MKV).mkv"
    rename = DownloadParser()
    new_name = rename.rename_pn(name, 1)
    print(new_name)