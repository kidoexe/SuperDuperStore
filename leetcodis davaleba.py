class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        count = 0
        x = None
        
        for num in nums:
            if count == 0:
                x = num
            count += (1 if num == x else -1)
        
        return x
        
# მოკლედ წერა მეზარება და გაკეთილის შემდეგ შემიძლია ავხსნა როგორ მუშაობს <3
# :3


           

            
