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
Created as part of Assignment 2 - Text Document Analyzer

## Version History

- v1.0.0 (2024): Initial release with core functionality
