from flask import Flask, jsonify, request, render_template_string
from pymongo import MongoClient
from bson import json_util, ObjectId
import json
from flask_mail import Mail, Message
import random
from flask_cors import CORS

app = Flask(__name__)
cors_origins = [
    "https://choose-fav.vercel.app",
    "https://choose-fav-smste.vercel.app",
    "http://choose-fav-git-master-smste.vercel.app",
    "http://choose-94khc0xo9-smste.vercel.app"
]

CORS(app, origins=cors_origins)
# Connect to MongoDB
client = MongoClient('mongodb+srv://tushar16:Crazyaccess123@cluster0.vj5kcmp.mongodb.net/?retryWrites=true&w=majority')
db = client['Hot_Rating']
collection = db['users']

all_users = list(collection.find({}))

def mongo_to_dict(obj):
    """Converts MongoDB document to a dictionary."""
    return json.loads(json_util.dumps(obj))

@app.route('/prnde143/<prn>', methods=['GET'])
# @cross_origin(origins=origins)
def get_user(prn):
    user = next((user for user in all_users if user.get('PRN') == prn), None)
    if user:
        return jsonify(mongo_to_dict(user)), 200
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/votevadav143/<prn>', methods=['PUT'])
# @cross_origin(origins=origins)
def increment_vote(prn):
    result = collection.update_one({'PRN': prn}, {'$inc': {'votes': 1}})
    if result.modified_count:
        return jsonify({'success': 'Vote incremented'}), 200
    else:
        return jsonify({'error': 'User not found or vote not incremented'}), 404
    
@app.route('/randompeoplede143/<gender>', methods=['GET'])
# @cross_origin(origins=origins)
def get_similar_f(gender):
    try:
        # Find two random users with gender 'f' whose votes are nearly the same
        if gender=='m':
            filtered_users = [user for user in all_users if user['Gender'] == 'f']
            selected_users = random.sample(filtered_users, 2)
            # Convert the query result to a list of dictionaries
            result = [mongo_to_dict(user) for user in selected_users]
            
            return jsonify(result), 200
        if gender=='f':
            filtered_users = [user for user in all_users if user['Gender'] == 'm']
            selected_users = random.sample(filtered_users, 2)
            # Convert the query result to a list of dictionaries
            result = [mongo_to_dict(user) for user in selected_users]
            
            return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/sagleusersde143', methods=['GET'])
# @cross_origin(origins=origins)
def get_users():
    users = collection.find().sort('votes', -1)
    return jsonify([mongo_to_dict(user) for user in users]), 200


####################################################################################################
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'drdisrespect1616@gmail.com'  # Your Gmail address
app.config['MAIL_PASSWORD'] = 'ojsw yxaz uysl slxk'     # Your generated app password
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

# Temporary storage for OTPs
otps = {}

@app.route('/otpsendkar143/<prn>', methods=['GET'])
# @cross_origin(origins=origins)
def send_otp(prn):
    try:
        user = collection.find_one({'PRN': prn})
        if user and 'Email' in user:
            email = user['Email']
            otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            otps[email] = otp  # Store the OTP

            # HTML email content
            html_content = render_template_string("""
            <html>
                <head>
                    <style>
                        .email-body {font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;}
                        .email-container {background-color: #ffffff; padding: 20px; text-align: center; border-radius: 8px;}
                        .email-header {font-size: 24px; margin-bottom: 20px; color: #333333;}
                        .email-content {font-size: 16px; color: #555555; margin-bottom: 30px;}
                        .email-footer {font-size: 12px; color: #999999;}
                    </style>
                </head>
                <body>
                    <div class="email-body">
                        <div class="email-container">
                            <div class="email-header">Your One-Time Password (OTP) for Hot_Rating 😁🔥</div>
                            <div class="email-content">Your OTP is: <strong>{{ otp }}</strong></div>
                            <div class="email-footer">This OTP is valid for 10 minutes.</div>
                        </div>
                    </div>
                </body>
            </html>
            """, otp=otp)

            # Send email with HTML content
            msg = Message('Your OTP', sender='your-gmail@gmail.com', recipients=[email])
            msg.html = html_content
            mail.send(msg)

            return jsonify({'message': 'OTP sent to email'}), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/otpverifykar143/<email>', methods=['POST'])
# @cross_origin(origins=origins)
def verify_otp(email):
    data = request.json
    if email in otps and otps[email] == data.get('otp'):
        del otps[email]  # Remove OTP after verification
        return jsonify({'message': 'OTP verified'}), 200
    else:
        return jsonify({'error': 'Invalid OTP'}), 400
#########################################################################################
if __name__ == '__main__':
    app.run(host='127.0.0.1', port='8080')
