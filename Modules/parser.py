import os
import io
import gc
import spacy
import pandas as pd

from . import extractors
from . import accumolators
from . import utils
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
        self.reset()
    
    def get_extracted_data(self):
        return self.__details
    
    def reset(self):
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
            'links': None,
            'no_of_pages': None,
            'format': None
        }
    
    
    def parse(self, resume):
        """
        Parses the given resume to extract various details such as name, email, mobile number, skills, academic degree, 
        designation, companies worked at, and total experience.
        Args:
            resume (str or io.BytesIO): The resume file path or file-like object containing the resume data.
        Returns:
            dict: A dictionary containing the extracted resume details.
                - name (str): The name of the candidate.
                - email (str): The email address of the candidate.
                - mobile_numbers (list): A list of extracted mobile numbers.
                - skills (list): A list of extracted skills.
                - degree (str): The academic degree of the candidate.
                - designation (list): A list of designations held by the candidate.
                - companies_worked_at (list): A list of companies the candidate has worked at.
                - experience (str): The experience details extracted from the resume.
                - total_experience (float): The total experience in years.
        """
        self.reset()
        
        # Define the type of resume data
        if isinstance(resume, io.BytesIO):
            ext = resume.name.split('.')[1]
        elif '.docx' == resume[-5:] or '.pdf' == resume[-4:]:
            ext = os.path.splitext(resume)[1].split('.')[1]
            
            # Load the file to the memory
            resume = utils.load_to_memory(resume)
        else:
            if isinstance(resume, str):
                ext = None
            else:
                raise ValueError("Invalid resume data")
        
        # Extract text from resume
        self.__text_raw = extractors.extract_text(resume, ext).strip()
        self.__text_raw = utils.preprocess_text(self.__text_raw)
        
        #----------------------------------#
        # Extract resume details (Parsing) #
        #----------------------------------#
        
        # Extract Email
        email = extractors.extract_email(self.__text_raw)
        self.__details['email'] = email

        # Extract Mobile Number
        mobile = extractors.extract_mobile_numbers(self.__text_raw, self.__custom_mobile_regex)
        self.__details['mobile_numbers'] = mobile

        
        # Extract Links
        links = list(extractors.extract_links_from_text(self.__text_raw) | extractors.extract_hyperlinks(resume, ext))
        if links:
            self.__details['links'] = links
        
        # Model Outputs
        pretrained_output = self.__pretrained_nlp(self.__text_raw)
        
        # Extract entities
        cust_ent = extractors.extract_entities_wih_custom_model(pretrained_output)
        entities = extractors.extract_entity_sections(self.__text_raw)
        
        # Extract Skills
        skills = [ent.text for ent in pretrained_output.ents if ent.label_ == 'Skill']
        valid_skills = {skill for skill in skills if skill.strip().lower().replace(' ', '') in self.__skill_set}
        
        if valid_skills:
            self.__details['skills'] = list(valid_skills)
            
        elif 'skills' in entities:
            self.__details['skills'] = extractors.extract_skills('\n'.join(entities['skills']), self.__skill_set)
        
        
        # Extract Name
        if 'Name' in cust_ent:
            self.__details['name'] = cust_ent['Name'][0].strip()
        else:
            name = self.__text_raw.split('\n')[0].strip()
            self.__details['name'] = name
        
        # Extract Academic Degree
        if 'Degree' in cust_ent:
            self.__details['degree'] = cust_ent['Degree']

        # Extract Designation
        if 'Designation' in cust_ent:
            self.__details['designation'] = [ent.text for ent in pretrained_output.ents if ent.label_ == 'Designation']

        # Extract Company Names
        if 'Companies worked at' in cust_ent:
            self.__details['companies_worked_at'] = cust_ent['Companies worked at']
        
        # Calculate Total Experience
        if 'experience' in entities:
            # Get Experience in Months
            total_exp = accumolators.get_total_experience(entities['experience'])
            
            # Calculate Experience in Years
            self.__details['total_experience'] = round(total_exp / 12, 2) if total_exp else 0
        else:
            self.__details['total_experience'] = 0
        
        if ext:
            self.__details['format'] = ext
            number_of_pages = accumolators.get_number_of_pages(resume, ext)
            if number_of_pages:
                self.__details['no_of_pages'] = number_of_pages
        
        # To prevent memory leaks
        del resume
        gc.collect()
        
        return self.get_extracted_data()
