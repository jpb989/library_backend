import json
from datetime import datetime
from celery import shared_task
from books.models import Author, Book, BorrowRecord

@shared_task
def generate_report():
    # Generate the report data
    report_data = {
        "total_authors": Author.objects.count(),
        "total_books": Book.objects.count(),
        "total_books_borrowed": BorrowRecord.objects.filter(return_date__isnull=True).count(),
    }

    # Generate the report file path
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"report_{timestamp}.json"
    report_path = f"reports/{report_filename}"

    # Save the report as a JSON file
    with open(report_path, "w") as report_file:
        json.dump(report_data, report_file)

    return report_path
