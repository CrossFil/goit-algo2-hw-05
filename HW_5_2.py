import re
import time
import mmh3
import math
import json

class HyperLogLog:
    def __init__(self, p: int = 14):
        """
        :param p: precision (number of bits), valid range 4–16
        """
        if not (4 <= p <= 16):
            raise ValueError("Precision p must be between 4 and 16")
        self.p = p
        self.m = 1 << p
        self.registers = [0] * self.m
        self.alpha = self._get_alpha()
        self.small_range_correction = 5 * self.m / 2

    def _get_alpha(self) -> float:
        if self.m == 16:
            return 0.673
        elif self.m == 32:
            return 0.697
        elif self.m == 64:
            return 0.709
        return 0.7213 / (1 + 1.079 / self.m)

    def add(self, item: str):
        """Add an item to the HyperLogLog registers."""
        x = mmh3.hash(str(item), signed=False)
        j = x & (self.m - 1)
        w = x >> self.p
        self.registers[j] = max(self.registers[j], self._rho(w))

    def _rho(self, w: int) -> int:
        """Position of leftmost 1-bit."""
        return w.bit_length() if w > 0 else self.p + 1

    def count(self) -> float:
        """Return the estimated cardinality."""
        Z = sum(2.0 ** -r for r in self.registers)
        E = self.alpha * (self.m ** 2) / Z
        # Small range correction
        if E <= self.small_range_correction:
            V = self.registers.count(0)
            if V > 0:
                return self.m * math.log(self.m / V)
        return E

def load_ip_addresses(path: str) -> list:
    """Load valid IPv4 addresses from a log file.
       Handles both JSON lines with 'remote_addr' and plain-text logs."""
    ips = []
    pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            ip = None
            # Try JSON format
            if line.startswith('{') and line.endswith('}'):
                try:
                    record = json.loads(line)
                    ip = record.get('remote_addr')
                except json.JSONDecodeError:
                    ip = None
            # Fallback to whitespace-split format
            if ip is None:
                parts = line.split()
                if parts:
                    ip = parts[0]
            # Validate and append
            if ip and pattern.match(ip):
                ips.append(ip)
    return ips

def exact_unique_count(ips: list) -> int:
    """Return exact count of unique IPs using set."""
    return len(set(ips))

def hll_unique_count(ips: list, p: int = 14) -> float:
    """Return approximate count of unique IPs using HyperLogLog."""
    hll = HyperLogLog(p=p)
    for ip in ips:
        hll.add(ip)
    return hll.count()

if __name__ == "__main__":
    log_path = "/Users/admin/PycharmProjects/Algo/lms-stage-access.log"

    # Load and clean data
    start_load = time.time()
    ip_list = load_ip_addresses(log_path)
    load_time = time.time() - start_load

    # Exact unique count
    start_exact = time.time()
    exact = exact_unique_count(ip_list)
    time_exact = time.time() - start_exact

    # HyperLogLog estimate
    start_hll = time.time()
    estimate = hll_unique_count(ip_list, p=14)
    time_hll = time.time() - start_hll

    # Print comparison results
    print(f"Loaded {len(ip_list)} valid IPs in {load_time:.2f}s")
    print("Comparison results:")
    print(f"{'':<25}{'Exact Count':>15}{'HyperLogLog':>15}")
    print(f"{'Unique elements':<25}{exact:>15.0f}{estimate:>15.0f}")
    print(f"{'Execution time (s)':<25}{time_exact:>15.2f}{time_hll:>15.2f}")

# (base) admin@CrossFil-MBP ~ % python /Users/admin/PycharmProjects/Algo/hw_5_2.py
# Loaded 29553 valid IPs in 0.44s
# Comparison results:
#                              Exact Count    HyperLogLog
# Unique elements                       28             28
# Execution time (s)                  0.00           0.02