from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from . import util
from django.http import HttpResponseRedirect
import re
import markdown2
from markdown2 import Markdown
from random import choice
from django import forms


markdowner = Markdown()

class NewAddForm(forms.Form):
    title = forms.CharField(label= "Title", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(label="New Entry", required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))

class Edit(forms.Form):
    title = forms.CharField(label= "Title", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(label="Edit Content", required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        
    })

def get_title(request, title):
    markdowner = Markdown()
    entries = util.list_entries()

    if title in entries:
        page = util.get_entry(title)
        markdowner = markdowner.convert(page)
        return render(request, "encyclopedia/pagetitle.html",{
            "page": markdowner,
            "title": title
        })
    else:
        return render(request, "encyclopedia/404Error.html",{
            "page": title
        })

def search(request):
    if request.method == "GET":
        query = request.GET["q"]
        entry = util.get_entry(query)
        
        if entry:
            page = markdown2.markdown(util.get_entry(query))
            return render(request, "encyclopedia/pagetitle.html",{
                "title": query,
                "page": page
            })

        else:
            entries = util.list_entries()
            substring = []
            for entry1 in entries:
                print(entry1)
                if re.search(query, entry1, re.IGNORECASE):
                    substring.append(entry1)
                    print(substring)
                    
            if substring:
                return render(request, "encyclopedia/index.html",{
                    "entries":substring
                })
            else:
                return render(request, "encyclopedia/404Error.html",{
                    "page": query
                })

def random(request):
    return get_title(request,choice(util.list_entries()))

def create(request):
    if request.method == "POST":
            form = NewAddForm(request.POST)

            if form.is_valid():
                title = form.cleaned_data['title']
                content = form.cleaned_data['content']
                entries1 = util.list_entries()
                for name in entries1:
                    if title.lower() == name.lower() or title.upper() == name.upper():
                        message = "Page exists with title '%s'" %name
                        return render(request, "encyclopedia/new.html",{
                            "form": form,
                            "error": message
                        })
                        
                
                if util.get_entry(title) is None:
                    util.save_entry(title,content)
                    return HttpResponseRedirect(reverse("wiki:index"))
    else:
        if request.method == "GET":
            return render(request,"encyclopedia/new.html",{
                "form": NewAddForm()
            })

def edit(request):
    title = request.POST.get("edit")
    content = util.get_entry(title)
    

    form_edit = Edit(initial={'title':title,'content':content})
    
    if form_edit.is_valid():

        return render(request, "encyclopedia/edit.html",{
            "title":title,
            "form_edit": form_edit
        })
    else:
        return render(request, "encyclopedia/edit.html",{
            "title":title,
            "form_edit": form_edit
        })


def save(request):

    form_edit = Edit(request.POST)
    
    if form_edit.is_valid():
        title = form_edit.cleaned_data["title"]
        content = form_edit.cleaned_data["content"]
        

        util.save_entry(title,content)
        converted = markdowner.convert(content)
        return render(request,"encyclopedia/pagetitle.html",{
                'page': converted,
                'title': title
            })
    else:
        return render(request, "encyclopedia/edit.html",{
            "title":title,
            "form_edit": form_edit
        })

    


                
  
            


             


            
                



      

        
       







