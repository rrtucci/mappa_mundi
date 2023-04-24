from downloading_imsdb import *
from cleaning import *
from spell_checking import *
import importlib as imp
zsimp = imp.import_module(ZTZ_SIMPLIFIER)
from DagAtlas import *
from utils import *

remove_dialog = True
num_movies = 2

all_steps = [
"downloading",
"cleaning",
"spelling",
"simplifying",
"cartography"
]
steps_to_perform= all_steps
assert set(steps_to_perform).issubset(set(all_steps))

# downloading_imsdb
if "downloading" in steps_to_perform:
    d1_urls, titles = get_d1_urls_and_titles()
    get_batch_of_m_scripts(d1_urls, titles,
                           first=1, last=2000, stub_only=False)

# cleaning
if "cleaning" in steps_to_perform:
    clean_batch_of_m_scripts(
        in_dir = M_SCRIPTS_DIR,
        out_dir = CLEAN_DIR if not remove_dialog else CLEAN_RD_DIR,
        batch_file_names=my_listdir(M_SCRIPTS_DIR)[0:num_movies],
        remove_dialog=remove_dialog)

# spell-checking
if "spelling" in steps_to_perform:

# ztz_simplification
if "simplifying" in steps_to_perform:
    simplify_batch_of_m_scripts(
        in_dir=CLEAN_DIR if not remove_dialog else CLEAN_RD_DIR,
        out_dir=SIMP_DIR if not remove_dialog else SIMP_RD_DIR,
        batch_file_names=my_listdir(M_SCRIPTS_DIR)[0:num_movies])

# cartography
if "cartography" in steps_to_perform:
    atlas = DagAtlas(
        txt_dir=SIMP_DIR if not remove_dialog else SIMP_RD_DIR,
        dag_dir=DAG_DIR)
    all_titles = [file_name[:-len(".txt")] \
                  for file_name in my_listdir(M_SCRIPTS_DIR)]
    atlas.update_arrows_in_batch_of_m_scripts(batch_titles=\
        all_titles[0:num_movies])

# greetings
print_welcome_message()