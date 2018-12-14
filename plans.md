# DB

### User (istID - string)

- Current Position (gson point)
- name (string)
- last seen (datetime)

### Building (building_ID - long int)

- Name (string)
- Location (gson point)

### Message (message_ID - int)

- from_istID (string)
- sentstamp (datetime)
- content (text)
- to_istID (string)
- sent_from (long int)

### Activity (istID - string, arrival - datetime)

- buildingID - long int
- departure - datetime
