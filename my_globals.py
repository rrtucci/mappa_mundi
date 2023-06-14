"""

This file contains all the global variables used by Mappa Mundi (MM).

"""

BASE_URL = "https://imsdb.com"

M_SCRIPTS_DIR = "m_scripts"
CLEAN_DIR = "m_scripts_clean"
CLEAN_RD_DIR = "m_scripts_clean_rd"
SPELL_DIR = "m_scripts_spell"
SPELL_RD_DIR = "m_scripts_spell_rd"
SIMP_DIR = "m_scripts_simp"
SIMP_RD_DIR = "m_scripts_simp_rd"
DAG_DIR = "m_script_dag_atlas"
DAG_RD_DIR = "m_script_dag_atlas_rd"

# ZTZ_SIMPLIFIER = "simp_stanford"
# ZTZ_SIMPLIFIER = "simp_spacy_claucy"
# ZTZ_SIMPLIFIER = "simp_spacy1"
# ZTZ_SIMPLIFIER = "simp_spacy2"
# ZTZ_SIMPLIFIER = "simp_spacy3" # originally recommended
ZTZ_SIMPLIFIER = "simp_openie6"  # recommended

# SIMI_DEF = "similarity_spacy"
# SIMI_DEF = "similarity_spacy2"
# SIMI_DEF = "similarity_nltk" # originally recommended
SIMI_DEF = "similarity_bert"  # recommended

# good threshold values gleaned from similarity.py examples
# SIMI_THRESHOLD = 2.2 for NLTK
# SIMI_THRESHOLD = 2.69 for SpaCy
SIMI_THRESHOLD = 2.5  # for bert, recommended

ZTZ_SEPARATOR = "*"

CAUSAL_MISMATCH_PENALTY = 2 / 3  # CAUSAL_MISMATCH_PENALTY >= 2/3

SPELLING_CORRECTION_RISK = 1e-8

# POS (part of speech) in stopwords.py
# ['ADJ', 'ADP', 'ADV', 'AUX', 'CCONJ', 'DET', 'INTJ',
# 'NOUN', 'NUM', 'PART', 'PRON', 'PUNCT', 'SCONJ', 'VERB']

# To see full list of POS, see jpg in pics folder

# ADP (adposition) are mostly prepositions
# AUX contains verbs like 'is'
# DET (determiner) contains 'whose'
# NUM contains number words like 'three'
# PART (particle) contains 'not'

RETAINED_POS = ['ADJ', 'ADV', 'NOUN', 'VERB']

# See stopwords.py
# RETAINED_STOPWORD_POS should be subset of RETAINED_POS
# RETAINED_STOPWORD_POS = RETAINED_POS
RETAINED_STOPWORD_POS = []  # recommended

USE_GPU = True