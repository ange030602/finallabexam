from rest_framework import generics, permissions, viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from .models import Product, Checkout
from .serializers import (
    UserSerializer,
    ProductSerializer,
    CheckoutSerializer,
    AdminCheckoutSerializer
)

# --- Register
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

# --- Login
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({
            'token': token.key,
            'user_id': token.user_id,
        })

# --- Get Role
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_role(request):
    return Response({'role': request.user.userprofile.role})

# --- Product ViewSet
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

# --- Checkout ViewSet
class CheckoutViewSet(viewsets.ModelViewSet):
    queryset = Checkout.objects.all()
    serializer_class = CheckoutSerializer
    permission_classes = [permissions.IsAuthenticated]

# --- Checkout (Consumer)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def checkout_view(request):
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

# --- Admin Checkout List (Custom Admin Role Check)
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def admin_checkout_list(request):
    if not hasattr(request.user, 'userprofile') or request.user.userprofile.role != 'admin':
        return Response({'detail': 'Forbidden: Admins only'}, status=status.HTTP_403_FORBIDDEN)

    checkouts = Checkout.objects.select_related('user', 'product')
    serializer = AdminCheckoutSerializer(checkouts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
