import uuid

def random_file_prefix(file_name):
    random_file_name = ''.join([str(uuid.uuid4().hex[:6]), file_name])
    
    return random_file_name