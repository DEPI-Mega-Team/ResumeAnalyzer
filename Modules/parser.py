import os
import io
import gc
import pandas as pd

from . import extractors
from . import accumolators
from . import utils
from . import constants as cs

from transformers import pipeline

class ResumeParser(object):

    def __init__(self,
                 skills_file= cs.workspace_dir +'/Data/skills.csv',
                 companies_file= cs.workspace_dir +'/Data/companies.csv',
                 custom_mobile_regex= None):
        
        # Load NLP Models
        self.__pretrained_nlp = pipeline("token-classification", "reyhanemyr/bert-base-NER-finetuned-cv")
        
        # Define basic attributes
        self.__custom_mobile_regex = custom_mobile_regex
        self.__skill_set = set(pd.read_csv(skills_file)['Skill'])
        self.__company_set = set(pd.read_csv(companies_file)['Company'])
        self.reset()
    
    def get_extracted_data(self):
        """
        Returns the extracted details from the resume
        """
        return self.__details
    
    def reset(self):
        """
        Resets the __details dictionary to its initial state
        """
        self.__details = {
            'name': None,
            'email': None,
            'mobile_numbers': None,
            'role': None,
            'locations': None,
            'skills': None,
            'college': None,
            'degree': None,
            'companies': None,
            'experience': None,
            'links': None,
            'no_of_pages': None,
            'format': None
        }
    
    
    def parse(self, resume):
        """
        Parses the given resume to extract various details such as name, email, mobile number, skills, academic degree,
        companies worked at, and experience.
        Args:
            resume (str or io.BytesIO): The resume file path or file-like object containing the resume data.
        Returns:
            dict: A dictionary containing the extracted resume details.
                - name (str): The name of the candidate.
                - email (str): The email address of the candidate.
                - mobile_numbers (list): A list of extracted mobile numbers.
                - skills (list): A list of extracted skills.
                - colleges (str): The colleges the candidate mentioned in the resume.
                - degree (str): The academic degree of the candidate.
                - companies (list): A list of companies the candidate mentioned in the resume.
                - experience (float): Total experience in years.
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
        self.__text_raw = utils.encode_text(self.__text_raw)
        
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
        text_links = extractors.extract_links_from_text(self.__text_raw)
        hyper_links = extractors.extract_hyperlinks(resume, ext)
        links = list(text_links | hyper_links)
        
        if links:
            self.__details['links'] = links
        
        # Model Outputs
        pretrained_output = self.__pretrained_nlp(self.__text_raw)
        pretrained_output = utils.preprocess_bert_output(pretrained_output)
        
        # Extract entities
        cust_ent = extractors.extract_entities_wih_custom_model(pretrained_output)
        entities = extractors.extract_entity_sections(self.__text_raw)
        
        # Extract Skills
        skills = [ent['text'] for ent in pretrained_output if ent['entity'] == 'SKILL']

        valid_skills = {skill for skill in skills if utils.preprocess_skill(skill) in self.__skill_set}
        
        if valid_skills:
            self.__details['skills'] = list(valid_skills)
        elif 'skills' in entities:
            # First Approach: Find skills in skills section
            self.__details['skills'] = extractors.extract_skills('\n'.join(entities['skills']), self.__skill_set)
        
        if not self.__details['skills']:
            # Second Approach: Find skills in the whole document (Brute-Force)
            self.__details['skills'] = extractors.extract_skills('\n'.join(self.__text_raw), self.__skill_set, cs.OBJECT_PATTERN)

        
        # Extract Name
        if 'PER' in cust_ent:
            self.__details['name'] = cust_ent['PER'][0].strip()
        else:
            name = self.__text_raw.split('\n')[0].strip()
            self.__details['name'] = name
        
        # Extract Academic Degree
        if 'DEGREE' in cust_ent:
            self.__details['degree'] = cust_ent['DEGREE'][0]
        else:
            self.__details['degree'] = extractors.extract_highest_degree(self.__text_raw)
        
        if 'ROLE' in cust_ent:
            self.__details['role'] = cust_ent['ROLE']
        
        # Extract Locations
        if 'LOC' in cust_ent:
            self.__details['locations'] = list({loc for loc in cust_ent['LOC']})
        
        # Extract Company Names
        if 'COMPANY' in cust_ent:
            self.__details['companies'] = [company for company in cust_ent['COMPANY']]
        else:
            self.__details['companies'] = extractors.extract_companies(self.__text_raw, list(self.__company_set))
        
        # Extract College Name
        if 'INSTITUTION' in cust_ent:
            self.__details['college'] = cust_ent['INSTITUTION']
        else:
            self.__details['college'] = extractors.extract_college(self.__text_raw)
        
        # Calculate Total Experience
        if 'experience' in entities:
            # Get Experience in Months
            total_exp = accumolators.get_total_experience(entities['experience'])
            
            # Calculate Experience in Years
            self.__details['experience'] = round(total_exp / 12, 2) if total_exp else 0
        else:
            self.__details['experience'] = 0
        
        if ext:
            self.__details['format'] = ext
            self.__details['no_of_pages'] = accumolators.get_number_of_pages(resume, ext)
        
        self.set_empty_attributes_to_none()
        
        # To prevent memory leaks
        del resume
        gc.collect()
        
        return self.get_extracted_data()

    def set_empty_attributes_to_none(self):
        """
        Sets any empty attributes in __details dictionary to None
        """
        for key in self.__details:
            if not self.__details[key]:
                self.__details[key] = None