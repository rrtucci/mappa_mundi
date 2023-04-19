BASE_URL = "https://imsdb.com"

M_SCRIPTS_DIR = "m_scripts"
CLEAN_DIR = "m_scripts_clean"
CLEAN_RD_DIR = "m_scripts_clean_rd"
SIMP_DIR = "m_scripts_simp"
SIMP_RD_DIR = "m_scripts_simp_rd"
DAG_DIR = "dag_atlas"
DAG_RD_DIR = "dag_atlas_rd"

# ZTZ_SIMPLIFIER = "simp_stanford"
# ZTZ_SIMPLIFIER = "simp_spacy_claucy"
# ZTZ_SIMPLIFIER = "simp_spacy1"
# ZTZ_SIMPLIFIER = "simp_spacy2"
ZTZ_SIMPLIFIER = "simp_spacy3" # recommended

# SIMI_DEF = "similarity_spacy"
SIMI_DEF = "similarity_nltk" # recommended


ZTZ_SEPARATOR = "*"

CAUSAL_MISMATCH_PENALTY = 2 / 3  # CAUSAL_MISMATCH_PENALTY >= 2/3

# good good results with:
# 1e-7 for error_type=random
# 1e-6 for error_type=tt
SPELLING_CORRECTION_RISK = 1e-6

# pos (part of speech) in stopwords.py
# ['ADJ', 'ADP', 'ADV', 'AUX', 'CCONJ', 'DET', 'INTJ',
# 'NOUN', 'NUM', 'PART', 'PRON', 'PUNCT', 'SCONJ', 'VERB']

# To see full list, see jpg in pics folder

# ADP (adposition) are mostly prepositions
# AUX contains verbs like 'is'
# DET (determiner) contains 'whose'
# NUM contains number words like 'three'
# PART (particle) contains 'not'

RETAINED_POS = ['ADJ', 'ADV', 'NOUN', 'VERB']

# See stopwords.py
# should be subset of RETAINED_POS
# RETAINED_STOPWORD_POS = RETAINED_POS
RETAINED_STOPWORD_POS = [] # recommended