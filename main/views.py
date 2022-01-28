from django.shortcuts import render
from django.core.paginator import Paginator
from firebase_admin import credentials, firestore
from decouple import config
import firebase_admin
import re

# Firebase configuration 
project_config = {
  "type": "service_account",
  "project_id": "ammahelmets",
  "private_key_id": config("private_key_id"),
  "private_key": config("private_key"),
  "client_email": config("client_email"),
  "client_id": config("client_id"),
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-73r9f%40ammahelmets.iam.gserviceaccount.com"
}


cred = credentials.Certificate(project_config)
firebase_admin.initialize_app(cred)

db = firestore.client()


def homePage(request):
  # Collect all data from firestore and sent to home page.
  database = db.collection("Helmets").get()
  paginator = Paginator(database, 8)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number) # Show only 8 items per page
  content = {"data":page_obj}
  return render(request, "index.html", content)



def productDetails(request, id):
  # Get details of the product and show product details on page
  product = db.collection("Helmets").document(id).get()
  if product.exists:
    content = {"product": product.to_dict()}
    return render(request, "productDetails.html", content)
  else:
    return render(request, "noDataPage.html", {"errorTitle": "404: Page not found."})



def stylePage(request, style):
  # Filter out product by category
  product = db.collection("Helmets").where('style', '==', style).get()
  # Check if there is any product in this category

  if product: 
    paginator = Paginator(product, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)  # Show only 8 items per page
    content = {"styleProducts": page_obj, "style": style}
    return render(request, "stylePage.html", content)
  # If not than show no data page.
  else:
    return render(request, "noDataPage.html", {"errorTitle": "No product found in this category."})



def brandPage(request, brand):
  # Filter products by brand name
  product = db.collection("Helmets").where('brand', "==", brand).get()
  # Check if any product of this brand available in store

  if product:
    paginator = Paginator(product, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)  # Show only 8 items per page
    content = {"brandProducts": page_obj, "brand": brand}
    return render(request, 'brandPage.html', content)
  # If no product found than will redirect to No Data Page.
  else:
    return render(request, "noDataPage.html", {"errorTitle": "No product of this brand found."})



def searchProduct(request):
  database = db.collection("Helmets").get()

  # Fetch search bar data
  searchString = request.GET["search"]

  # A empty set to store fetched data from database. To avoid duplicate datas using set() is more wise
  finalProducts = set()

  for word in searchString.split():
    # Search through name of the product
    for data in database:
      dict_data = data.to_dict()
      if re.search(rf"{word.lower()}", dict_data["name"].lower()):
        finalProducts.add(data)

    # Search through name of the brand
    for dataBrand in database:
      dict_dataBrand = dataBrand.to_dict()
      if re.search(rf"{word.lower()}", dict_dataBrand["brand"].lower()):
        finalProducts.add(dataBrand)

    # Search through color of product
    for dataColor in database:
      dict_dataColor = dataColor.to_dict()
      if re.search(rf"{word.lower()}", dict_dataColor["color"].lower()):
        finalProducts.add(dataColor)

  
  if len(finalProducts) == 0:
    return render(request, "noDataPage.html", {"errorTitle": f"We couldn't found match for '{searchString}'."})
  else:
    paginator = Paginator(list(finalProducts), 8)
    pages = request.GET.get("page")
    page_obj = paginator.get_page(pages)
    content = {"datas": page_obj, "searchWord": searchString}
    return render(request, "searchResults.html", content)