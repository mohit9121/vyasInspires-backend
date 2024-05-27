from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# Replace the following with your MongoDB Atlas connection string
MONGO_URI = "mongodb+srv://mohit9121:Saarthi123@cluster0.kouyl34.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Initialize the MongoDB client
client = MongoClient(MONGO_URI)
db = client.get_database("SAARTHI1")  # Replace with your database name
collection = db.get_collection("blogs-vyas")  # Replace with your collection name

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/add', methods=['POST'])
def add_blog():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    image_link = data.get('image_link')
    if title and description and image_link:
        blog = {
            'title': title,
            'description': description,
            'image_link': image_link,
            'created_at': datetime.utcnow()
        }
        blog_id = collection.insert_one(blog).inserted_id
        return jsonify({"msg": "Blog added", "id": str(blog_id)}), 201
    else:
        return jsonify({"error": "Missing title, description, or image_link"}), 400

@app.route('/blogs', methods=['GET'])
def get_all_blogs():
    blogs = list(collection.find({}, {'_id': 1, 'title': 1, 'description': 1, 'image_link': 1, 'created_at': 1}))
    for blog in blogs:
        blog['_id'] = str(blog['_id'])
    return jsonify(blogs)

@app.route('/blog/<blog_id>', methods=['GET'])
def get_blog(blog_id):
    blog = collection.find_one({'_id': ObjectId(blog_id)}, {'_id': 1, 'title': 1, 'description': 1, 'image_link': 1, 'created_at': 1})
    if blog:
        blog['_id'] = str(blog['_id'])
        return jsonify(blog)
    else:
        return jsonify({"error": "Blog not found"}), 404

@app.route('/blog/<blog_id>', methods=['PUT'])
def update_blog(blog_id):
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    image_link = data.get('image_link')
    if title and description and image_link:
        updated_blog = {
            'title': title,
            'description': description,
            'image_link': image_link,
            'updated_at': datetime.utcnow()
        }
        result = collection.update_one({'_id': ObjectId(blog_id)}, {'$set': updated_blog})
        if result.matched_count:
            return jsonify({"msg": "Blog updated"}), 200
        else:
            return jsonify({"error": "Blog not found"}), 404
    else:
        return jsonify({"error": "Missing title, description, or image_link"}), 400

@app.route('/blog/<blog_id>', methods=['DELETE'])
def delete_blog(blog_id):
    result = collection.delete_one({'_id': ObjectId(blog_id)})
    if result.deleted_count:
        return jsonify({"msg": "Blog deleted"}), 200
    else:
        return jsonify({"error": "Blog not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
