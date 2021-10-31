from graph import Graph
import bisect
from typing import List, Tuple


def insert_if_not_contains(lst, el):
    index = bisect.bisect_left(lst, el)
    if index >= len(lst):
        return lst + [el]
    elif lst[index] != el:
        return lst[:index] + [el] + lst[index:]
    else:
        return lst


def longest_sequences(spans: List[Tuple[int, int]]):
    # if a span follows another span directly, merge them into a bigger span
    # return the longest non-overlapping spans
    # used for merchandise
    '''
    :param spans: [(0,1), (0,2), (1,3)]
    :return: [(0,3)]
    '''
    spans = sorted(spans, key=lambda span: (span[0], span[1]))

    graph = Graph()

    result = []

    for ind, this_span in enumerate(spans):
        matched = False

        # momorize all node connectedness info in the graph
        for next_ind, next_span in enumerate(spans[ind + 1:]):
            next_ind += ind + 1
            if this_span[1] == next_span[0]:
                graph.add_edge(ind, next_ind)
                matched = True
            elif this_span[1] < next_span[0]:
                break
        if not matched:
            # insert_if_not_contains was written more for the path loop below,
            # but result may empty at the beginning but if you have a very long spans list,
            # there may be very many disconnected spans so you still want to use this function
            # to avoid duplicates
            result = insert_if_not_contains(result, spans[ind])

    # beginnings of paths
    keys = list(graph.graph.keys())

    for key in keys:

        graph.visited_list = []
        # find_paths is a recursive function that will call itself until the path ends
        graph.find_paths(key, [], 1, min_depth=1, max_depth=10)

        for path in graph.visited_list:
            if len(path) == 1:
                result = insert_if_not_contains(result, spans[path[0]])
            else:
                snippet = [spans[ind] for ind in path]
                result = insert_if_not_contains(result, (snippet[0][0], snippet[-1][1]))


        #@todo: for each path found, save the full span in result
        # use insert_if_not_contains instead of append
        # some paths have length of one and should be approached differently than loner paths

    return result


if __name__ == '__main__':
    matches = [(0, 1), (1, 2), (3, 4), (5, 6), (6, 7), (7, 8)]
    result = longest_sequences(matches)
    print(result)

    # if you fixed the sequence function, the result should be [(0, 1), (0, 2), (1, 2), (3, 4), (5, 6), (5, 7), (6, 7)]
