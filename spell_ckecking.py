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

from spellchecker import SpellChecker
import os
import re

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
    with open(in_file_path, "r", encoding="utf-8") as f:
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
                           words_to_reps,
                           local_word_count):

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
        guess_local0 , p_guess_local0 = word, p_global
        guess_global0, p_guess_global0 = word, p_global
        use_local_guess = True
        if p_global < 1e-5 and word.isalpha() and len(word)>=2:
            for guess in checker_global.edit_distance_1(word):
                cond1 = (guess[0:2] == word[0:2])
                guess_plural = (guess[-1] == "s")
                cond2a = implies(word[-1] == "s", guess[-1] == "s")
                cond2b = implies(word[-2:] == "ed", guess[-2:] == "ed")
                cond3 = (has_double_letter(guess) or has_double_letter(word)) \
                         and (len(guess)!=len(word)) and set(guess)==set(word)
                # this fixes tt, ss, dd, ll, errors
                if cond1 and cond2a and cond2b and cond3:
                    p_guess_global = checker_global.word_usage_frequency(
                         guess.lower())
                    if p_guess_global > p_guess_global0:
                        guess_global0, p_guess_global0 = guess, p_guess_global
                        use_local_guess = False
                # this fixes typos
                # if cond1 and cond2a and cond2b and use_local_guess and \
                #         words_to_reps:
                #     if guess in words_to_reps:
                #         p_guess_local = \
                #             words_to_reps[guess]/local_word_count
                #     else:
                #         p_guess_local = 0
                #     # print("gghj", guess, p_guess_local, p_guess_local0)
                #     if p_guess_local > p_guess_local0:
                #         guess_local0, p_guess_local0 = guess, p_guess_local
                
        if use_local_guess:
            fin_guess = guess_local0
        else:
            fin_guess = guess_global0
        if capitalized:
            fin_guess = fin_guess[0].upper() + fin_guess[1:]
            word = word[0].upper() + word[1:]

        corrected_words.append(fin_guess)
        if word != fin_guess:
            changes.append((word, fin_guess))

    return " ".join(corrected_words), changes


def correct_this_file(in_dir,
                      out_dir,
                      file_name,
                      verbose=True):
    """
    in_dir and out_dir can be the same, but this will overwrite the files
    """
    inpath = in_dir + "/" + file_name
    outpath = out_dir + "/" + file_name

    checker_global = SpellChecker(distance=1)
    word_to_reps, local_word_count = get_word_to_reps(inpath)
    # print("nmjk", local_word_count, word_to_reps)

    # this didn't work. It merges TEMPO_DICT_FILE with global dict
    # instead of producing a dict solely from TEMP0_DICT_FILE
    # checker_local.word_frequency.load_dictionary("./" + TEMPO_DICT_FILE)

    corrected_lines = []
    all_changes = []
    with open(inpath, "r", encoding="utf-8") as f:
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

    with open(outpath, "w", encoding="utf-8") as f:
        for corr_line in corrected_lines:
            f.write(corr_line + "\n")

def correct_this_batch_of_files(in_dir,
                                out_dir,
                                batch_file_names,
                                verbose=True):
    all_file_names = os.listdir(in_dir)
    assert set(batch_file_names).issubset(set(all_file_names))
    for file_name in batch_file_names:
        i = all_file_names.index(file_name)
        print('%i.' % (i + 1))
        correct_this_file(in_dir, out_dir, file_name, verbose)

if __name__ == "__main__":
    def main1():
        in_dir = "spell_checking_in_dir"
        out_dir = "spell_checking_out_dir"
        batch_file_names = os.listdir(in_dir)
        correct_this_batch_of_files(in_dir,
                                    out_dir,
                                    batch_file_names,
                                    verbose=True)

    def main2():
        in_dir = "short_stories_prep"
        out_dir = "spell_checking_out_dir"
        batch_file_names = os.listdir(in_dir)
        correct_this_batch_of_files(in_dir,
                                    out_dir,
                                    batch_file_names,
                                    verbose=False)


    # main1()
    main2()


