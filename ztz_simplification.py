from my_globals import *
import os
import importlib as imp
zsimp = imp.import_module(ZTZ_SIMPLIFIER)

def simplify_one_m_script(
    in_dir, out_dir,
    file_name,
    verbose=False):
    inpath = in_dir + "/" + file_name
    outpath = out_dir + "/" + file_name
    new_lines = []
    with open(inpath, "r", encoding="utf-8") as f:
        count = 1
        for line in f:
            print(str(count) + ".")
            simple_ztz_list = zsimp.simplify_ztz(line, verbose)
            new_lines.append(ZNTZ_SEPARATOR.join(simple_ztz_list))
            count += 1
    with open(outpath, "w", encoding="utf-8") as f:
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
        path = "All_types_of_inputs.txt"
        with open(path, "r", encoding='utf-8') as f:
            count = 1
            for line in f:
                print(str(count) + ".")
                zsimp.simplify_ztz(line, verbose=True)
                count += 1
    def main3():
        print("************ simplifier:", ZTZ_SIMPLIFIER)
        in_dir = "short_stories_prep"
        out_dir = "short_stories_simp"
        batch_file_names = os.listdir(in_dir)[0:2]
        simplify_batch_of_m_scripts(
            in_dir, out_dir,
            batch_file_names,
            verbose=True)

    def main4():
        print("************ simplifier:", ZTZ_SIMPLIFIER)
        remove_dialogs = False
        in_dir = PREP_DIR if not remove_dialogs else PREP_RD_DIR
        out_dir = SIMP_DIR if not remove_dialogs else SIMP_RD_DIR
        batch_file_names = os.listdir(in_dir)[0:10]
        simplify_batch_of_m_scripts(
            in_dir, out_dir,
            batch_file_names)

    # main1()
    # main2()
    # main3()
    main4()
