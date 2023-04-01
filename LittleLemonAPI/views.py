from rest_framework.viewsets import ModelViewSet
from .models import MenuItem, Cart, Order
from .serializers import MenuItemSerializer, CartSerializer, OrderSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.contrib.auth.models import User, Group
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions, exceptions


# Create your views here.

class ManagerPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.groups.filter(name="manager").exists():
            raise exceptions.PermissionDenied("You are not authorized to access this resource")
        return True


class MenuItemViews(ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [ManagerPermissions | IsAdminUser]

        return [permission() for permission in permission_classes]
    

@api_view(['GET', 'POST'])
@permission_classes([ManagerPermissions])
def list_add_managers(request):
    user = request.user
    manager_group = Group.objects.get(name='manager')
    if request.method == 'GET':

        managers = User.objects.filter(groups=manager_group).values("id", "username")
        return Response({"data": managers}, status.HTTP_200_OK)
    
    elif request.method == 'POST':
        username = request.data['username']
        if username:
            user = User.objects.get(username=username)
            manager_group.user_set.add(user)
            return Response(status=status.HTTP_201_CREATED)
        return Response({"msg": "error"}, status=status.HTTP_400_BAD_REQUEST)


    return Response({}, 200)

@permission_classes([ManagerPermissions])
@api_view(['DELETE'])
def delete_managers(request, userId):
    user = User.objects.get(id=userId)
    manager_group = Group.objects.get(name='manager')

    if request.method == 'DELETE':
        manager_group.user_set.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET', 'POST'])
@permission_classes([ManagerPermissions])
def list_add_delivery_crew(request):
    user = request.user
    delivery_crew_group = Group.objects.get(name='manager')
    if request.method == 'GET':

        delivery_crew = User.objects.filter(groups=delivery_crew_group).values("id", "username")
        return Response({"data": delivery_crew}, status.HTTP_200_OK)
    
    elif request.method == 'POST':
        username = request.data['username']
        if username:
            user = User.objects.get(username=username)
            delivery_crew_group.user_set.add(user)
            return Response(status=status.HTTP_201_CREATED)
        return Response({"msg": "error"}, status=status.HTTP_400_BAD_REQUEST)


    return Response({}, 200)

@permission_classes([ManagerPermissions])
@api_view(['DELETE'])
def delete_delivery_crew(request, userId):
    user = User.objects.get(id=userId)
    delivery_crew_group = Group.objects.get(name='deliverry crew')

    if request.method == 'DELETE':
        delivery_crew_group.user_set.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartViews(ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        cart_items = Cart.objects.filter(user=user)
        return cart_items

    def get_object(self):
        queryset = self.get_queryset()
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    


class OrderViews(ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    