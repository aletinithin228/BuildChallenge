# Text Document Analyzer

A comprehensive Python tool for analyzing text documents and generating detailed word frequency statistics.

## Overview

This project analyzes plain text files to provide insights into word usage patterns, frequency distributions, and various statistical metrics. It's designed for educational purposes, demonstrating file I/O operations, string manipulation, data structures, and object-oriented programming principles.

## Features

- **Text Normalization**: Converts text to lowercase and removes punctuation
- **Smart Tokenization**: Filters out short words (<3 characters) and common stop words
- **Frequency Analysis**: Counts occurrences of each unique word
- **Statistical Metrics**: Calculates total word count, unique words, average word length, and more
- **Flexible Querying**: Get top N words, search by prefix
- **Report Generation**: Creates formatted analysis reports and exports to file

## Project Structure

```
text-analyzer/
├── text_analyzer.py          # Main implementation
├── test_text_analyzer.py     # Comprehensive unit tests
├── sample_text.txt            # Sample text file (500+ words)
├── README.md                  # This file
└── requirements.txt           # Python dependencies
```

## Requirements

- Python 3.7 or higher
- No external dependencies (uses only Python standard library)

## Installation

1. Clone or download this project to your local machine

2. Navigate to the project directory:
```bash
cd text-analyzer
```

3. (Optional) Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. No additional packages needed - uses Python standard library only!

## Usage

### Basic Usage

```python
from text_analyzer import analyze_text_file

# Analyze a text file and export report
report = analyze_text_file("sample_text.txt", "analysis_report.txt")

# Print report to console
print(report.generate_report())
```

### Advanced Usage

```python
from text_analyzer import TextReader, WordCounter, StatisticsReport

# Step 1: Read and normalize text
reader = TextReader("sample_text.txt")
normalized_text = reader.get_normalized_content()

# Step 2: Tokenize and count frequencies
counter = WordCounter(normalized_text)
counter.tokenize()
counter.count_frequencies()

# Step 3: Generate statistics
report = StatisticsReport(counter)

# Get specific statistics
print(f"Total words: {report.get_total_word_count()}")
print(f"Unique words: {report.get_unique_word_count()}")
print(f"Average word length: {report.get_average_word_length()}")
print(f"Longest word: {report.get_longest_word()}")

# Get top 5 most frequent words
top_5 = report.get_top_n_words(5)
for word, count in top_5:
    print(f"{word}: {count}")

# Find words starting with "exp"
words = report.get_words_starting_with("exp")
print(f"Words starting with 'exp': {words}")

# Export report
report.export_report("my_report.txt")
```

### Command Line Usage

```bash
python text_analyzer.py
```

This will analyze `sample_text.txt` and create `analysis_report.txt`.

## Running Tests

Run the comprehensive test suite:

```bash
python -m unittest test_text_analyzer.py -v
```

Or run specific test classes:

```bash
# Test TextReader only
python -m unittest test_text_analyzer.TestTextReader -v

# Test WordCounter only
python -m unittest test_text_analyzer.TestWordCounter -v

# Test StatisticsReport only
python -m unittest test_text_analyzer.TestStatisticsReport -v
```

### Test Coverage

The test suite includes:
- **TextReader Tests**: File reading, normalization, error handling
- **WordCounter Tests**: Tokenization, filtering, frequency counting
- **StatisticsReport Tests**: All statistical methods and report generation
- **Integration Tests**: Complete workflow testing
- **Edge Cases**: Empty text, only stop words, unicode handling

## API Documentation

### TextReader Class

Reads and normalizes file content.

**Methods:**
- `__init__(file_path: str)`: Initialize with file path
- `read_file() -> str`: Read raw file content
- `normalize_text(text: str) -> str`: Normalize text (lowercase, remove punctuation)
- `get_normalized_content() -> str`: Read and normalize file in one step

### WordCounter Class

Tokenizes text and counts word frequencies.

**Methods:**
- `__init__(text: str)`: Initialize with normalized text
- `tokenize() -> List[str]`: Split text into words (filters short words and stop words)
- `count_frequencies() -> Dict[str, int]`: Count word occurrences
- `get_word_frequencies() -> Dict[str, int]`: Get frequency dictionary

**Class Attributes:**
- `STOP_WORDS`: Set of common words to exclude (20+ words)

### StatisticsReport Class

Generates formatted statistics reports.

**Methods:**
- `__init__(word_counter: WordCounter)`: Initialize with WordCounter instance
- `get_total_word_count() -> int`: Total words analyzed
- `get_unique_word_count() -> int`: Number of unique words
- `get_average_word_length() -> float`: Average word length (rounded to 2 decimals)
- `get_longest_word() -> str`: Longest word found
- `get_most_frequent_word() -> Tuple[str, int]`: Most common word and its count
- `get_top_n_words(n: int) -> List[Tuple[str, int]]`: Top N words by frequency
- `get_words_starting_with(prefix: str) -> List[str]`: Words matching prefix
- `generate_report() -> str`: Create formatted report
- `export_report(output_file_path: str) -> None`: Save report to file

## Sample Input/Output

### Input (sample_text.txt excerpt)
```
The Evolution of Space Exploration: From Dreams to Reality

Space exploration has captivated human imagination for centuries,
transforming from ancient stargazing into one of humanity's greatest
achievements...
```

### Output (analysis_report.txt)
```
============================================================
TEXT ANALYSIS REPORT
============================================================

GENERAL STATISTICS:
------------------------------------------------------------
Total Word Count:        523
Unique Word Count:       287
Average Word Length:     7.42
Longest Word:            telecommunications
Most Frequent Word:      exploration (15 occurrences)

TOP 10 MOST FREQUENT WORDS:
------------------------------------------------------------
 1. exploration                15
 2. space                      14
 3. human                       8
 4. missions                    6
 5. scientific                  5
 6. technology                  5
 7. systems                     4
 8. development                 4
 9. international               4
10. program                     4

============================================================
```

## Design Decisions & Assumptions

### Text Normalization
- **Lowercase conversion**: Ensures "Word" and "word" are counted as the same
- **Punctuation removal**: Keeps only alphanumeric characters and spaces
- **Multiple spaces**: Reduced to single spaces for clean tokenization

### Word Filtering
- **Minimum length**: Words must be 3+ characters (excludes "a", "to", "in", etc.)
- **Stop words**: Excludes 20+ common words that don't add analytical value
- **Case-insensitive**: All comparisons done in lowercase

### Frequency Counting
- **Dictionary/Map**: Uses Python dict for O(1) average lookup and insertion
- **Counter**: Leverages collections.Counter for efficient counting

### Sorting
- **Top N words**: Sorted by frequency (descending), then alphabetically for ties
- **Prefix search**: Results sorted alphabetically for easy reading

### File I/O
- **UTF-8 encoding**: Handles international characters
- **Error handling**: Specific exceptions for file not found vs. read errors
- **Resource management**: Uses context managers for automatic file closing

### Edge Cases Handled
- Empty files or text
- Files with only stop words
- Files with only short words
- Unicode/special characters
- Very large files (memory efficient tokenization)

## Limitations & Future Enhancements

### Current Limitations
- Loads entire file into memory (not suitable for multi-GB files)
- ASCII-focused (non-English characters are removed)
- Fixed stop word list (no customization)
- No stemming/lemmatization (e.g., "running" and "run" counted separately)

### Future Enhancements
- Stream processing for large files
- Configurable stop words
- Multi-language support
- Word stemming/lemmatization
- N-gram analysis
- Sentiment analysis
- Export to JSON, CSV, or Excel formats
- Visualization (word clouds, frequency charts)

## Contributing

Feel free to extend this project! Some ideas:
- Add support for PDF or DOCX files
- Implement parallel processing for large files
- Create a GUI interface
- Add more statistical metrics (median word length, word diversity score)

## License

This project is provided for educational purposes.

## Author

Created as part of Assignment 2 - Text Document Analyzer

## Version History

- v1.0.0 (2024): Initial release with core functionality
