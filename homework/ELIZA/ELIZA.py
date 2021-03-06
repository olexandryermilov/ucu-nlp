import random
import re

reflections = {
    "am": "are",
    "was": "were",
    "i": "you",
    "i'd": "you would",
    "i've": "you have",
    "i'll": "you will",
    "my": "your",
    "are": "am",
    "you've": "I have",
    "you'll": "I will",
    "your": "my",
    "yours": "mine",
    "you": "I",
    "me": "you"
}

psychobabble = [
    (
        r'quit',
        [
            "Thank you for talking with me.",
            "Good-bye.",
            "Thank you, that will be $150. Have a good day!"
         ]
    ), (
        r'(I am feeling) (.*)',
        [
            "What happened, why {} {}?",
            "Why do you think {} {}?"
        ]
    ),
    (r'(I think) (I am) (.*)', ['Why do {} {} {}?']),
    (r'(I want to) (.*)', ['If you {1} tomorrow, will it make you happier?']),
    (r'(I need) (.*)', ["What will you do if you get {1}?"]),
    (r'(I remember) (.*)', ['Is {1} a good or bad memory for you?']),
    (r'(You are) (.*)', ['Why do you think {} {}?']),
    (r'(My name is) (.*)', ['Nice to meet you, {1}. I am ELIZA']),
    (r'(I am) (\d+) years* old', ["How do you feel about being {1}?"]),
    (r'(I am) (.*)', ['How long {} {}?']),
    (r'(I) (.*)', ['What it means for {} to {}?']),
]


def reflect(fragment):
    tokens = fragment.lower().split()
    for i, token in enumerate(tokens):
        if token in reflections:
            tokens[i] = reflections[token]
    return ' '.join(tokens)


def analyze(statement):
    for pattern, responses in psychobabble:
        match = re.match(pattern, statement.rstrip(".!"))
        if match:
            response = random.choice(responses)
            return response.format(*[reflect(g) for g in match.groups()])
    return "I don't know what to say. Tell me more."


def main():
    print("Hello. How are you feeling today?")

    while True:
        statement = input("YOU: ")
        print("ELIZA: " + analyze(statement))

        if statement == "quit":
            break


if __name__ == "__main__":
    main()
