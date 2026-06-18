import requests
import json

VITE = "http://localhost:5174/api"

def login(u, p):
    r = requests.post(VITE + "/auth/login", data={"username": u, "password": p})
    assert r.status_code == 200, f"login {u} failed: {r.status_code}"
    return r.json()["access_token"]

print("[1] admin login via vite proxy")
at = login("admin", "admin123")
print("   OK token_len", len(at))

print("[2] user1 login via vite proxy")
ut = login("user1", "user123")
print("   OK")

print("[3] lawyer1 login via vite proxy")
lt = login("lawyer1", "lawyer123")
print("   OK")

print("[4] GET /users/me (user1)")
r = requests.get(VITE + "/users/me", headers={"Authorization": "Bearer " + ut})
assert r.status_code == 200
d = r.json()
print(f"   OK id={d['id']} username={d['username']} role={d['role']}")

print("[5] GET /lawyers?page=1&page_size=8")
r = requests.get(VITE + "/lawyers/", params={"page": 1, "page_size": 8})
assert r.status_code == 200
d = r.json()
print(f"   OK total={d['total']} items={len(d['items'])}")
assert d["total"] >= 3
assert len(d["items"]) >= 1

print("[6] GET /lawyers/1")
r = requests.get(VITE + "/lawyers/1")
assert r.status_code == 200
d = r.json()
print(f"   OK firm_name={d.get('firm_name')} rating={d.get('rating')}")

print("[7] GET /admin/stats")
r = requests.get(VITE + "/admin/stats", headers={"Authorization": "Bearer " + at})
assert r.status_code == 200
d = r.json()
print(f"   OK users={d['total_users']} lawyers={d['total_lawyers']}")
print(f"      pending_lawyers={d.get('pending_lawyers')} pending_complaints={d.get('pending_complaints')}")
assert "pending_lawyers" in d
assert "pending_complaints" in d

print("[8] GET /knowledge")
r = requests.get(VITE + "/knowledge")
assert r.status_code == 200
print(f"   OK count={len(r.json())}")

print("[9] GET /documents/templates")
r = requests.get(VITE + "/documents/templates")
assert r.status_code == 200
print(f"   OK count={len(r.json())}")

print("[10] GET /lawyers/me/profile (lawyer)")
r = requests.get(VITE + "/lawyers/me/profile", headers={"Authorization": "Bearer " + lt})
assert r.status_code == 200
d = r.json()
print(f"   OK id={d['id']} license={d.get('license_number')}")

print("[11] POST /consultations (user1)")
r = requests.post(VITE + "/consultations/",
    headers={"Authorization": "Bearer " + ut},
    json={
        "lawyer_id": 1,
        "title": "测试咨询标题E2E",
        "description": "这是端到端测试咨询的详细描述",
        "category": "marriage",
        "city": "北京",
    })
assert r.status_code == 201, f"create consultation failed: {r.status_code} {r.text}"
print(f"   OK id={r.json()['id']}")

print("[12] POST /consultations/1/match")
r = requests.post(VITE + "/consultations/1/match",
    headers={"Authorization": "Bearer " + ut},
    json={"category": "marriage"})
assert r.status_code == 200
print(f"   OK matched count={len(r.json())}")

print("[13] POST /appointments (user1)")
r = requests.post(VITE + "/appointments/",
    headers={"Authorization": "Bearer " + ut},
    json={
        "lawyer_id": 1,
        "title": "端到端测试预约",
        "appointment_date": "2026-06-20",
        "start_time": "14:00:00",
        "end_time": "15:00:00",
        "appointment_type": "online",
    })
assert r.status_code == 201, f"{r.status_code} {r.text}"
print(f"   OK id={r.json()['id']}")

print("[14] POST /documents/generate (lawyer)")
r = requests.post(VITE + "/documents/generate/",
    headers={"Authorization": "Bearer " + lt},
    json={"template_id": 1, "variables": {"name": "E2E测试用户", "date": "2026-06-18"}})
assert r.status_code == 201, f"{r.status_code} {r.text}"
print(f"   OK id={r.json()['id']} title={r.json()['title']}")

print("[15] GET /admin/complaints")
r = requests.get(VITE + "/admin/complaints", headers={"Authorization": "Bearer " + at})
assert r.status_code == 200
print(f"   OK count={len(r.json())}")

print("[16] GET /admin/lawyers")
r = requests.get(VITE + "/admin/lawyers", headers={"Authorization": "Bearer " + at})
assert r.status_code == 200
print(f"   OK count={len(r.json())}")

print("\n========= ALL 16 E2E API TESTS PASSED via Vite Proxy =========")
