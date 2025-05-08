import io
import re
import pymupdf
import docx2txt
from docx import Document

from . import constants as cs
from . import utils


def handle_io_bytes(func):
    def checker(input_file):
        is_byte = True
        if not isinstance(input_file, io.BytesIO):
            # extract text from local pdf file
            input_file = open(input_file, 'rb')
            is_byte = False

        result = func(input_file)

        if not is_byte:
            input_file.close()

        return result

    return checker


@handle_io_bytes
def extract_text_from_docx(doc_file: str):
    '''
    Helper function to extract plain text from .docx files

    :param doc_file: path to .docx file to be extracted
    :return: string of extracted text
    '''
    text = docx2txt.process(doc_file)
    return text


@handle_io_bytes
def extract_text_from_pdf(pdf_file):
    '''
    Helper function to extract the plain text from .pdf files

    :param pdf_path: path to PDF file to be extracted (remote or local)
    :return: iterator of string of extracted text
    '''
    # Open PDF file
    with pymupdf.open(stream=pdf_file, filetype="pdf") as pdf_document:
        # Initialize text variable
        text = ""
        # Iterate through pages
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text()

    return text


def extract_text(resume: str, extension: str = None):
    '''
    Wrapper function to detect the file extension and call text
    extraction function accordingly

    :param resume: resume text or path of file of which text is to be extracted
    :param extension: extension of file `file_name`
    '''
    text = ''
    if extension == 'pdf':
        text = extract_text_from_pdf(resume)
    elif extension == 'docx':
        text = extract_text_from_docx(resume)
    else:
        text = resume

    text = [line.replace('\t', ' ') for line in text.split('\n') if line]
    return '\n'.join(text)


def extract_entities_wih_custom_model(nlp_entities: list[dict]):
    '''
    Helper function to extract different entities with custom
    trained model using SpaCy's NER

    :param custom_nlp_text: object of `spacy.tokens.doc.Doc`
    :return: dictionary of entities
    '''
    entities = {}
    for ent in nlp_entities:
        if ent['entity'] not in entities.keys():
            entities[ent['entity']] = [ent['text']]
        else:
            entities[ent['entity']].append(ent['text'])
    
    for key in entities.keys():
        entities[key] = list(set(entities[key]))
    
    return entities


def extract_entity_sections(text: str) -> dict:
    '''
    Helper function to extract all the raw text from sections of
    resume specifically for professionals

    :param text: Raw text of resume
    :return: dictionary of entities
    '''
    assert isinstance(text, str), "Input text must be a string"

    resume_lines = [i.strip() for i in text.split('\n')]
    resume_sections = set(cs.RESUME_SECTIONS)

    entities = {}
    key = ""

    for line in resume_lines:
        line = line.strip()
        if not line:  # If line is empty
            continue

        # Remove all non-alphabet characters
        words_list = [word for word in line.lower().split() if word.isalpha()]

        # Check if the line is a section header
        if len(words_list) < 5:  # Titles are usually less then 5 words

            p_key = set(words_list) & resume_sections

            if p_key:  # If there is a match

                # Convert the set of matches to a list for accessibility
                # Access the first element
                p_key = list(p_key)[0]

                if p_key not in entities.keys():
                    entities[p_key] = []
                    key = p_key
                    continue

        if key:
            entities[key].append(line)

    assert isinstance(entities, dict), "Output entities must be a dictionary"
    return entities


def extract_email(text: str):
    '''
    Helper function to extract email id from text

    :param text: plain text extracted from resume file
    '''
    email = re.findall(cs.EMAIL_PATTERN, text)
    if email:
        try:
            return email[0].split()[0].strip(';')
        except IndexError:
            return None


def extract_mobile_numbers(text: str, custom_regex: str = None):
    '''
    Helper function to extract mobile number from text

    :param text: plain text extracted from resume file
    :return: string of extracted mobile numbers
    '''
    if not custom_regex:
        mob_num_regex = cs.PHONE_PATTERN
        matches = re.findall(mob_num_regex, text)
    else:
        matches = re.findall(custom_regex, text)
    if matches:
        phone = list({number.replace(" ", "").replace("-", "").replace(".", "").replace(
            "(", "").replace(")", "") for number in matches if len(number) > 9})
        return phone


def extract_skills(skills_section, skill_set, pattern= cs.SKILL_PATTERN):
    '''
    Helper function to extract skills from skills section

    :param skills_section: string of skills section extracted from resume
    :return: list of skills extracted
    '''

    skills = re.findall(pattern, skills_section)
    skills = list({skill.capitalize() for skill in skills if utils.preprocess_skill(skill) in skill_set})

    return skills


def extract_companies(text: str, companies_list: list):
    '''
    Helper function to extract companies from text
    '''
    companies = [company for company in companies_list if re.search(r'\b'+company+r'\b', text)]
    return companies


def extract_college(text: str):
    '''
    Helper function to extract college from text
    '''
    lines = text.split('\n')
    
    colleges = set()
    for line in lines:
        colleges.update(re.findall(cs.COLLEGE_PATTERN, line))
    
    return list(colleges)


def extract_links_from_text(text: str):
    '''
    Helper function to extract links from text

    :param text: plain text extracted from resume file
    :return: string of extracted links
    '''
    links = re.findall(cs.URL_PATTERN, text)
    links = {link for link in list(links) if utils.validate_link(link)}
    return links


def extract_highest_degree(text: str):
    '''
    Helper function to extract degree from text
    '''
    # Define Patterns
    patterns = {}
    
    for degree_type, words in cs.DEGREE.items():
        concat = '|'.join([degree for degree in words])
        patterns[degree_type] = re.compile(r'\b' + concat + r'\b', re.IGNORECASE)
    
    
    # Search for degree types in the resume text
    phd_match = re.search(patterns['phd'], text)
    masters_match = re.search(patterns['master'], text)
    bachelors_match = re.search(patterns['bachelor'], text)
    diploma_match = re.search(patterns['diploma'], text)
    high_school_match = re.search(patterns['high_school'], text)
    
    if phd_match:
        return 'PhD'
    elif masters_match:
        return 'Master'
    elif bachelors_match:
        return 'Bachelor'
    elif diploma_match:
        return 'Diploma'
    elif high_school_match:
        return 'High School'
    else:
        return 'Unknown'

@handle_io_bytes
def extract_hyperlinks_from_pdf(pdf_file):
    links = set()

    with pymupdf.open(stream=pdf_file, filetype="pdf") as pdf_document:
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            links_in_page = page.get_links()

            for link in links_in_page:
                if link["kind"] == 2 and link["uri"]:
                    links.add(link["uri"])

    return links


@handle_io_bytes
def extract_hyperlinks_from_docx(docx_file):
    links = set()

    doc = Document(docx_file)
    for rel in doc.part.rels.values():
        if "hyperlink" in rel.reltype:
            links.add(rel.target_ref)

    return links


def extract_hyperlinks(resume_file: str, extension: str = None):
    links = set()

    if extension == 'pdf':
        links.update(extract_hyperlinks_from_pdf(resume_file))

    elif extension == 'docx':
        links.update(extract_hyperlinks_from_docx(resume_file))

    else:
        raise ValueError("Unsupported file extension")

    # Preprocessing
    links = {link for link in list(links) if utils.validate_link(link)}

    return links
