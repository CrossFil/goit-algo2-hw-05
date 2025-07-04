## Task 1. Password Uniqueness Check Using a Bloom Filter

**Objective**  
Determine whether a password has been used before without storing the actual passwords, by means of a Bloom filter.

**Technical Requirements**  
1. **BloomFilter class**  
   - **Constructor**  
     - `size`: total number of bits in the filter  
     - `num_hashes`: number of hash functions  
   - **Methods**  
     - `add(item: str)`: set bits corresponding to the item  
     - `__contains__(item: str) -> bool`: return `True` if item is possibly present, `False` if definitely absent  

2. **check_password_uniqueness function**  
   - **Inputs**  
     - an instance of `BloomFilter` preloaded with existing passwords  
     - a list of new passwords to check  
   - **Output**  
     - a mapping `{ password: status }` where `status` is one of:  
       - `"already used"`  
       - `"unique"`  
       - `"invalid value"` (for empty or non‐string inputs)  

3. **Data handling**  
   - Treat passwords strictly as strings  
   - Handle empty or non‐string inputs gracefully  

4. **Performance**  
   - Use minimal memory (bit array only)  
   - Ensure constant‑time add/check operations  


## Task 2. Comparing HyperLogLog vs. Exact Unique Count

**Objective**  
Write a Python script that loads IP addresses from a real log file, computes the exact number of unique addresses using a set, estimates the cardinality with HyperLogLog, and compares both methods by execution time.

**Technical Requirements**  
1. **Data Loading**  
   - Read `lms-stage-access.log` from `/Users/admin/PycharmProjects/Algo/`  
   - Ignore malformed lines  
2. **Exact Count**  
   - Implement `exact_unique_count(ips: list) -> int` using a Python `set`  
3. **HyperLogLog Estimate**  
   - Implement a `HyperLogLog` class (precision parameter `p`) with methods:  
     - `add(item: str)`  
     - `count() -> float`  
   - Implement `hll_unique_count(ips: list, p: int) -> float`  
4. **Performance Measurement**  
   - Measure and record:  
     - Time to load and clean the IP list  
     - Time to compute the exact count  
     - Time to compute the HLL estimate  
5. **Results Presentation**  
   - Print a table with:  
     - **Unique elements** (exact vs. HLL)  
     - **Execution time (s)** for each method  

