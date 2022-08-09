from django.shortcuts import render
from pymongo import MongoClient

from django.utils import timezone
from django.core.paginator import Paginator 

def connect_db():
    client = MongoClient(host='192.168.0.138', port=27017)
    db = client['restaurants']
    return db, client

def test(request):
    return render(request, "test.html")

def check_data(col):
    count = 0
    data_list = []
    for data in col.find().sort("_id"):
        name = data.get("name")
        addr = data.get("info")[2]
        count += 1  
        data_list.append([name,addr])
    
    return data_list, count
    #print(count)

def check_data1(col2):
    count2 = 0
    menu_list = []
    for data in col2.find().sort("_id"):
        name = data.get("name")
        menu = data.get("menu")
        if menu != {}:
            menu_list.append({"name":name, "menu":menu})
        else:
            menu_list.append({"name":name, "menu":"None"})
    #print(menu_list2)
    return menu_list, count2
    # print(count)


def check_data2(res_name):
    db, client = connect_db()
    col6 = db["review_info_list"]
    col7 = db["location_info"]

    data1 = col6.find_one({"name": res_name})
    name = data1["name"]
    g_1 = data1["count"][1]
    g_2 = data1["count"][2]
    g_3 = data1["count"][3]
    review_rate = {"name": name, "G": g_1, "S": g_2, "B": g_3}

    data = col7.find_one({"name": res_name})
    name = data.get("name")
    addr_x = data.get("loc")["X"]
    addr_y = data.get('loc')["Y"]
    location = {"name": name, "X": addr_x, "Y": addr_y}

    return location, review_rate



def index(request):
    db, client = connect_db()
    col = db["info_list"]
    col2 = db["menu_list"]
    data_list, count = check_data(col)
    menu_list, count2 = check_data1(col2)
    page = request.GET.get('page')  # 페이지
    paginator = Paginator(data_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {
        'data_list': data_list,
        'menu_list': menu_list,
        'count': count,
        'count2': count2,
        'data_list': page_obj,
    }
    return render(request, "index.html", context)


def detail(request):
    res_name = request.GET.get("res_name")
    request.session["res_name"] = res_name
    print(res_name)

    db, client = connect_db()
    res_name = "왕스덕"
    col1 = db["info_list"]
    col2 = db["menu_list"]
    location, review_rate = check_data2(res_name)
    target = col1.find({'name': res_name})[0]
    menu_list = col2.find_one({"name": res_name})["menu"]

    context = {
        'data_list1': location["Y"],
        'data_list2': location["X"],
        'review_rate1': review_rate["G"],
        'review_rate2': review_rate["S"],
        'review_rate3': review_rate["B"],
        'name': target['name'],
        'star': target['info'][0],
        'view': target['info'][1],
        'addr': target['info'][2],
        'tel': target['info'][3],
        'menu_list': menu_list,
    }
    return render(request, "detail.html", context)


def favors(request):
    context = {
        
    }
    return render(request, "favors.html", context)