class WordGuesser:
    """
    This class is used by `spell_checking.py` to store and update the word
    `best_guess` which is a guess for the word `word`. Also stored in this
    class: the probabilities for `best_guess` and `word`.


    Attributes
    ----------
    best_guess: str
        a word which is the best guess so far for the word `word`
    global_checker: SpellChecker
        a class of pyspellchecker that can give global probabilities of words
    local_word_count: int
        number of different words in the single local document being considered
    prob_for_best_guess: float
        probability for `best_guess` (average of local and global probs)
    prob_for_word: float
        probability for `word` (average of local and global probs)
    word: str
        low probability word, likely a misspelled word. `best_guess` is a
        replacement for it.
    word_to_reps: dict[str, int]
        a dictionary mapping each word in the local document being considered,
        to its number of repetitions in that document.

    """

    def __init__(self, word, global_checker,
                 word_to_reps=None, local_word_count=None):
        """
        Constructor

        Parameters
        ----------
        word: str
        global_checker: SpellChecker
        word_to_reps: dict[str, int]
        local_word_count: int

        """
        assert word[0].islower()
        self.word = word
        self.global_checker = global_checker
        self.word_to_reps = word_to_reps
        self.local_word_count = local_word_count
        if word_to_reps:
            assert local_word_count

        self.prob_for_word = \
            global_checker.word_usage_frequency(word)
        if word_to_reps:
            local_prob = word_to_reps[word] / local_word_count
            self.prob_for_word = (self.prob_for_word + local_prob) / 2

        self.best_guess = word
        self.prob_for_best_guess = 0
        self.do_update(word)

    def do_update(self, guess):
        """
        This method finds the probability of the word `guess` in the local
        dictionary, and if that probability is greater that
        `prob_best_guess`, it replaces `best_guess` by `guess`. It also
        updates `prob_for_best_guess`.

        Parameters
        ----------
        guess: str

        Returns
        -------
        None

        """
        prob_for_guess = \
            self.global_checker.word_usage_frequency(guess)
        if self.word_to_reps:
            local_prob = self.word_to_reps[guess] / self.local_word_count
            prob_for_guess = (prob_for_guess + local_prob) / 2
        if prob_for_guess > self.prob_for_best_guess:
            self.best_guess = guess
            self.prob_for_best_guess = prob_for_guess
