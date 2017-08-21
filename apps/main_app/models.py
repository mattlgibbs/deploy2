from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
#Registration checker for name, email and password:
    def regVal(self, PostData):
        results = {"status": True, 'errors': []}
        if len(PostData['name']) < 2:
            results['errors'].append('Name must be at least 2 letters')
        if not re.match(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", PostData['email']):
            results['errors'].append('Not a valid email address')
        if PostData['password'] != PostData['c_password']:
            results['errors'].append('Passwords must match')
        if len(self.filter(email = PostData['email'])) > 0:
            results['errors'].append('User already exists')
        if len(results['errors']) > 0:
            results['status'] = False
        return results

#Creates salted password and user in the database upon successful creation:
    def creator(self, PostData):
        hashed = bcrypt.hashpw(PostData['password'].encode(), bcrypt.gensalt())
        print hashed
        user = User.objects.create(name = PostData['name'], email = PostData['email'], password = hashed, gold=200)

#Logon validation to see if user logging on exists and is using correct password:
    def logVal(self, PostData):
        results = {'status': True, 'errors': [], 'user':None}
        user = User.objects.filter(email= PostData['email'])
        if len(user) < 1:
            results['errors'].append('User not found.')
        else:
            if bcrypt.checkpw(PostData['password'].encode(), user[0].password.encode()) == False:
                results['errors'].append('Passwords do not match.')
            if len(results['errors']) > 0:
                results['status'] = False
            else:
                results['user'] = user[0]
        return results

#User class attributes:
class User(models.Model): ##Create User Table
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    gold = models.IntegerField(default=200)
    objects = UserManager()

class Logs(models.Model): ##Create Logs Table
    content = models.TextField()
    user = models.ForeignKey(User, related_name="User_Id")
    created_at = models.DateTimeField(auto_now_add=True)
