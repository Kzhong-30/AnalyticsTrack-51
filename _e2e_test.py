import os
os.environ["NO_PROXY"] = "localhost,127.0.0.1"
import requests
BASE = "http://localhost:8000/api"
def login(u, p):
    r = requests.post(BASE + "/auth/login", data={"username": u, "password": p})
    assert r.status_code == 200, f"login {u} failed: {r.status_code}"
    return r.json()["access_token"]

results = []

def test(name, func):
    try:
        func()
        results.append(f"✅ {name}")
        print(f"✅ {name}")
    except Exception as e:
        results.append(f"❌ {name}: {e}")
        print(f"❌ {name}: {e}")

def t1():
    global ut
    ut = login("user1", "user123")

def t2():
    global at
    at = login("admin", "admin123")

def t3():
    global lt
    lt = login("lawyer1", "lawyer123")

def t4():
    r = requests.get(BASE + "/users/me", headers={"Authorization": "Bearer " + ut})
    assert r.status_code == 200
    d = r.json()
    assert d["full_name"] is not None

def t5():
    r = requests.get(BASE + "/lawyers/", params={"page": 1, "page_size": 8}, headers={"Authorization": "Bearer " + ut})
    assert r.status_code == 200
    d = r.json()
    assert d["total"] >= 1
    assert "full_name" in d["items"][0]
    assert "firm_name" in d["items"][0]

def t6():
    r = requests.get(BASE + "/lawyers/1", headers={"Authorization": "Bearer " + ut})
    assert r.status_code == 200
    d = r.json()
    assert d["full_name"] is not None
    assert d["firm_name"] is not None

def t7():
    r = requests.get(BASE + "/admin/stats", headers={"Authorization": "Bearer " + at})
    assert r.status_code == 200
    d = r.json()
    assert "pending_lawyers" in d
    assert "pending_complaints" in d

def t8():
    r = requests.get(BASE + "/knowledge/", headers={"Authorization": "Bearer " + ut})
    assert r.status_code == 200
    assert len(r.json()) > 0

def t9():
    r = requests.get(BASE + "/documents/templates", headers={"Authorization": "Bearer " + lt})
    assert r.status_code == 200
    assert len(r.json()) > 0

def t10():
    r = requests.get(BASE + "/lawyers/me/profile", headers={"Authorization": "Bearer " + lt})
    assert r.status_code == 200
    d = r.json()
    assert d["full_name"] is not None

def t11():
    r = requests.post(BASE + "/consultations/", headers={"Authorization": "Bearer " + ut}, json={"title": "test", "description": "test", "category": "labor"})
    assert r.status_code == 201
    d = r.json()
    assert d["lawyer_id"] is not None

def t12():
    r = requests.post(BASE + "/appointments/", headers={"Authorization": "Bearer " + ut}, json={"lawyer_id": 1, "appointment_type": "online", "appointment_time": "2026-06-20 10:00"})
    assert r.status_code == 201

def t13():
    r = requests.get(BASE + "/appointments/", headers={"Authorization": "Bearer " + ut})
    assert r.status_code == 200
    assert isinstance(r.json(), list)

def t14():
    r = requests.post(BASE + "/documents/generate", headers={"Authorization": "Bearer " + lt}, json={"template_id": 1, "variables": {"plaintiff": "张三", "defendant": "李四", "claim": "赔偿", "facts": "欠钱", "court": "北京法院", "date": "2026-06-18"}})
    assert r.status_code == 201

def t15():
    r = requests.get(BASE + "/admin/lawyers", headers={"Authorization": "Bearer " + at})
    assert r.status_code == 200
    d = r.json()
    if d:
        assert "full_name" in d[0]

test("用户登录", t1)
test("管理员登录", t2)
test("律师登录", t3)
test("获取用户信息", t4)
test("律师列表(分页+用户字段)", t5)
test("律师详情(用户字段)", t6)
test("管理端统计(含pending字段)", t7)
test("知识库列表", t8)
test("文书模板列表", t9)
test("律师个人资料", t10)
test("发布咨询(自动匹配律师)", t11)
test("创建预约(appointment_time解析)", t12)
test("预约列表(数组格式)", t13)
test("生成文书", t14)
test("管理端律师列表(含用户信息)", t15)

print()
passed = sum(1 for r in results if r.startswith("✅"))
failed = sum(1 for r in results if r.startswith("❌"))
print(f"结果: {passed} 通过, {failed} 失败, 共 {len(results)} 项")
for r in results:
    print(r)
