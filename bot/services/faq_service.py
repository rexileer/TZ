from asgiref.sync import sync_to_async
from products.models import FAQ


@sync_to_async
def get_faq_questions_from_db():
    return FAQ.objects.all()

@sync_to_async
def get_answer_from_db(faq_id):
    return FAQ.objects.filter(id=faq_id).first()

@sync_to_async
def search_faq_from_db(search_text: str):
    return FAQ.objects.filter(question__icontains=search_text)

