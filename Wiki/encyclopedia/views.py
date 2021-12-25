
from django import forms
from django.shortcuts import render
from django.shortcuts import HttpResponse

from . import util

import markdown2
from random import randint


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea, label="Content")


def randomEntry():
    listOfEntries = util.list_entries()
    n = len(listOfEntries)

    return listOfEntries[randint(0, n - 1)]


def index(request):
    return render(request, "encyclopedia/index.html", {
        "TITLE": "Encyclopedia",
        "HEADING": "All Pages",
        "entries": util.list_entries(),
        "randEntry": randomEntry()
    })


def error(request, errorTitle, errorMessage):
    return render(request, "encyclopedia/error.html", {
            "errorTitle": errorTitle,
            "errorMessage": errorMessage,
            "randEntry": randomEntry()
        })


def entry(request, TITLE):

    mdText = util.get_entry(TITLE)

    if not mdText:  # entry does not exist
        return error(request, "ERROR 404", "The requested page not found !")

    else:   # entry does exist
        return render(request, "encyclopedia/entry.html", {
            "TITLE": TITLE,
            "content": markdown2.markdown(mdText),
            "randEntry": randomEntry()
        })


def search(request):
    if request.method == "POST":
        
        query = request.POST.get('q')
        lenQ = len(query)   # length of the query

        listOfEntries = util.list_entries()

        if query in listOfEntries:  # query matches a name of an encyclopedia entry ?
            return entry(request, query)

        searchList = []
        for elt in listOfEntries:

            if query in elt:    # is query a substring of elt ?
                searchList.append(elt)

        return render(request, "encyclopedia/index.html", {
            "TITLE": query,
            "HEADING": f"Search Results for '{query}'",
            "entries": searchList,
            "randEntry": randomEntry()
        })
    else:
        return index(request)


def create(request):
    if request.method == "POST":

        title = request.POST.get("title")

        if title in util.list_entries():    # already exists ?
            return error(request, "ERROR (Conflict found)", "A page with the same title already exists !")
        
        content = request.POST.get("content")

        util.save_entry(title, content)     # creating new page

        return entry(request, title)

    return render(request, "encyclopedia/create.html", {
        "form": NewEntryForm()
    })


def edit(request):
    if request.method == "POST":
        
        title = request.POST.get("title")   # it exists !
        content = util.get_entry(title)

        return render(request, "encyclopedia/edit.html", {
            "form": NewEntryForm(initial={'title': title, 'content': content})
        })
    
def modify(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        util.save_entry(title, content)     # modifying the page
        return entry(request, title)