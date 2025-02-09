import nltk
import os

# Add the local data path
nltk.data.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/Data/nltk_data')

# Name Entity Recognition Pattern #Todo: Add more patterns
NAME_PATTERN = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]

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

NUMBER = r'\d+'

# For finding date ranges
MONTHS_SHORT = r'''(jan)|(feb)|(mar)|(apr)|(may)|(jun)|(jul)
                   |(aug)|(sep)|(oct)|(nov)|(dec)'''
MONTHS_LONG = r'''(january)|(february)|(march)|(april)|(may)|(june)|(july)|
                   (august)|(september)|(october)|(november)|(december)'''
MONTH = r'(' + MONTHS_SHORT + r'|' + MONTHS_LONG + r')'
YEAR = r'(((20|19)(\d{2})))'

STOPWORDS = set(nltk.corpus.stopwords.words('english'))

RESUME_SECTIONS = [
                    'accomplishments',
                    'experience',
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