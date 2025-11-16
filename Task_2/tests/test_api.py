import requests
import uuid

BASE_URL = "https://qa-internship.avito.com"
SELLER_ID = 784512

def create_payload(
        seller_id=SELLER_ID,
        name="Test Item",
        price=100,
        likes=1,
        viewCount=1,
        contacts=1
):
    return {
        "sellerID": seller_id,
        "name": name,
        "price": price,
        "statistics": {
            "likes": likes,
            "viewCount": viewCount,
            "contacts": contacts
        }
    }

def create_item():
    payload = create_payload()
    resp = requests.post(f"{BASE_URL}/api/1/item", json=payload)
    assert resp.status_code == 200
    status_text = resp.json().get("status", "")
    assert "Сохранили объявление - " in status_text
    item_id = status_text.split(" - ")[1]
    return item_id

# TC-01
def test_TC01_create_item_valid():
    payload = create_payload()
    r = requests.post(f"{BASE_URL}/api/1/item", json=payload)
    assert r.status_code == 200
    assert "Сохранили объявление - " in r.json()["status"]

# TC-02
def test_TC02_create_item_price_zero():
    payload = create_payload(price=0)
    r = requests.post(f"{BASE_URL}/api/1/item", json=payload)
    assert r.status_code == 400

# TC-03
def test_TC03_create_item_zero_statistics():
    payload = create_payload(likes=0, viewCount=0, contacts=0)
    r = requests.post(f"{BASE_URL}/api/1/item", json=payload)
    assert r.status_code == 400

# TC-04
def test_TC04_create_two_items():
    id1 = create_item()
    id2 = create_item()
    assert id1 != id2

# TC-05
def test_TC05_create_item_no_seller_id():
    payload = create_payload()
    del payload["sellerID"]
    r = requests.post(f"{BASE_URL}/api/1/item", json=payload)
    assert r.status_code == 400

# TC-06
def test_TC06_create_item_invalid_seller_id_string():
    payload = create_payload(seller_id="abc")
    r = requests.post(f"{BASE_URL}/api/1/item", json=payload)
    assert r.status_code == 400

# TC-07
def test_TC07_create_item_no_name():
    payload = create_payload()
    del payload["name"]
    r = requests.post(f"{BASE_URL}/api/1/item", json=payload)
    assert r.status_code == 400

# TC-08
def test_TC08_create_item_negative_price():
    payload = create_payload(price=-5)
    r = requests.post(f"{BASE_URL}/api/1/item", json=payload)
    assert r.status_code == 200

# TC-09
def test_TC09_create_item_invalid_statistics_type():
    payload = create_payload()
    payload["statistics"]["likes"] = "string"
    r = requests.post(f"{BASE_URL}/api/1/item", json=payload)
    assert r.status_code == 400

# TC-10
def test_TC10_create_item_long_name():
    payload = create_payload(name="A" * 256)
    r = requests.post(f"{BASE_URL}/api/1/item", json=payload)
    assert r.status_code == 200

# TC-11
def test_TC11_get_existing_item():
    item_id = create_item()
    r = requests.get(f"{BASE_URL}/api/1/item/{item_id}")
    assert r.status_code == 200
    assert r.json()[0]["id"] == item_id

# TC-12
def test_TC12_get_item_createdAt_format():
    item_id = create_item()
    r = requests.get(f"{BASE_URL}/api/1/item/{item_id}")
    assert "createdAt" in r.json()[0]

# TC-13
def test_TC13_get_item_not_found():
    random_id = str(uuid.uuid4())
    r = requests.get(f"{BASE_URL}/api/1/item/{random_id}")
    assert r.status_code == 404

# TC-14
def test_TC14_get_item_invalid_id_format():
    r = requests.get(f"{BASE_URL}/api/1/item/123")
    assert r.status_code == 400

# TC-15
def test_TC15_get_item_no_id_in_url():
    r = requests.get(f"{BASE_URL}/api/1/item/")
    assert r.status_code in (400, 404)

# TC-16
def test_TC16_get_items_by_seller_positive():
    create_item()
    create_item()
    r = requests.get(f"{BASE_URL}/api/1/{SELLER_ID}/item")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

# TC-17
def test_TC17_get_items_by_seller_empty():
    r = requests.get(f"{BASE_URL}/api/1/999999/item")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

# TC-18
def test_TC18_get_items_invalid_seller_string():
    r = requests.get(f"{BASE_URL}/api/1/abc/item")
    assert r.status_code == 400

# TC-19
def test_TC19_get_items_negative_seller():
    r = requests.get(f"{BASE_URL}/api/1/-1/item")
    assert r.status_code == 200

# TC-20
def test_TC20_get_statistics_positive():
    item_id = create_item()
    r = requests.get(f"{BASE_URL}/api/1/statistic/{item_id}")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

# TC-21
def test_TC21_statistics_values_correct():
    item_id = create_item()
    r = requests.get(f"{BASE_URL}/api/1/statistic/{item_id}")
    assert "likes" in r.json()[0]

# TC-22
def test_TC22_get_statistics_not_found():
    random_id = str(uuid.uuid4())
    r = requests.get(f"{BASE_URL}/api/1/statistic/{random_id}")
    assert r.status_code == 404

# TC-23
def test_TC23_get_statistics_invalid_format():
    r = requests.get(f"{BASE_URL}/api/1/statistic/123")
    assert r.status_code == 400

# TC-24
def test_TC24_delete_existing_item():
    item_id = create_item()
    r = requests.delete(f"{BASE_URL}/api/2/item/{item_id}")
    assert r.status_code == 200
    check = requests.get(f"{BASE_URL}/api/1/item/{item_id}")
    assert check.status_code in (400, 404)

# TC-25
def test_TC25_delete_not_found():
    random_id = str(uuid.uuid4())
    r = requests.delete(f"{BASE_URL}/api/2/item/{random_id}")
    assert r.status_code == 404

# TC-26
def test_TC26_delete_invalid_format():
    r = requests.delete(f"{BASE_URL}/api/2/item/123")
    assert r.status_code == 400

# TC-27
def test_TC27_delete_no_id_in_url():
    r = requests.delete(f"{BASE_URL}/api/2/item/")
    assert r.status_code in (400, 404)
