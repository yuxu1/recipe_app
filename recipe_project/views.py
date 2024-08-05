from django.shortcuts import render, redirect
#Django authentication libraries
from django.contrib.auth import authenticate, login, logout
#Django Form for authentication
from django.contrib.auth.forms import AuthenticationForm


#function-based view 'login_view' that takes a request from user
def login_view(request):
    #initialize
    #error_message to None
    error_message = None
    #form object with username and password fields
    form = AuthenticationForm()

    #when user hits "login" button, then POST request is generated
    if request.method == 'POST':
        #read the data sent by the form via POST request
        form = AuthenticationForm(data=request.POST)

        #check if form is valid
        if form.is_valid():
            #read username and password
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            #use Django authenticate function to validate the user
            user = authenticate(username=username, password=password)

            #if user is authenticated
            if user is not None:
                #then use pre-defined Django function to login
                login(request, user)
                #and send user to desired page(list view of all recipes)
                return redirect('recipes:recipes')
        #in case of error
        else:
            error_message = 'oops...something went wrong'
        
    #prepare data (form data and error message) to send from view to template
    context = {
        'form': form,
        'error_message': error_message
    }
    #load the login page using "context" information
    return render(request, 'auth/login.html', context)


#define a function-based view ('logout_view') that takes a request from user
def logout_view(request):
    #use the pre-defined Django function to logout
    logout(request)
    #redirect to home page after logging out
    return render(request, 'auth/logout.html')