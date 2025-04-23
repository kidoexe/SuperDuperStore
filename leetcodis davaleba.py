#1
class Solution:
    def findComplement(self, num: int) -> int:
        res = ''
        for i in bin(num)[2:]:
            res += '1' if i == '0' else '0'
        return int(res, 2)


#2
class Solution:
    def arrayStringsAreEqual(self, word1: List[str], word2: List[str]) -> bool:
        str1="".join(word1)
        str2="".join(word2)
        if str1==str2:
            return True
        else:
            return False

#3
def twoSum(numbers, target):
    left = 0
    right = len(numbers) - 1

    while left < right:
        current_sum = numbers[left] + numbers[right]
        if current_sum == target:
            return [left + 1, right + 1]  
        elif current_sum < target:
            left += 1
        else:
            right -= 1
