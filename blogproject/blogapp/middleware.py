from django.http import HttpResponse
class AppMaintenanceMiddleware(object):
      def __init__(self,get_response):
            self.get_response=get_response
      def __call__(self,request):
            return HttpResponse('<h1>Currently Application under maintenance...Please try after 2 days !!!</h1>')

class ErrorMessageMiddleware(object):
      def __init__(self,get_response):
           self.get_response=get_response
      def __call__(self,request):
            response=self.get_response(request)
            return response
      def process_exception(self,request,exception):

                      s1='<h1>Currently we are facing some technical problems,Plz try after some time</h1><hr>'

                      s2=f'<h2>Raised Exception:{exception.__class__.__name__}</h2>'

                      s3=f'<h2>Exception Description/Message:{exception}</h2>'

                      return HttpResponse(s1+s2+s3)
