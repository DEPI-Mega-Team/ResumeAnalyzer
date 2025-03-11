import re
from spacy.language import Language
from spacy.tokens import Span
from . import constants as cs

@Language.component("skill_ner")
def skill_ner(doc):
    original_ents = list(doc.ents)
    skill_blocks = [ent for ent in doc.ents if ent.label_ == 'Skills']

    pattern = cs.SKILL_PATTERN

    mwt_ents = []
    for block in skill_blocks:
        for match in re.finditer(pattern, block.text):
            start, end = match.span()
            start += block.start_char
            end += block.start_char
            
            span = doc.char_span(start, end)
            if span is not None:
                mwt_ents.append((span.start, span.end, span.text))

    for ent in mwt_ents:
        start, end, _ = ent
        per_ent = Span(doc, start, end, label="Skill")
        original_ents.append(per_ent)

    original_ents = [ent for ent in original_ents if ent.label_ != 'Skills']
    doc.ents = original_ents
    
    return (doc)

@Language.component("degree_ner")
def degree_ner(doc):
    pattern = cs.OBJECT_PATTERN
    
    original_ents = list(doc.ents)
    skill_blocks = [ent for ent in doc.ents if ent.label_ == 'Degree']

    mwt_ents = []
    for block in skill_blocks:
        for match in re.finditer(pattern, block.text):
            start, end = match.span()
            start += block.start_char
            end += block.start_char
            span = doc.char_span(start, end)
            if span is not None:
                mwt_ents.append((span.start, span.end, span.text))

    original_ents = [ent for ent in original_ents if ent.label_ != 'Degree']

    for ent in mwt_ents:
        start, end, text = ent
        
        words = text.split()
        for word in words:
            if word.lower() in cs.DEGREE or word in cs.EDUCATION:
                per_ent = Span(doc, start, end, label="Degree")
                original_ents.append(per_ent)
                break
    
    doc.ents = original_ents

    return (doc)