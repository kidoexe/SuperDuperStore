#pirveli 
class Solution:
    def intersect(self, nums1: List[int], nums2: List[int]) -> List[int]:
        sortedArr1 = sorted(nums1)
        sortedArr2 = sorted(nums2)
        i = 0
        j = 0
        output = []
        
        while i < len(sortedArr1) and j < len(sortedArr2):
            if sortedArr1[i] < sortedArr2[j]:
                i += 1
            elif sortedArr2[j] < sortedArr1[i]:
                j += 1
            else:
                output.append(sortedArr1[i])
                i += 1
                j += 1
        
        return output

#meore 
class Solution:
    def getCommon(self, nums1: List[int], nums2: List[int]) -> int:
        s1 , s2 = 0 , 0
        while s1 < len(nums1) and s2 < len(nums2):
            if nums1[s1] == nums2[s2]:
                return nums1[s1]
            elif nums1[s1] < nums2[s2]:
                s1 += 1
            else:
                s2 += 1
        return -1
