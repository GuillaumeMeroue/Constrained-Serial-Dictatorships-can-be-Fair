
# https://stackoverflow.com/questions/58915599/generate-restricted-weak-integer-compositions-or-partitions-of-an-integer-n-in
def generate_policy(n, m):
    def helper(remaining_objects, agents_left, current_policy):
        if agents_left == 0:
            if remaining_objects == 0:
                yield current_policy
        elif agents_left == 1:
            if 0 <= remaining_objects <= m:
                yield current_policy + (remaining_objects,)
        elif 0 <= remaining_objects <= m * agents_left:
            for v in range(m, -1, -1):
                yield from helper(remaining_objects - v, agents_left - 1, current_policy + (v,))
    
    return helper(m, n, ())


# Test
# n = 10
# m = 20
# all_policies = generate_policy(n,m)
# print(next(all_policies))
# print(next(all_policies))