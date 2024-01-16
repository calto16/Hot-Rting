from pymongo import MongoClient

# Connect to the MongoDB client
client = MongoClient('mongodb+srv://tushar16:tushar16@cluster0.vj5kcmp.mongodb.net/?retryWrites=true&w=majority')

# Select the database and collection
db = client['Hot_Rating']
collection = db['users']

# Update all documents to set the 'votes' field to 0
result = collection.update_many({}, {'$set': {'votes': 0}})

# Output the result
print(f"Documents modified: {result.modified_count}")
