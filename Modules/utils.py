import io
import re
from .constants import EMAIL_PATTERN

def load_to_memory(file):
    with open(file, 'rb') as memory_file:
        memory_file = io.BytesIO(memory_file.read())
        memory_file.name = file
    
    return memory_file

def validate_link(link):
    if link.startswith("mailto:") or link.startswith("tel:") or link.startswith("sms:"):
        return False

    if re.match(EMAIL_PATTERN, link):
        return False
    
    return True

def encode_text(doc):
    return doc.encode('ascii', 'replace').decode('ascii').replace('?', '-')

def preprocess_skill(skill):
    return skill.strip().lower().replace(' ', '')

def preprocess_bert_output(results):
    counter = 0
    for i in range(len(results)):
        if results[i]['word'].startswith('##'):
            counter += 1
        else:
            break
        
    results = [item for item in results[counter:] if item['entity'] not in ['None', 'O']]
    
    output = []
    for item in results:
        etype, entity = item['entity'].split('-')
        word = item['word']
        start = item['start']
        end = item['end']

        new = True
        
        if word.startswith('##') and start - output[-1]['end'] < 2 and output[-1]['entity'] == entity:
            new = False
            word = word[2:]
            output[-1]['text'] += word
            output[-1]['end'] = end
            
        elif (etype == 'I' or word.lower() == 'skills') and output[-1]['entity'] == entity:
            new = False
            word = ' ' + word
            output[-1]['text'] += word
            output[-1]['end'] = end

            
        if new:
            output.append({'entity': entity, 'text': word, 'start': start, 'end': end})

    output = [item for item in output if not item['text'].startswith('#')]
    return output