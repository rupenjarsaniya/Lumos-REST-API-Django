from django.shortcuts import render

from pymongo.mongo_client import MongoClient
from django.http import HttpResponse, JsonResponse
from backend.models import User
import json
from bson import ObjectId
from django.views.decorators.csrf import csrf_exempt
import jwt
import os
from dotenv import load_dotenv

load_dotenv()
MONGODB_URI = os.getenv('MONGODB_URI')
client = MongoClient(MONGODB_URI)
dbname = client['TaskDemo']
userCollection = dbname['user']

def decodeToken(request):
    token = request.headers.get('Authorization')
    if token:
        decoded_token = jwt.decode(token, "your_secret_key", algorithms=["HS256"])
        userId = decoded_token.get('user_id')
        return userId;
    else:
        return JsonResponse({'error': 'Token not provided.'}, status=401)

@csrf_exempt    
def get_user(request):
    if request.method=='GET':
        users = []
        user_id = decodeToken(request)
        user_details = userCollection.find({"_id":ObjectId(user_id)})
        for doc in user_details:
            doc['_id'] = str(doc['_id'])
            users.append(doc)
        return JsonResponse( {"data":users})

    else:
        return HttpResponse("Invalid Request")

@csrf_exempt 
def create_user(request):
    try:
        if request.method=='POST':
            received_json_data=json.loads(request.body)
            existing_user = userCollection.find_one({"email": received_json_data['email']})
            if existing_user:
                return HttpResponse("User already exists")
            user = User(
                name = received_json_data["name"],
                email = received_json_data["email"],
                password = received_json_data["password"]
            )
            result = userCollection.insert_one(json.loads(user.__str__()))
            if result:
                inserted_id = str(result.inserted_id)
                token = jwt.encode({"user_id": inserted_id}, "your_secret_key", algorithm="HS256")
                
                response_data = {
                    "token": token,
                    "name": user.name,
                    "email": user.email,
                }
                return JsonResponse(response_data)

        else:
            return HttpResponse("Invalid Request")
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")

@csrf_exempt
def login(request):
    if request.method == 'POST':
        received_json_data = json.loads(request.body)
        email = received_json_data.get("email")
        password = received_json_data.get("password")

        user = userCollection.find_one({"email": email})
        if not user:
            return HttpResponse("User does not exist")

        if user["password"] != password:
            return HttpResponse("Invalid password")

        token = jwt.encode({"user_id": str(user['_id'])}, "your_secret_key", algorithm="HS256")

        return HttpResponse(token)

    else:
        return HttpResponse("Invalid Request")

@csrf_exempt
def update_user(request):
    if request.method=='PUT':
        users = []
        try:
            user_id = decodeToken(request)
            received_json_data=json.loads(request.body)
            userCollection.update_one({"_id":ObjectId(user_id)}, {"$set": received_json_data})

            user_details = userCollection.find({"_id":ObjectId(user_id)})
            for doc in user_details:
                doc['_id'] = str(doc['_id'])
                users.append(doc)
            return JsonResponse( { "data":users})
        except ValueError:
            return HttpResponse("Invalid Request")

    else:
        return HttpResponse("Invalid Request")

@csrf_exempt 
def delete_user(request):
    if request.method=='DELETE':
        try:
            user_id = decodeToken(request)
            userCollection.delete_one({"_id":ObjectId(user_id)})
            return JsonResponse({"message": "User Deleted"})
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}")

    else:
        return HttpResponse("Invalid Request")

# python manage.py makemigrations 
# python manage.py migrate