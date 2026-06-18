from datetime import datetime
from .database import SessionLocal, engine, Base
from . import models
from .security import hash_password
from .models import UserRole, LawyerStatus, LegalCategory, DocumentType


def run_seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        _create_admin(db)
        _create_lawyers(db)
        _create_clients(db)
        _create_knowledge_entries(db)
        _create_document_templates(db)
        _print_summary()
    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {e}")
        raise
    finally:
        db.close()


def _create_admin(db):
    admin = db.query(models.User).filter(models.User.username == "admin").first()
    if not admin:
        admin = models.User(
            username="admin",
            email="admin@example.com",
            hashed_password=hash_password("admin123"),
            full_name="系统管理员",
            role=UserRole.ADMIN,
            is_active=True,
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
        print("Created admin user: admin/admin123")
    return admin


def _create_lawyers(db):
    lawyer_list = [
        {
            "username": "lawyer1",
            "email": "lawyer1@example.com",
            "password": "lawyer123",
            "full_name": "张明律师",
            "phone": "13800138001",
            "license_number": "1101012015001",
            "firm_name": "正义律师事务所",
            "years_of_experience": 8,
            "bio": "资深民商事律师，执业8年，处理各类合同纠纷、房产纠纷案件超过500起。",
            "specialties": "合同纠纷,房产纠纷,公司法务",
            "category": LegalCategory.CIVIL,
            "consultation_fee": 200.0,
            "appointment_fee": 500.0,
            "rating": 4.8,
            "review_count": 128,
        },
        {
            "username": "lawyer2",
            "email": "lawyer2@example.com",
            "password": "lawyer123",
            "full_name": "李婷律师",
            "phone": "13800138002",
            "license_number": "1101012017002",
            "firm_name": "明德律师事务所",
            "years_of_experience": 6,
            "bio": "专注婚姻家庭法律事务，擅长离婚诉讼、财产分割、子女抚养权争取。",
            "specialties": "婚姻家庭,财产分割,遗产继承",
            "category": LegalCategory.FAMILY,
            "consultation_fee": 150.0,
            "appointment_fee": 400.0,
            "rating": 4.9,
            "review_count": 95,
        },
        {
            "username": "lawyer3",
            "email": "lawyer3@example.com",
            "password": "lawyer123",
            "full_name": "王浩律师",
            "phone": "13800138003",
            "license_number": "1101012012003",
            "firm_name": "恒信律师事务所",
            "years_of_experience": 11,
            "bio": "刑事辩护专家，曾办理多起有重大社会影响的刑事案件。",
            "specialties": "刑事辩护,取保候审,刑事自诉",
            "category": LegalCategory.CRIMINAL,
            "consultation_fee": 300.0,
            "appointment_fee": 800.0,
            "rating": 4.7,
            "review_count": 156,
        },
    ]

    for data in lawyer_list:
        user = db.query(models.User).filter(models.User.username == data["username"]).first()
        if not user:
            user = models.User(
                username=data["username"],
                email=data["email"],
                hashed_password=hash_password(data["password"]),
                full_name=data["full_name"],
                phone=data["phone"],
                role=UserRole.LAWYER,
                is_active=True,
            )
            db.add(user)
            db.commit()
            db.refresh(user)

            profile = models.LawyerProfile(
                user_id=user.id,
                license_number=data["license_number"],
                firm_name=data["firm_name"],
                years_of_experience=data["years_of_experience"],
                bio=data["bio"],
                specialties=data["specialties"],
                category=data["category"],
                consultation_fee=data["consultation_fee"],
                appointment_fee=data["appointment_fee"],
                rating=data["rating"],
                review_count=data["review_count"],
                status=LawyerStatus.APPROVED,
                verified_at=datetime.utcnow(),
            )
            db.add(profile)
            db.commit()
            print(f"Created lawyer: {data['username']}/lawyer123")


def _create_clients(db):
    client_list = [
        {"username": "user1", "email": "user1@example.com", "password": "user123", "full_name": "陈小明", "phone": "13900139001"},
        {"username": "user2", "email": "user2@example.com", "password": "user123", "full_name": "刘小华", "phone": "13900139002"},
        {"username": "user3", "email": "user3@example.com", "password": "user123", "full_name": "赵小红", "phone": "13900139003"},
    ]

    for data in client_list:
        user = db.query(models.User).filter(models.User.username == data["username"]).first()
        if not user:
            user = models.User(
                username=data["username"],
                email=data["email"],
                hashed_password=hash_password(data["password"]),
                full_name=data["full_name"],
                phone=data["phone"],
                role=UserRole.CLIENT,
                is_active=True,
            )
            db.add(user)
            db.commit()
            print(f"Created user: {data['username']}/user123")


def _get_admin(db):
    return db.query(models.User).filter(models.User.username == "admin").first()


def _create_knowledge_entries(db):
    admin = _get_admin(db)
    entries = [
        {
            "title": "中华人民共和国民法典（合同编）",
            "content": "第三编 合同\n\n第一分编 通则\n\n第一章 一般规定\n\n第四百六十三条 本编调整因合同产生的民事关系。\n\n第四百六十四条 合同是民事主体之间设立、变更、终止民事法律关系的协议。",
            "category": LegalCategory.CIVIL,
            "tags": "民法典,合同法",
        },
        {
            "title": "劳动合同法常见问题解答",
            "content": "1. 用人单位不与劳动者签订书面劳动合同怎么办？\n\n根据《劳动合同法》第八十二条规定，用人单位自用工之日起超过一个月不满一年未与劳动者订立书面劳动合同的，应当向劳动者每月支付二倍的工资。",
            "category": LegalCategory.LABOR,
            "tags": "劳动合同,劳动法,试用期",
        },
        {
            "title": "离婚财产分割原则",
            "content": "离婚时，夫妻的共同财产由双方协议处理；协议不成的，由人民法院根据财产的具体情况，按照照顾子女、女方和无过错方权益的原则判决。",
            "category": LegalCategory.FAMILY,
            "tags": "离婚,财产分割,婚姻法",
        },
        {
            "title": "刑法中关于盗窃罪的规定",
            "content": "第二百六十四条 盗窃公私财物，数额较大的，或者多次盗窃、入户盗窃、携带凶器盗窃、扒窃的，处三年以下有期徒刑、拘役或者管制，并处或者单处罚金。",
            "category": LegalCategory.CRIMINAL,
            "tags": "刑法,盗窃罪,量刑",
        },
        {
            "title": "房屋买卖合同注意事项",
            "content": "签订房屋买卖合同时需要注意以下事项：\n\n1. 核实房主身份和房屋权属证明\n2. 明确房屋价款及支付方式\n3. 约定交房时间和条件\n4. 明确违约责任",
            "category": LegalCategory.REAL_ESTATE,
            "tags": "房屋买卖,合同,房产",
        },
        {
            "title": "公司设立流程及法律要求",
            "content": "设立有限责任公司的流程：\n\n1. 公司名称预先核准\n2. 制定公司章程\n3. 股东认缴出资\n4. 申请设立登记\n5. 领取营业执照",
            "category": LegalCategory.COMMERCIAL,
            "tags": "公司法,公司设立,工商登记",
        },
    ]

    for data in entries:
        entry = db.query(models.KnowledgeEntry).filter(models.KnowledgeEntry.title == data["title"]).first()
        if not entry:
            entry = models.KnowledgeEntry(
                title=data["title"],
                content=data["content"],
                category=data["category"],
                tags=data["tags"],
                author_id=admin.id if admin else None,
                is_published=True,
                view_count=0,
            )
            db.add(entry)
            db.commit()
            print(f"Created knowledge entry: {data['title']}")


def _create_document_templates(db):
    admin = _get_admin(db)
    templates = [
        {
            "name": "民事起诉状模板",
            "description": "适用于一般民事纠纷的起诉状模板",
            "document_type": DocumentType.COMPLAINT,
            "category": LegalCategory.CIVIL,
            "variables": "原告姓名,性别,民族,出生日期,住址,身份证号,联系电话,被告姓名,诉讼请求,事实与理由,法院名称,起诉日期",
            "content": "民事起诉状\n\n原告：{{原告姓名}}\n\n被告：{{被告姓名}}\n\n诉讼请求：\n{{诉讼请求}}\n\n事实与理由：\n{{事实与理由}}\n\n此致\n{{法院名称}}人民法院\n\n具状人：{{原告姓名}}\n{{起诉日期}}",
        },
        {
            "name": "房屋买卖合同模板",
            "description": "二手房买卖合同标准模板",
            "document_type": DocumentType.CONTRACT,
            "category": LegalCategory.REAL_ESTATE,
            "variables": "卖方姓名,买方姓名,房屋地址,建筑面积,总价,交房日期,签订日期",
            "content": "房屋买卖合同\n\n甲方（卖方）：{{卖方姓名}}\n\n乙方（买方）：{{买方姓名}}\n\n第一条 房屋基本情况\n房屋坐落于：{{房屋地址}}，建筑面积：{{建筑面积}}平方米。\n\n第二条 房屋价款\n总价款为人民币{{总价}}元。\n\n第三条 房屋交付\n甲方应于{{交房日期}}前交付房屋。\n\n甲方（签字）：{{卖方姓名}}\n乙方（签字）：{{买方姓名}}\n签订日期：{{签订日期}}",
        },
        {
            "name": "律师函模板",
            "description": "通用律师函模板",
            "document_type": DocumentType.LEGAL_OPINION,
            "category": LegalCategory.CIVIL,
            "variables": "律所名称,收函人,委托人,事项,基本事实,法律分析,期限,要求,律师姓名,律师电话,发函日期",
            "content": "律师函\n\n致：{{收函人}}\n\n{{律所名称}}律师事务所接受{{委托人}}的委托，指派本律师就您与{{委托人}}之间的{{事项}}事宜，郑重致函如下：\n\n一、基本事实\n{{基本事实}}\n\n二、法律分析\n{{法律分析}}\n\n三、函告事项\n请您于{{期限}}日内，{{要求}}\n\n律师：{{律师姓名}}\n电话：{{律师电话}}\n{{发函日期}}",
        },
        {
            "name": "劳动合同模板",
            "description": "标准劳动合同模板",
            "document_type": DocumentType.CONTRACT,
            "category": LegalCategory.LABOR,
            "variables": "单位名称,劳动者姓名,岗位名称,工作地点,月工资,合同期限,签订日期",
            "content": "劳动合同\n\n甲方（用人单位）：{{单位名称}}\n\n乙方（劳动者）：{{劳动者姓名}}\n\n第一条 劳动合同期限\n合同期限：{{合同期限}}\n\n第二条 工作内容和工作地点\n岗位：{{岗位名称}}\n地点：{{工作地点}}\n\n第三条 劳动报酬\n月工资：{{月工资}}元\n\n甲方（盖章）：{{单位名称}}\n乙方（签字）：{{劳动者姓名}}\n签订日期：{{签订日期}}",
        },
        {
            "name": "民事答辩状模板",
            "description": "民事诉讼答辩状模板",
            "document_type": DocumentType.DEFENSE,
            "category": LegalCategory.CIVIL,
            "variables": "答辩人姓名,被答辩人姓名,纠纷类型,答辩意见,事实与理由,法院名称,答辩日期",
            "content": "民事答辩状\n\n答辩人：{{答辩人姓名}}\n\n被答辩人：{{被答辩人姓名}}\n\n因被答辩人诉答辩人{{纠纷类型}}一案，现答辩人提出答辩如下：\n\n一、答辩意见\n{{答辩意见}}\n\n二、事实与理由\n{{事实与理由}}\n\n此致\n{{法院名称}}人民法院\n\n答辩人：{{答辩人姓名}}\n{{答辩日期}}",
        },
    ]

    for data in templates:
        template = db.query(models.DocumentTemplate).filter(models.DocumentTemplate.name == data["name"]).first()
        if not template:
            template = models.DocumentTemplate(
                name=data["name"],
                description=data["description"],
                document_type=data["document_type"],
                category=data["category"],
                template_content=data["content"],
                variables=data["variables"],
                is_active=True,
                created_by=admin.id if admin else None,
            )
            db.add(template)
            db.commit()
            print(f"Created document template: {data['name']}")


def _print_summary():
    print("\n" + "=" * 50)
    print("种子数据初始化完成！")
    print("=" * 50)
    print("管理员账号: admin / admin123")
    print("律师账号:")
    print("  - lawyer1 / lawyer123 (民事律师)")
    print("  - lawyer2 / lawyer123 (婚姻家庭律师)")
    print("  - lawyer3 / lawyer123 (刑事律师)")
    print("普通用户账号:")
    print("  - user1 / user123")
    print("  - user2 / user123")
    print("  - user3 / user123")
    print("知识库条目: 6 条")
    print("文书模板: 5 个")
    print("=" * 50)


if __name__ == "__main__":
    run_seed()
