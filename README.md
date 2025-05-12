# Resume Analyzer

Resume Analyzer is a tool designed to help you analyze and evaluate resumes efficiently. It extracts key information from resumes and provides insights to help you make informed hiring decisions.
This tool is based on [PyResParser](https://github.com/OmkarPathak/pyresparser) by [OmkarPathak](https://github.com/OmkarPathak)

# Improvements:

- Retrained the NLP model using spaCy v3, replacing the previous spaCy v2 model.
- Optimized the code to rely on a single model instead of two, improving performance and reducing complexity.
- Enhanced the NLP model to extract individual skills directly using a built-in custom component, eliminating the need for an external skill extractor function.
- Refactored and reorganized the codebase into separate folders (`Data`, `Model`, `Modules`) and files (`extractors`, `accumulators`, `constants`, `parser`) for better maintainability and readability.
- Improved and Optimized function implementations
- Enhanced regular expression patterns to accommodate more recent resume formats.
- Removed unnecessary commented lines to clean up the code.

# Features

- Extracts key information:
  - name
  - email
  - mobile numbers
  - role
  - locations
  - skills
  - college name
  - degree
  - experience (Year of Experience)
  - companies
  - links
  - number of pages
  - resume file format

- Supports resume formats PDF and DOCX.

# Installation

1. Clone the repository:

2. Make a Virtual Environment:
    ```bash
    python -m venv .venv
    ```
3. Install the required dependencies:
    ```bash
    pip install -r ./ResumeAnalyzer/requirements.txt
    ```

# Usage
1. Import the needed function from `resume_analyzer.py`:
    ```python
    from ResumeAnalyzer.resume_analyzer import init_parser
    ```
2. Begin Parsing:
    1. Initialize the parser object to load the necessary models and modules (e.g., loading the NLP model).
    2. Invoke the parsing method for each resume to be analyzed:
    *You can use the resume file path, or directly pass the resume text*
       ```python
       # Initialize Parser (Used only once)
       parser = init_parser()

       # Parse a resume
       resume = "/path/to/resume.docx"
       result = praser.parse(resume)```

# License

This tool is based on [PyResParser](https://github.com/OmkarPathak/pyresparser) by [OmkarPathak](https://github.com/OmkarPathak) and is licensed under the [GNU GPLv3](LICENSE).

*- Avaliable on PyPI Soon -*