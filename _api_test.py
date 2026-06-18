import requests
import json

BASE = "http://localhost:8000/api"

def login(username, password):
    r = requests.post(f"{BASE}/auth/login",
        data={"username": username, "password": password})
    return r.status_code, r.json()

print("=== 1. 登录 admin ===")
code, data = login("admin", "admin123")
print(f"status={code}, access_token len={len(data.get('access_token',''))}")
admin_token = data["access_token"]

print("\n=== 2. 登录 user1 ===")
code, data = login("user1", "user123")
print(f"status={code}, access_token len={len(data.get('access_token',''))}")
user_token = data["access_token"]

print("\n=== 3. 登录 lawyer1 ===")
code, data = login("lawyer1", "lawyer123")
print(f"status={code}, access_token len={len(data.get('access_token',''))}")
lawyer_token = data["access_token"]

print("\n=== 4. 律师列表分页 ===")
r = requests.get(f"{BASE}/lawyers", params={"page": 1, "page_size": 2})
print(f"status={r.status_code}")
d = r.json()
print(f"total={d.get('total')}, items count={len(d.get('items',[]))}")
print("sample item keys:", list(d["items"][0].keys()) if d.get("items") else "NO ITEMS")

print("\n=== 5. /users/me ===")
r = requests.get(f"{BASE}/users/me", headers={"Authorization": f"Bearer {user_token}"})
print(f"status={r.status_code}")
d = r.json()
print(f"user: id={d.get('id')}, username={d.get('username')}, role={d.get('role')}")

print("\n=== 6. /admin/stats ===")
r = requests.get(f"{BASE}/admin/stats", headers={"Authorization": f"Bearer {admin_token}"})
print(f"status={r.status_code}")
d = r.json()
print(json.dumps(d, indent=2, ensure_ascii=False))

print("\n=== 7. /knowledge ===")
r = requests.get(f"{BASE}/knowledge")
print(f"status={r.status_code}, count={len(r.json())}")

print("\n=== 8. /documents/templates ===")
r = requests.get(f"{BASE}/documents/templates")
print(f"status={r.status_code}, count={len(r.json())}")

print("\n=== 9. POST /consultations ===")
r = requests.post(f"{BASE}/consultations",
    headers={"Authorization": f"Bearer {user_token}"},
    json={
        "lawyer_id": 1,
        "title": "测试咨询问题",
        "description": "这是一个测试咨询的详细描述内容",
        "category": "marriage",
        "city": "北京"
    })
print(f"status={r.status_code}, data={json.dumps(r.json(), ensure_ascii=False)}")

print("\n=== 10. POST /consultations/1/match ===")
r = requests.post(f"{BASE}/consultations/1/match",
    headers={"Authorization": f"Bearer {user_token}"},
    json={"category": "marriage"})
print(f"status={r.status_code}, count={len(r.json())}")

print("\n=== 11. POST /appointments ===")
r = requests.post(f"{BASE}/appointments",
    headers={"Authorization": f"Bearer {user_token}"},
    json={
        "lawyer_id": 1,
        "title": "测试预约",
        "appointment_date": "2026-06-20",
        "start_time": "10:00:00",
        "end_time": "11:00:00",
        "appointment_type": "online"
    })
print(f"status={r.status_code}, data={json.dumps(r.json(), ensure_ascii=False)}")

print("\n=== 12. POST /documents/generate ===")
r = requests.post(f"{BASE}/documents/generate",
    headers={"Authorization": f"Bearer {lawyer_token}"},
    json={
        "template_id": 1,
        "variables": {"name": "测试", "date": "2026-06-18"}
    })
print(f"status={r.status_code}, data={json.dumps(r.json(), ensure_ascii=False)[:200]}")

print("\n=== 13. /admin/complaints ===")
r = requests.get(f"{BASE}/admin/complaints",
    headers={"Authorization": f"Bearer {admin_token}"})
print(f"status={r.status_code}, count={len(r.json())}")

print("\n=== 14. /admin/lawyers ===")
r = requests.get(f"{BASE}/admin/lawyers",
    headers={"Authorization": f"Bearer {admin_token}"})
print(f"status={r.status_code}, count={len(r.json())}")

print("\n=== 15. /lawyers/me/profile (lawyer) ===")
r = requests.get(f"{BASE}/lawyers/me/profile",
    headers={"Authorization": f"Bearer {lawyer_token}"})
print(f"status={r.status_code}")
d = r.json()
print(f"profile: id={d.get('id')}, license={d.get('license_number')}, firm={d.get('firm_name')}")

print("\n=== DONE ===")
