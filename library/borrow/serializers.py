from rest_framework import serializers
from .models import BorrowRecord


class BorrowRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRecord
        fields = ['id', 'book', 'borrowed_by', 'borrow_date', 'return_date']
        read_only_fields = ['borrowed_by', 'borrow_date', 'return_date']

    def validate(self, data):
        # Ensure there are available copies of the book
        book = data['book']
        if book.available_copies <= 0:
            raise serializers.ValidationError("No copies of the book are available for borrowing.")
        return data

    def create(self, validated_data):
        # Automatically associate the `borrowed_by` field with the logged-in user
        user = self.context['request'].user
        validated_data['borrowed_by'] = user

        # Decrease available copies of the book
        book = validated_data['book']
        book.available_copies -= 1
        book.save()

        return super().create(validated_data)