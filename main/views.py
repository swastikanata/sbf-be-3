from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import FilmDetailSerializer, FilmSerializer
from .models import Film

# Create your views here.
class Showcase(APIView):
 
    def get(self,request):
        sort = request.GET.get("sort", None)
        
        if sort == "asc":
            film = Film.objects.all().order_by("year_released", "title")
            serializers = FilmSerializer(film, many=True)
        elif sort == "dsc":
            film = Film.objects.all().order_by("-year_released", "title")
            serializers = FilmSerializer(film, many=True)

        else:
            film = Film.objects.all()
            serializers = FilmSerializer(film, many=True)
            
            result = {}
            for temp in serializers.data:
                if temp['genre'] in result.keys():
                    result[temp['genre']].append(temp)
                else:
                    result[temp['genre']] = [temp]
            
            benchmarks = []
            for genre, films in result.items():
                result[genre] = sorted(films, key=lambda x: (-x['likes'], x['title']))
                benchmarks.append(result[genre][0])
            benchmarks = sorted(benchmarks, key=lambda x: (-x['likes'], x['title']))
            
            data = []
            for benchmark in benchmarks:
                data.extend(result[benchmark['genre']])
            return Response({
                "status" : 200,
                "message" : "berhasil mendapatkan film",
                "data": data,
            })
        
        return Response({
            "status" : 200,
            "message" : "berhasil mendapatkan film",
            "data": serializers.data,
        })
            
    def post(self,request):
        films = Film.objects.all()

        judul = request.data['title']
        for film in films:
            if judul == film.title:
                return Response({
                    "status" : 400,
                    "message" : f"Film dengan judul {judul} sudah ada di daftar",
                })

        new_film = Film.objects.create(
            title = request.data['title'],
            poster = request.data['poster'],
            trailer = request.data['trailer'],
            genre = request.data['genre'],
            year_released = request.data['year_released']
        )
        
        return Response({
            "status" : 200,
            "message" : "berhasil menambahkan film",
        })
             
        
class Search(APIView):
    def get(self, request, title):
        try:
            film = Film.objects.filter(title__icontains= title) 
        except Film.DoesNotExist:
            return Response({
                "error": f"tidak ada film dengan judul {title}"
            })
       
        sort = request.GET.get("sort", None)
        
        if sort == "asc":
            film = Film.objects.all().order_by("year_released", "title")
            serializers = FilmSerializer(film, many=True)
        elif sort == "dsc":
            film = Film.objects.all().order_by("-year_released", "title")
            serializers = FilmSerializer(film, many=True)
        
        else:
            film = Film.objects.all()
            serializers = FilmSerializer(film, many=True)
            
            result = {}
            for temp in serializers.data:
                if temp['genre'] in result.keys():
                    result[temp['genre']].append(temp)
                else:
                    result[temp['genre']] = [temp]
            
            benchmarks = []
            for genre, films in result.items():
                result[genre] = sorted(films, key=lambda x: (-x['likes'], x['title']))
                benchmarks.append(result[genre][0])
            benchmarks = sorted(benchmarks, key=lambda x: (-x['likes'], x['title']))
            
            data = []
            for benchmark in benchmarks:
                data.extend(result[benchmark['genre']])
            return Response({
                "status" : 200,
                "message" : "berhasil mendapatkan film",
                "data": data,
            })
        
        return Response({
            "status" : 200,
            "message" : "berhasil mendapatkan film",
            "data": serializers.data,
        })

class Detail(APIView):
    def get(self, request, id):
        try:
            film = Film.objects.get(id=id)
            serializers = FilmDetailSerializer(film)
        except Film.DoesNotExist:
            return Response({
                "error" : f"tidak ada film dengan id {id}"
            })
        
        return Response({
            "status" : 200,
            "message" : "berhasil mendapatkan film",
            "data" : serializers.data
        })
        

    def delete(self, request, id):
        try:
            film = Film.objects.get(id=id)
            film.delete()
            return Response({
                "message" : f"berhasil menghapus film dengan id {id}"
            })
        except Film.DoesNotExist:
            return Response({
                "error" : f"tidak ada film dengan id {id}"
            })

class Like(APIView):
    def put(self, request, id, event):
        try:
            film = Film.objects.get(id=id)
        except Film.DoesNotExist:
            return Response({
                "error" : f"tidak ada film dengan id {id}"
            })

        message = 'berhasil menambahkan '
        if event == 'like':
            film.likes += 1
            message += 'like'
        elif event == 'dislike':
            film.dislikes += 1
            message += 'dislike'
        else:
            return Response({
                "status" : 404,
                "error" : "url tidak ditemukan"
            })
        film.save()

        return Response({
            "status" : 200,
            "message" : message,
        })
