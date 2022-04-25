import os

from awpy import DemoParser

CORE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.dirname(CORE_DIR)
BASE_DIR = os.path.dirname(SRC_DIR)
DEMOS_DIR = os.path.join(BASE_DIR, "demos")
DEMOS_COMPRESSED_DIR = os.path.join(BASE_DIR, "demos-compressed")
DEMOS_PARSED_DIR = os.path.join(BASE_DIR, "demos-parsed")

class DemoPipeline():
    def __init__(self, demo_id=None, description=None, match_id=None, rate=128) -> None:
        self.demo_id = str(demo_id)
        self.url = f'https://www.hltv.org/download/demo/{self.demo_id}'
        self.description = description
        self.match_id = str(match_id)
        self.rate = 128

    def create_dir(self, dir_name=None):
        try:
            os.mkdir(dir_name)
            print("Directory " , dir_name ,  " Created ") 
        except FileExistsError:
            print("Directory " , dir_name ,  " already exists")
        return None

    def prepare(self):
        list_dir = ['database','demos','demos-compressed','demos-parsed']
        for dir_name in list_dir:
            self.create_dir(dir_name=dir_name)
        return None

    def download(self):
        demo_file = os.path.join(DEMOS_COMPRESSED_DIR, str(self.match_id))
        os.system(f'wget -O {demo_file}.rar {self.url}')
        return None

    def extract(self):
        demo_file = os.path.join(DEMOS_COMPRESSED_DIR, str(self.match_id))
        os.system(f'unrar x {demo_file}.rar {DEMOS_DIR}')
        return None

    def parse(self):
        list_demos = os.listdir(DEMOS_DIR)
        index = 1
        for demo in list_demos:    
            demofile = os.path.join(DEMOS_DIR, demo)
            json_file = 'demos-parsed/' + str(self.demo_id) + f'_{index}'
            demo_parser = DemoParser(demofile=demofile, demo_id=json_file, parse_rate=self.rate)
            demo_parser.parse()
            index += 1

    def clear_demos(self):
        demo_file = os.path.join(DEMOS_COMPRESSED_DIR, str(self.match_id))
        os.remove(f'{demo_file}.rar')

        list_demos = os.listdir(DEMOS_DIR)
        for demo in list_demos:
            demo_path = os.path.join(DEMOS_DIR,demo)
            os.remove(demo_path)

    def start(self):
        self.prepare()
        self.download()
        self.extract()
        self.parse()
        self.clear_demos()
        return None