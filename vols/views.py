from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import categories
import json
from .models import categories, Sentence
from .serializers import latest_categoriesSerializer, SentenceSerializer, get_categorySerializer
from django.contrib.auth.models import User, auth
import random
import json
from .Crawler import CrawlerInterface
class latest_categories(APIView):
    def get(self, request, pk, format=None):
        number = categories.objects.all().count()
        if number < (pk - 1) * 10 + 1:
            raise Http404
        elif number < pk * 10:
            category = categories.objects.all()[(pk - 1) * 10 :]
        else :
            category = categories.objects.all()[(pk - 1) * 10 : pk * 10]
        serializer = latest_categoriesSerializer(category, many=True)
        return Response(serializer.data)
class all_categories(APIView):
    def get(self, request, format=None):
        category = categories.objects.all()
        serializer = latest_categoriesSerializer(category, many=True)
        return Response(serializer.data)
class get_category(APIView):
    def get(self, request, id, format=None):
        if categories.objects.filter(id=id).exists():
            category = categories.objects.filter(id=id)[0]
            serializer = get_categorySerializer(category)
            return Response(serializer.data)
        else:
            return Response({
                'info': 'Wrong category id !'
            }, status=status.HTTP_400_BAD_REQUEST)

def get_by_id(id):
    if not categories.objects.filter(id=id).exists():
        return Response({
            'info': 'Wrong category id !'
        }, status=status.HTTP_400_BAD_REQUEST)
    Category = categories.objects.filter(id = id)[0]
    words = Category.vol_list
    ret = []
    for word in words:
        print(word)
        sentences = list(Sentence.objects.filter(word = word))
        sentence = random.choice(sentences)
        ret.append(sentence)
    random.shuffle(ret)
    return ret
 
class get_sentences(APIView):
    def get(self, request, id, format=None):
        sentences = get_by_id(id)
        if len(sentences) == 0:
            return Response({
                'info': 'No this word'
            }, status=status.HTTP_400_BAD_REQUEST)
        else :
            serializer = SentenceSerializer(sentences, many=True)
            return Response(serializer.data)

class check(APIView):
    def post(self, request, format=None):
        correct = []
        chinese = []
        data = request.data
        print(data)
        print(correct)
        count = 0
        for item in data:
            word = Sentence.objects.filter(id = item['id'])[0].ans
            if word == item['word']:
                count += 1
                correct.append(True)
                
            else:
                correct.append(False)
            
            chinese.append(Sentence.objects.filter(id = item['id'])[0].chinese)
            
        return Response({"score": count, "correct": correct, "chinese": chinese})

class register(APIView):
    def post(self, request, format=None):
        return
        data = request.data
        username = data['username']
        email = data['email']
        password = data['password']
        _password = data['password']
        if password == _password:
            if User.objects.filter(email=email).exists():
                return Response({
                    'info': 'Email already exists !'
                }, status=status.HTTP_400_BAD_REQUEST)
            elif User.objects.filter(username=username).exists():
                return Response({
                    'info': 'Username already exists !'
                }, status=status.HTTP_400_BAD_REQUEST)
            else :
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                return Response({
                    'info': 'Success !'
                })

class add_category(APIView):
    def post(self, request, format=None):
        data = request.data
        name = data['name']
        description = data['description']
        print(data['vol_list'], type(data['vol_list']))
        vol_list = data['vol_list']
        
        ret = buildwords(vol_list)
        if ret[0] != 'Success':
            return Response({
                'info': 'The word ' + ret[1] + ' was not found in dictionary'
            }, status=status.HTTP_400_BAD_REQUEST)
        else :
            new_category = categories.objects.create(name = name, description = description, vol_list = vol_list)
            new_category.save()
            buildwords(vol_list)
            return Response({
                'info': 'Success !',
                'id': new_category.id
            })

def buildwords(vol_list):
    for word in vol_list:
        if Sentence.objects.filter(word = word).exists():
            continue
        else:
            result = CrawlerInterface.GetWebData(word)
            if len(result[7]) == 2:
                return ('Error', word)
            wordchanges = [word]
            for i in range(2, 7):
                for j in result[i]:
                    wordchanges.append(j)
            length = len(wordchanges)
            for i in range(length):
                wordchanges.append(wordchanges[i].replace(wordchanges[i], wordchanges[i][0].upper() + wordchanges[i][1:]))
            for i in range(len(result[0])):
                sentence = result[0][i]
                if len(sentence) > 90:
                    continue
                words = sentence.split(' ')
                ans = ''
                for _word in wordchanges:
                    if _word in words:
                        sentence = sentence.replace(_word, _word[0] + '___' + _word[len(_word) - 1])
                        ans = _word
                if ans == '':
                    continue
                Sentence.objects.create(name = sentence, word = word, source = 'Cambridge', chinese = result[1][i], ans = ans)
            if not Sentence.objects.filter(word = word).exists():
                return ('Error', word)
    return ('Success', 0)

class edit_category(APIView):
    def post(self, request, id, format=None):
        data = request.data
        name = data['name']
        description = data['description']
        vol_list = dict(request.data)['vol_list']
        if not categories.objects.filter(id = id).exists():
            return Response({
                'info': 'No this category !'
            }, status=status.HTTP_400_BAD_REQUEST)
        else :
            category = categories.objects.filter(id = id)[0]
            
            ret = buildwords(vol_list)
            if ret[0] != 'Success':
                return Response({
                    'info': 'The word ' + ret[1] + ' was not found in dictionary'
                }, status=status.HTTP_400_BAD_REQUEST)
            else :
                category.name = name
                category.description = description
                category.vol_list = vol_list
                category.save()
                return Response({
                    'info': 'Success !'
                })