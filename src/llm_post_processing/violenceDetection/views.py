
from rest_framework.views import APIView
from violenceDetection.serializers import InputTextSerializer
from rest_framework.response import Response
from violenceDetection.checkViolence import ViolenceDetector

class InputTextViewSet(APIView):
    serializer_class = InputTextSerializer

    def post(self, request):
        text = request.data['input_text']
        result = ViolenceDetector().checkViolence(text)
        
        if result==1:
            return Response({"verdict": result, "message": "Sorry I cannot process your request as the text you entered contains violent content."})
        else:
            return Response({"verdict": result, "message": "The text does not contain violent content."})
