from django.http import HttpResponse, JsonResponse
from backend.models import Task
from bson import ObjectId
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
import json
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv('MONGODB_URI')
client = MongoClient(MONGODB_URI)
dbname = client['TaskDemo']
taskCollection = dbname['task']

def decodeToken(request):
    token = request.headers.get('Authorization')
    if token:
        decoded_token = jwt.decode(token, "your_secret_key", algorithms=["HS256"])
        userId = decoded_token.get('user_id')
        return userId;
    else:
        return JsonResponse({'error': 'Token not provided.'}, status=401)


@csrf_exempt
def create_task(request):
    if request.method == 'POST':
        userId = decodeToken(request)
        data = json.loads(request.body)
        user_id = data.get('user_id')
        name = data.get('name')
        status = data.get('status')

        if userId == user_id:
            if user_id and name and status:
                task = Task(user=user_id, name=name, status=status)
                taskCollection.insert_one(json.loads(task.__str__()))
                return JsonResponse({'message': 'Task created successfully.'})
            else:
                return JsonResponse({'error': 'Invalid request parameters.'}, status=400)
        else:
            return JsonResponse({'error': 'Invalid user.'}, status=401)
    else:
        return HttpResponse("Invalid Request")

def get_task(request):
    if request.method == 'GET':
        try:
            user_id = decodeToken(request)
            if user_id:
                tasks = []
                task_details = taskCollection.find({"user": user_id})
                for doc in task_details:
                    doc['_id'] = str(doc['_id'])
                    tasks.append(doc)
                return JsonResponse({"data": tasks})
            else:
                return JsonResponse({"error": "userId parameter is required."}, status=400)
        except Exception:
            return JsonResponse({'error': 'Something went wrong.'}, status=400)
    else:
        return HttpResponse("Invalid Request")


@csrf_exempt
def delete_task(request, id):
    if request.method == 'DELETE':
        try:
            user_id = decodeToken(request)
            task_id = ObjectId(id)
            result = taskCollection.delete_one({"_id": task_id, "user": user_id})
            if result:
                return JsonResponse({'message': 'Task deleted successfully.'})
            else:
                return JsonResponse({'error': 'Task not found or Invalid user.'}, status=400)
        except Exception:
            return JsonResponse({'error': 'Invalid task ID.'}, status=400)
    else:
        return HttpResponse("Invalid Request")

@csrf_exempt
def update_task(request, id):
    if request.method == 'PUT':
        try:
            user_id = decodeToken(request)
            task_id = ObjectId(id)
            data = json.loads(request.body)
            result = taskCollection.find_one({"_id": task_id})

            if(result and result.get("user") == user_id):
                taskCollection.update_one({"_id": task_id, "user": user_id}, {"$set": data})
                return JsonResponse({'message': 'Task updated successfully.'})
            else:
                return JsonResponse({'error': 'Invalid task id or Invalid user.'}, status=400)
        except ValueError:
            return JsonResponse({'error': 'Invalid task ID or request body.'}, status=400)
    else:
        return HttpResponse("Invalid Request")

def get_task_by_id(request, id):
    if request.method == 'GET':
        try:
            user_id = decodeToken(request)
            task_id = ObjectId(id)
            task = taskCollection.find_one({"_id": task_id, "user": user_id})
            if task:
                task['_id'] = str(task['_id'])
                return JsonResponse({"data": task})
            else:
                return JsonResponse({'error': 'Task not found.'}, status=404)
        except ValueError:
            return JsonResponse({'error': 'Invalid task ID.'}, status=400)
    else:
        return HttpResponse("Invalid Request")
