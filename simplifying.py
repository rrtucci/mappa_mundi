from my_globals import *
import os
import re
import importlib as imp
zsimp = imp.import_module(ZTZ_SIMPLIFIER)


def simplify_one_m_script(
    in_dir, out_dir,
    file_name,
    verbose=False):
    """
    in_dir and out_dir can be the same, but this will overwrite the files
    """
    inpath = in_dir + "/" + file_name
    outpath = out_dir + "/" + file_name
    new_lines = []
    with open(inpath, "r") as f:
        count = 1
        for line in f:
            if verbose:
                print(str(count) + ".")
            simple_ztz_list = zsimp.simplify_ztz(line, verbose)

            # remove empty clauses
            simple_ztz_list = [ztz for ztz in simple_ztz_list if ztz]

            if simple_ztz_list == []:
                simple_ztz_list = [ZTZ_SEPARATOR]

            # replace multiple white spaces by single white space
            simple_ztz_list = [re.sub('\s+', ' ',ztz) for ztz in
                               simple_ztz_list]

            if len(simple_ztz_list)>1:
                xx = " " + ZTZ_SEPARATOR + " "
                new_lines.append(xx.join(simple_ztz_list))
            elif len(simple_ztz_list) == 1:
                new_lines.append(simple_ztz_list[0])
            else:
                assert False

            count += 1
    with open(outpath, "w") as f:
        for line in new_lines:
            f.write(line + "\n")


def simplify_batch_of_m_scripts(
        in_dir, out_dir,
        batch_file_names,
        verbose=False):
    all_file_names = os.listdir(in_dir)
    assert set(batch_file_names).issubset(set(all_file_names))
    for file_name in batch_file_names:
        i = all_file_names.index(file_name)
        print('%i.' % (i + 1), file_name)
        simplify_one_m_script(in_dir, out_dir, file_name, verbose)


if __name__ == "__main__":

    def main1():
        print("************ simplifier:", ZTZ_SIMPLIFIER)
        ztz = \
        'The man, who had never liked the words "booby" and "boobyhatch,"' \
        ' and who liked them even less on a shining morning when there' \
        ' was a unicorn in the garden, thought for a moment.'
        zsimp.simplify_ztz(ztz, verbose=True)

    def main2():
        print("************ simplifier:", ZTZ_SIMPLIFIER)
        path = "simplifying_test.txt"
        with open(path, "r") as f:
            count = 1
            for line in f:
                print(str(count) + ".")
                zsimp.simplify_ztz(line, verbose=True)
                count += 1
    def main3():
        print("************ simplifier:", ZTZ_SIMPLIFIER)
        in_dir = "short_stories_spell"
        out_dir = "short_stories_simp"
        batch_file_names = os.listdir(in_dir)[0:3]
        simplify_batch_of_m_scripts(
            in_dir, out_dir,
            batch_file_names,
            verbose=False)

    def main4():
        print("************ simplifier:", ZTZ_SIMPLIFIER)
        remove_dialogs = True
        in_dir = SPELL_DIR if not remove_dialogs else SPELL_RD_DIR
        out_dir = SIMP_DIR if not remove_dialogs else SIMP_RD_DIR
        batch_file_names = os.listdir(in_dir)[0:3]
        simplify_batch_of_m_scripts(
            in_dir, out_dir,
            batch_file_names)

    # main1()
    # main2()
    main3()
    # main4()
