from werkzeug.datastructures import FileStorage

def file_is_valid(file: FileStorage):
    """
    Validates the file type of the uploaded file.
    """
    if file.filename != '':
        return True
    if file.mimetype == 'text/csv':
        return True
    return False
