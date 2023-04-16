BASE_URL = "https://imsdb.com"

M_SCRIPTS_DIR = "m_scripts"
PREP_DIR = "m_scripts_prep"
PREP_RD_DIR = "m_scripts_prep_rd"
SIMP_DIR = "m_scripts_simp"
SIMP_RD_DIR = "m_scripts_simp_rd"
DAG_DIR = "dag_atlas"
DAG_RD_DIR = "dag_atlas_rd"

# ZTZ_SIMPLIFIER = "ztz_simp_stanford"
# ZTZ_SIMPLIFIER = "ztz_simp_spacy_claucy"
# ZTZ_SIMPLIFIER = "ztz_simp_spacy1"
# ZTZ_SIMPLIFIER = "ztz_simp_spacy2"
ZTZ_SIMPLIFIER = "ztz_simp_spacy3" # best

SIMI_DEF = "similarity_nlkt" # best
# SIMI_DEF = "similarity_spacy"

ZNTZ_SEPARATOR = " (^) "
CAUSAL_MISMATCH_PENALTY = 2 / 3  # CAUSAL_MISMATCH_PENALTY >= 2/3

SPELLING_CORRECTION_RISK = 1e-7  # should be >= 1e-7)
