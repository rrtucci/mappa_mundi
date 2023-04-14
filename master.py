from downloading_imsdb import *
from preprocessing_m_scripts import *
from ztz_simplification_stanford import *
from DagAtlas import *

remove_dialog = True
num_movies = 2

# downloading_imsdb
d1_urls, titles = get_d1_urls_and_titles()
get_batch_of_m_scripts(d1_urls, titles,
                       first=1, last=2000, stub_only=False)

# preprocessing_m_scripts
preprocess_batch_of_m_scripts(
    in_dir = M_SCRIPTS_DIR,
    out_dir = PREP_DIR if not remove_dialog else PREP_RD_DIR,
    batch_file_names=os.listdir(M_SCRIPTS_DIR)[0:num_movies],
    remove_dialog=remove_dialog)

# ztz_simplification
simplify_batch_of_m_scripts(
    in_dir=PREP_DIR if not remove_dialog else PREP_RD_DIR,
    out_dir=SIMP_DIR if not remove_dialog else SIMP_RD_DIR,
    batch_file_names=os.listdir(M_SCRIPTS_DIR)[0:num_movies])

# DagAtlas
atlas = DagAtlas(
    txt_dir=SIMP_DIR if not remove_dialog else SIMP_RD_DIR,
    dag_dir=DAG_DIR,
    simi_threshold=SIMI_THRESHOLD)
all_titles = [file_name[:-len(".txt")] \
              for file_name in os.listdir(M_SCRIPTS_DIR)]
atlas.update_arrows_in_batch_of_m_scripts(batch_titles=\
    all_titles[0:num_movies])

