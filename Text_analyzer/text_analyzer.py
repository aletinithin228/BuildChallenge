"""
Text Document Analyzer
A comprehensive tool for analyzing text documents and generating word frequency statistics.
"""

import re
from typing import Dict, List, Tuple
from collections import Counter


class TextReader:
    """Reads and normalizes file content."""
    
    def __init__(self, file_path: str):
        """
        Initialize TextReader with a file path.
        
        Args:
            file_path: Path to the text file to analyze
        """
        self.file_path = file_path
        self.raw_content = ""
        self.normalized_content = ""
    
    def read_file(self) -> str:
        """
        Read the content from the file.
        
        Returns:
            Raw file content as string
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            IOError: If there's an error reading the file
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                self.raw_content = file.read()
            return self.raw_content
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {self.file_path}")
        except Exception as e:
            raise IOError(f"Error reading file: {str(e)}")
    
    def normalize_text(self, text: str) -> str:
        """
        Normalize text by converting to lowercase and removing punctuation.
        Keeps only alphanumeric characters and spaces.
        
        Args:
            text: Raw text to normalize
            
        Returns:
            Normalized text string
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove all non-alphanumeric characters except spaces
        # Keep only letters, numbers, and spaces
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        
        # Replace multiple spaces with single space
        text = re.sub(r'\s+', ' ', text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        self.normalized_content = text
        return text
    
    def get_normalized_content(self) -> str:
        """
        Read and normalize the file content.
        
        Returns:
            Normalized content
        """
        self.read_file()
        return self.normalize_text(self.raw_content)


class WordCounter:
    """Tokenizes text and counts word frequencies."""
    
    # Common stop words to exclude (at least 20)
    STOP_WORDS = {
        'the', 'and', 'is', 'at', 'which', 'on', 'a', 'an', 'as', 'are',
        'was', 'were', 'been', 'be', 'have', 'has', 'had', 'do', 'does',
        'did', 'of', 'to', 'in', 'for', 'it', 'with', 'that', 'this',
        'by', 'from', 'or', 'but'
    }
    
    def __init__(self, text: str):
        """
        Initialize WordCounter with normalized text.
        
        Args:
            text: Normalized text to analyze
        """
        self.text = text
        self.words: List[str] = []
        self.word_frequencies: Dict[str, int] = {}
    
    def tokenize(self) -> List[str]:
        """
        Tokenize text into individual words.
        Ignores words with fewer than 3 characters.
        
        Returns:
            List of valid words
        """
        # Split text into words
        all_words = self.text.split()
        
        # Filter: keep only words with 3+ characters and not in stop words
        self.words = [
            word for word in all_words 
            if len(word) >= 3 and word not in self.STOP_WORDS
        ]
        
        return self.words
    
    def count_frequencies(self) -> Dict[str, int]:
        """
        Count frequency of each unique word.
        
        Returns:
            Dictionary mapping words to their frequencies
        """
        if not self.words:
            self.tokenize()
        
        self.word_frequencies = dict(Counter(self.words))
        return self.word_frequencies
    
    def get_word_frequencies(self) -> Dict[str, int]:
        """
        Get word frequency dictionary (compute if not already done).
        
        Returns:
            Dictionary of word frequencies
        """
        if not self.word_frequencies:
            self.count_frequencies()
        return self.word_frequencies


class StatisticsReport:
    """Generates formatted statistics reports."""
    
    def __init__(self, word_counter: WordCounter):
        """
        Initialize StatisticsReport with a WordCounter.
        
        Args:
            word_counter: WordCounter instance with analyzed text
        """
        self.word_counter = word_counter
        self.word_frequencies = word_counter.get_word_frequencies()
        self.all_words = word_counter.words
    
    def get_total_word_count(self) -> int:
        """
        Calculate total word count (including duplicates).
        
        Returns:
            Total number of words
        """
        return len(self.all_words)
    
    def get_unique_word_count(self) -> int:
        """
        Calculate unique word count.
        
        Returns:
            Number of unique words
        """
        return len(self.word_frequencies)
    
    def get_average_word_length(self) -> float:
        """
        Calculate average word length.
        
        Returns:
            Average length of words (rounded to 2 decimal places)
        """
        if not self.all_words:
            return 0.0
        
        total_length = sum(len(word) for word in self.all_words)
        return round(total_length / len(self.all_words), 2)
    
    def get_longest_word(self) -> str:
        """
        Find the longest word.
        
        Returns:
            Longest word in the text
        """
        if not self.all_words:
            return ""
        
        return max(self.all_words, key=len)
    
    def get_most_frequent_word(self) -> Tuple[str, int]:
        """
        Find the most frequent word.
        
        Returns:
            Tuple of (word, frequency)
        """
        if not self.word_frequencies:
            return ("", 0)
        
        most_frequent = max(self.word_frequencies.items(), key=lambda x: x[1])
        return most_frequent
    
    def get_top_n_words(self, n: int) -> List[Tuple[str, int]]:
        """
        Get the top N most frequent words sorted by count descending.
        
        Args:
            n: Number of top words to return
            
        Returns:
            List of (word, frequency) tuples sorted by frequency descending
        """
        sorted_words = sorted(
            self.word_frequencies.items(),
            key=lambda x: (-x[1], x[0])  # Sort by frequency desc, then alphabetically
        )
        return sorted_words[:n]
    
    def get_words_starting_with(self, prefix: str) -> List[str]:
        """
        Get words starting with a specific prefix, sorted alphabetically.
        
        Args:
            prefix: Prefix to search for (case-insensitive)
            
        Returns:
            Sorted list of matching words
        """
        prefix = prefix.lower()
        matching_words = [
            word for word in self.word_frequencies.keys()
            if word.startswith(prefix)
        ]
        return sorted(matching_words)
    
    def generate_report(self) -> str:
        """
        Generate a formatted statistics report.
        
        Returns:
            Formatted report as string
        """
        most_freq_word, most_freq_count = self.get_most_frequent_word()
        
        report = []
        report.append("=" * 60)
        report.append("TEXT ANALYSIS REPORT")
        report.append("=" * 60)
        report.append("")
        report.append("GENERAL STATISTICS:")
        report.append("-" * 60)
        report.append(f"Total Word Count:        {self.get_total_word_count()}")
        report.append(f"Unique Word Count:       {self.get_unique_word_count()}")
        report.append(f"Average Word Length:     {self.get_average_word_length()}")
        report.append(f"Longest Word:            {self.get_longest_word()}")
        report.append(f"Most Frequent Word:      {most_freq_word} ({most_freq_count} occurrences)")
        report.append("")
        report.append("TOP 10 MOST FREQUENT WORDS:")
        report.append("-" * 60)
        
        top_words = self.get_top_n_words(10)
        for i, (word, count) in enumerate(top_words, 1):
            report.append(f"{i:2d}. {word:<20s} {count:>5d}")
        
        report.append("")
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def export_report(self, output_file_path: str) -> None:
        """
        Write all statistics to a formatted text file.
        
        Args:
            output_file_path: Path to output file
            
        Raises:
            IOError: If there's an error writing the file
        """
        try:
            report = self.generate_report()
            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.write(report)
        except Exception as e:
            raise IOError(f"Error writing report file: {str(e)}")


def analyze_text_file(input_file: str, output_file: str = None) -> StatisticsReport:
    """
    Main function to analyze a text file and optionally export report.
    
    Args:
        input_file: Path to input text file
        output_file: Optional path to output report file
        
    Returns:
        StatisticsReport instance with all analysis
    """
    # Read and normalize text
    reader = TextReader(input_file)
    normalized_text = reader.get_normalized_content()
    
    # Count word frequencies
    counter = WordCounter(normalized_text)
    counter.tokenize()
    counter.count_frequencies()
    
    # Generate statistics
    report = StatisticsReport(counter)
    
    # Export if output file specified
    if output_file:
        report.export_report(output_file)
    
    return report


if __name__ == "__main__":
    # Example usage
    try:
        report = analyze_text_file("sample_text.txt", "analysis_report.txt")
        print(report.generate_report())
    except Exception as e:
        print(f"Error: {str(e)}")
