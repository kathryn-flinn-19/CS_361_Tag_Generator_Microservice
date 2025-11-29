# for tag generator
import zmq
import json
import random

"""
sample json:
    {
        "title": "txt",
        "notes": "txt",
        "date": "txt",
        "location": "txt"
    }

"""

def date_to_tags(date):
    return date

def title_to_tags(title):
    return title

def location_to_tags(location):
    return location

def find_tag_len(num_words):
    if num_words == 1:
        return 1
    elif num_words < 10:
        return 2
    elif num_words < 20:
        return 4
    else:
        return 5

def find_num_tags(num_words):
    if num_words < 4:
        return num_words
    else:
        return 3

def check_validity(strs, tag_list):
    invalid_words = ["to", "the", "a", "on", "in", "of", "as", "be", "am", "is", "this", "had", "have", "has", "and"]

    if list_to_str(strs) in tag_list:
        return False

    for word in strs:
        if not word in invalid_words:
            return True
    
    return False

def list_to_str(l):
    s = ""
    for w in l:
        s = s + " " + w
    return s


def make_tag_from_notes(words, max_tag_len, tag_list):
    num_words = len(words)

    while True:
        tag_len = random.randint(1, max_tag_len)

        max_start_pos = num_words - tag_len - 1

        start_pos = random.randint(0, max_start_pos)

        generated_tag = words[start_pos:start_pos + tag_len + 1]

        if check_validity(generated_tag, tag_list):
            return list_to_str(generated_tag)


def notes_to_tags(notes):
    words = notes.split()
    num_words = len(words)

    max_tag_len = find_tag_len(num_words)

    tags = ""
    tag_list = []
    num_tags = find_num_tags(num_words)
    
    for i in range(num_tags):
        t = make_tag_from_notes(words, max_tag_len, tag_list)
        tags = tags + ";" + t
        tag_list.append(t)
    
    return tags

def remove_double_semicolon(tags):
    updated = ""
    while tags.find(";;") != -1:
        updated = tags[0:tags.find(";;")] + tags[tags.find(";;") + 1:]
        tags = updated
    
    return updated

def append_tag(tags, new_tag):
    if tags[len(tags) - 1] != ';':
        tags = tags + ";"
    
    tags = tags + new_tag
    return tags

def generate_all_tags(data):
    title = data.get("title")
    date = data.get("date", "")
    location = data.get("location", "")
    notes = data.get("notes", "")

    tags = ""
    tags = tags + title_to_tags(title)

    if date != "":
        tags = append_tag(tags, date_to_tags(date))

    if location != "":
        tags = append_tag(tags, location_to_tags(location))
    
    if notes != "":
        tags = append_tag(tags, notes_to_tags(notes))

    return remove_double_semicolon(tags)
    

def server():
    context = zmq.Context()
    socket = context.socket(zmq.REP)

    socket.bind("tcp://*:8932")

    while True:
        # receive and decode a request from the client

        message = socket.recv()

        full_msg = message.decode()

        # if asked to quit, break
        if full_msg == "Q":
            break

        json_data = json.loads(full_msg)

        response = generate_all_tags(json_data)

        socket.send_string(response)

    context.destroy()
    socket.close()

if __name__ == "__main__":
    server()