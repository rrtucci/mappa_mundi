class WordGuesser:

    def __init__(self, word, global_checker,
                 word_to_reps=None, local_word_count=None):
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
            self.prob_for_word = (self.prob_for_word + local_prob)/2

        self.best_guess = word
        self.prob_for_best_guess = 0
        self.do_update(word)
                   
    def do_update(self, guess):
        prob_for_guess = \
            self.global_checker.word_usage_frequency(guess)
        if self.word_to_reps:
            local_prob = self.word_to_reps[guess] / self.local_word_count
            prob_for_guess = (prob_for_guess + local_prob)/2
        if prob_for_guess > self.prob_for_best_guess:
            self.best_guess = guess
            self.prob_for_best_guess = prob_for_guess
                





