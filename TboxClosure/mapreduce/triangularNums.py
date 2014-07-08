__author__ = 'mpetyx'


# source = dict(zip(range(100), range(100)))
#
# def final(key, value):
#     print key, value
#
# # client
# def mapfn(key, value):
#     for i in range(value + 1):
#         yield key, i
#
# def reducefn(key, value):
#     return sum(value)


a = [1, 2, 3]
b = [4, 5, 6, 7]
c = [8, 9, 1, 2, 3]
L = map(lambda x:len(x), [a, b, c])

print L

# L == [3, 4, 5]
N = reduce(lambda x, y: x+y, L)
print N
# N == 12
# Or, if we want to be fancy and do it in one line
N = reduce(lambda x, y: x+y, map(lambda x:len(x), [a, b, c]))
print N