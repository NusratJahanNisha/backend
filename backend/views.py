from .firebase import db
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
import re

#view class that fetches data from the db
def home(request):
    trans_ref = db.collection(u'transactions')
    snapshots = list(trans_ref.get())
    docs = []

    for snapshot in snapshots:
        doc = snapshot.to_dict() #change snapshot index to see change in home.html template
        docs.append(doc)

    #return render(request, "home.html", {"tid": tid, "amount": amount, "sender": sender, "reciever": reciever})
    return render(request, "home.html", {"doclist": docs})

def update(request):
    trans_ref = db.collection(u'transactions')

    error = False
    if request.POST:
        print(request.POST)
        if 'tid' in request.POST:
            tid = request.POST.get("tid")
        else:
            error = True

        if 'amount' in request.POST:
            amount = request.POST.get("amount")
        else:
            error = True
        
        if 'sender_name' in request.POST:
            name = request.POST.get("sender_name")
        else:
            error = True

        if not error:
            tid_ref = trans_ref.document(tid)
            if tid_ref.get().exists:
                tid_ref.update({'amount': amount, 'sender': name})
                return HttpResponse("Document {tid} successfully updated.".format(tid=tid))
            else:
                return HttpResponse("Document {tid} doesn't exist. Cannot update.".format(tid=tid))
        else:
            return HttpResponse("Error")

    else:
        return render(request, 'home.html')

def add(request):
    trans_ref = db.collection(u'transactions')
    snapshots = list(trans_ref.get())
    doc = snapshots[-1].to_dict()

    tid = doc.get('tid')
    tid = re.sub(r'[0-9]+$', 
             lambda x: f"{str(int(x.group())+1).zfill(len(x.group()))}",  
             tid)
    print(tid)

    error = False
    if request.POST:
        print(request.POST)
        if 'amount' in request.POST:
            amount = request.POST.get("amount")
        else:
            error = True
        
        if 'sender_name' in request.POST:
            sender = request.POST.get("sender_name")
        else:
            error = True

        if 'sender_name' in request.POST:
            reciever = request.POST.get("sender_name")
        else:
            error = True

        if not error:
            data = {
                u'tid': tid,
                u'amount': amount,
                u'sender': sender,
                u'reciever': reciever
            }
            trans_ref.document(tid).set(data)
            return HttpResponse("Entry Added")
        else:
            return HttpResponse("Error")
            
    else:
        return render(request, 'home.html')

def delete(request):
    trans_ref = db.collection(u'transactions')

    error = False
    if request.POST:
        print(request.POST)
        if 'tid' in request.POST:
            tid = request.POST.get("tid")
        else:
            error = True

        if not error:
            tid_ref = trans_ref.document(tid)
            if tid_ref.get().exists:
                tid_ref.delete()
                return HttpResponse("Document {tid} successfully deleted.".format(tid=tid))
            else:
                return HttpResponse("Document {tid} doesn't exist. Cannot delete.".format(tid=tid))
        else:
            return HttpResponse("Error")

    else:
        return render(request, 'home.html')