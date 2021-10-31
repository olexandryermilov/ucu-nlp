from collections import OrderedDict

class MyStemmer:
    def isVowel(self, char, prevLetter):
        return char == 'a' or char =='o' or char =='e' or char =='u' or char == 'i' or (char =='y' and self.isConsOne(prevLetter))

    def isConsOne(self, char):
        return not(char == 'a' or char == 'o' or char == 'e' or char == 'u' or char == 'i')

    def isCons(self, char, prevLetter):
        return not self.isVowel(char, prevLetter)

    def createRulesForStep2(self):
        dict = OrderedDict()
        dict['ational'] = 'ate'
        dict['tional'] = 'tion'
        dict['enci'] = 'ence'
        dict['anci'] = 'ance'
        dict['izer'] = 'ize'
        dict['abli'] = 'able'
        dict['alli'] = 'al'
        dict['entli'] = 'ent'
        dict['eli'] = 'e'
        dict['ousli'] = 'ous'
        dict['ization'] = 'ize'
        dict['ation'] = 'ate'
        dict['ator'] = 'ate'
        dict['alism'] = 'al'
        dict['iveness'] = 'ive'
        dict['fulness'] = 'ful'
        dict['ousness'] = 'ous'
        dict['aliti'] = 'al'
        dict['iviti'] = 'ive'
        dict['biliti'] = 'ble'
        return dict

    def createRulesForStep3(self):
        dict = OrderedDict()
        dict['icate'] = 'ic'
        dict['ative'] = ''
        dict['alize'] = 'al'
        dict['iciti'] = 'ic'
        dict['ical'] = 'ic'
        dict['ful'] = ''
        dict['ness'] = ''
        return dict

    def createRulesForStep4(self):
        rules = ['al', 'ance', 'ence', 'er', 'ic', 'able', 'ible', 'ant', 'ement', 'ment', 'ent', 'sion', 'tion', 'ou', 'ism', 'ate', 'iti', 'ous', 'ive', 'ize']
        return rules

    def calculateForm(self, word):
        form = []
        i = 1
        if self.isConsOne(word[0]):
            form.append('C')
        else:
            form.append('V')
        while i < len(word):
            if self.isVowel(word[i], word[i-1]):
                form.append('V')
                while i < len(word) and self.isVowel(word[i], word[i-1]):
                    i = i + 1
            else:
                if self.isCons(word[i], word[i-1]):
                    form.append('C')
                    while i < len(word) and self.isCons(word[i], word[i-1]):
                        i = i + 1
        if len(form) > 1 and form[0] == form[1]:
            form = form[1:]
        return ''.join(form)

    def replace(self, word, pattern, replacement):
        result = word.rfind(pattern)
        base = word[:result]
        replaced = base + replacement
        return replaced

    def calculateM(self, word):
        form = self.calculateForm(word)
        m = form.count('VC')
        return m

    def starVstar(self, word):
        prevChar = word[0]
        for char in word[1:-1]:
            if(self.isVowel(char, prevChar)):
                return True
            prevChar = char
        return False

    def stard(self, word):
        return word[-1] == word[-2] and self.isCons(word[-1], word[-2])

    def starOSecondCons(self, char):
        return char != 'w' and char != 'x' and char != 'y'

    def staro(self, word):
        return len(word) >= 3 and self.isCons(word[-1], word[-2]) and self.isConsOne(word[-3]) and self.isVowel(word[-2], word[-3]) and self.starOSecondCons(word[-1])

    def step1a(self, word):
        rules = {'sses': 'ss', 'ies': 's', 'ss':'ss', 's': ''}
        keys = list(rules.keys())
        sorted_keys = sorted(keys, key=len, reverse=True)
        new_word = word
        for rule in sorted_keys:
            if word.endswith(rule):
                new_word = self.replace(word, rule, rules[rule])
                break
        return new_word

    def step1b_restoreE(self, word):
        rules = {'at': 'ate', 'bl': 'ble', 'iz': 'ize'}
        new_word = word
        for rule in list(rules.keys()):
            if(word.endswith(rule)):
                new_word = self.replace(word, rule, rules[rule])
                break
        if new_word == word:
            if self.stard(word) and word[-1] not in 'lzs':
                new_word = word[:-1]
            elif self.calculateM(word) == 1 and self.staro(word):
                new_word = word + 'e'
        return new_word

    def step1b(self, word):
        rules = {'eed': 'ee', 'ed': '', 'ing': ''}
        new_word = word
        if word.endswith('eed') and self.calculateM(word[:-3]) > 0:
            new_word = self.replace(word, 'eed', rules['eed'])
        elif word.endswith('ed') and self.starVstar(word[:-2]):
            new_word = self.replace(word, 'ed', rules['ed'])
            new_word = self.step1b_restoreE(new_word)
        elif word.endswith('ing') and self.starVstar(word[:-3]):
            new_word = self.replace(word, 'ing', rules['ing'])
            new_word = self.step1b_restoreE(new_word)
        return new_word

    def step1c(self, word):
        new_word = word
        if word[-1] == 'y' and self.starVstar(word[:-1]):
            new_word = word[:-1] + 'i'
        return new_word

    def step2(self, word):
        rules = self.createRulesForStep2()
        new_word = word
        for rule in rules.keys():
            if word.endswith(rule) and self.calculateM(word[:-len(rule)]) > 0:
                new_word = self.replace(word, rule, rules[rule])
                break
        return new_word

    def step3(self, word):
        rules = self.createRulesForStep3()
        new_word = word
        for rule in rules.keys():
            if word.endswith(rule) and self.calculateM(word[:-len(rule)]) > 0:
                new_word = self.replace(word, rule, rules[rule])
                break
        return new_word

    def step4(self, word):
        rules = self.createRulesForStep4()
        new_word = word
        for rule in rules:
            letter = ''
            if(rule == 'tion' or rule == 'sion'):
                letter = rule[0]
                rule = rule[1:]
            if word.endswith(letter+rule) and self.calculateM(word[:-len(rule)]) > 1:
                new_word = self.replace(word, rule, '')
                break
        return new_word

    def step5a(self, word):
        new_word = word
        if word.endswith('e') and self.calculateM(word[:-1]) > 1:
            new_word = word[:-1]
        elif word.endswith('e') and self.calculateM(word[:-1]) == 1 and not self.staro(word[:-1]):
            new_word = word[:-1]
        return new_word

    def step5b(self, word):
        new_word = word
        if self.calculateM(word) > 1 and self.stard(word) and word[-1] == 'l':
            new_word = word[:-1]
        return new_word

    def stem(self, word):
        word = self.step1a(word)
        word = self.step1b(word)
        word = self.step1c(word)
        word = self.step2(word)
        word = self.step3(word)
        word = self.step4(word)
        word = self.step5a(word)
        word = self.step5b(word)
        return word

if __name__ == '__main__':
    print(MyStemmer().step1b("hopping"))
    print(MyStemmer().step1b("conflated"))
    print(MyStemmer().step1b("trouble"))
    print(MyStemmer().step1b("tanned"))
    print(MyStemmer().step1b("falling"))
    print(MyStemmer().step1b("hissing"))
    print(MyStemmer().step1b("fizzed"))
    print(MyStemmer().step1b("failing"))
    print(MyStemmer().step1b("filing"))
    print(MyStemmer().step1b("sized"))

    print(MyStemmer().step1c("happy"))
    print(MyStemmer().step1c("sky"))


    print(MyStemmer().step2("relational"))
    print(MyStemmer().step2("conditional"))
    print(MyStemmer().step2("rational"))
    print(MyStemmer().step2("valenci"))
    print(MyStemmer().step2("hesitanci"))
    print(MyStemmer().step2("digitizer"))
    print(MyStemmer().step2("conformabli"))
    print(MyStemmer().step2("radicalli"))
    print(MyStemmer().step2("differentli"))
    print(MyStemmer().step2("vileli"))
    print(MyStemmer().step2("analogousli"))
    print(MyStemmer().step2("vietnamization"))
    print(MyStemmer().step2("predication"))
    print(MyStemmer().step2("operator"))
    print(MyStemmer().step2("feudalism"))
    print(MyStemmer().step2("decisiveness"))
    print(MyStemmer().step2("hopefulness"))
    print(MyStemmer().step2("callousness"))
    print(MyStemmer().step2("formaliti"))
    print(MyStemmer().step2("sensitiviti"))
    print(MyStemmer().step2("sensibiliti"))

    print(MyStemmer().step3("triplicate"))
    print(MyStemmer().step3("formative"))
    print(MyStemmer().step3("formalize"))
    print(MyStemmer().step3("electriciti"))
    print(MyStemmer().step3("electrical"))
    print(MyStemmer().step3("hopeful"))
    print(MyStemmer().step3("goodness"))

    print(MyStemmer().step4("revival"))
    print(MyStemmer().step4("allowance"))
    print(MyStemmer().step4("inference"))
    print(MyStemmer().step4("airliner"))
    print(MyStemmer().step4("gyroscopic"))
    print(MyStemmer().step4("adjustable"))
    print(MyStemmer().step4("defensible"))
    print(MyStemmer().step4("irritant"))
    print(MyStemmer().step4("replacement"))
    print(MyStemmer().step4("adjustment"))
    print(MyStemmer().step4("dependent"))
    print(MyStemmer().step4("adoption"))
    print(MyStemmer().step4("homologou"))
    print(MyStemmer().step4("communism"))
    print(MyStemmer().step4("activate"))
    print(MyStemmer().step4("angulariti"))
    print(MyStemmer().step4("homologous"))
    print(MyStemmer().step4("effective"))
    print(MyStemmer().step4("bowdlerize"))

    print(MyStemmer().step5a("probate"))
    print(MyStemmer().step5a("rate"))
    print(MyStemmer().step5a("cease"))
    print(MyStemmer().step5b("controll"))
    print(MyStemmer().step5b("roll"))
