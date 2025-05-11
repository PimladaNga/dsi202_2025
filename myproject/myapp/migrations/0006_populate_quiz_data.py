# myapp/migrations/000X_populate_quiz_data.py
# (แทน 000X ด้วยเลข migration ที่ถูกสร้างขึ้นจริง)

from django.db import migrations
from django.utils.text import slugify

# --- ข้อมูลประเภทผีเสื้อ ---
BUTTERFLY_TYPES_DATA = [
    {
        "name": "ผีเสื้อนักเดินทาง",
        "name_en": "The Wanderer Butterfly",
        "description": "คุณคือผีเสื้อนักเดินทางผู้รักอิสระและการผจญภัย พร้อมโบยบินไปค้นพบประสบการณ์ใหม่ๆ อยู่เสมอ",
        "long_description": "รักอิสระ, ไม่ชอบหยุดนิ่ง สนใจกิจกรรมกลางแจ้ง, ท่องเที่ยว, เดินป่า, ตั้งแคมป์, กีฬาผาดโผน เปิดรับประสบการณ์และวัฒนธรรมใหม่ๆ",
        "strengths": "กล้าหาญ, ปรับตัวเก่ง, มีพลังงาน, ชอบสำรวจ",
        "theme_colors_description": "สีส้ม, เหลือง, เอิร์ธโทน, ท้องฟ้า",
        # "theme_color_start": "orange-400", # ตัวอย่าง (ถ้าจะใช้)
        # "theme_color_end": "yellow-300",   # ตัวอย่าง (ถ้าจะใช้)
        # "text_color": "orange-800",      # ตัวอย่าง (ถ้าจะใช้)
    },
    {
        "name": "ผีเสื้อสีสันสังคม",
        "name_en": "The Vibrant Socialite Butterfly",
        "description": "คุณคือผีเสื้อสีสันสังคมผู้เจิดจรัสและรักการพบปะ เฉิดฉายในทุกวงสังคมและนำความสนุกสนานมาสู่ทุกคน",
        "long_description": "ชอบเข้าสังคม, พบปะผู้คนใหม่ๆ, สร้างเครือข่าย มีพลังงานสูง, ชอบกิจกรรมสนุกสนาน, มีชีวิตชีวา สนใจงานปาร์ตี้, อีเวนต์, คอนเสิร์ต กล้าแสดงออก, เป็นจุดสนใจ",
        "strengths": "มีพลังงาน, เข้ากับคนง่าย, กล้าแสดงออก, สร้างสรรค์บรรยากาศ",
        "theme_colors_description": "สีสดใสหลากหลาย (แดง, ชมพู, ฟ้า), ลวดลายกราฟิก",
    },
    {
        "name": "ผีเสื้อศิลปินนุ่มนวล",
        "name_en": "The Gentle Artist Butterfly",
        "description": "คุณคือผีเสื้อศิลปินผู้นุ่มนวลและช่างฝัน มองโลกผ่านเลนส์แห่งความงามและสร้างสรรค์สิ่งดีๆ ด้วยหัวใจ",
        "long_description": "รักศิลปะ, ความสวยงาม, ความละเอียดอ่อน, มีสุนทรียภาพ ชอบกิจกรรมที่ใช้ความคิดสร้างสรรค์ อ่อนโยน, ช่างสังเกต, ใส่ใจในรายละเอียด ชอบสภาพแวดล้อมที่สงบ",
        "strengths": "สร้างสรรค์, มีจินตนาการ, อ่อนโยน, ใส่ใจรายละเอียด",
        "theme_colors_description": "สีพาสเทล, ขาว, ฟ้าอ่อน, ลายดอกไม้",
    },
    {
        "name": "ผีเสื้อนักปราชญ์รอบรู้",
        "name_en": "The Wise Scholar Butterfly",
        "description": "คุณคือผีเสื้อนักปราชญ์ผู้รอบรู้และเฉลียวฉลาด ชอบการเรียนรู้และค้นหาความหมายในทุกสิ่ง",
        "long_description": "ใฝ่รู้, ชอบเรียนรู้สิ่งใหม่ๆ, ค้นคว้าหาข้อมูล, ชอบตั้งคำถาม ชอบวิเคราะห์, คิดเชิงตรรกะ, แก้ปัญหา สนใจกิจกรรมที่ได้ใช้สมอง สุขุม, รอบคอบ",
        "strengths": "มีเหตุผล, วิเคราะห์เก่ง, ใฝ่รู้, รอบคอบ",
        "theme_colors_description": "สีน้ำตาล, เทา, เขียวเข้ม, กรมท่า, ลายหนังสือ",
    },
    {
        "name": "ผีเสื้อผู้พิทักษ์ชุมชน",
        "name_en": "The Guardian Butterfly",
        "description": "คุณคือผีเสื้อผู้พิทักษ์ชุมชนผู้เปี่ยมด้วยความอบอุ่นและห่วงใย พร้อมสร้างสรรค์สิ่งดีๆ เพื่อส่วนรวม",
        "long_description": "ใส่ใจผู้อื่น, ชอบช่วยเหลือ, มีความเป็นผู้นำหรือผู้สนับสนุนที่ดี รักชุมชน, ให้ความสำคัญกับความสัมพันธ์และความสามัคคี สนใจกิจกรรมอาสาสมัคร มีความรับผิดชอบ, น่าเชื่อถือ",
        "strengths": "เห็นอกเห็นใจ, มีความรับผิดชอบ, ชอบช่วยเหลือ, สร้างความสามัคคี",
        "theme_colors_description": "สีเขียว, ฟ้า, เหลืองอบอุ่น, สัญลักษณ์รูปหัวใจ",
    },
]

# --- ข้อมูลคำถามและตัวเลือก ---
# Key ของ dictionary นี้คือ 'order' ของคำถาม
# Value คือ dictionary ที่มี 'text' ของคำถาม และ 'choices' (list of dictionaries)
# ในแต่ละ choice, 'points_to_type_name_en' คือ name_en ของ ButterflyType ที่ choice นี้จะให้คะแนน
QUESTIONS_DATA = {
    1: {
        "text": "วันหยุดสุดสัปดาห์ที่สมบูรณ์แบบของคุณคือ...",
        "choices": [
            {"text": "ออกไปสำรวจเส้นทางเดินป่าใหม่ๆ หรือขับรถเที่ยวต่างจังหวัด", "points_to_type_name_en": "The Wanderer Butterfly"},
            {"text": "ไปงานเทศกาลดนตรี หรืองานอีเวนต์ที่มีคนเยอะๆ และกิจกรรมสนุกๆ", "points_to_type_name_en": "The Vibrant Socialite Butterfly"},
            {"text": "ใช้เวลาเงียบๆ วาดรูป อ่านบทกวี หรือไปเดินเล่นในสวนสวยๆ", "points_to_type_name_en": "The Gentle Artist Butterfly"},
            {"text": "เข้าร่วมเวิร์คช็อปพัฒนาตนเอง หรืออ่านหนังสือแนวปรัชญา", "points_to_type_name_en": "The Wise Scholar Butterfly"},
            {"text": "รวมกลุ่มเพื่อนทำกิจกรรมอาสาสมัคร หรือจัดงานเล็กๆ ในชุมชน", "points_to_type_name_en": "The Guardian Butterfly"},
        ]
    },
    2: {
        "text": "เมื่อคุณต้องทำงานกลุ่ม คุณมักจะ...",
        "choices": [
            {"text": "เสนอไอเดียใหม่ๆ ที่ท้าทายและผลักดันให้ทีมลองทำสิ่งที่ไม่เคยทำ", "points_to_type_name_en": "The Wanderer Butterfly"},
            {"text": "เป็นคนสร้างบรรยากาศให้ทีมสนุกสนานและกระตุ้นให้ทุกคนมีส่วนร่วม", "points_to_type_name_en": "The Vibrant Socialite Butterfly"},
            {"text": "ช่วยออกแบบการนำเสนอให้สวยงาม หรือใส่ใจในรายละเอียดเล็กๆ น้อยๆ ของงาน", "points_to_type_name_en": "The Gentle Artist Butterfly"},
            {"text": "วิเคราะห์ปัญหา วางแผนการทำงานอย่างเป็นระบบ และหาข้อมูลสนับสนุน", "points_to_type_name_en": "The Wise Scholar Butterfly"},
            {"text": "คอยประสานงาน ดูแลให้ทุกคนในทีมทำงานร่วมกันได้อย่างราบรื่นและมีความสุข", "points_to_type_name_en": "The Guardian Butterfly"},
        ]
    },
    3: {
        "text": "สิ่งที่คุณให้ความสำคัญมากที่สุดในการเลือกเข้าร่วมกิจกรรมคือ...",
        "choices": [
            {"text": "โอกาสที่จะได้ผจญภัยและสัมผัสประสบการณ์ที่ไม่เหมือนใคร", "points_to_type_name_en": "The Wanderer Butterfly"},
            {"text": "การได้พบปะผู้คนใหม่ๆ และขยายวงสังคม", "points_to_type_name_en": "The Vibrant Socialite Butterfly"},
            {"text": "การได้แสดงออกถึงความคิดสร้างสรรค์หรือชื่นชมความงาม", "points_to_type_name_en": "The Gentle Artist Butterfly"},
            {"text": "การได้เรียนรู้สิ่งใหม่ๆ หรือท้าทายความคิดของตัวเอง", "points_to_type_name_en": "The Wise Scholar Butterfly"},
            {"text": "การได้เป็นส่วนหนึ่งในการสร้างสิ่งดีๆ ให้กับส่วนรวมหรือช่วยเหลือผู้อื่น", "points_to_type_name_en": "The Guardian Butterfly"},
        ]
    },
    4: {
        "text": "ถ้าให้เลือกของขวัญให้ตัวเองหนึ่งชิ้น คุณจะเลือก...",
        "choices": [
            {"text": "ตั๋วเครื่องบินไปในที่ที่ไม่เคยไป หรืออุปกรณ์เดินป่าชิ้นใหม่", "points_to_type_name_en": "The Wanderer Butterfly"},
            {"text": "บัตรคอนเสิร์ตศิลปินคนโปรด หรือชุดสวยๆ สำหรับไปงานปาร์ตี้", "points_to_type_name_en": "The Vibrant Socialite Butterfly"},
            {"text": "สมุดสเก็ตช์ภาพอย่างดีพร้อมสีชุดใหม่ หรือเครื่องดนตรีชิ้นเล็กๆ", "points_to_type_name_en": "The Gentle Artist Butterfly"},
            {"text": "หนังสือแนววิทยาศาสตร์ ปรัชญา หรือคอร์สเรียนออนไลน์ที่น่าสนใจ", "points_to_type_name_en": "The Wise Scholar Butterfly"},
            {"text": "ของขวัญที่สามารถแบ่งปันกับคนในครอบครัวหรือเพื่อนๆ ได้ หรือบริจาคให้องค์กรการกุศล", "points_to_type_name_en": "The Guardian Butterfly"},
        ]
    },
    5: {
        "text": "เวลาว่างส่วนใหญ่คุณมักจะใช้ไปกับ...",
        "choices": [
            {"text": "การวางแผนทริปต่อไป หรือดูสารคดีท่องเที่ยว", "points_to_type_name_en": "The Wanderer Butterfly"},
            {"text": "การพูดคุยกับเพื่อนๆ ผ่านโซเชียลมีเดีย หรือนัดเจอสังสรรค์", "points_to_type_name_en": "The Vibrant Socialite Butterfly"},
            {"text": "การทำงานอดิเรกที่ต้องใช้ความประณีต เช่น จัดดอกไม้ เขียน Calligraphy", "points_to_type_name_en": "The Gentle Artist Butterfly"},
            {"text": "การอ่านบทความวิชาการ หรือเล่นเกมที่ต้องใช้การวางแผน", "points_to_type_name_en": "The Wise Scholar Butterfly"},
            {"text": "การติดตามข่าวสารในชุมชน หรือให้คำปรึกษาเพื่อนที่มีปัญหา", "points_to_type_name_en": "The Guardian Butterfly"},
        ]
    },
    6: {
        "text": "สไตล์การแต่งตัวที่บ่งบอกความเป็นคุณคือ...",
        "choices": [
            {"text": "เน้นความคล่องตัว สบายๆ พร้อมลุยทุกสถานการณ์", "points_to_type_name_en": "The Wanderer Butterfly"},
            {"text": "สีสันสดใส โดดเด่น และตามเทรนด์แฟชั่น", "points_to_type_name_en": "The Vibrant Socialite Butterfly"},
            {"text": "เรียบง่ายแต่มีรายละเอียดที่สวยงาม เน้นความนุ่มนวล", "points_to_type_name_en": "The Gentle Artist Butterfly"},
            {"text": "เน้นประโยชน์ใช้สอย ดูดีแบบคลาสสิก ไม่ฉูดฉาด", "points_to_type_name_en": "The Wise Scholar Butterfly"},
            {"text": "สบายๆ เป็นกันเอง และดูอบอุ่นน่าเข้าหา", "points_to_type_name_en": "The Guardian Butterfly"},
        ]
    },
    7: {
        "text": "เมื่อคุณเห็นความไม่ถูกต้องหรือไม่เป็นธรรมเกิดขึ้น คุณมักจะ...",
        "choices": [
            {"text": "กล้าที่จะท้าทายและมองหาวิธีการใหม่ๆ เพื่อเปลี่ยนแปลง", "points_to_type_name_en": "The Wanderer Butterfly"}, # อาจจะเหมาะกับ Wanderer หรือ Socialite ที่กล้าแสดงออก
            {"text": "ใช้ทักษะการสื่อสารของตัวเองเพื่อสร้างความเข้าใจและหาแนวร่วม", "points_to_type_name_en": "The Vibrant Socialite Butterfly"},
            {"text": "สะท้อนความคิดผ่านงานศิลปะหรือการเขียนเพื่อสร้างความตระหนักรู้", "points_to_type_name_en": "The Gentle Artist Butterfly"},
            {"text": "ศึกษาข้อมูลและกฎระเบียบเพื่อหาทางแก้ไขอย่างเป็นระบบและมีหลักการ", "points_to_type_name_en": "The Wise Scholar Butterfly"},
            {"text": "พยายามปกป้องผู้ที่อ่อนแอกว่า และร่วมกันหาทางออกที่เป็นธรรมกับทุกฝ่าย", "points_to_type_name_en": "The Guardian Butterfly"},
        ]
    },
    8: {
        "text": "เป้าหมายหลักในชีวิตของคุณคืออะไร?",
        "choices": [
            {"text": "การได้ใช้ชีวิตอย่างอิสระและเต็มไปด้วยประสบการณ์ที่น่าตื่นเต้น", "points_to_type_name_en": "The Wanderer Butterfly"},
            {"text": "การเป็นที่รักและเป็นที่รู้จักในวงกว้าง มีเพื่อนมากมาย", "points_to_type_name_en": "The Vibrant Socialite Butterfly"},
            {"text": "การได้สร้างสรรค์ผลงานที่สวยงามและทิ้งร่องรอยที่ดีไว้บนโลก", "points_to_type_name_en": "The Gentle Artist Butterfly"},
            {"text": "การได้เข้าใจโลกและจักรวาลอย่างลึกซึ้ง และแบ่งปันความรู้นั้น", "points_to_type_name_en": "The Wise Scholar Butterfly"},
            {"text": "การได้ทำให้โลกนี้น่าอยู่ขึ้นสำหรับทุกคนและสร้างชุมชนที่เข้มแข็ง", "points_to_type_name_en": "The Guardian Butterfly"},
        ]
    },
}

def populate_data(apps, schema_editor):
    ButterflyType = apps.get_model('myapp', 'ButterflyType')
    Question = apps.get_model('myapp', 'Question')
    Choice = apps.get_model('myapp', 'Choice')

    # --- สร้าง Butterfly Types ---
    # เก็บ ButterflyType objects ที่สร้างขึ้นเพื่อใช้อ้างอิงใน Choice
    butterfly_type_objects = {}
    for bt_data in BUTTERFLY_TYPES_DATA:
        slug_source = bt_data.get("name_en", bt_data["name"])
        # สร้าง slug: ถ้ามี name_en ใช้ name_en (ASCII), ถ้าไม่มีใช้ name (ไทย, allow_unicode=True)
        slug = slugify(slug_source, allow_unicode=True if not bt_data.get("name_en") else False)

        butterfly_type, created = ButterflyType.objects.update_or_create(
            name_en=bt_data.get("name_en"), # ใช้ name_en เป็น unique identifier ถ้ามี
            defaults={
                'name': bt_data["name"],
                'slug': slug,
                'description': bt_data["description"],
                'long_description': bt_data.get("long_description", ""),
                'strengths': bt_data.get("strengths", ""),
                'theme_colors_description': bt_data.get("theme_colors_description", ""),
                # เพิ่ม field อื่นๆ ของ ButterflyType ที่นี่ถ้ามี เช่น theme_color_start, icon_image path (ถ้าจะ hardcode path)
                # 'theme_color_start': bt_data.get("theme_color_start"),
                # 'theme_color_end': bt_data.get("theme_color_end"),
                # 'text_color': bt_data.get("text_color"),
            }
        )
        # เก็บ object โดยใช้ name_en เป็น key เพื่อให้ง่ายต่อการ map ใน Choice
        # ถ้าไม่มี name_en ให้ใช้ name (ไทย) แต่ควรระวังถ้าชื่อไทยซ้ำกัน (ซึ่งไม่ควรเกิดขึ้นถ้า name เป็น unique)
        key_name = bt_data.get("name_en", bt_data["name"])
        butterfly_type_objects[key_name] = butterfly_type
        if created:
            print(f"Created ButterflyType: {butterfly_type.name}")
        else:
            print(f"Updated ButterflyType: {butterfly_type.name}")


    # --- สร้าง Questions และ Choices ---
    for order, q_data in QUESTIONS_DATA.items():
        question, q_created = Question.objects.update_or_create(
            order=order,
            defaults={'text': q_data["text"]}
        )
        if q_created:
            print(f"Created Question (Order {order}): {question.text[:30]}...")
        else:
            print(f"Updated Question (Order {order}): {question.text[:30]}...")

        # ลบ Choices เก่าของคำถามนี้ (ถ้ามี) เพื่อป้องกันการสร้างซ้ำซ้อนถ้า migration รันหลายครั้ง
        Choice.objects.filter(question=question).delete()

        for choice_data in q_data["choices"]:
            # ดึง ButterflyType object จาก name_en ที่เก็บไว้
            points_to_type_obj = butterfly_type_objects.get(choice_data["points_to_type_name_en"])
            if points_to_type_obj:
                Choice.objects.create(
                    question=question,
                    text=choice_data["text"],
                    points_to_type=points_to_type_obj
                )
            else:
                print(f"Warning: Could not find ButterflyType for choice '{choice_data['text']}' "
                      f"with type name_en '{choice_data['points_to_type_name_en']}'")

def clear_data(apps, schema_editor):
    # (Optional) ฟังก์ชันสำหรับลบข้อมูลถ้าต้องการ rollback migration นี้
    # แต่โดยทั่วไปสำหรับ data migration อาจจะไม่จำเป็นต้อง clear แบบสมบูรณ์
    # หรือถ้าจะ clear ควรระมัดระวัง
    ButterflyType = apps.get_model('myapp', 'ButterflyType')
    Question = apps.get_model('myapp', 'Question')
    Choice = apps.get_model('myapp', 'Choice')

    # ลบเฉพาะข้อมูลที่ migration นี้สร้างขึ้น (อาจจะยากถ้าไม่มี identifier เฉพาะ)
    # หรือลบทั้งหมด (ระวัง!)
    print("Clearing quiz data (ButterflyTypes, Questions, Choices)...")
    # Choice.objects.all().delete() # ลบ choices ก่อนเพราะมี foreign key
    # Question.objects.all().delete()
    # ButterflyType.objects.filter(name_en__in=[bt['name_en'] for bt in BUTTERFLY_TYPES_DATA if 'name_en' in bt]).delete()
    # ButterflyType.objects.filter(name__in=[bt['name'] for bt in BUTTERFLY_TYPES_DATA]).delete()
    # การลบแบบนี้อาจจะไม่ปลอดภัยถ้ามีข้อมูลอื่นอยู่แล้ว การใช้ identifier เฉพาะจะดีกว่า
    # ในที่นี้ จะปล่อยให้ comment ไว้ก่อน หรือถ้าต้องการลบจริงๆ ควรทำอย่างระมัดระวัง
    pass


class Migration(migrations.Migration):

    # ระบุ migration ก่อนหน้านี้ (ถ้ามี) ที่ migration นี้ต้องทำงานหลังจากนั้น
    # ปกติ Django จะใส่ให้ แต่อาจจะต้องปรับถ้า migration นี้ต้องขึ้นกับ model ที่เพิ่งสร้าง
    dependencies = [
        ('myapp', '0005_butterflytype_text_color_and_more'), # <--- !!! แก้ไข 000Y_previous_migration เป็นชื่อไฟล์ migration ก่อนหน้าไฟล์นี้ !!!
                                            # หรือถ้าเป็น migration แรกๆ ของ app อาจจะไม่ต้องมี dependencies ที่ซับซ้อน
    ]

    operations = [
        migrations.RunPython(populate_data, reverse_code=clear_data),
    ]