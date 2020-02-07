import Levenshtein


def fuzzy_match(base_str, candidate_str, threshold):
    dist = Levenshtein.distance(base_str, candidate_str)
    base_len = len(base_str)
    return (dist <= round(base_len * threshold))
