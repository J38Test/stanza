


import stanza
from stanza.protobuf import EvaluateParserRequest, EvaluateParserResponse
from stanza.server.java_protobuf_requests import send_request, JavaProtobufContext


EVALUATE_JAVA = "edu.stanford.nlp.parser.metrics.EvaluateExternalParser"

def send_evaluate_request(request):
    return send_request(request, EvaluateParserResponse, EVALUATE_JAVA)

def build_request(gold_tree, predicted_trees):
    """
    predicted_trees should be a list of pairs:  [(predicted_tree, score)]
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

