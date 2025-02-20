class Solution:
    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
        pp = {}
        for num in nums1:
            pp[num] = pp.get(num, 0) + 1
        
        result = []
        for num in nums2:
            if num in pp:
                result.append(num)
                del pp[num]
        
        return result
