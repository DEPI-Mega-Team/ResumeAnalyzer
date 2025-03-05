import os

# Name Entity Recognition Pattern #Todo: Add more patterns
NAME_PATTERN = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]
URL_PATTERN = r'(?:http[s]?:\/\/.)?(?:www\.)?[-a-zA-Z0-9@%._\+~#=]{2,256}\.[a-z]{2,6}\b(?:[-a-zA-Z0-9@:%_\+.~#?&\/\/=]*)'
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

# Education (Upper Case Mandatory)
EDUCATION = {
            'BE', 'B.E.', 'B.E', 'BS', 'B.S',  # Bachelor of Engineering, Bachelor of Science
            'ME', 'M.E', 'M.E.', 'MS', 'M.S',  # Master of Engineering, Master of Science
            'BTECH', 'MTECH',                   # Bachelor of Technology, Master of Technology
            'SSC', 'HSC',                       # Secondary School Certificate, Higher Secondary Certificate
            'CBSE', 'ICSE',                     # Central Board of Secondary Education, Indian Certificate of Secondary Education
            'X', 'XII'                          # 10th Standard, 12th Standard
            }

DEGREE = {'bachelor', 'master', 'phd', 'doctorate', 'associate',
            'diploma', 'certificate', 'graduate', 'undergraduate',
            'postgraduate', 'BE', 'B.E.', 'B.E', 'BS', 'B.S',  # Bachelor of Engineering, Bachelor of Science
            'ME', 'M.E', 'M.E.', 'MS', 'M.S',  # Master of Engineering, Master of Science
            'BTECH', 'MTECH',                   # Bachelor of Technology, Master of Technology
            'SSC', 'HSC',                       # Secondary School Certificate, Higher Secondary Certificate
            'CBSE', 'ICSE',                     # Central Board of Secondary Education, Indian Certificate of Secondary Education
            'X', 'XII'  
         }

NOT_ALPHA_NUMERIC = r'[^a-zA-Z\d]'
OBJECT_PATTERN = r"\b\w+(?:[- ]\w+)*\b"
NUMBER = r'\d+'

# For finding date ranges
MONTHS_SHORT = r'''(jan)|(feb)|(mar)|(apr)|(may)|(jun)|(jul)
                   |(aug)|(sep)|(oct)|(nov)|(dec)'''
MONTHS_LONG = r'''(january)|(february)|(march)|(april)|(may)|(june)|(july)|
                   (august)|(september)|(october)|(november)|(december)'''
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
                    'languages',
                    'language'
                ]