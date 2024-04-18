from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from fuzzywuzzy import process

from .models import Receipt, Category
from .forms import ReceiptForm, ProfileForm
from . import utils


def home(request):
    
    receipts = Receipt.objects.order_by('?')[:5]
    print(receipts)

    context = {
        'receipts': receipts,
    
    }
    return render(request, 'receiptsapp/home.html', context)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                print(f'Ошибки проверки {field}: {errors}')
    else:
        form = UserCreationForm()
    return render(request, 'receiptsapp/registration.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home') 
    return render(request, 'receiptsapp/login.html')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'receiptsapp/edit_profile.html', {'form': form})


def receipts(request):
    return render(request, 'receiptsapp/home.html')


def get_receipt(request, receipt_id):
    receipt = get_object_or_404(Receipt, pk=receipt_id)

    context = {
        'receipt': receipt,
        'steps': utils.make_sequence_steps_article(receipt.sequence_steps),
    }

    return render(request, 'receiptsapp/receipt_detail.html', context)


@login_required
def add_receipt(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = ReceiptForm(request.POST, request.FILES) 
        if form.is_valid():
            new_receipt = form.save(commit=False) 
            new_receipt.author = request.user  
            new_receipt.save() 

            categories = request.POST.getlist('categories')
            new_receipt.categories.set(Category.objects.filter(pk__in=categories))

            return redirect('home')
    else:
        form = ReceiptForm()  

    return render(request, 'receiptsapp/add_receipt.html', {'form': form, 'categories': categories})


def find_best_matching_receipt(request, receipt_name):
    all_receipt_names = Receipt.objects.values_list('name', flat=True)

    best_match = process.extractOne(receipt_name, all_receipt_names)

    if best_match[1] >= 50:
        return best_match[0]

    return None


def get_receipt_by_name(request, receipt_name):
    best_matching_receipt = find_best_matching_receipt(request, receipt_name)

    if best_matching_receipt:
        receipt = Receipt.objects.filter(name=best_matching_receipt).first()
        return redirect('receipt', receipt_id=receipt.id)
    return render(request, 'receiptsapp/no_receipt_found.html')


@login_required  
def edit_receipt(request, receipt_id):
    receipt = get_object_or_404(Receipt, id=receipt_id)
    categories = Category.objects.all()

    if request.user == receipt.author:
        if request.method == 'POST':
            form = ReceiptForm(request.POST, instance=receipt)
            if form.is_valid():
                form.save()
                return redirect('receipt_detail', receipt.id)  
        else:
            form = ReceiptForm(instance=receipt)
        return render(request,
                      'receiptsapp/edit_receipt.html',
                      {'form': form, 'receipt': receipt, 'categories': categories}
                      )
    else:
        return redirect('home')


def get_receipts(request, user=None):
    if user:
        user_obj = User.objects.filter(username=user).first()
        if user_obj:
            receipts = Receipt.objects.filter(author=user_obj)
        else:
            receipts = []
    else:

        receipts = Receipt.objects.all()

    context = {
        'receipts': receipts
    }

    return render(request, 'receiptsapp/receipt_list.html', context)


def search_receipts(request):
    query = request.GET.get('q', '') 
    results = get_receipt_by_name(query) 

    return render(request, 'receiptsapp/search_results.html', {'results': results, 'query': query})