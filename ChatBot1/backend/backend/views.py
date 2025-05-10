from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CV
from .serializers import CVSerializer
from .ai_utils import extract_text_from_file, update_embeddings, answer_question
from rest_framework import status




@api_view(['POST'])
def upload_cv(request):
    file = request.FILES.get('file')
    if file:
        # Save it or process it here
        return Response({'message': 'CV uploaded successfully'}, status=status.HTTP_201_CREATED)
    return Response({'error': 'No file received'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def chat(request):
    question = request.GET.get('q', '')
    if not question:
        return Response({'error': 'No question provided'}, status=400)
    answer = answer_question(question)
    return Response({'answer': answer})

class CVViewSet(viewsets.ModelViewSet):
    queryset = CV.objects.all()
    serializer_class = CVSerializer

    def perform_create(self, serializer):
        cv = serializer.save()
        text = extract_text_from_file(cv.file.path)
        cv.extracted_text = text
        cv.save()
        update_embeddings(CV.objects.all())

    def perform_update(self, serializer):
        cv = serializer.save()
        text = extract_text_from_file(cv.file.path)
        cv.extracted_text = text
        cv.save()
        update_embeddings(CV.objects.all())

    def perform_destroy(self, instance):
        instance.delete()
        update_embeddings(CV.objects.all())