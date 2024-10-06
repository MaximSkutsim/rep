def update_note(notes, note_id, new_content):
    """
    Updates the content of an existing note.

    Args:
    - notes (dict): A dictionary containing all notes.
    - note_id (str): The ID of the note to be updated.
    - new_content (str): The new content for the note.

    Returns:
    - notes (dict): The updated dictionary of notes.
    """
    if note_id in notes:
        notes[note_id] = new_content  # Обновляем только поле "content"
    else:
        raise ValueError('note_id is missing from notes')
    return notes

def add_note(notes, note_id, title, content):
    """
    Adds a new note to the collection.

    Args:
    - notes (dict): A dictionary containing all notes.
    - note_id (str): The ID of the new note.
    - title (str): The title of the new note.
    - content (str): The content of the new note.

    Returns:
    - notes (dict): The updated dictionary of notes.
    """
    if note_id  in notes:
        raise ValueError('a note with such id exists')
    else:
        notes[note_id] = {'title': title, 'content': content}
    return notes

def delete_note(notes, note_id):
    """
    Deletes an existing note from the collection.

    Args:
    - notes (dict): A dictionary containing all notes.
    - note_id (str): The ID of the note to be deleted.

    Returns:
    - notes (dict): The updated dictionary of notes.
    """
    if note_id in notes:
        del notes[note_id]
    else:
        raise ValueError('note_id is missing from notes')
    return notes
