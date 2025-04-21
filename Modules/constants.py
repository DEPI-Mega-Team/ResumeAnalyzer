import os

workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Patterns
NAME_PATTERN = r'[A-Z][a-z]+'
NOT_ALPHA_NUMERIC = r'[^a-zA-Z\d]'
OBJECT_PATTERN = r"\b\w+(?:[- ]\w+)*\b"
NUMBER = r'\d+'
PHONE_PATTERN = r'\(?\+?\d{1,3}\)?[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}'
URL_PATTERN = r'(?:http[s]?:\/\/.)?(?:www\.)?[-a-zA-Z0-9@%._\+~#=]{2,256}\.[a-z]{2,6}\b(?:[-a-zA-Z0-9@:%_\+.~#?&\/\/=]*)'
EMAIL_PATTERN = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
SKILL_PATTERN = r"[Cc](?:\+\+|\#)?|" + OBJECT_PATTERN

# Scholar Keywords
SCHOLAR_KEYWORDS = r'[Uu]niversity|[Cc]ollege|[Ii]nstitute'
OBJECT_MULTIPLE_NAME_PATTERN = f"(?:{NAME_PATTERN} )+"
COLLEGE_PATTERN = r'\b(?:' + f"(?:{SCHOLAR_KEYWORDS})" + r' of (?:[Tt]he )?' + f"(?:{OBJECT_MULTIPLE_NAME_PATTERN})?" + NAME_PATTERN + ')|(?:' + OBJECT_MULTIPLE_NAME_PATTERN + SCHOLAR_KEYWORDS + r')\b'

# Education (Upper Case Mandatory)
EDUCATION = {
            'BE', 'B.E.', 'B.E', 'BS', 'B.S',  # Bachelor of Engineering, Bachelor of Science
            'ME', 'M.E', 'M.E.', 'MS', 'M.S',  # Master of Engineering, Master of Science
            'BTECH', 'MTECH',                   # Bachelor of Technology, Master of Technology
            'SSC', 'HSC',                       # Secondary School Certificate, Higher Secondary Certificate
            'CBSE', 'ICSE',                     # Central Board of Secondary Education, Indian Certificate of Secondary Education
            'X', 'XII'                          # 10th Standard, 12th Standard
            }

DEGREE = {
    'high_school': {
        'High School', 'Secondary School',  # Secondary School Certificate, Higher Secondary Certificate
    },
    'diploma': {
        'Diploma'  # Diploma qualifications
    },
    'bachelor': {
        'Bachelor', 'Undergraduate',  # General bachelor terms
    },
    'master': {
        'Master', 'Graduate', 'Postgraduate',  # General master terms
    },
    'phd': {
        'PhD', 'Doctorate'  # Doctorate level
    },
}


# For finding date ranges
MONTHS_SHORT = r'''(jan)|(feb)|(mar)|(apr)|(may)|(jun)|(jul)|(aug)|(sep)|(oct)|(nov)|(dec)'''
MONTHS_LONG = r'''(january)|(february)|(march)|(april)|(may)|(june)|(july)|(august)|(september)|(october)|(november)|(december)'''
MONTH = r'(' + MONTHS_SHORT + r'|' + MONTHS_LONG + r')'
YEAR = r'(((20|19)(\d{2})))'

RESUME_SECTIONS = [
                    'accomplishments',
                    'experience',
                    'volunteering',
                    'activities',
                    'education',
                    'interests',
                    'projects',
                    'professional experience',
                    'publications',
                    'skills',
                    'certifications',
                    'certificates',
                    'objective',
                    'career objective',
                    'summary',
                    'leadership',
                ]