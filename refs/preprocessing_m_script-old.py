"""
https://www.datacamp.com/tutorial/python-regular-expression-tutorial

----------------------------------------
Here's a regular expression that detects strings with no lowercase letters:

^[^a-z]*$

Explanation:

^ and $ anchor the regex to the beginning and end of the string,
respectively, so that the entire string must match the pattern.

[^a-z] matches any character that is not a lowercase letter.

The * quantifier means that there can be zero or more matches of the negated
character class.

Together, ^[^a-z]*$ matches any string that consists entirely of characters
that are not lowercase letters.
-----------------------------------------
Here's a regular expression that detects strings with at least one uppercase
and one lowercase letter:

^(?=.*[A-Z])(?=.*[a-z]).+$

Explanation:

^ and $ anchor the regex to the beginning and end of the string,
respectively, so that the entire string must match the pattern.

(?=.*[A-Z]) is a positive lookahead that checks if the string contains at
least one uppercase letter. The .* matches any number of characters (
including zero), and the [A-Z] matches any uppercase letter.

(?=.*[a-z]) is a positive lookahead that checks if the string contains at
least one lowercase letter. The .* matches any number of characters (
including zero), and the [a-z] matches any lowercase letter.

.+ matches one or more of any character (except for line breaks), ensuring
that the string is not empty.

Together, the two lookaheads and the .+ ensure that the string contains at
least one uppercase and one lowercase letter.

--------------
def num_leading_wh_sp(s):
    count = 0
    for char in s:
        if char.isspace():
            count += 1
        else:
            break
    return count

    # reject lines that don't contain at least 4 lower case letters
    # string contains at least 10 lower case letters
    pattern = re.compile(r'^(.*[a-z]){4,}.*$')
    lines = [line for line in lines if not re.search(pattern, line)]

    # reject all lines in the beginning of script
    # that have more leading white space than minimum
    white_spaces = [num_leading_wh_sp(line) for line in lines])
    min_ws = min(white_spaces)
    for i in range(len(lines)):
        if white_spaces[i] > min_ws or not line[i][0].isupper():
            lines = lines.pop(0)
        else:
            break

    # remove from beginning of a line anything that isn't a letter
    pattern = r"^[^a-zA-Z]*"
    lines = [re.sub(pattern, "", line) for line in lines]

   # strip trailing white space
    lines = [line.rstrip() for line in lines]

    # reject lines at end of script that don't end in [".", "!", "?"]
    for i in reversed(len(lines)):
        if line[i][-1] not in [".", "!", "?"]
            lines = lines.pop(lines[-1])
        else:
            break

    # remove all empty lines
    lines = [line for line in lines if line]

# join lines to create new, simplified script
 script = ' '.join(lines)

 # remove parenthetical remarks
pattern = re.compile(r'\[(.*?)\]|\((.*?)\)|\{(.*?)\}')
script = re.subn(pattern, "", script)



# split script into sentences
 from nltk import tokenize
 lines = tokenize.sent_tokenize(script)


2. merge lines to get script without character names or stage directions,




3. split m_script so that separator is regex for non-optional period or
question mark or exclamation point, followed by optional white space,
followed by non-optional capital letter.

"""

import re

def extract_scenes_and_characters(path):

    with open(path, "r", encoding='utf-8') as f:
        lines = [line.strip() for line in f]
        lines = [line for line in lines if line !='']


    print("ddfg", lines[0:10])

    scenes = []
    begin_scene_pattern = r'(INT\.|EXT\.)\s[A-Z0-9/\s\-.]+'

    for line in lines:
        match = re.search(begin_scene_pattern, line)
        if match:
            scenes.append(match.group())

    # char_pattern = \
    #     r'(^[A-Z]+[A-Z]+(\.\s+)?(\'S\s+)?(\&\s+)?[A-Z]+[A-Z]+\s*)'
    # characters = [re.findall(char_pattern, x) for x in lines]
    # characters = [x for x in characters if x != []]

    # print("aadr", lines[0:50])

    characters = []
    for x in lines:
        xters = re.findall(r'(^[A-Z]+[A-Z]+\n)|(^[A-Z]+[A-Z]+\s+\n)|(^[A-Z]+\.\s+[A-Z]+\n)|(^[A-Z]+[A-Z]+\s+[A-Z]+[A-Z]+\s\n)\
        |(^[A-Z]+[A-Z]+\s+[A-Z]+[A-Z]+\s+[A-Z]+[A-Z]+\n)|(^[A-Z]+[A-Z]+\s+[A-Z]+[A-Z]+\n)|(^[A-Z]+[A-Z]+\'S\s+[A-Z]+[A-Z]+\s+[A-Z]+[A-Z]+\n)\
        |(^[A-Z]+[A-Z]+\'S\s+[A-Z]+[A-Z]+\n)|(^[A-Z]+[A-Z]+\'S\s+[A-Z]+[A-Z]+\s+\n)|(^MR\s+[A-Z]+[A-Z]+|MRS\s+[A-Z]+[A-Z]+\n)\
        |(^[A-Z]+[A-Z]+\s+\&\s+[A-Z]+[A-Z]+\n)|(^MR\s+[A-Z]+[A-Z]+|MRS\s+[A-Z]+[A-Z]+\s+\n)',
                           x)
        characters.append(xters)

    characters = [x for x in characters if x != []]

    print("ddfgh", characters)

    return scenes, characters


def extract_scene_characters(filename):
    # read the data into a list (each row is one list element)
    with open(filename, "r", encoding='utf-8', errors='ignore') as f:
        data = [row for row in f]

    dat = []
    for x in data:
        x = re.sub(r'\(.*\)', '', x)
        x = re.sub(r'\-|\#\d+', '', x)
        # x = re.sub(r"[^a-zA-Z0-9.,?'\n ]+", '', x)
        x = re.sub(r"POINT OF VIEW", 'Point of view', x)
        x = re.sub(r"TEXT", 'Text', x)
        x = re.sub(r"NEXT", 'Next', x)
        dat.append(x.replace('\t', ' ').lstrip(" "))

    scenes = []
    for l in dat:
        match = re.search(r'(((INT\.|EXT\.)\s[A-Z]+.*)|((INT\.|EXT\.)\s+[A-Z]+.*)|((INT\.|EXT\.)\s[A-Z]+)|((INT\.|EXT\.)\s[0-9]+.*)|\
        ((INT\./EXT\.|EXT\./INT\.)\s[A-Z]+.*)|((INT\.|EXT\.)\s[0-9]+)|((INT\./EXT\.|EXT\./INT\.)\s[0-9]+.*)|(INT\.\s+.*|EXT\.\s+.*)\
        |((INT\.|EXT\.)\s[A-Z]+\W+.+)|((INT|EXT)\s[A-Z]+.*)|((INT|EXT)\s+[A-Z]+.*)|((INT|EXT)\s[A-Z]+)|((INT|EXT)\s[0-9]+.*)\
        |((INT/EXT|EXT/INT)\s[A-Z]+.*)|((INT|EXT)\s[0-9]+)|((INT/EXT|EXT/INT)\s[0-9]+.*)|((I/E\.|E/I\.)\s+[A-Z].*)\
        |((INT|EXT)\s[A-Z]+\W+.+)|((I/E\.|E/I\.)\s+.*))\n', l)
        if match:
            scenes.append(match.group(1))
    # scenes = [x.strip(" ") for x in scenes]

    characters = []
    for x in dat:
        xters = re.findall(r'(^[A-Z]+[A-Z]+\n)|(^[A-Z]+[A-Z]+\s+\n)|(^[A-Z]+\.\s+[A-Z]+\n)|(^[A-Z]+[A-Z]+\s+[A-Z]+[A-Z]+\s\n)\
        |(^[A-Z]+[A-Z]+\s+[A-Z]+[A-Z]+\s+[A-Z]+[A-Z]+\n)|(^[A-Z]+[A-Z]+\s+[A-Z]+[A-Z]+\n)|(^[A-Z]+[A-Z]+\'S\s+[A-Z]+[A-Z]+\s+[A-Z]+[A-Z]+\n)\
        |(^[A-Z]+[A-Z]+\'S\s+[A-Z]+[A-Z]+\n)|(^[A-Z]+[A-Z]+\'S\s+[A-Z]+[A-Z]+\s+\n)|(^MR\s+[A-Z]+[A-Z]+|MRS\s+[A-Z]+[A-Z]+\n)\
        |(^[A-Z]+[A-Z]+\s+\&\s+[A-Z]+[A-Z]+\n)|(^MR\s+[A-Z]+[A-Z]+|MRS\s+[A-Z]+[A-Z]+\s+\n)',
                           x)
        characters.append(xters)

    characters = [x for x in characters if x != []]
    refined_characters = []
    for c in characters:
        cc = [tuple(filter(None, i)) for i in c]
        refined_characters.append(cc)
    refined_xters = [x[0][0] for x in refined_characters]

    best_ = ['BEST DIRECTOR', 'BEST ADAPTED SCREENPLAY', 'BROADCASTING STATUS',
             'BEST COSTUME DESIGN', 'TWENTIETH CENTURY FOX',
             'BEST ORIGINAL SCORE', 'BEST ACTOR', 'BEST SUPPORTING ACTOR',
             'BEST CINEMATOGRAPHY', 'BEST PRODUCTION DESIGN',
             'BEST FILM EDITING', 'BEST SOUND MIXING', 'BEST SOUND EDITING',
             'BEST VISUAL EFFECTS']
    transitions = ['RAPID CUT TO:', 'TITLE CARD', 'FINAL SHOOTING SCRIPT',
                   'CUT TO BLACK', 'CUT TO:', 'SUBTITLE:', 'SMASH TO:',
                   'BACK TO:', 'FADE OUT:', 'END', 'CUT BACK:', 'CUT BACK',
                   'DISSOLVE TO:', 'CONTINUED', 'RAPID CUT', 'RAPID CUT TO',
                   'FADE TO:', \
                   'FADE IN:', 'FADE OUT:', 'FADES TO BLACK', 'FADE TO',
                   'CUT TO', 'FADE TO BLACK', 'FADE UP:', 'BEAT', 'CONTINUED:',
                   'FADE IN', \
                   'TO:', 'CLOSE-UP', 'WIDE ANGLE', 'WIDE ON LANDING',
                   'THE END', 'FADE OUT', 'CONTINUED:', 'TITLE:', 'FADE IN',
                   'DISSOLVE TO', 'CUT-TO', 'CUT TO', 'CUT TO BLACK', \
                   'INTERCUT', 'INSERT', 'CLOSE UP', 'CLOSE', 'ON THE ROOF',
                   'BLACK', 'BACK IN SILENCE', 'TIMECUT', 'BACK TO SCENE', \
                   'REVISED', 'PERIOD', 'PROLOGUE', 'TITLE', 'SPLITSCREEN.',
                   'BLACK.', \
                   'FADE OUT', 'CUT HARD TO:', 'OMITTED', 'DISSOLVE',
                   'WIDE SHOT', 'NEW ANGLE']
    movie_characters = []
    for x in refined_xters:
        x = re.sub(r'INT\..*|EXT\..*', '', x)
        x = re.sub(r'ANGLE.*', '', x)
        trans = re.compile(
            "({})+".format("|".join(re.escape(c) for c in transitions)))
        x = trans.sub(r'', x)
        best = re.compile(
            "({})+".format("|".join(re.escape(c) for c in best_)))
        x = best.sub(r'', x)
        movie_characters.append(x.replace('\n', '').strip())
    movie_characters = [x.strip() for x in movie_characters if x]

    return scenes, movie_characters

if __name__ == "__main__":
    def main1():
        path = "../m_scripts/10-things-i-hate-about-you.txt"
        scenes, characters = extract_scenes_and_characters(path)
        # print(scenes[0:5])

    def main2():
        path = "../m_scripts/10-things-i-hate-about-you.txt"
        scenes, characters = extract_scene_characters(path)
        print(set(characters))
        print(scenes)

    main2()