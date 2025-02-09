import os
import io
import spacy
from spacy.matcher import Matcher
import pandas as pd

from . import extractors
from . import accumolators
from .custom_components import skill_ner, degree_ner

workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class ResumeParser(object):

    def __init__(self,
                 skills_file= workspace_dir +'/Data/skills.csv',
                 custom_mobile_regex=None):
        
        # Load NLP Models
        self.__pretrained_nlp = spacy.load(workspace_dir + '/Model/ResumeAnalyzerV3')
        
        # Define basic attributes
        self.__custom_mobile_regex = custom_mobile_regex
        self.__skill_set = set(pd.read_csv(skills_file)['Skill'])
        self.__details = {
            'name': None,
            'email': None,
            'mobile_numbers': None,
            'skills': None,
            'college_name': None,
            'degree': None,
            'designation': None,
            'experience': None,
            'companies_worked_at': None,
            'total_experience': None,
        }
        

    
    def get_extracted_data(self):
        return self.__details

    def parse(self, resume):
        # Define the type of resume data
        if isinstance(resume, io.BytesIO):
            ext = resume.name.split('.')[1]
        else:
            ext = os.path.splitext(resume)[1].split('.')[1]

        # Extract text from resume
        self.__text_raw = extractors.extract_text(resume, '.' + ext)
        
        #----------------------------------#
        # Extract resume details (Parsing) #
        #----------------------------------#
        
        # Model Outputs
        pretrained_output = self.__pretrained_nlp(self.__text_raw)
        
        # Extract entities
        cust_ent = extractors.extract_entities_wih_custom_model(pretrained_output)
        email = extractors.extract_email(self.__text_raw).strip()
        mobile = extractors.extract_mobile_numbers(self.__text_raw, self.__custom_mobile_regex)
        entities = extractors.extract_entity_sections(self.__text_raw)
        
        if 'Name' in cust_ent:
            self.__details['name'] = cust_ent['Name'][0]
        else:
            name = self.__text_raw.split('\n')[0]
            self.__details['name'] = name
        
        self.__details['name'] = self.__details['name'].strip()

        # Extract Email
        self.__details['email'] = email

        # Extract Mobile Number
        self.__details['mobile_numbers'] = mobile

        # Extract Skills
        skills = [ent.text for ent in pretrained_output.ents if ent.label_ == 'Skill']
        valid_skills = [skill for skill in skills if skill.lower() in self.__skill_set]
        
        if valid_skills:
            self.__details['skills'] = list(set(valid_skills))
        else:
            self.__details['skills'] = extractors.extract_skills('\n'.join(entities['skills']), self.__skill_set)
            
        
        # Extract Academic Degree
        if 'Degree' in cust_ent:
            self.__details['degree'] = cust_ent['Degree']

        # Extract Designation
        if 'Designation' in cust_ent:
            self.__details['designation'] = [ent.text for ent in pretrained_output.ents if ent.label_ == 'Designation']

        # Extract Company Names
        if 'Companies worked at' in cust_ent:
            self.__details['companies_worked_at'] = cust_ent['Companies worked at']

        # Exract and Calculate Experience
        if 'experience' in entities:
            self.__details['experience'] = entities['experience']
            
            # Get Experience in Months
            total_exp = accumolators.get_total_experience(entities['experience'])
            
            # Calculate Experience in Years
            self.__details['total_experience'] = round(total_exp / 12, 2) if total_exp else 0
        else:
            self.__details['total_experience'] = 0
        
        return self.get_extracted_data()


def resume_result_wrapper(resume):
    parser = ResumeParser(resume)
    return parser.get_extracted_data()
