import PyPDF2
import os
import re
from collections import Counter



from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from werkzeug.utils import secure_filename

from flask import Blueprint, request, jsonify

from db import mongo

from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from bson.objectid import ObjectId

routes_bp = Blueprint("routes", __name__)


# ---------------- REGISTER API ----------------
@routes_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    # Validation
    if not username or not email or not password:
        return jsonify({
            "message": "All fields required"
        }), 400

    # Check existing user
    existing_user = mongo.db.users.find_one({
        "email": email
    })

    if existing_user:
        return jsonify({
            "message": "User already exists"
        }), 409

    # Password Hashing
    hashed_password = generate_password_hash(password)

    # Store user
    mongo.db.users.insert_one({
        "username": username,
        "email": email,
        "password": hashed_password
    })

    return jsonify({
        "message": "User Registered Successfully 🚀"
    })


# ---------------- LOGIN API ----------------
@routes_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    # Validation
    if not email or not password:
        return jsonify({
            "message": "Email & Password required"
        }), 400

    # Find user
    user = mongo.db.users.find_one({
        "email": email
    })

    if user:

        if check_password_hash(user["password"], password):

            # Generate JWT Token
            access_token = create_access_token(identity=email)

            return jsonify({
                "message": "Login Successful 🚀",
                "token": access_token
            })

        else:
            return jsonify({
                "message": "Invalid Password"
            }), 401

    return jsonify({
        "message": "User not found"
    }), 404


# ---------------- PROTECTED PROFILE API ----------------
@routes_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():

    current_user = get_jwt_identity()

    return jsonify({
        "message": "Protected Route Accessed 🚀",
        "logged_in_as": current_user
    })


# ---------------- ADD NOTES API ----------------
@routes_bp.route("/add-note", methods=["POST"])
@jwt_required()
def add_note():

    current_user = get_jwt_identity()

    data = request.get_json()

    title = data.get("title")
    content = data.get("content")

    if not title or not content:
        return jsonify({
            "message": "Title & Content required"
        }), 400

    mongo.db.notes.insert_one({
        "title": title,
        "content": content,
        "user_email": current_user
    })

    return jsonify({
        "message": "Note Added Successfully 🚀"
    }), 201


# ---------------- GET USER NOTES API ----------------
@routes_bp.route("/my-notes", methods=["GET"])
@jwt_required()
def get_notes():

    current_user = get_jwt_identity()

    notes = mongo.db.notes.find({
        "user_email": current_user
    })

    notes_list = []

    for note in notes:

        notes_list.append({
            "id": str(note["_id"]),
            "title": note["title"],
            "content": note["content"]
        })

    return jsonify({
        "notes": notes_list
    }), 200


# ---------------- UPDATE NOTES API ----------------
@routes_bp.route("/update-note/<note_id>", methods=["PUT"])
@jwt_required()
def update_note(note_id):

    current_user = get_jwt_identity()

    data = request.get_json()

    title = data.get("title")
    content = data.get("content")

    if not title or not content:
        return jsonify({
            "message": "Title & Content required"
        }), 400

    note = mongo.db.notes.find_one({
        "_id": ObjectId(note_id),
        "user_email": current_user
    })

    if not note:
        return jsonify({
            "message": "Note not found"
        }), 404

    mongo.db.notes.update_one(
        {
            "_id": ObjectId(note_id)
        },
        {
            "$set": {
                "title": title,
                "content": content
            }
        }
    )

    return jsonify({
        "message": "Note Updated Successfully 🚀"
    }), 200


# ---------------- DELETE NOTES API ----------------
@routes_bp.route("/delete-note/<note_id>", methods=["DELETE"])
@jwt_required()
def delete_note(note_id):

    current_user = get_jwt_identity()

    note = mongo.db.notes.find_one({
        "_id": ObjectId(note_id),
        "user_email": current_user
    })

    if not note:
        return jsonify({
            "message": "Note not found"
        }), 404

    mongo.db.notes.delete_one({
        "_id": ObjectId(note_id)
    })

    return jsonify({
        "message": "Note Deleted Successfully 🚀"
    }), 200


# ---------------- PDF UPLOAD API ----------------
@routes_bp.route("/upload-pdf", methods=["POST"])
@jwt_required()
def upload_pdf():

    if "pdf" not in request.files:
        return jsonify({
            "message": "No PDF file uploaded"
        }), 400

    pdf = request.files["pdf"]

    if pdf.filename == "":
        return jsonify({
            "message": "No selected file"
        }), 400

    filename = secure_filename(pdf.filename)

    filepath = os.path.join("uploads", filename)

    pdf.save(filepath)

    return jsonify({
        "message": "PDF Uploaded Successfully 🚀",
        "filename": filename
    }), 201


# ---------------- PDF TEXT EXTRACTION API ----------------
@routes_bp.route("/extract-pdf-text/<filename>", methods=["GET"])
@jwt_required()
def extract_pdf_text(filename):

    filepath = os.path.join("uploads", filename)

    if not os.path.exists(filepath):
        return jsonify({
            "message": "PDF file not found"
        }), 404

    extracted_text = ""

    with open(filepath, "rb") as pdf_file:

        reader = PyPDF2.PdfReader(pdf_file)

        for page in reader.pages:
            extracted_text += page.extract_text()



    return jsonify({
        "filename": filename,
        "extracted_text": extracted_text
    }), 200




# ---------------- AI TAGS API ----------------
@routes_bp.route("/ai-tags", methods=["POST"])
@jwt_required()
def ai_tags():

    data = request.get_json()

    notes_text = data.get("text")

    if not notes_text:
        return jsonify({
            "message": "Notes text required"
        }), 400

    # Convert to lowercase
    text = notes_text.lower()

    # Remove special characters
    words = re.findall(r'\b[a-zA-Z]+\b', text)

    # Common stopwords
    stopwords = [
        "is", "a", "the", "and", "for",
        "to", "of", "in", "on", "it",
        "this", "that", "with", "used"
    ]

    # Remove stopwords
    filtered_words = [
        word for word in words
        if word not in stopwords
    ]

    # Count word frequency
    word_counts = Counter(filtered_words)

    # Get top 5 tags
    top_tags = [
        word for word, count
        in word_counts.most_common(10)
    ]

    return jsonify({
        "tags": top_tags
    }), 200


# ---------------- SMART SEARCH API ----------------
@routes_bp.route("/smart-search", methods=["POST"])
@jwt_required()
def smart_search():

    current_user = get_jwt_identity()

    data = request.get_json()

    search_query = data.get("query")

    if not search_query:
        return jsonify({
            "message": "Search query required"
        }), 400

    # Get all notes of current user
    notes = list(mongo.db.notes.find({
        "user_email": current_user
    }))

    # No notes found
    if len(notes) == 0:
        return jsonify({
            "message": "No notes found"
        }), 404

    # Combine note title + content
    notes_text = [
        note["title"] + " " + note["content"]
        for note in notes
    ]

    # TF-IDF Vectorizer
    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(
        notes_text + [search_query]
    )

    # Similarity check
    similarity = cosine_similarity(
        vectors[-1],
        vectors[:-1]
    )

    # Get similarity scores
    scores = similarity.flatten()

    # Store results
    results = []

    for index, score in enumerate(scores):

        if score > 0:

            results.append({
                "title": notes[index]["title"],
                "content": notes[index]["content"],
                "similarity_score": round(float(score), 2)
            })

    # Sort by highest similarity
    results = sorted(
        results,
        key=lambda x: x["similarity_score"],
        reverse=True
    )

    return jsonify({
        "results": results
    }), 200