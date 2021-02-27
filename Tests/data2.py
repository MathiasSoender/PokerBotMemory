from Tree.data2 import Data
import random

def find_denom2(n,c):
    return (c**n - 1) / (c-1)
D = Data()


nums = list(reversed(list(range(0,10))))

nums = [-2] * 100000

for n in nums:
    D.update(1, n)


print(D)
print(sum(nums)/len(nums))
print(D.c_reward[5] / find_denom2(len(nums), 0.985))


