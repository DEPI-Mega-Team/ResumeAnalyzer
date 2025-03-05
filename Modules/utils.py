import io

def load_to_memory(file):
    with open(file, 'rb') as memory_file:
        memory_file = io.BytesIO(memory_file.read())
        memory_file.name = file
    
    return memory_file