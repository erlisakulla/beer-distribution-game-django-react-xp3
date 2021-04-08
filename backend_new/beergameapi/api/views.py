from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
import json
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAdminUser,IsAuthenticated, SAFE_METHODS, DjangoModelPermissions, BasePermission
from .models import Game, User, Role, Week
from .serializers import GameSerializer, UserSerializer, RoleSerializer, WeekSerializer
# Create your views here.


#permission to edit the game : only by instructor
class GameUserWritePermission(BasePermission):
    message="editing only by the instructor "

    def has_object_permission(self,request,view,obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.instructor==request.user


#creation possible by only instructor
class GameCreatePermission(BasePermission):
    message="creating only by the instructor "

    def has_permission(self,request,view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_instructor


# For all routes api/game/
#  /game/{gameid}
#   /game/{gameid}/getroles - fetch availiable roles
#  /game/{gameid}/getweek - fetch weeks for user in current role.


class gameview(viewsets.ModelViewSet):

    permission_classes=[IsAuthenticated,GameCreatePermission,GameUserWritePermission]
    serializer_class = GameSerializer
    queryset = Game.objects.all()
    # def get_queryset(self):
    #        # user = request.user
    #        # queryset = Game.objects.filter(instructor=user)
    #        # serializer = GameSerializer(queryset, many=True)
    #        # return Response(serializer.data)
    #        return Game.objects.filter(instructor=self.request.user)




    def list(self,request):
        queryset = Game.objects.all().filter(instructor=request.user)
        #return queryset
        serializer = GameSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        user = request.user
        serializer=GameSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save(instructor=user)
            return Response(serializer.data)
        return Response(serializer.error)

    # def list(self,request):
    #     queryset=Game.objects.filter(instructor=request.user)
    #     serializer=GameSerializer(queryset,many=True)
    #     return Response(serializer.deta)


    def retrieve(self, request, pk=None):

        queryset = Game.objects.all()
        game = get_object_or_404(queryset, pk=pk)
        serializer = GameSerializer(game)
        return Response(serializer.data)



    @action(detail=False)
    def all(self,request):
        allgame=Game.objects.all()

        serialized=GameSerializer(allgame,many=True)
        return Response(serialized.data)

    @action(detail=True, methods=['get'])
    # get availiable roles #free roles
    def getroles(self, request, pk=None):
        game = self.get_object()
        roles = game.gameroles.all().filter(playedBy=None)
        serialize = RoleSerializer(roles, many=True)
        return Response(serialize.data)

    @action(detail=True, methods=['get'])
    def getweek(self, request, pk=None):
        game = self.get_object()

        try:  # reverse lookup
            role = game.gameroles.get(playedBy=self.request.user)
            if role:
                print("HERE DEBUG")
                # reverse lookup using relatedname
                weeks = role.roleweeks.all()
                serialize = WeekSerializer(weeks, many=True)
                return Response(serialize.data)
        except:
            return Response({"detail": "Not Registered for this Game"}, status=status.HTTP_403_FORBIDDEN)




# For Route /api/user
# Returns user details name ,email,role
class userview(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request, format="json"):
        serialized = UserSerializer(request.user)
        return Response(serialized.data, status=status.HTTP_200_OK)


# for route /api/create
# only post method allowed for register

class registerview(generics.CreateAPIView):
    serializer_class = UserSerializer



# class roleregister(generics.RetrieveUpdateAPIView):

#     queryset= Role.objects.all()
#     serializer_class= RoleSerializer
#     lookup_field='pk'
#     lookup_field_kwarg='pk'

#viewsets hadnling multiple routes
# starting from /api/role
# /api/role/{roleid} -GET 
# /api/role/{roleid}/register -patch 

class roleview(mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    permission_classes=[IsAuthenticated]
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    #for route /api/role
    #returns active registered roles. 
    def list(self, request):
        user=request.user
        queryset=user.playerrole.all()
        serialized = RoleSerializer(queryset,many=True)
        return Response(serialized.data)

    #for route /api/role/{roleid}/register
    # only patch update playedby field.

    @action(detail=True, methods=['patch'])
    def register(self, request, pk=None):
        user=request.user
        role = self.get_object()
        if user.is_instructor:
            return Response({"detail":"Only a Player can Join a Game"},status=status.HTTP_406_NOT_ACCEPTABLE)

        if(role.playedBy):
            return Response({"detail":"Role already assigned to a Player"},status=status.HTTP_406_NOT_ACCEPTABLE)
        serialized=RoleSerializer(role,data={"playedBy":user.id},partial=True)
        print(serialized)
        if(serialized.is_valid()):
            serialized.save()
            return Response(serialized.data)
        else:
            return Response(serialized.errors,status=status.HTTP_406_NOT_ACCEPTABLE)