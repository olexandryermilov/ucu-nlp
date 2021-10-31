import spacy
from spacy.tokens import Doc, Token
nlp = spacy.load("en_core_web_sm")
from typing import List, Tuple, Dict
from get_sequences import longest_sequences

class DocParser:
    def __init__(self, doc: Doc):
        self.doc = doc
        self.featureMap = {
            'POS': 'pos_',
            'TAG': 'tag_',
            'DEP': 'dep_',
            'LOWER': 'lower',
            'TEXT': 'text',
            'IS_ALPHA': 'is_alpha',
            'IS_DIGIT': 'is_digit',
            'IS_LOWER': 'is_lower',
            'IS_UPPER': 'is_upper',
            'IS_TITLE': 'is_title',
            'IS_PUNCT': 'is_punct',
            'IS_SPACE': 'is_space',
            'IS_STOP': 'is_stop',
            'IS_START': 'is_start',
            'IS_END': 'is_end',
            'LIKE_NUM': 'like_num',
            'LIKE_URL': 'like_url',
            'LIKE_EMAIL': 'like_email',
            'LEMMA': 'lemma',
            'ORIGINAL': 'original',
            'SHAPE': 'shape',
        }

    def parse_token_features(self, token: Token, token_features: Dict) -> bool:
        for key in token_features:
            if key == 'OP':
                continue
            if getattr(token, self.featureMap[key]) != token_features[key]:
                return False
        return True

    def get_all_nodes(self, feats):
        # first run - loop over all tokens
        OP = feats['OP'] if 'OP' in feats else None
        if not self.prev_spans:

            if OP and OP == '+':
                all_matches = []
                for token in self.doc:
                    if self.parse_token_features(token, feats):
                        all_matches.append((token.i, token.i + 1))
                self.prev_spans = longest_sequences(all_matches)
            elif OP and OP == '*':
                all_matches = []
                all_tokens = []
                for token in self.doc:
                    if self.parse_token_features(token, feats):
                        all_matches.append((token.i, token.i + 1))
                    all_tokens.append((token.i + 1, token.i + 1))
                self.prev_spans = longest_sequences(all_matches) + all_tokens
            elif OP and OP == '?':
                all_matches = []
                all_tokens = []
                for token in self.doc:
                    if self.parse_token_features(token, feats):
                        all_matches.append((token.i, token.i + 1))
                    all_tokens.append((token.i + 1, token.i + 1))
                self.prev_spans = all_matches + all_tokens
            elif OP and OP == '!':
                all_matches = []
                for token in self.doc:
                    if not self.parse_token_features(token, feats):
                        all_matches.append((token.i, token.i + 1))
                self.prev_spans = all_matches
            else:
                for token in self.doc:
                    if self.parse_token_features(token, feats):
                        self.prev_spans.append((token.i, token.i + 1))
        else:
            this_state_result = []

            # @todo: apply the sequence function here to handle the + operator
            if OP and OP == '+':
                all_matches = []
                for token in self.doc:
                    if self.parse_token_features(token, feats):
                        all_matches.append((token.i, token.i + 1))
                all_sequences = longest_sequences(all_matches)
                for prev_span_start, prev_span_end in self.prev_spans:
                    for seq_start, seq_end in all_sequences:
                        if prev_span_end == seq_start:
                            if self.parse_token_features(self.doc[prev_span_end], feats):
                                this_state_result.append((prev_span_start, prev_span_end + 1))
            elif OP and OP == '*':
                all_matches = []
                all_tokens = []
                for token in self.doc:
                    if self.parse_token_features(token, feats):
                        all_matches.append((token.i, token.i + 1))
                    all_tokens.append((token.i + 1, token.i + 1))
                all_sequences = longest_sequences(all_matches) + all_tokens
                for prev_span_start, prev_span_end in self.prev_spans:
                    for seq_start, seq_end in all_sequences:
                        if prev_span_end == seq_start:
                            if self.parse_token_features(self.doc[prev_span_end], feats):
                                this_state_result.append((prev_span_start, prev_span_end + 1))
            elif OP and OP == '?':
                all_matches = []
                all_tokens = []
                for token in self.doc:
                    if self.parse_token_features(token, feats):
                        all_matches.append((token.i, token.i + 1))
                    all_tokens.append((token.i + 1, token.i + 1))
                all_sequences = all_matches + all_tokens
                for prev_span_start, prev_span_end in self.prev_spans:
                    for seq_start, seq_end in all_sequences:
                        if prev_span_end == seq_start:
                            if self.parse_token_features(self.doc[prev_span_end], feats):
                                this_state_result.append((prev_span_start, prev_span_end + 1))
            elif OP and OP == '!':
                all_matches = []
                for token in self.doc:
                    if not self.parse_token_features(token, feats):
                        all_matches.append((token.i, token.i + 1))
                        all_matches.append((token.i + 1, token.i + 1))
                all_sequences = all_matches
                for prev_span_start, prev_span_end in self.prev_spans:
                    for seq_start, seq_end in all_sequences:
                        if prev_span_end == seq_start:
                            if self.parse_token_features(self.doc[prev_span_end], feats):
                                this_state_result.append((prev_span_start, prev_span_end + 1))
            else:
                for prev_span_start, prev_span_end in self.prev_spans:
                    if prev_span_end < len(self.doc):
                        if self.parse_token_features(self.doc[prev_span_end], feats):
                            this_state_result.append((prev_span_start, prev_span_end+1))
                self.prev_spans = this_state_result

    def parse_expression(self, expression: List[Dict]) -> List[Tuple[int, int]]:
        self.prev_spans = []

        for feats in expression:
            self.get_all_nodes(feats)

        return self.prev_spans

# we can implement the same thing in a function, but it wouldn't allow us to memorize results
# for a doc and reuse them for other expressions that may be related
# we can reuse this object to run multiple expressions for one document


if __name__ == '__main__':
    text = 'I work at J&L Consulting Ltd. and this is my favorite Ltd.'
    doc = nlp(text)
    parser = DocParser(doc)
    result = parser.parse_expression(
        [{'POS': 'PROPN', 'OP': '!'},
         {'TEXT': 'Ltd.'}]
    )
    print(result)
    for start, end in result:
        print(doc[start:end])

    parser = DocParser(doc)
    result = parser.parse_expression(
        [{'POS': 'PROPN', 'OP': '*'},
         {'TEXT': 'Ltd.'}]
    )
    print(result)
    for start, end in result:
        print(doc[start:end])

    parser = DocParser(doc)
    result = parser.parse_expression(
        [{'POS': 'PROPN', 'OP': '?'},
         {'TEXT': 'Ltd.'}]
    )
    print(result)
    for start, end in result:
        print(doc[start:end])

    parser = DocParser(doc)
    result = parser.parse_expression(
        [{'POS': 'PROPN', 'OP': '+'},
         {'TEXT': 'Ltd.'}]
    )
    print(result)
    for start, end in result:
        print(doc[start:end])

    # if you fixed the + operator, the result should be [(3, 6), (4, 6)]
