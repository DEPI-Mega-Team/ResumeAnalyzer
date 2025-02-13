import io
import re
import os
import nltk
import docx2txt
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFSyntaxError

from . import constants as cs

# Add the local data path
nltk.data.path.append(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))) + '/Data/nltk_data')


def extract_text_from_docx(doc_path: str):
    '''
    Helper function to extract plain text from .docx files

    :param doc_path: path to .docx file to be extracted
    :return: string of extracted text
    '''
    text = docx2txt.process(doc_path)
    return text


def extract_text_from_pdf(pdf_path):
    '''
    Helper function to extract the plain text from .pdf files

    :param pdf_path: path to PDF file to be extracted (remote or local)
    :return: iterator of string of extracted text
    '''
    # https://www.blog.pythonlibrary.org/2018/05/03/exporting-data-from-pdfs-with-python/
    if not isinstance(pdf_path, io.BytesIO):
        # extract text from local pdf file
        with open(pdf_path, 'rb') as fh:
            try:
                for page in PDFPage.get_pages(
                        fh,
                        caching=True,
                        check_extractable=True
                ):
                    resource_manager = PDFResourceManager()
                    fake_file_handle = io.StringIO()
                    converter = TextConverter(
                        resource_manager,
                        fake_file_handle,
                        laparams=LAParams()
                    )
                    page_interpreter = PDFPageInterpreter(
                        resource_manager,
                        converter
                    )
                    page_interpreter.process_page(page)

                    text = fake_file_handle.getvalue()
                    yield text

                    # close open handles
                    converter.close()
                    fake_file_handle.close()
            except PDFSyntaxError:
                raise PDFSyntaxError(
                    "Error Occurred while reading the PDF file, The file may be encrypted")
    else:
        # extract text from remote pdf file
        try:
            for page in PDFPage.get_pages(
                    pdf_path,
                    caching=True,
                    check_extractable=True
            ):
                resource_manager = PDFResourceManager()
                fake_file_handle = io.StringIO()
                converter = TextConverter(
                    resource_manager,
                    fake_file_handle,
                    codec='utf-8',
                    laparams=LAParams()
                )
                page_interpreter = PDFPageInterpreter(
                    resource_manager,
                    converter
                )
                page_interpreter.process_page(page)

                text = fake_file_handle.getvalue()
                yield text

                # close open handles
                converter.close()
                fake_file_handle.close()
        except PDFSyntaxError:
            raise PDFSyntaxError(
                "Error Occurred while reading the PDF file, The file may be encrypted")


def extract_text(resume: str, extension: str = None):
    '''
    Wrapper function to detect the file extension and call text
    extraction function accordingly

    :param resume: resume text or path of file of which text is to be extracted
    :param extension: extension of file `file_name`
    '''
    text = ''
    if extension == 'pdf':
        for page in extract_text_from_pdf(resume):
            text += ' ' + page
    elif extension == 'docx':
        text = extract_text_from_docx(resume)
    else:
        text = resume
    
    text = [line.replace('\t', ' ') for line in text.split('\n') if line]
    return '\n'.join(text)


def extract_entities_wih_custom_model(custom_nlp_text: str):
    '''
    Helper function to extract different entities with custom
    trained model using SpaCy's NER

    :param custom_nlp_text: object of `spacy.tokens.doc.Doc`
    :return: dictionary of entities
    '''
    entities = {}
    for ent in custom_nlp_text.ents:
        if ent.label_ not in entities.keys():
            entities[ent.label_] = [ent.text]
        else:
            entities[ent.label_].append(ent.text)
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
    email = re.findall(r"([^@|\s]+@[^@]+\.[^@|\s]+)", text)
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
        mob_num_regex = r'''\(?\+?\d{1,3}\)?[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}'''
        matches = re.findall(re.compile(mob_num_regex), text)
    else:
        matches = re.findall(re.compile(custom_regex), text)
    if matches:
        phone = [number.replace(" ", "").replace("-", "").replace(".", "").replace("(", "").replace(")", "") for number in matches if len(number) > 9]
        return phone


def extract_skills(skills_section, skill_set):
    '''
    #--- DEPRECATED ---#
    
    Helper function to extract skills from spacy nlp text

    :param skills_section: string of skills section extracted from resume
    :return: list of skills extracted
    '''
    
    # Object REGEX
    object_pattern = r"\b\w+(?:[^\w\n]\w+)*\b"
    
    skills = re.findall(object_pattern, skills_section)
    skills = [skill.capitalize() for skill in skills if skill in skill_set]
    
    return skills