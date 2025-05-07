from rest_framework import generics, permissions, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Product, Checkout
from .serializers import UserSerializer, ProductSerializer, CheckoutSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Product, Checkout

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'user_id': token.user_id})

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_role(request):
    return Response({'role': request.user.userprofile.role})


@api_view(['POST'])
def checkout_view(request):
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)

    product_id = request.data.get('product')
    quantity = int(request.data.get('quantity', 0))
    user_id = request.data.get('user')

    if not product_id or not user_id:
        return Response({'error': 'Missing product or user ID'}, status=status.HTTP_400_BAD_REQUEST)

    if quantity <= 0:
        return Response({'error': 'Quantity must be positive.'}, status=status.HTTP_400_BAD_REQUEST)

    product = get_object_or_404(Product, id=product_id)

    if product.stock < quantity:
        return Response({'error': f'Only {product.stock} items left in stock.'}, status=status.HTTP_400_BAD_REQUEST)

    product.stock -= quantity
    product.save()

    Checkout.objects.create(
        user_id=user_id,
        product=product,
        quantity=quantity
    )

    return Response({
        'message': f'{quantity} item(s) of {product.name} checked out successfully.',
        'remaining_stock': product.stock
    }, status=status.HTTP_201_CREATED)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

class CheckoutViewSet(viewsets.ModelViewSet):
    queryset = Checkout.objects.all()
    serializer_class = CheckoutSerializer
    permission_classes = [permissions.IsAuthenticated]
