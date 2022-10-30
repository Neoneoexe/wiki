from django.contrib import messages
from django.shortcuts import redirect, render
from django import forms
from django.urls import reverse
import random

from . import util

from markdown2 import Markdown

#form to create a new entery
class cnpform(forms.Form):
    name = forms.CharField(label='', widget=forms.TextInput(attrs={
      "placeholder": "Entry Name"}))
    content = forms.CharField(label='', widget=forms.Textarea(attrs={
      "placeholder": "Content"
    }))
class cedit(forms.Form):
    content = forms.CharField(label='', widget=forms.Textarea(attrs={
      "placeholder": "Content"
    }))
markdowner = Markdown()
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def wiki(request, name):
    wiki = util.get_entry(name)
    if not wiki:
        return render(request,"encyclopedia/error.html")
    else:
        return render(request, "encyclopedia/wiki.html", {
            "name": str(name),#debbuging reason we print out name varible
            "wiki": markdowner.convert(wiki),
             })
def search(request):
    #gets q
    query = request.POST.get('q')
    #entries is a simple varible that holds util.list_entries()
    entries = util.list_entries()
    #title is a varible that has the query inside of it
    title = util.get_entry(query)
    
    #list the queries
    queried = []
    for ls in entries:
        lw = ls.lower()
        ew = query.lower()
        if ew in lw or lw in ew:
            queried.append(ls)

    #checks if the title is not empty
    if title != None:
        return render(request, "encyclopedia/search.html", {
            "qt": markdowner.convert(title)
        })
    else:
        return render(request, "encyclopedia/search_list.html", {
                "ls": queried,
                })
    

def cnp(request):
    #lets user create a new page CNP - Create New Page
    if request.method == "GET":
        return render(request,"encyclopedia/cnp.html", {
            "form": cnpform(),
        })
    elif request.method == "POST":
        form = cnpform(request.POST)
        #check if form is valid
        if form.is_valid():
            #clean the data from the form
            name = form.cleaned_data["name"]
            content = form.cleaned_data["content"]
        else:
            #if theres a error with the form then we will redirect them to the form so it can be resubmitted
            messages.error(request, "something went wrong!")
            return redirect('paths:cnp')
        if util.get_entry(name) != None:
            #if theres a entery with that name then will will give a warning message that theres a 
            #excisting entery with that name. 
            messages.error(request, "Entery with that name already exsits!")
            return redirect("paths:cnp")
        else:
            #if everything checks out will go ahead and save that entery.
            util,util.save_entry(name, content)
            #I know I am clever here haha, simplest solution to redirect to the saved entery ;)
            return render(request, "encyclopedia/wiki.html", {
                "wiki": markdowner.convert(util.get_entry(name)),
                "name":name
            })
#I checked on stackoverflow on how to use the messages.error function reference link:
#https://stackoverflow.com/questions/47923952/python-django-how-to-display-error-messages-on-invalid-login

#Random takes the python provided random function and picks a random entery
def random1(request):
    if request.method == "GET":
        title = random.choice(util.list_entries())
        #after picking the random enetery we get the enterys and then simply converte it
        entery = util.get_entry(title)
        #converting the entery
        t = markdowner.convert(entery)


        return render(request, "encyclopedia/wiki.html", {
            "wiki":t,
            "name":title
        })
    else:
        messages.error("Error Occurred!")
        return render(request, "encyclopedia/error.html")

#hardest function I had to work on personally found it more challanging then the rest
def edit(request, name):
    #if method is get then we go ahead and let them use the form before submitting it
    if request.method == "GET":
        content = util.get_entry(name)

        if content == None:
            return messages.error("Empty Page!")
        else:
            return render(request, "encyclopedia/edit.html", {
                "edit": cedit(initial={'content':content}),
                "n":name
            })
    #when submit is clicked we go ahead and follow throught the steps
    elif request.method == "POST":
        #1.assie the subbmited post data to a varible that I called Form
        form = cedit(request.POST)
        #2.Check if that form is valid with the following .is_valid() function
        if form.is_valid():
            #3. If valid we get that data cleaned and assigned to varible / Very boiler plate checking just like in the lecture/notes
            content = form.cleaned_data["content"]
            #4.Save that entry and for debbuging reasons I assigned it to a varible that I name "f"
            f = util.save_entry(name, content)
            #5.if everything checks out then we go ahead and say that it was a succesful edit
            messages.success(request, f"succesfully edited {name} entery!")
            #6.Finally redirect the user to that entery
            return redirect(f"/wiki/{name}")
        #if the form is not valid its going to send them to resubmit just like the GET version up above
        else:
            
            content = util.get_entry(name)

            return render(request, "encyclopedia/edit.html", {
                "edit": cedit(initial={'content':content}),
                "n":name
            })
    #if everthing else fails go ahead and redirect the user to a error page
    else:
        return render(request,"encyclopedia/error.html")

#Personal struggles while coding this project:
#The most annyoing part was setting up the app routs since I couldn't get the edit function to get the name parameter of the wiki function
#Even after trying sevrale methos I ended up finind a simple yet elegant solutin (atleast for me) that was just to simply hardcode
#the url redirects myself I know it may not be very scalable if say the project go bigger but it worked and in the end I was satisfied with it
#hardcoded the url to -> /edit/{{n}} since the optimal {% url 'edit' name=name %} (name being the wiki/<str:name> in urls
# and =name being edit<str:name>)
# wouldn't work
# I used some resources such as stack overflow when I got stuck on a question but not to copy and paste code
# the code that I used is from the following link
#I checked on stackoverflow on how to use the messages.error function reference link:
#https://stackoverflow.com/questions/47923952/python-django-how-to-display-error-messages-on-invalid-login
#I also found the search function quite challenging but after I looked at it in some other prespective it got easier
#I am sorry for any gramatical errors my english is not the best since I am not a native speaker
#Through out the annoying error that a forgotten semiconlen causes I am in love with coding and these cs50 courses
#I loved the experince of doing these challanges and pushing myself if any staff member reads this comment 
#_____$$$$$$$$$____ 111111111111111111111111111 I wish you a wonderful day!
# ____$$$$$$$$$____ 1_________________________1
# ______$$$$$______ 1_________________________1
# ______$$$$$______ 1_______¶¶¶¶¶¶¶¶¶¶________1
# ______$$$$$______ 1_________¶¶¶¶¶¶__________1 
# ______$$$$$______ 1_________¶¶¶¶¶¶__________1
# ____$$$$$$$$$____ 1_________¶¶¶¶¶¶__________1
# ____$$$$$$$$$____ 1_________¶¶¶¶¶¶__________1
# _________________ 1_________¶¶¶¶¶¶__________1
# _$$$$$$___$$$$$$_ 1_________¶¶¶¶¶¶__________1
# $$$$$$$$_$$$$$$$$ 1_________¶¶¶¶¶¶__________1
# $$$$$$$$$$$$$$$$$ 1_________¶¶¶¶¶¶__________1
# _$$$$$$$$$$$$$$$_ 1_________¶¶¶¶¶¶__________1
# ___$$$$$$$$$$$___ 1_______¶¶¶¶¶¶¶¶¶¶________1
# _____$$$$$$$_____ 1_________________________1
# _______$$$_______ 1_________________________1
# ________$________ 1____¶¶¶¶¶_______¶¶¶¶¶____1
# _________________ 1__¶¶¶¶¶¶¶¶¶___¶¶¶¶¶¶¶¶¶__1
# __$$$$$___$$$$$__ 1_¶¶¶¶¶¶¶¶¶¶¶_¶¶¶¶¶¶¶¶¶¶¶_1
# __$$$$$$_$$$$$$__ 1_¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶_1
# ___$$$$$$$$$$$___ 1__¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶__1
# _____$$$$$$$_____ 1____¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶____1
# ______$$$$$______ 1______¶¶¶¶¶¶¶¶¶¶¶¶¶______1
# ______$$$$$______ 1________¶¶¶¶¶¶¶¶¶________1
# ______$$$$$______ 1_________¶¶¶¶¶¶¶_________1
# _________________ 1__________¶¶¶¶¶__________1
# _____$$$$$$$_____ 1___________¶¶¶___________1
# ___$$$$$$$$$$$___ 1____________¶____________1
# __$$$$$___$$$$$__ 1_________________________1
# __$$$$$___$$$$$__ 1_________________________1
# __$$$$$___$$$$$__ 1_¶¶¶¶¶¶¶¶¶_____¶¶¶¶¶¶¶¶¶_1
# ___$$$$$$$$$$$___ 1___¶¶¶¶¶_________¶¶¶¶¶___1
# _____$$$$$$$_____ 1___¶¶¶¶¶_________¶¶¶¶¶___1
# _________________ 1___¶¶¶¶¶_________¶¶¶¶¶___1
# __$$$$$___$$$$$__ 1___¶¶¶¶¶_________¶¶¶¶¶___1
# __$$$$$___$$$$$__ 1___¶¶¶¶¶_________¶¶¶¶¶___1
# __$$$$$___$$$$$__ 1___¶¶¶¶¶_________¶¶¶¶¶___1
# __$$$$$___$$$$$__ 1___¶¶¶¶¶_________¶¶¶¶¶___1
# __$$$$$$_$$$$$$__ 1___¶¶¶¶¶¶_______¶¶¶¶¶¶___1
# ___$$$$$$$$$$$___ 1____¶¶¶¶¶¶_____¶¶¶¶¶¶____1
# ____$$$$$$$$$____ 1______¶¶¶¶¶¶¶¶¶¶¶¶¶______1
#                   1________¶¶¶¶¶¶¶¶¶________1
#                   1_________________________1
#                   111111111111111111111111111  
                    

