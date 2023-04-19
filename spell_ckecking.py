"""
https://pyspellchecker.readthedocs.io/en/latest/code.html

Spell checkers that don't take context into consideration
don't work too well. Those that do take context into
consideration are better but much slower.

This is a very conservative spell checker that doesn't know about context.

1. It doesn't change the spelling if a word starts with a capital letter.

2. if the word is plural, it only considers plural matches.

3. it assumes that the first 2 letters of all words are always correct.

4. It retains capitalization of first letter of a word.

5. It retains punctuation
"""
from my_globals import *
from spellchecker import SpellChecker
import os
import re
from WordGuesser import *
from collections import defaultdict

def has_double_letter(word):
    pattern = r'(\w)\1'
    match = re.search(pattern, word)
    if match:
        return True
    else:
        return False

def fancy_split(in_ztz):
    # match any pattern that is not a word character
    #  or a white space,
    # this is the same as a punctuation mark.
    punctuation_pattern = re.compile(r'([^\w\s])+')
    # add a whitespace before and after each punctuation mark
    in_ztz0 = punctuation_pattern.sub(r' \1 ', in_ztz)
    return in_ztz0.split()

def get_word_to_reps(in_file_path):
    # tempo dictionary words are lower case
    word_to_reps = defaultdict(lambda: 0)
    with open(in_file_path, "r") as f:
        local_word_count = 0
        for line in f:
            words = fancy_split(line)
            for word in words:
                word = word.lower()
                if word.isalpha() and len(word)>=2:
                    local_word_count += 1
                    if word in word_to_reps:
                        word_to_reps[word] +=1
                    else:
                        word_to_reps[word] = 1
            
    return word_to_reps, local_word_count

def get_corrected_sentence(in_ztz, 
                           global_checker,
                           error_type,
                           word_to_reps=None,
                           local_word_count=None):
    if word_to_reps:
        assert local_word_count

    def implies(x, y):
        return (not x) or y

    words = fancy_split(in_ztz)
    # print("dfgh", words)
    best_guesses = []
    changes = []
    for word in words:
        capitalized = word[0].isupper()
        word = word.lower()
        best_guess = word
        prob_global_for_word = global_checker.word_usage_frequency(word)
        if word.isalpha() and len(word)>=2 and\
                prob_global_for_word < SPELLING_CORRECTION_RISK\
                and not capitalized:
            word_guessers = {}
            simple_error_types = ["tt", "random"]
            if error_type in simple_error_types:
                word_guessers[error_type]=\
                    WordGuesser(word, global_checker,
                                word_to_reps, local_word_count)
            if error_type == "all":
                for err in simple_error_types:
                    word_guessers[err] = \
                        WordGuesser(word, global_checker,
                                    word_to_reps, local_word_count)
            assert word_guessers

            for guess in global_checker.edit_distance_1(word):
                cond1 = (guess[0:2] == word[0:2])
                cond2a = implies(word[-1] == "s", guess[-1] == "s")
                cond2b = implies(word[-2:] == "ed", guess[-2:] == "ed")

                if cond1 and cond2a and cond2b:
                    # this fixes tt, ss, dd, ll, errors
                    if error_type in ["tt", "all"]:
                        cond4 = (has_double_letter(guess) or has_double_letter(
                            word)) and (len(guess) != len(word)) and set(
                            guess) == set(word)
                        if cond4:
                            word_guessers['tt'].do_update(guess)
                    if error_type in ["random", "all"]:
                        word_guessers["random"].do_update(guess)
            guesser0 = None
            prob0 = -1
            for guesser in word_guessers.values():
                # print("fgyt", guesser)
                if guesser.prob_for_best_guess> prob0:
                    guesser0 = guesser
                    prob0 = guesser.prob_for_best_guess
            best_guess = guesser0.best_guess
        if capitalized:
            word = word[0].upper() + word[1:]
            best_guess = best_guess[0].upper() + best_guess[1:]
        best_guesses.append(best_guess)
        if word != best_guess:
            changes.append((word, best_guess))

    return " ".join(best_guesses), changes


def correct_this_file(in_dir,
                      out_dir,
                      file_name,
                      error_type,
                      verbose=True,
                      use_local_dict=False):
    """
    in_dir and out_dir can be the same, but this will overwrite the files
    """
    inpath = in_dir + "/" + file_name
    if out_dir:
        outpath = out_dir + "/" + file_name
    else:
        outpath = None

    global_checker = SpellChecker(distance=1)
    if use_local_dict:
        word_to_reps, local_word_count = get_word_to_reps(inpath)
    else:
        word_to_reps, local_word_count = None, None
    # print("nmjk", local_word_count, word_to_reps)

    # this didn't work. It merges TEMPO_DICT_FILE with global dict
    # instead of producing a dict solely from TEMP0_DICT_FILE
    # checker_local.word_frequency.load_dictionary("./" + TEMPO_DICT_FILE)

    if verbose:
        def print_probs(word1, word2):
            print()
            print("global probs:")
            print(word1, global_checker.word_usage_frequency(word1))
            print(word2, global_checker.word_usage_frequency(word2))
            print("local_probs:")
            if word_to_reps:
                print(word1, word_to_reps[word1])
                print(word2, word_to_reps[word2])
            else:
                print("N/A")
            print()

        print_probs("beautifull", "beautiful")
        print_probs("tomatos", "tomatoes")
        print_probs("mitty", "misty")

    corrected_lines = []
    all_changes = []
    with open(inpath, "r") as f:
        for line in f:
            corr_line, changes = get_corrected_sentence(
                line, global_checker, error_type,
                word_to_reps, local_word_count)
            corrected_lines.append(corr_line)
            all_changes += changes
            if verbose:
                print(line.strip())
                print(corr_line)
                print()
        print("all changes:", all_changes)

    if outpath:
        with open(outpath, "w") as f:
            for corr_line in corrected_lines:
                f.write(corr_line + "\n")

def correct_this_batch_of_files(in_dir,
                                out_dir,
                                batch_file_names,
                                error_type,
                                verbose=True,
                                use_local_dict=False):
    all_file_names = os.listdir(in_dir)
    assert set(batch_file_names).issubset(set(all_file_names))
    for file_name in batch_file_names:
        i = all_file_names.index(file_name)
        print('%i.' % (i + 1), file_name)
        correct_this_file(in_dir, out_dir, file_name,
                          error_type,
                          verbose,
                          use_local_dict)

if __name__ == "__main__":
    def main1(use_local_dict, error_type):
        print("**************************")
        print("use_local_dict=", use_local_dict)
        print("error_type=", error_type)
        print("SPELLING_CORRECTION_RISK=", SPELLING_CORRECTION_RISK)
        print()

        in_dir = "."
        out_dir = "" # if empty out_dir, won't write to a file
        file_name = "spell_checking_test.txt"

        correct_this_file(in_dir,
                        out_dir,
                        file_name,
                        error_type,
                        verbose=True,
                        use_local_dict=use_local_dict)


    def main2(use_local_dict, error_type):
        print("**************************")
        print("use_local_dict=", use_local_dict)
        print("error_type=", error_type)
        print("SPELLING_CORRECTION_RISK=", SPELLING_CORRECTION_RISK)
        print()

        in_dir = "short_stories_clean"
        out_dir = "short_stories_spell"
        batch_file_names = os.listdir(in_dir)
        correct_this_batch_of_files(in_dir,
                                    out_dir,
                                    batch_file_names,
                                    error_type= error_type,
                                    verbose=False,
                                    use_local_dict=use_local_dict)

    def main3(use_local_dict, error_type):
        print("**************************")
        print("use_local_dict=", use_local_dict)
        print("error_type=", error_type)
        print("SPELLING_CORRECTION_RISK=", SPELLING_CORRECTION_RISK)
        print()

        remove_dialogs = False
        in_dir = CLEAN_DIR if not remove_dialogs else CLEAN_RD_DIR
        out_dir = SPELL_DIR if not remove_dialogs else SPELL_RD_DIR
        batch_file_names = os.listdir(in_dir)[0:3]
        correct_this_batch_of_files(in_dir,
                                    out_dir,
                                    batch_file_names,
                                    error_type= error_type,
                                    verbose=False,
                                    use_local_dict=use_local_dict)


    # main1(use_local_dict=True, error_type="all")
    # main2(use_local_dict=True, error_type="all")
    main3(use_local_dict=True, error_type="all")
