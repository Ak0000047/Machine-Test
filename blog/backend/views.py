from django.shortcuts import render

# Create your views here.
from rest_framework.views  import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User,Posts
import re
from datetime import datetime
class UserRegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        name = request.data.get('name')
        email = request.data.get('email')
        phone = request.data.get('phone')
        if not username or not password or not name or not email or not phone:
            return Response({'error': 'All fields are required: username, password, name, email, phone'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        if not self.is_password_strong(password):
            return Response({'error': 'Password does not meet strength criteria'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.create(username=username, password=password, name=name, email=email, phone=phone, is_loggedin=0)
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def is_password_strong(self, password):
        min_length = 8
        if len(password) < min_length:
            return False
        if not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'[a-z]', password):
            return False
        if not re.search(r'\d', password):
            return False
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False
        return True


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({'error': 'fields  required: username, password'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(username=username)
            if user.password == password:
                user.is_loggedin = 1
                user.save()
                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Incorrect password'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({'error': 'Incorrect username'}, status=status.HTTP_401_UNAUTHORIZED)



class CreatePostView(APIView):
    def post(self,request):
        user=request.data.get('username')
        title = request.data.get('title')
        description = request.data.get('description')
        tags = request.data.get('tags')
        if not user or not title or  not description or not tags:
            return Response({'error': 'fields  required: username,tags,description'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        islogged=User.objects.get(username=user).is_loggedin
        if islogged == 1:
            post = Posts.objects.create(
                title=title,
                description=description,
                tags=tags,
                username=user,
               date = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
               is_posted=1,
               likes=0
            )
            post.save()
            return Response({'message': 'Post created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'the  user is not logged in'}, status=status.HTTP_401_UNAUTHORIZED)


class ListPostView(APIView):
    def get(self,request):
        user=request.data.get('username')
        if not user :
            return Response({'error': 'fields  required: username'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        islogged=User.objects.get(username=user).is_loggedin
        if islogged==1:
            posts = Posts.objects.filter(is_posted=1)
            post_data = []
            for post in posts:
                post_data.append({
                    'id':post.id,
                    'username': post.username,
                    'title': post.title,
                    'description': post.description,
                    'tags': post.tags,
                    'date': post.date,
                    'likes':post.likes
                })
            return Response(post_data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'the  user need to login to see the posts'}, status=status.HTTP_401_UNAUTHORIZED)


class UnPublishPostView(APIView):
    def put(self,request):
        user=request.data.get('username')
        post_id = request.data.get('post_id')
        if not user or not post_id:
            return Response({'error': 'fields  required: username, post_id'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        islogged=User.objects.get(username=user).is_loggedin
        if islogged==1:
            try:
                post = Posts.objects.get(id=post_id, username=username)
            except Posts.DoesNotExist:
                return Response({'error': 'Post not found or does not belong to the user'}, status=status.HTTP_404_NOT_FOUND)
            if post.is_posted==1:
                post.is_posted=0
                post.save()
                return Response({'message': 'Post unpublished successfully'}, status=status.HTTP_200_OK)
            return  Response({'message': 'Post is already unpublished'}, status=status.HTTP_200_OK)
            
        else:
            return Response({'error': 'the  user need to login to unpulish the posts'}, status=status.HTTP_401_UNAUTHORIZED)

class PostLikeView(APIView):
    def post(self, request):
        user=request.data.get('username')
        post_id = request.data.get('post_id')
        if not user or not post_id:
            return Response({'error': 'fields  required: username, post_id'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            existing_like=Posts.objects.get(id=post_id).likes
        
        except existing_like == None:
                return Response({'error': 'Post not found or does not belong to the user'}, status=status.HTTP_404_NOT_FOUND)
        like=int(existing_like) + 1
        islogged=User.objects.get(username=user).is_loggedin
        if islogged==1:
            if Posts.objects.get(id=post_id).is_posted==1:
                post = Posts.objects.filter(id=post_id).update(likes=like)
                return Response({'message': 'Post liked.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'The post is not published.'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'error': 'the  user need to login to like the posts'}, status=status.HTTP_401_UNAUTHORIZED)



class PostUnLikeView(APIView):
    def put(self, request):
        user=request.data.get('username')
        post_id = request.data.get('post_id')
        if not user or not post_id:
            return Response({'error': 'fields  required: username, post_id'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            existing_like=Posts.objects.get(id=post_id).likes
        
        except existing_like == None:
                return Response({'error': 'Post not found or does not belong to the user'}, status=status.HTTP_404_NOT_FOUND)
        like=int(existing_like) - 1
        if like <= 0:
            like =0
        islogged=User.objects.get(username=user).is_loggedin
        if islogged==1:
            if Posts.objects.get(id=post_id).is_posted==1:
                post = Posts.objects.filter(id=post_id).update(likes=like)
                return Response({'message': 'Post  unliked.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'The post is not published.'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'error': 'the  user need to login to like the posts'}, status=status.HTTP_401_UNAUTHORIZED)