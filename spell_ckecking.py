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
    word_to_reps = {}
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

def get_corrected_sentence(in_ztz, checker_global, 
                           word_to_reps=None,
                           local_word_count=None):
    if word_to_reps:
        assert local_word_count

    def implies(x, y):
        return (not x) or y

    words = fancy_split(in_ztz)
    # print("dfgh", words)
    corrected_words = []
    changes = []
    for word in words:
        capitalized = word[0].isupper()
        word = word.lower()
        p_global = checker_global.word_usage_frequency(word)
        if word_to_reps:
            if word in word_to_reps:
                p_local = word_to_reps[word]/local_word_count
            else:
                p_local = 0
        else:
            p_local = 0

        if not word_to_reps:
            if p_global < SPELLING_CORRECTION_RISK:  # very high
                # prob that it's wrong
                best_dict = "global"
                # if word == "beautifull":
                #     print("erft", p_global)
                #     print("cvbft", checker_global.word_usage_frequency(
                #         "beautiful"))
            else:
                best_dict = None
        else:
            if p_global < SPELLING_CORRECTION_RISK: # rare globally
                if word in word_to_reps and word_to_reps[word]==1: # rare
                    # locally too
                    best_dict = "local"
                else:
                    best_dict = "global"
            else:
                best_dict = None

        guess_best, p_guess_best = word, 0
            
        if word.isalpha() and len(word)>=2:
            for guess in checker_global.edit_distance_1(word):
                cond1 = (guess[0:2] == word[0:2])
                cond2a = implies(word[-1] == "s", guess[-1] == "s")
                cond2b = implies(word[-2:] == "ed", guess[-2:] == "ed")

                if cond1 and cond2a and cond2b:
                    # this fixes tt, ss, dd, ll, errors
                    if best_dict == "global":
                        cond4 = (has_double_letter(guess) or has_double_letter(
                            word)) and (len(guess) != len(word)) and set(
                            guess) == set(word)
                        if cond4:
                            # print(".......global")
                            p_guess = checker_global.word_usage_frequency(
                                 guess.lower())
                            if p_guess > p_guess_best:
                                guess_best, p_guess_best = guess, p_guess
                                use_local_dict = False

                    elif best_dict == "local" and guess in word_to_reps:
                        # this fixes typos
                       #  print("uuio-------local")
                        p_guess = word_to_reps[guess]/local_word_count
                        # print("gghj", guess, p_guess_local, p_guess_best)
                        if p_guess > p_guess_best:
                            guess_best, p_guess_best = guess, p_guess
        if capitalized:
            guess_best = guess_best[0].upper() + guess_best[1:]
            word = word[0].upper() + word[1:]

        corrected_words.append(guess_best)
        if word != guess_best:
            changes.append((word, guess_best))

    return " ".join(corrected_words), changes


def correct_this_file(in_dir,
                      out_dir,
                      file_name,
                      verbose=True,
                      use_local_dict=False):
    """
    in_dir and out_dir can be the same, but this will overwrite the files
    """
    inpath = in_dir + "/" + file_name
    outpath = out_dir + "/" + file_name

    checker_global = SpellChecker(distance=1)
    if use_local_dict:
        word_to_reps, local_word_count = get_word_to_reps(inpath)
    else:
        word_to_reps, local_word_count = None, None
    # print("nmjk", local_word_count, word_to_reps)

    # this didn't work. It merges TEMPO_DICT_FILE with global dict
    # instead of producing a dict solely from TEMP0_DICT_FILE
    # checker_local.word_frequency.load_dictionary("./" + TEMPO_DICT_FILE)

    corrected_lines = []
    all_changes = []
    with open(inpath, "r") as f:
        for line in f:
            corr_line, changes = get_corrected_sentence(
                line, checker_global, word_to_reps,
                    local_word_count)
            corrected_lines.append(corr_line)
            all_changes += changes
            if verbose:
                print(line.strip())
                print(corr_line)
                print()
        print("all changes:", all_changes)

    with open(outpath, "w") as f:
        for corr_line in corrected_lines:
            f.write(corr_line + "\n")

def correct_this_batch_of_files(in_dir,
                                out_dir,
                                batch_file_names,
                                verbose=True,
                                use_local_dict=False):
    all_file_names = os.listdir(in_dir)
    assert set(batch_file_names).issubset(set(all_file_names))
    for file_name in batch_file_names:
        i = all_file_names.index(file_name)
        print('%i.' % (i + 1))
        correct_this_file(in_dir, out_dir, file_name, verbose,
                          use_local_dict)

if __name__ == "__main__":
    def main1(use_local_dict):
        in_dir = "spell_checking_in_dir"
        out_dir = "spell_checking_out_dir"
        batch_file_names = os.listdir(in_dir)
        correct_this_batch_of_files(in_dir,
                                    out_dir,
                                    batch_file_names,
                                    verbose=True,
                                    use_local_dict=use_local_dict)

    def main2(use_local_dict):
        in_dir = "short_stories_clean"
        out_dir = "spell_checking_out_dir"
        batch_file_names = os.listdir(in_dir)
        correct_this_batch_of_files(in_dir,
                                    out_dir,
                                    batch_file_names,
                                    verbose=False,
                                    use_local_dict=use_local_dict)


    main1(use_local_dict=False)
    main2(use_local_dict=False)


