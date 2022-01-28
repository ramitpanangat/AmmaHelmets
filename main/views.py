from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import Http404
from firebase_admin import credentials, firestore
import firebase_admin
import re

# Firebase configuration 
config = {
  "type": "service_account",
  "project_id": "ammahelmets",
  "private_key_id": "fd10ced8566d04dbb48e19a78f2d87bd4a617f0e",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDU9zqdPVediLF4\nIv7KOcdWxX3wHP7wu4L8U4slCnm/udInqVuiQd8lEO7EkN+HuFFVp5AwPhe45JMj\nvbXYHIqrDQR/8dHC7SKnq7edYUMVRpTr6BufsFOMoSxgCkbWYv5+ke49kctFgq0N\ntzvl7Rtwfo+/DCrlXOWeQ6yWSpl9mTIZ806x/25yD3BD3mh+v3AoJwo7egJA2YEQ\nJYBfYivkSR7qFyo5p6XG/CYfY8Cq3nXtpLQ5v6pxqFUxuGO6yByvRbcotPhM08VA\n1vL0Y/dywialxED5yBlzRpMBftyGgONIk5PjhU+PmB2kHEt5QI03QcqpRsTA/p4B\nrSnW9+97AgMBAAECggEAV8TKVdpdnRGkXmhBzJMyabr707UHhqwo6BgAPRRLp+4L\nxAfCuaTfM7X+SWmRjiwy7ROhU5iLi0o8r9q0MmxU4/j59UbylZzIjwSwqD5Y+NA9\neNoQZGg1jrwv/ybNGfbzfrNi1eIbvbqE2qW9HF3zVJH8aRa5KQz3nxmx68Cz8HQt\nmsNbeYJhmM6+luAQlCJHJjVUPZXW5nFzsa1qfTzilmLhUAaGsFoPNsWby3vAfZae\nke8e8SEiLdUZcrOoiu7FnE5S95vP5MLuVY7z5we3Xun40vu9ngPhqsAqlPcuIB8C\nRuszm2WzqSlIQDWTbiTMLfEoBpyqaKr+claYiJpoKQKBgQDtXnCx3WfkoqPP9nAp\nEuoyRz+mzmqJe2sLMbMbW+fnL3C6HYzqwTG0fQcvG8KZDhEhjbYnP2xMeCeKPpkZ\n8JR7FI24BhgXuZfh+U/m37kkjThpkb9kdGW+7CqXBifUn9LAppJOmbBgaPYZ+cgE\nhMuEdqONXSoaiT3EnrjHA/9e+QKBgQDlrnHntrt/Vci8WN/CKmbmMQvptCe+1LxA\nQmIlwA+NBHKjo9Zw0wzsjmBnXzsJlR+smf91/HjD0oa81q/QPcGaoLIA++zTTN/k\nWvNE37sPkdtixVXmC00KUB5iRMnTFzsSUR+XTBDRCkZY5c0t2GBBSYu0ihGc+nfy\naRKHGsS7EwKBgQDGIuvs/ESJy9zzbeFH19sX5vNR2MGDSzsaF/1KnBfimW3+XUZQ\ner1zzF2fzAtO2Tghivn+nulWl4Fh20jPJ0u5xXlan/OicjA+124D6MHRqfPp41gg\nkSyRBu+yKtg6msJAP4qnA5D/mP28xwxYAUUkqCdzi83mYqLlqhvRPBwBeQKBgGrY\nTsai+/ANYPc1RMoXXYzh7g/GreKZJgWim/PBt7o7AnVbZwtPMqjsxq3v4A/iHjz1\n2p/xVeCKlAFOwbTWtbSP4p6QkyfskA6zvI0ioutoR61X7VC5mxocETZXl6eqG+G2\neUKxsPT9maILLPqRuJ1GcEYJII5s+dV7yZGuAyyfAoGBANUZS51QXWOPqrK1SQOq\n254va4b3UCIvdhd79N875yjkXphFuiJsSvieqvifHZ2mcFDMCub8PGi2TYsrdDa+\nhLmgR2QRPF0B+CfxkARGJ6c1bSu5eqXHAdYT7RgKOBf7ITyBJUfIKGrR3fseMirs\n5+mNWoN+AgJHYtswafUsJucG\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-73r9f@ammahelmets.iam.gserviceaccount.com",
  "client_id": "104597412278810775543",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-73r9f%40ammahelmets.iam.gserviceaccount.com"
}


cred = credentials.Certificate(config)
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