import mmh3

class BloomFilter:
    def __init__(self, size: int, num_hashes: int):
      if size <= 0 or num_hashes <= 0:
            raise ValueError("size and num_hashes must be positive integers")
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [0] * size

    def add(self, item: str) -> None:
        if not isinstance(item, str) or not item:
            # skip invalid inputs
            return
        for i in range(self.num_hashes):
            index = mmh3.hash(item, i, signed=False) % self.size
            self.bit_array[index] = 1

    def __contains__(self, item: str) -> bool:
        """
        Check membership: returns True if possibly present, False if definitely absent.
        """
        if not isinstance(item, str) or not item:
            return False
        for i in range(self.num_hashes):
            index = mmh3.hash(item, i, signed=False) % self.size
            if self.bit_array[index] == 0:
                return False
        return True


def check_password_uniqueness(bloom: BloomFilter, passwords: list) -> dict:
    results = {}
    for pwd in passwords:
        if not isinstance(pwd, str) or pwd == "":
            results[pwd] = "invalid value"
        elif pwd in bloom:
            results[pwd] = "already used"
        else:
            results[pwd] = "unique"
    return results

# Example usage
if __name__ == "__main__":
    bloom = BloomFilter(size=1000, num_hashes=3)
    existing_passwords = ["password123", "admin123", "qwerty123"]
    for pwd in existing_passwords:
        bloom.add(pwd)

    new_passwords = ["password123", "newpass", "admin123", "guest", "", None]
    results = check_password_uniqueness(bloom, new_passwords)
    for pwd, status in results.items():
        print(f"Password '{pwd}' — {status}.")

#
# (base) admin@CrossFil-MBP ~ % python /Users/admin/PycharmProjects/Algo/hw_5_1.py
# Password 'password123' — already used.
# Password 'newpass' — unique.
# Password 'admin123' — already used.
# Password 'guest' — unique.
# Password '' — invalid value.
# Password 'None' — invalid value.