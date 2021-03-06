from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Stock
from .forms import StockForm

  


def home(request):
    import requests
    import json
 
    
    if request.method == 'POST':
        ticker = request.POST['ticker']
        # https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_fc70752e289f4678a3853a8a9ad0769f
        api_request = requests.get("https://api.worldtradingdata.com/api/v1/stock?symbol=" + ticker + "&api_token=iSyKW4kT4N99ZqdRhzN0v0psVf7QvGpzj2bH9cmwWZN0Hpeo6CaNc6ZIk13P")
        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error..."    
        return render(request, 'home.html', {'title':'Tarpons.Trade - Stocks Screener', 'api':api}) 

    else:
         return render(request, 'home.html', {'title':'Tarpons.Trade - Stocks Screener', 'ticker':"Enter Ticker Symbol"})
    
   
def add_stock(request):
    import requests
    import json

    if request.method == 'POST':
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request,("Stock has been added succesfully"))
            return redirect ('add_stock')

    else:
        ticker = Stock.objects.all()
        output = []
        for ticker_item in ticker:
            #https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_fc70752e289f4678a3853a8a9ad0769f
            api_request = requests.get("https://api.worldtradingdata.com/api/v1/stock?symbol=" + str(ticker_item) + "&api_token=iSyKW4kT4N99ZqdRhzN0v0psVf7QvGpzj2bH9cmwWZN0Hpeo6CaNc6ZIk13P")
            try:
                api = json.loads(api_request.content)
                output.append(api)
            except Exception as e:
                api = "Error..."

 

        return render(request, 'add_stock.html', {'title':'Stocks Portfolio', 'ticker':ticker, 'output':output})

def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, ("Stock has been Deleted!"))
    return redirect(delete_stock)    

 
def about(request):   
    return render(request, 'about.html', {'title':'Tarpons.Trade - About'})  

def delete_stock(request): 
    ticker = Stock.objects.all() 
    return render(request, 'delete_stock.html', {'title':'Tarpons.Trade - Delete Stock','ticker':ticker})   