class Utility:
    def __init__(self):
        pass

    @staticmethod
    def sort_and_stringify(iter_obj=None, handle_el_cb=lambda el: el):
        if iter_obj is None:
            iter_obj = []

        iter_type = type(iter_obj).__name__
        res = map(lambda el: handle_el_cb(str(el)), sorted(iter_obj))

        if iter_type == "list":
            return list(res)
        elif iter_type == "tuple":
            return tuple(res)
        elif iter_type == "set":
            return set(res)

        raise TypeError()

    @staticmethod
    def intersect_num_iterables(iter_a=None, iter_b=None):
        if iter_a is None:
            iter_a = []

        if iter_b is None:
            iter_b = []

        a_ptr = 0
        b_ptr = 0

        a_len = len(iter_a)
        b_len = len(iter_b)

        res = []

        while a_ptr < a_len and b_ptr < b_len:
            a_el = iter_a[a_ptr]
            b_el = iter_b[b_ptr]

            if a_el < b_el:
                a_ptr += 1
            elif b_el < a_el:
                b_ptr += 1
            else:
                res.append(a_el)
                a_ptr += 1
                b_ptr += 1

        return res

    @staticmethod
    def union_num_iterables(iter_a=None, iter_b=None):
        # this approach consumes more cycle, but shorted to write
        if iter_a is None:
            iter_a = []

        if iter_b is None:
            iter_b = []

        return sorted(list(set(iter_a + iter_b)))

    @staticmethod
    def diff_num_iterables(iter_a=None, iter_b=None):
        # this approach consumes more cycle, but shorted to write
        if iter_a is None:
            iter_a = []

        if iter_b is None:
            iter_b = []

        return [el for el in iter_a if el not in iter_b]

