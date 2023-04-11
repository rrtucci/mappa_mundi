from downloading_imsdb import *
from preprocessing_m_scripts import *
from ztnz_simplification import *
from DagAtlas import *

remove_dialog = True

# downloading_imsdb
d1_urls, titles = get_d1_urls_and_titles()
get_batch_of_m_scripts(d1_urls, titles,
                       first=1, last=10, stub_only=False)

# preprocessing_m_scripts
preprocess_batch_of_m_scripts(
    in_dir = M_SCRIPTS_DIR,
    out_dir = PREP_DIR if not remove_dialog else PREP_RD_DIR,
    file_names=os.listdir(M_SCRIPTS_DIR)[0:2],
    remove_dialog=remove_dialog)

# zntz_simplification
simplify_batch_of_m_scripts(
    in_dir=PREP_DIR if not remove_dialog else PREP_RD_DIR,
    out_dir=SIMP_DIR if not remove_dialog else SIMP_RD_DIR,
    file_names=os.listdir(M_SCRIPTS_DIR)[0:2])

# DagAtlas
atlas = DagAtlas(
    txt_dir=SIMP_DIR if not remove_dialog else SIMP_RD_DIR,
    dag_dir=DAG_DIR,
    simi_threshold=SIMI_THRESHOLD)
all_titles = [file_name[:-len(".txt")] \
              for file_name in os.listdir(M_SCRIPTS_DIR)]
atlas.update_arrows_in_batch_of_m_scripts(titles_list=all_titles[0:2])

