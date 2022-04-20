import os
import pandas as pd

from awpy import DemoParser

NOTEBOOKS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(NOTEBOOKS_DIR)
DEMOS_DIR = os.path.join(BASE_DIR, "demos")

demofile = os.path.join(DEMOS_DIR, "outsiders-vs-unique-dust2.dem")
demo_parser = DemoParser(demofile=demofile, demo_id="demos-parsed/teste_parse", parse_rate=128)

demo_parser.parse()