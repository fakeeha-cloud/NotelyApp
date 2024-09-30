from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import permissions,authentication
from rest_framework.views import APIView

from notes.serializers import UserSerializer,TaskSerializer
from notes.models import User,Task
from notes.permissions import OwnerOnly

class UserCreationView(generics.CreateAPIView):

    serializer_class=UserSerializer

    # def post(self,request,*args,**kwargs):
    #     serializer_instance=UserSerializer(data=request.data)
    #     if serializer_instance.is_valid():
    #         data=serializer_instance.validated_data
    #         user_obj=User.objects.create_user(**data)
    #         serializer_instance=UserSerializer(user_obj)
    #         return Response(data=serializer_instance.data)
    #     else:
    #         return Response(data=serializer_instance.errors)

class TaskCreateListView(generics.ListCreateAPIView):
    serializer_class=TaskSerializer
    queryset=Task.objects.all()

   # authentication_classes=[authentication.BasicAuthentication]          #for authentication
    authentication_classes=[authentication.TokenAuthentication]  
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):                               #overriding perform_create() for adding owner when doing save task
        return serializer.save(owner=self.request.user)
    
    # def list(self,request,*args,**kwargs):                         Overriding list() method for changing query set(orm query), same as below
    #     qs=Task.objects.filter(owner=request.user)                                    (here is changing orm query)
    #     serializer_instance=TaskSerializer(qs,many=True)
    #     return Response(data=serializer_instance.data)


    def get_queryset(self):                                          #overriding get_queryset() method for changing query set : this code is same as above
       qs=Task.objects.filter(owner=self.request.user)

       if 'category' in self.request.query_params:                   #for optional query parameter =>eg:api- http://127.0.0.1:8000/api/tasks?category=business
           
           #print(request.query_params)=>{'category':['business']} :querydict
          
           cat_value=self.request.query_params.get('category')

           qs=qs.filter(category=cat_value)

       if 'priority' in self.request.query_params:                       #eg:api- http://127.0.0.1:8000/api/tasks?priority=low
           
           pr_value=self.request.query_params.get('priority')

           qs=qs.filter(priority=pr_value)
       
       return qs
    

class TaskRetriveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Task.objects.all()
    serializer_class=TaskSerializer

   # authentication_classes=[authentication.BasicAuthentication]
    authentication_classes=[authentication.TokenAuthentication]                #authentication via token
    permission_classes=[OwnerOnly]                                              #custom permissions (in permissions.py)


from django.db.models import Count
class TaskSummaryApiView(APIView):


    #authentication_classes=[authentication.BasicAuthentication] 
    authentication_classes=[authentication.TokenAuthentication] 
    permission_classes=[permissions.IsAuthenticated]


    def get(self,request,*args,**Kwargs):

        qs=Task.objects.filter(owner=request.user)

        cat_summary=qs.values('category').annotate(count=Count('category'))

        status_summary=qs.values('status').annotate(count=Count('status'))

        priority_summary=qs.values('priority').annotate(count=Count('priority'))

        total_task=qs.count()

        context={
            'category summary':cat_summary,
            'status summary':status_summary,
            'priority summary':priority_summary,
            'total tasks ':total_task
        }

        return Response(data=context)
    
class GetCategoriesAPIView(APIView):
    def get(self,request,*args,**kwargs):
        
        categories=Task.category_choices

        #st=set()
        # for tp in categories:
        #     for cat in tp:
        #         st.add(cat)         (same as below)  

        st={cat for tp in categories for cat in tp}                     #set comprehension : for avoid duplication when taking categories

        return Response(data=st)
    
#In Python, set comprehensions are a concise and readable way to create sets using an expression inside curly braces {}. 
#Set comprehensions are similar to list comprehensions, but the difference is that they generate a set, which automatically removes duplicates and is unordered.