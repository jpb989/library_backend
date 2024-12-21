from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import BorrowRecord
from .serializers import BorrowRecordSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

#Borrow Record APIs

class BorrowBookView(APIView):
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return BorrowRecord.objects.all()

    request_body = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'book': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the book being borrowed")
        },
        required=['book', 'borrow_date']  # Make sure these fields are required
    )

    @swagger_auto_schema(request_body=request_body)
    def post(self, request):
        serializer = BorrowRecordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()  # `borrowed_by` is automatically set to the logged-in user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReturnBookView(APIView):
    authentication_classes = [JWTAuthentication]
    
    def get_queryset(self):
        return BorrowRecord.objects.all()

    request_body = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'return_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description="Return date of the book in format YYYY-MM-DD")
        },
        required=['return_date']  # Make sure these fields are required
    )

    @swagger_auto_schema(request_body=request_body)
    def put(self, request, pk):  # changed 'id' to 'pk'
        try:
            # Fetch the borrow record by pk (primary key)
            borrow_record = BorrowRecord.objects.get(
                pk=pk, return_date__isnull=True  # changed 'id' to 'pk'
            )
        except BorrowRecord.DoesNotExist:
            return Response(
                {"error": "No active borrow record found with this ID."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Ensure the book is being returned by the correct user
        if borrow_record.borrowed_by != request.user:
            return Response(
                {"error": "You are not authorized to return this book."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Validate the return date
        return_date = request.data.get("return_date")
        if not return_date:
            return Response(
                {"error": "Return date is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if return_date < str(borrow_record.borrow_date):
            return Response(
                {"error": "Return date cannot be earlier than the borrow date."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Mark the book as returned
        borrow_record.return_date = return_date
        borrow_record.save()

        # Increase available copies
        book = borrow_record.book
        book.available_copies += 1
        book.save()

        return Response(
            {"message": "Book returned successfully."}, status=status.HTTP_200_OK
        )
