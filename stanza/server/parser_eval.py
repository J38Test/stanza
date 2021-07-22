


import stanza
from stanza.protobuf import EvaluateParserRequest, EvaluateParserResponse
from stanza.server.java_protobuf_requests import send_request, build_tree, JavaProtobufContext


EVALUATE_JAVA = "edu.stanford.nlp.parser.metrics.EvaluateExternalParser"

def build_request(gold_trees, predictions):
    """
    predicted_trees should be a list of list of pairs:  [[(predicted_tree, score)]]
      one list for each gold_tree
    Note that for now, only one tree is measured, but this may be extensible in the future
    Trees should be in the form of a Tree from parse_tree.py
    """
    request = SemgrexRequest()
    for semgrex in semgrex_patterns:
        request.semgrex.append(semgrex)

    for sent_idx, sentence in enumerate(doc.sentences):
        query = request.query.add()
        word_idx = 0
        for token in sentence.tokens:
            for word in token.words:
                add_token(query.token, word, token)
                add_word_to_graph(query.graph, word, sent_idx, word_idx)

                word_idx = word_idx + 1

    return request


class EvaluateParser(JavaProtobufContext):
    """
    Parser evaluation context window

    This is a context window which keeps a process open.  Should allow
    for multiple requests without launching new java processes each time.
    """
    def __init__(self, classpath=None):
        super(EvaluateParser, self).__init__(classpath, EvaluateParserResponse, EVALUATE_JAVA)

    def process(self, doc, *semgrex_patterns):
        request = build_request(doc, semgrex_patterns)
        return self.process_request(request)

