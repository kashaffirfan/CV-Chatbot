from rest_framework.decorators import api_view
from rest_framework.response import Response
from backend.ai_utils import answer_question

@api_view(['GET'])
def chat(request):
    question = request.GET.get('q', '')
    if not question:
        return Response({'error': 'No question provided'}, status=400)
    answer = answer_question(question)
    return Response({'answer': answer})
