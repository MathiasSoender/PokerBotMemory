from Tree.data2 import Data
import random

D = Data()


nums = []
nums = list(range(0,1000))

for _ in range(0, 10000):
    nums.append(2)


nums.append(3)


for n in nums:
    D.update(1,n)


print(D)
print(sum(nums)/len(nums))