"""
Unit tests for Text Document Analyzer
Tests all core functionality including edge cases
"""

import unittest
import os
import tempfile
from text_analyzer import TextReader, WordCounter, StatisticsReport, analyze_text_file


class TestTextReader(unittest.TestCase):
    """Test cases for TextReader class"""
    
    def setUp(self):
        """Create temporary test files"""
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, "test.txt")
        
    def tearDown(self):
        """Clean up temporary files"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        os.rmdir(self.test_dir)
    
    def test_read_file_success(self):
        """Test successful file reading"""
        content = "Hello World! This is a test."
        with open(self.test_file, 'w') as f:
            f.write(content)
        
        reader = TextReader(self.test_file)
        result = reader.read_file()
        self.assertEqual(result, content)
    
    def test_read_file_not_found(self):
        """Test file not found exception"""
        reader = TextReader("nonexistent.txt")
        with self.assertRaises(FileNotFoundError):
            reader.read_file()
    
    def test_normalize_text_lowercase(self):
        """Test text normalization converts to lowercase"""
        reader = TextReader(self.test_file)
        result = reader.normalize_text("HELLO World")
        self.assertEqual(result, "hello world")
    
    def test_normalize_text_remove_punctuation(self):
        """Test punctuation removal"""
        reader = TextReader(self.test_file)
        result = reader.normalize_text("Hello, World! How's it going?")
        self.assertEqual(result, "hello world how s it going")
    
    def test_normalize_text_multiple_spaces(self):
        """Test multiple spaces are reduced to single space"""
        reader = TextReader(self.test_file)
        result = reader.normalize_text("Hello    World   Test")
        self.assertEqual(result, "hello world test")
    
    def test_normalize_text_special_characters(self):
        """Test special characters are removed"""
        reader = TextReader(self.test_file)
        result = reader.normalize_text("Hello@World#123$Test%")
        self.assertEqual(result, "hello world 123 test")
    
    def test_get_normalized_content(self):
        """Test complete read and normalize workflow"""
        content = "Hello, World! This is a TEST."
        with open(self.test_file, 'w') as f:
            f.write(content)
        
        reader = TextReader(self.test_file)
        result = reader.get_normalized_content()
        self.assertEqual(result, "hello world this is a test")


class TestWordCounter(unittest.TestCase):
    """Test cases for WordCounter class"""
    
    def test_tokenize_basic(self):
        """Test basic tokenization"""
        text = "hello world test example"
        counter = WordCounter(text)
        result = counter.tokenize()
        self.assertEqual(result, ["hello", "world", "test", "example"])
    
    def test_tokenize_filter_short_words(self):
        """Test filtering words with fewer than 3 characters"""
        text = "a ab abc abcd"
        counter = WordCounter(text)
        result = counter.tokenize()
        self.assertEqual(result, ["abc", "abcd"])
    
    def test_tokenize_filter_stop_words(self):
        """Test filtering stop words"""
        text = "the quick brown fox and the lazy dog"
        counter = WordCounter(text)
        result = counter.tokenize()
        self.assertNotIn("the", result)
        self.assertNotIn("and", result)
        self.assertIn("quick", result)
        self.assertIn("brown", result)
    
    def test_count_frequencies_basic(self):
        """Test basic frequency counting"""
        text = "hello world hello test world hello"
        counter = WordCounter(text)
        counter.tokenize()
        result = counter.count_frequencies()
        self.assertEqual(result["hello"], 3)
        self.assertEqual(result["world"], 2)
        self.assertEqual(result["test"], 1)
    
    def test_count_frequencies_empty(self):
        """Test frequency counting with empty text"""
        text = ""
        counter = WordCounter(text)
        result = counter.count_frequencies()
        self.assertEqual(result, {})
    
    def test_get_word_frequencies_auto_compute(self):
        """Test auto-computation of frequencies"""
        text = "test test example"
        counter = WordCounter(text)
        # Don't call tokenize or count_frequencies manually
        result = counter.get_word_frequencies()
        self.assertEqual(result["test"], 2)
        self.assertEqual(result["example"], 1)


class TestStatisticsReport(unittest.TestCase):
    """Test cases for StatisticsReport class"""
    
    def setUp(self):
        """Create a WordCounter instance for testing"""
        text = "machine learning algorithms require data and computation power"
        self.counter = WordCounter(text)
        self.counter.tokenize()
        self.counter.count_frequencies()
        self.report = StatisticsReport(self.counter)
    
    def test_get_total_word_count(self):
        """Test total word count calculation"""
        # Text: "machine learning algorithms require data and computation power"
        # After filtering: machine, learning, algorithms, require, data, computation, power (7 words)
        self.assertEqual(self.report.get_total_word_count(), 7)
    
    def test_get_unique_word_count(self):
        """Test unique word count"""
        self.assertEqual(self.report.get_unique_word_count(), 7)
    
    def test_get_average_word_length(self):
        """Test average word length calculation"""
        avg_length = self.report.get_average_word_length()
        self.assertIsInstance(avg_length, float)
        self.assertGreater(avg_length, 0)
    
    def test_get_longest_word(self):
        """Test finding longest word"""
        longest = self.report.get_longest_word()
        # "algorithms" or "computation" are the longest (11 and 11 characters)
        self.assertIn(longest, ["algorithms", "computation"])
    
    def test_get_most_frequent_word(self):
        """Test finding most frequent word"""
        text = "test test test other other word"
        counter = WordCounter(text)
        counter.tokenize()
        counter.count_frequencies()
        report = StatisticsReport(counter)
        
        word, count = report.get_most_frequent_word()
        self.assertEqual(word, "test")
        self.assertEqual(count, 3)
    
    def test_get_top_n_words(self):
        """Test getting top N words"""
        text = "apple apple apple banana banana cherry"
        counter = WordCounter(text)
        counter.tokenize()
        counter.count_frequencies()
        report = StatisticsReport(counter)
        
        top_2 = report.get_top_n_words(2)
        self.assertEqual(len(top_2), 2)
        self.assertEqual(top_2[0][0], "apple")
        self.assertEqual(top_2[0][1], 3)
        self.assertEqual(top_2[1][0], "banana")
        self.assertEqual(top_2[1][1], 2)
    
    def test_get_top_n_words_more_than_available(self):
        """Test requesting more words than available"""
        top_100 = self.report.get_top_n_words(100)
        self.assertEqual(len(top_100), 7)  # Only 7 unique words
    
    def test_get_words_starting_with_prefix(self):
        """Test getting words with specific prefix"""
        text = "data database datascience computer computing"
        counter = WordCounter(text)
        counter.tokenize()
        counter.count_frequencies()
        report = StatisticsReport(counter)
        
        words = report.get_words_starting_with("dat")
        self.assertEqual(len(words), 3)
        self.assertIn("data", words)
        self.assertIn("database", words)
        self.assertIn("datascience", words)
    
    def test_get_words_starting_with_case_insensitive(self):
        """Test prefix search is case-insensitive"""
        text = "data database datascience"
        counter = WordCounter(text)
        counter.tokenize()
        counter.count_frequencies()
        report = StatisticsReport(counter)
        
        # Test that uppercase prefix works
        words = report.get_words_starting_with("DAT")
        self.assertEqual(len(words), 3)
        
        # Test lowercase prefix also works
        words_lower = report.get_words_starting_with("dat")
        self.assertEqual(words, words_lower)
    
    def test_get_words_starting_with_no_match(self):
        """Test prefix with no matches"""
        words = self.report.get_words_starting_with("xyz")
        self.assertEqual(words, [])
    
    def test_generate_report(self):
        """Test report generation"""
        report_text = self.report.generate_report()
        self.assertIsInstance(report_text, str)
        self.assertIn("TEXT ANALYSIS REPORT", report_text)
        self.assertIn("Total Word Count:", report_text)
        self.assertIn("Unique Word Count:", report_text)
    
    def test_export_report(self):
        """Test exporting report to file"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            output_file = f.name
        
        try:
            self.report.export_report(output_file)
            self.assertTrue(os.path.exists(output_file))
            
            with open(output_file, 'r') as f:
                content = f.read()
            self.assertIn("TEXT ANALYSIS REPORT", content)
        finally:
            if os.path.exists(output_file):
                os.remove(output_file)


class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflow"""
    
    def setUp(self):
        """Create temporary test files"""
        self.test_dir = tempfile.mkdtemp()
        self.input_file = os.path.join(self.test_dir, "input.txt")
        self.output_file = os.path.join(self.test_dir, "output.txt")
    
    def tearDown(self):
        """Clean up temporary files"""
        for file in [self.input_file, self.output_file]:
            if os.path.exists(file):
                os.remove(file)
        os.rmdir(self.test_dir)
    
    def test_analyze_text_file_complete_workflow(self):
        """Test complete analysis workflow"""
        content = """
        The quick brown fox jumps over the lazy dog.
        Machine learning is a subset of artificial intelligence.
        Data science involves statistics, programming, and domain knowledge.
        """
        
        with open(self.input_file, 'w') as f:
            f.write(content)
        
        report = analyze_text_file(self.input_file, self.output_file)
        
        # Check report is created
        self.assertIsInstance(report, StatisticsReport)
        
        # Check output file is created
        self.assertTrue(os.path.exists(self.output_file))
        
        # Check statistics are reasonable
        self.assertGreater(report.get_total_word_count(), 0)
        self.assertGreater(report.get_unique_word_count(), 0)
    
    def test_analyze_text_file_without_output(self):
        """Test analysis without export"""
        content = "test example data"
        
        with open(self.input_file, 'w') as f:
            f.write(content)
        
        report = analyze_text_file(self.input_file)
        
        # Check report is created
        self.assertIsInstance(report, StatisticsReport)
        
        # Check no output file is created
        self.assertFalse(os.path.exists(self.output_file))


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions"""
    
    def test_empty_text(self):
        """Test with empty text"""
        counter = WordCounter("")
        counter.tokenize()
        counter.count_frequencies()
        report = StatisticsReport(counter)
        
        self.assertEqual(report.get_total_word_count(), 0)
        self.assertEqual(report.get_unique_word_count(), 0)
        self.assertEqual(report.get_average_word_length(), 0.0)
        self.assertEqual(report.get_longest_word(), "")
        self.assertEqual(report.get_most_frequent_word(), ("", 0))
    
    def test_only_stop_words(self):
        """Test text with only stop words"""
        text = "the and is at which on a an as are"
        counter = WordCounter(text)
        counter.tokenize()
        counter.count_frequencies()
        report = StatisticsReport(counter)
        
        self.assertEqual(report.get_total_word_count(), 0)
        self.assertEqual(report.get_unique_word_count(), 0)
    
    def test_only_short_words(self):
        """Test text with only short words"""
        text = "a ab to in of at"
        counter = WordCounter(text)
        counter.tokenize()
        counter.count_frequencies()
        report = StatisticsReport(counter)
        
        self.assertEqual(report.get_total_word_count(), 0)
    
    def test_unicode_characters(self):
        """Test handling of unicode characters"""
        reader = TextReader("")
        result = reader.normalize_text("café résumé naïve")
        # Non-ASCII characters should be removed
        self.assertNotIn("é", result)
    
    def test_numbers_in_text(self):
        """Test that numbers are handled correctly"""
        text = "test123 abc456 xyz789"
        counter = WordCounter(text)
        counter.tokenize()
        freqs = counter.count_frequencies()
        # Numbers should be kept as part of alphanumeric words
        self.assertIn("test123", freqs)
        self.assertIn("abc456", freqs)
        self.assertIn("xyz789", freqs)
    
    def test_single_word(self):
        """Test with single valid word"""
        text = "hello"
        counter = WordCounter(text)
        counter.tokenize()
        counter.count_frequencies()
        report = StatisticsReport(counter)
        
        self.assertEqual(report.get_total_word_count(), 1)
        self.assertEqual(report.get_unique_word_count(), 1)
        self.assertEqual(report.get_longest_word(), "hello")
        self.assertEqual(report.get_most_frequent_word(), ("hello", 1))
    
    def test_all_same_word(self):
        """Test with all identical words"""
        text = "test test test test test"
        counter = WordCounter(text)
        counter.tokenize()
        counter.count_frequencies()
        report = StatisticsReport(counter)
        
        self.assertEqual(report.get_total_word_count(), 5)
        self.assertEqual(report.get_unique_word_count(), 1)
        self.assertEqual(report.get_most_frequent_word(), ("test", 5))
    
    def test_exact_3_character_words(self):
        """Test that 3-character words are included (boundary)"""
        text = "abc def ghi"
        counter = WordCounter(text)
        counter.tokenize()
        words = counter.words
        
        self.assertEqual(len(words), 3)
        self.assertIn("abc", words)
        self.assertIn("def", words)
        self.assertIn("ghi", words)
    
    def test_get_top_n_with_zero(self):
        """Test getTopNWords with n=0"""
        text = "apple banana cherry"
        counter = WordCounter(text)
        counter.tokenize()
        counter.count_frequencies()
        report = StatisticsReport(counter)
        
        result = report.get_top_n_words(0)
        self.assertEqual(result, [])
    
    def test_get_top_n_with_negative(self):
        """Test getTopNWords with negative n"""
        text = "apple banana cherry"
        counter = WordCounter(text)
        counter.tokenize()
        counter.count_frequencies()
        report = StatisticsReport(counter)
        
        result = report.get_top_n_words(-5)
        self.assertEqual(result, [])
    
    def test_tie_in_frequency_alphabetical_order(self):
        """Test that ties are broken alphabetically"""
        text = "zebra apple banana zebra apple banana"
        counter = WordCounter(text)
        counter.tokenize()
        counter.count_frequencies()
        report = StatisticsReport(counter)
        
        top_words = report.get_top_n_words(3)
        # All have frequency 2, should be alphabetical
        self.assertEqual(top_words[0][0], "apple")
        self.assertEqual(top_words[1][0], "banana")
        self.assertEqual(top_words[2][0], "zebra")
    
    def test_prefix_empty_string(self):
        """Test prefix search with empty string"""
        text = "apple banana cherry"
        counter = WordCounter(text)
        counter.tokenize()
        counter.count_frequencies()
        report = StatisticsReport(counter)
        
        # Empty prefix should return all words
        words = report.get_words_starting_with("")
        self.assertEqual(len(words), 3)
    
    def test_very_long_word(self):
        """Test with very long word"""
        long_word = "a" * 100
        text = f"short {long_word} medium"
        counter = WordCounter(text)
        counter.tokenize()
        counter.count_frequencies()
        report = StatisticsReport(counter)
        
        self.assertEqual(report.get_longest_word(), long_word)
        self.assertEqual(len(report.get_longest_word()), 100)
    
    def test_whitespace_only(self):
        """Test with only whitespace"""
        text = "     \n\n\t\t    "
        counter = WordCounter(text)
        counter.tokenize()
        counter.count_frequencies()
        report = StatisticsReport(counter)
        
        self.assertEqual(report.get_total_word_count(), 0)
    
    def test_mixed_case_same_word(self):
        """Test that mixed case words are counted as same"""
        # Use TextReader to normalize first
        reader = TextReader("")
        normalized = reader.normalize_text("Hello HELLO hello HeLLo")
        
        counter = WordCounter(normalized)
        counter.tokenize()
        counter.count_frequencies()
        
        # All should be counted as "hello"
        self.assertEqual(counter.word_frequencies["hello"], 4)
        self.assertEqual(len(counter.word_frequencies), 1)


if __name__ == "__main__":
    unittest.main()


class TestAdditionalEdgeCases(unittest.TestCase):
    """Additional edge cases for comprehensive testing"""
    
    def test_words_exactly_at_stop_word_boundary(self):
        """Test words that are exactly 3 characters and are stop words"""
        # "the", "and" are stop words but different lengths
        # "was", "are", "has", "had", "did" are 3-char stop words
        text = "was are has had did run cat dog"
        counter = WordCounter(text)
        counter.tokenize()
        
        # Stop words should be filtered even if they're 3+ chars
        self.assertNotIn("was", counter.words)
        self.assertNotIn("are", counter.words)
        self.assertNotIn("has", counter.words)
        
        # Non-stop words should be included
        self.assertIn("run", counter.words)
        self.assertIn("cat", counter.words)
        self.assertIn("dog", counter.words)
    
    def test_export_report_creates_file(self):
        """Test that export actually creates the file"""
        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "test.txt")
            output_file = os.path.join(tmpdir, "report.txt")
            
            with open(input_file, 'w') as f:
                f.write("testing export functionality works correctly")
            
            report = analyze_text_file(input_file, output_file)
            
            # File should exist
            self.assertTrue(os.path.exists(output_file))
            
            # File should have content
            with open(output_file, 'r') as f:
                content = f.read()
            self.assertGreater(len(content), 0)
            self.assertIn("TEXT ANALYSIS REPORT", content)
    
    def test_multiple_punctuation_marks(self):
        """Test multiple consecutive punctuation marks"""
        reader = TextReader("")
        result = reader.normalize_text("Hello!!! World??? Test... Done---")
        # All punctuation should be removed
        self.assertEqual(result, "hello world test done")
    
    def test_words_with_apostrophes(self):
        """Test contractions and possessives"""
        reader = TextReader("")
        result = reader.normalize_text("don't can't won't Mary's")
        # Apostrophes should be removed, splitting words
        self.assertNotIn("'", result)
        self.assertIn("don", result)
        self.assertIn("mary", result)
    
    def test_hyphenated_words(self):
        """Test hyphenated words"""
        reader = TextReader("")
        result = reader.normalize_text("well-known state-of-the-art")
        # Hyphens should be removed/converted to spaces
        self.assertNotIn("-", result)
    
    def test_statistics_with_duplicate_frequencies(self):
        """Test statistics when multiple words have same frequency"""
        text = "apple apple banana banana cherry cherry"
        counter = WordCounter(text)
        counter.tokenize()
        counter.count_frequencies()
        report = StatisticsReport(counter)
        
        # All words have frequency 2
        top_3 = report.get_top_n_words(3)
        self.assertEqual(len(top_3), 3)
        # Should be alphabetically ordered when frequencies are same
        self.assertEqual(top_3[0][0], "apple")
        self.assertEqual(top_3[1][0], "banana")
        self.assertEqual(top_3[2][0], "cherry")
    
    def test_get_longest_word_multiple_same_length(self):
        """Test longest word when multiple words have same length"""
        text = "test runs jump walk"  # all 4 characters
        counter = WordCounter(text)
        counter.tokenize()
        counter.count_frequencies()
        report = StatisticsReport(counter)
        
        longest = report.get_longest_word()
        # Should return one of them
        self.assertIn(longest, ["test", "runs", "jump", "walk"])
        self.assertEqual(len(longest), 4)
    
    def test_average_word_length_precision(self):
        """Test that average word length has correct precision"""
        text = "cat dog bird"  # lengths: 3, 3, 4 = avg 3.33...
        counter = WordCounter(text)
        counter.tokenize()
        counter.count_frequencies()
        report = StatisticsReport(counter)
        
        avg = report.get_average_word_length()
        # Should be rounded to 2 decimal places
        self.assertAlmostEqual(avg, 3.33, places=2)
        # Check it's actually rounded, not truncated
        self.assertEqual(avg, 3.33)
    
    def test_file_with_only_newlines(self):
        """Test file containing only newlines"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("\n\n\n\n\n")
            temp_file = f.name
        
        try:
            reader = TextReader(temp_file)
            content = reader.get_normalized_content()
            counter = WordCounter(content)
            counter.tokenize()
            
            self.assertEqual(len(counter.words), 0)
        finally:
            os.remove(temp_file)
    
    def test_get_words_starting_with_special_chars(self):
        """Test prefix search handles lowercase conversion"""
        text = "apple apricot banana"
        counter = WordCounter(text)
        counter.tokenize()
        counter.count_frequencies()
        report = StatisticsReport(counter)
        
        # Special chars in prefix won't match anything (by design)
        # because words don't have special chars after normalization
        words = report.get_words_starting_with("@#$ap")
        self.assertEqual(len(words), 0)
        
        # But normal prefix works fine
        words = report.get_words_starting_with("ap")
        self.assertEqual(len(words), 2)
    
    def test_counting_with_numbers_only(self):
        """Test words that are only numbers"""
        text = "123 456 789 abc123"
        counter = WordCounter(text)
        counter.tokenize()
        freqs = counter.count_frequencies()
        
        # Pure numbers 3+ digits should be kept
        self.assertIn("123", freqs)
        self.assertIn("456", freqs)
        self.assertIn("789", freqs)
        self.assertIn("abc123", freqs)
    
    def test_report_generation_format(self):
        """Test that report has required sections"""
        text = "machine learning data science artificial intelligence"
        counter = WordCounter(text)
        counter.tokenize()
        counter.count_frequencies()
        report = StatisticsReport(counter)
        
        report_text = report.generate_report()
        
        # Check all required sections exist
        self.assertIn("TEXT ANALYSIS REPORT", report_text)
        self.assertIn("GENERAL STATISTICS:", report_text)
        self.assertIn("Total Word Count:", report_text)
        self.assertIn("Unique Word Count:", report_text)
        self.assertIn("Average Word Length:", report_text)
        self.assertIn("Longest Word:", report_text)
        self.assertIn("Most Frequent Word:", report_text)
        self.assertIn("TOP 10 MOST FREQUENT WORDS:", report_text)
