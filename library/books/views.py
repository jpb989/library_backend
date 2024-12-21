import json
from rest_framework.pagination import PageNumberPagination
from .models import Author, Book, BorrowRecord
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView, ListAPIView
from rest_framework.views import APIView
from .serializers import AuthorSerializer, BookSerializer, BorrowRecordSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from library.tasks import generate_report
import os

#Pagination for limiting number of data retreived
class PaginationConfig(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


#Author APIs

class AuthorListView(ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    pagination_class = PaginationConfig
    

class AuthorDetailView(RetrieveAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class AuthorCreateView(CreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]


class AuthorDeleteView(DestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

class AuthorUpdateView(UpdateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]


#Book APIs


class BookListView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = PaginationConfig
    

class BookDetailView(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookCreateView(CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]


class BookDeleteView(DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

class BookUpdateView(UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]


#Borrow Record APIs

class BorrowBookView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = BorrowRecordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()  # `borrowed_by` is automatically set to the logged-in user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReturnBookView(APIView):
    authentication_classes = [JWTAuthentication]

    def put(self, request, id):
        try:
            # Fetch the borrow record by ID where the return date is NULL
            borrow_record = BorrowRecord.objects.get(
                id=id, return_date__isnull=True
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


class ReportView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Get the latest report file
        reports_dir = "reports/"
        try:
            latest_report = sorted(os.listdir(reports_dir))[-1]
            with open(os.path.join(reports_dir, latest_report), "r") as report_file:
                report_data = report_file.read()
            return Response(json.loads(report_data), status=status.HTTP_200_OK)
        except (IndexError, FileNotFoundError):
            return Response({"error": "No reports available."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        # Trigger the Celery task
        result = generate_report.delay()
        return Response(
            {"message": "Report generation started.", "task_id": result.id},
            status=status.HTTP_202_ACCEPTED,
        )