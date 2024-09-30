import time
import random
import string
import tracemalloc


class TestTrie:
    def __init__(self, trie_class):
        self.trie = trie_class()

    def test_insertion_search(self):
        """
        Test insertion and search correctness.
        """
        print("-- Test: Insertion and Search --")
        self.trie.insert("ABC123")
        self.trie.insert("XYZ789")
        self.trie.insert("A1BCD7")

        assert "ABC123" in self.trie.search("ABC"), "ABC123 should be found"
        assert "XYZ789" in self.trie.search("XYZ"), "XYZ789 should be found"
        assert "A1BCD7" in self.trie.search("A1B"), "A1BCD7 should be found"

        print("Passed: Insertion and Search")

    def test_custom_plates(self):
        """
        Test insertion of custom plates with mixed alphanumeric formats.
        """
        print("\n-- Test: Custom Plates --")
        self.trie.insert("123ABC")
        self.trie.insert("XYZ123")
        self.trie.insert("DEF456")

        assert "123ABC" in self.trie.search("123"), "123ABC should be found"
        assert "XYZ123" in self.trie.search("XYZ"), "XYZ123 should be found"
        assert "DEF456" in self.trie.search("DEF"), "DEF456 should be found"

        print("Passed: Custom Plates")

    def test_deletion(self):
        """
        Test deletion and verify correctness.
        """
        print("\n-- Test: Deletion --")
        self.trie.insert("DELETE123")
        assert "DELETE123" in self.trie.search("DELETE"), "DELETE123 should be found"

        self.trie.delete("DELETE123")
        assert "DELETE123" not in self.trie.search("DELETE"), "DELETE123 should be deleted"

        print("Passed: Deletion")

    def test_edge_cases(self):
        """
        Test various edge cases, such as empty string insertion, search for non-existent plates.
        """
        print("\n-- Test: Edge Cases --")
        self.trie.insert("")  # Test empty string
        assert len(self.trie.search("")) == 0, "Empty string should not result in any plates"

        assert "NONEXISTENT" not in self.trie.search("NON"), "Non-existent plates should not be found"

        print("Passed: Edge Cases")

    def test_large_dataset(self, num_plates=100000):
        """
        Insert a large dataset to test performance and scalability.
        """
        print(f"\n --Test: Large Dataset with {num_plates} plates --")
        start_time = time.time()

        # Generate random license plates
        for _ in range(num_plates):
            random_plate = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            self.trie.insert(random_plate)

        duration = time.time() - start_time
        print(f"Time to insert {num_plates} plates: {duration:.5f} seconds")

        # Randomly search for some plates
        search_time_start = time.time()
        for _ in range(100):
            prefix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
            self.trie.search(prefix)
        search_duration = time.time() - search_time_start
        print(f"Time to perform 100 searches: {search_duration:.5f} seconds")

        print("Passed: Large Dataset")

    def stress_test_prefix_collision(self):
        """
        Insert plates with similar prefixes to test deep prefix collisions.
        """
        print("\n-- Test: Prefix Collision Stress Test --")
        self.trie = CompressedTrie() # Give a fresh Trie data structure to prevent previous inputs from messing with the test
        prefix = "NLZ"
        for i in range(1000):
            plate = prefix + str(i).zfill(3)
            self.trie.insert(plate)
        assert len(self.trie.search("NLZ")) == 1000, "All 1000 plates with prefix 'NLZ' should be found"

        print("Passed: Prefix Collision Stress Test")

    def test_memory_usage(self, num_plates=100000):
        print(f"\n-- Test: Memory Usage with {num_plates} plates --")

        tracemalloc.start()

        self.trie = CompressedTrie() # Give a fresh Trie data structure to prevent previous inputs from messing with the test

        start_time = time.time()

        for _ in range(num_plates):
            random_plate = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            self.trie.insert(random_plate)

        duration = time.time() - start_time

        current, peak = tracemalloc.get_traced_memory()

        tracemalloc.stop()

        print(f"Time to insert {num_plates} plates: {duration:.2f} seconds")
        print(f"Current memory usage: {current / 10 ** 6:.2f} MB; Peak memory usage: {peak / 10 ** 6:.2f} MB")

        print("Passed: Memory Usage Test")


# Example Usage of the Test Suite
if __name__ == "__main__":
    from feature_data_structures.plate_lookup_registry import CompressedTrie  # Import your optimized Trie class

    test_trie = TestTrie(CompressedTrie)

    # Correctness Tests
    test_trie.test_insertion_search()
    test_trie.test_custom_plates()
    test_trie.test_deletion()
    test_trie.test_edge_cases()

    # Performance Tests
    test_trie.test_large_dataset(100000)  # Test with 100,000 plates

    # Stress Tests
    test_trie.stress_test_prefix_collision()
    test_trie.test_memory_usage(100000)
