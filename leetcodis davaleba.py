class Solution:
    def lengthOfLastWord(self, s: str) -> int:
        words = s.strip().split()
        return len(words[-1])
        
#მოკლედ რომ ვთქვათ strip-ს ვიყენბთ რომ ზედმეტი სპასები მოვშალოთ თუ არის, split-ს რომ დაყოს წინადადება სიტყვებად და შექმნას ლისთი ხოლო len(words[-1])-ს რომ ბოლო სიტყვა ამოიღოს ლისთიდან და დაითვალოს რამდენი ასოსგან შედგება :3333

#○( ＾皿＾)っ Hehehe…