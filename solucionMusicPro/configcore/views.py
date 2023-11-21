from django.shortcuts import render
import Transaction

def index(request):
    tx = Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY, IntegrationType.TEST))
    
    if request.method=="POST":
        resp = tx.create(buy_order, session_id, amount, return_url)
        return render(request,'success.html',resp)
    return render(request,'index.html',)

    
