import xmlrpc.client

s = xmlrpc.client.ServerProxy('http://localhost:8000')

while True:
    action = input("Do you want to add a note (add), get notes (get), or search Wikipedia (wiki)? ")
    username = input("Enter username: ")
    password = input("Enter password: ")

    if action == "add":
        topic = input("Enter topic: ")
        text = input("Enter text: ")
        timestamp = input("Enter timestamp (MM/DD/YY - HH:MM:SS): ")
        result = s.add_note(topic, text, timestamp, username, password)
        print(result)
    elif action == "get":
        topic = input("Enter topic to fetch notes for: ")
        notes = s.get_notes(topic, username, password)
        if isinstance(notes, list):
            for note in notes:
                print(f"Text: {note['text']}, Timestamp: {note['timestamp']}")
        else:
            print(notes)
    elif action == "wiki":
        topic = input("Enter topic to search on Wikipedia: ")
        result = s.search_wikipedia(topic, username, password)
        if isinstance(result, dict):
            print(f"Found Wikipedia article: {result['title']} - {result['url']}")
        else:
            print(result)
    else:
        print("Invalid action.")