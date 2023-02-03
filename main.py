from typing import Union
from fastapi import FastAPI, Request, File, Query
import requests
import json
import xmltodict
import re
import csv
import aiomysql
import pprint
from utilis import engine_msssql
app = FastAPI()






@app.post("/sendrequest")
def send_request():
    url = "https://swahiliesapi.invict.site/Api"
    callbackurl = "https://00bd-41-139-210-222.ngrok.io"
    payload = {
        "api": 170,
        "code": 104,
        "data": {
            "api_key": "ODM3ODQ0Mjk2M2E3NDY0ZTgyMjA3ODdmMTk2YmVlNmI=",
            "order_id": 21,
            "amount": 20,
            "username": "test company",
            "is_live": False,
            "phone_number": 255783262616,
            "cancel_url": callbackurl+str("/cancel"),
            "webhook_url": callbackurl+str("/response"),
            "success_url": callbackurl+str("/success"),
            "metadata": {
                "anykey": "testkey",
                "another_anyKey": "another_anyvalue"
            }

        }
    }
    # return payload
    headers = {'Content-type': 'application/json'}
    data = json.dumps(payload)
    response = requests.request("POST", url, headers=headers, data=data)
    print(response.text)

    

@app.post("/cancel")
def cancel_request(request):
    return request

@app.post("/response")
async def respons_return(request: Request):
    data = json.loads(await request.body())
    print(data)
    # print(data["code"])
    # print(data["timestamp"])
    # print(data["transaction_details"]["order_id"])
    # print(data["transaction_details"]["reference_id"])
    # print(data["transaction_details"]["amount"])
    # print(data["transaction_details"]["metadata"])
    
@app.post("/success")
def success_request(request):
    return request

@app.post("/reconciliation")
def reconciliate():
    url = "https://swahiliesapi.invict.site/Api"
    payload = {
        "api" :170,
        "code":103,
        "data":{
            "api_key": "ODM3ODQ0Mjk2M2E3NDY0ZTgyMjA3ODdmMTk2YmVlNmI=",
        }
    }
    
    # return payload
    headers = {'Content-type': 'application/json'}
    data = json.dumps(payload)
    response = requests.request("POST", url, headers=headers, data=data)
    data  = json.loads(response.text)
    return data["orders"]
    # return data
    
@app.post("/make-payments")
def payments():
    order_id = "15c541126db941e79c558de35dc1f327"
    url = "https://swahiliespay.invict.site/make-payment-1.html?order="+str(order_id)
    return url

@app.post("/upload-xml")
async def upload_xml(file: bytes = File(...)):
    # connects = engine_msssql.connect()
    
    connection = await aiomysql.connect(host='localhost',user='root', password='', db='invoices')
    cursor = await connection.cursor()
    data = xmltodict.parse(file)
    insert_stmt = '''INSERT INTO invoices (invoice_number, cu_serial_number, cu_invoice_number,amount,invoice_date) VALUES (?,?,?,?,?)'''
    for invoice in data ['BatchResult']['Invoice']:
        invoice_number = invoice["@Number"]
        authorised_hash = invoice["AuthorisedHash"]
        cu_serial_match = re.search(r"CU Serial Number:(\S+)", authorised_hash)
        cu_invoice_match = re.search(r"CU Invoice Number:(\S+)", authorised_hash)
        match = re.search(r"CU Invoice Number:(\S+)", authorised_hash)
        match1 = re.search(r"CU Invoice Number:\S+\s(\S+)", authorised_hash)
        date_time = authorised_hash.split("\n")[-1]
        cu_serial_number = cu_serial_match.group(1)
        cu_invoice_number = cu_invoice_match.group(1)
        amount = match1.group(1)
        result = engine_msssql.execute(insert_stmt, (invoice_number, cu_serial_number,cu_invoice_number, amount, date_time))
        print(result)
        
        with open("invoice_data.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Invoice Number", "CU Serial Number", "CU Invoice Number", "Amount", "Date-time"])
            for invoice in data["BatchResult"]["Invoice"]:
                invoice_number = invoice["@Number"]
                match = re.search(r"CU Serial Number:(\S+) CU Invoice Number:(\S+) (\S+)", invoice["AuthorisedHash"])
                cu_invoice_match = re.search(r"CU Invoice Number:(\S+)", authorised_hash)
                cu_serial_number = match.group(1)
                cu_invoice_number = invoice['AuthorisedHash'].split("CU Invoice Number:")[1].split(" ")[0]
                amount = match.group(3)
                date_time = re.search(r"(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})", invoice["AuthorisedHash"]).group(1)
                writer.writerow([invoice_number, cu_serial_number, str(cu_invoice_number), amount, date_time])
                print("Invoice Number:", cu_invoice_number)







        # return value_after_cu_invoice_number
        sql = "INSERT INTO invoices (invoice_number,cu_serial_number, cu_invoice_number,amount, invoice_date) VALUES (%s, %s, %s,%s,%s)"
        await cursor.execute(sql, (invoice_number, cu_serial_number,cu_invoice_number,amount, date_time))
        await connection.commit()
        print("Invoice Number:", invoice_number)
        print("CU Serial Number:", cu_serial_number)
        print("CU Invoice Number:", cu_invoice_number)
        print("Datetime:", date_time)
        print("amount:", amount)
        
@app.get("/paye")
async def calculate_paye(income: float = Query(..., description="The user's income")):
    nssf = min(200, income * 0.05)
    taxable_income = income - nssf
    paye = 0
    nhif = 0
    insurance_relief = 0
    if income <= 5999:
        nhif = 150
    elif income <= 7999:
        nhif = 300
    elif income <= 11999:
        nhif = 400
    elif income <= 14999:
        nhif = 500
    elif income <= 19999:
        nhif = 600
    elif income <= 24999:
        nhif = 750
    elif income <= 29999:
        nhif = 850
    elif income <= 34999:
        nhif = 900
    elif income <= 39000:
        nhif = 950
    elif income <= 44999:
        nhif = 1000
    elif income <= 49000:
        nhif = 1100
    elif income <= 59999:
        nhif = 1200
    else:
        nhif = 1700
    relief = 2400
    insurance_relief = nhif * 0.15
    if income > 32334:
        taxable_income = taxable_income - 32334
        paye = taxable_income * 0.30 + (8333 * 0.25) + (24000 * 0.1) - relief
    elif income > 24001:
        taxable_income = taxable_income - 24001
        paye = taxable_income * 0.25 + (24000 * 0.1) - relief
    else:
        paye = taxable_income * 0.1 - relief
        
    paye = paye - insurance_relief
    return {"income": income, "nssf": nssf, "nhif": nhif,"NHIF relief": insurance_relief, "tax charged": taxable_income,"relief": relief, "PAYE": paye}
    