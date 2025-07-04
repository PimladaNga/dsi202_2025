# README: แอปพลิเคชัน ชุมชนลิงก์ (Chum-Chon Link)

## บทนำ: จุดเริ่มต้นและแรงบันดาลใจ

แอปพลิเคชัน **ชุมชนลิงก์ (Chum-Chon Link)** ถือกำเนิดขึ้นจากความต้องการสร้างพื้นที่ออนไลน์ที่ตอบโจทย์การเชื่อมโยงผู้คนเข้าด้วยกันผ่านกิจกรรมและความสนใจร่วม โดยได้รับแรงบันดาลใจสำคัญจากแพลตฟอร์มระดับโลกอย่าง Meetup ซึ่งประสบความสำเร็จในการเป็นสื่อกลางให้ผู้คนค้นพบและเข้าร่วมกลุ่มกิจกรรมตามความสนใจที่หลากหลาย จุดเริ่มต้นของการพัฒนา "ชุมชนลิงก์" มุ่งเน้นไปที่การแก้ไขปัญหาและความต้องการของผู้ใช้ (User Stories) ที่สำคัญ 3 ประการ ซึ่งเป็นหัวใจหลักในการออกแบบและพัฒนาฟังก์ชันต่างๆ ของแอปพลิเคชันนี้

## การตอบโจทย์ความต้องการของผู้ใช้ (User Stories)

เพื่อให้เข้าใจถึงแก่นแท้ของ "ชุมชนลิงก์" เราจะอธิบายอย่างละเอียดว่าแอปพลิเคชันนี้ตอบสนองต่อ User Stories แต่ละข้ออย่างไร:

### 1. "ฉันต้องการแพลตฟอร์มสำหรับให้คนในชุมชนของฉันสามารถรวมตัวกันเพื่อทำกิจกรรมร่วมกันได้"

* **ความท้าทาย:** ในโลกปัจจุบัน ผู้คนมักมีปฏิสัมพันธ์กันในวงจำกัด หรืออาจไม่ทราบถึงกิจกรรมที่น่าสนใจซึ่งเกิดขึ้นในชุมชนของตนเอง ทำให้พลาดโอกาสในการทำความรู้จักและมีส่วนร่วมกับคนรอบข้าง
* **"ชุมชนลิงก์" แก้ปัญหานี้อย่างไร:**
    * **ฟังก์ชัน "ชุมชน" (Communities):** แอปพลิเคชันมีระบบที่ให้ผู้ใช้สามารถสร้างหรือเข้าร่วม "ชุมชน" ที่เฉพาะเจาะจงได้ เช่น ชุมชนคนรักการถ่ายภาพในมหาวิทยาลัยธรรมศาสตร์ ศูนย์รังสิต, ชุมชนนักวิ่งสวน คลองหลวง, หรือแม้แต่ชุมชนศิษย์เก่าโรงเรียน เป็นต้น กิจกรรมที่จัดขึ้นสามารถถูกผูกเข้ากับชุมชนเหล่านี้ได้โดยตรง
    * **การค้นหากิจกรรมตามชุมชน:** ผู้ใช้สามารถเรียกดูและค้นหากิจกรรมที่จัดขึ้นโดยชุมชนที่ตนเองสนใจหรือเป็นสมาชิกอยู่ ทำให้ง่ายต่อการค้นพบกิจกรรมที่เกี่ยวข้องและตรงประเด็นกับกลุ่มคนที่ตนเองต้องการมีปฏิสัมพันธ์ด้วย
    * **ศูนย์กลางข้อมูลกิจกรรม:** "ชุมชนลิงก์" ทำหน้าที่เป็นศูนย์รวมข้อมูลกิจกรรมต่างๆ ภายในชุมชน ทำให้สมาชิกไม่พลาดข่าวสารและสามารถวางแผนเข้าร่วมได้อย่างสะดวก

### 2. "ฉันต้องการแพลตฟอร์มที่ทุกคนสามารถโปรโมทกิจกรรมที่ตนเองจัดขึ้นได้อย่างง่ายดาย"

* **ความท้าทาย:** การประชาสัมพันธ์กิจกรรม โดยเฉพาะสำหรับบุคคลทั่วไปหรือกลุ่มขนาดเล็กที่ไม่มีงบประมาณหรือช่องทางสื่อสารที่กว้างขวาง อาจเป็นเรื่องยากและมีข้อจำกัด ทำให้กิจกรรมดีๆ หลายครั้งไม่เป็นที่รู้จักเท่าที่ควร
* **"ชุมชนลิงก์" แก้ปัญหานี้อย่างไร:**
    * **ระบบการสร้างกิจกรรมที่เปิดกว้าง:** ทุกคนที่เป็นสมาชิกของ "ชุมชนลิงก์" สามารถสวมบทบาทเป็น "ผู้จัดกิจกรรม" (Organizer) ได้โดยไม่มีค่าใช้จ่ายหรือขั้นตอนที่ซับซ้อน
    * **เครื่องมือสร้างกิจกรรมที่ครบครัน:** ผู้จัดสามารถกรอกรายละเอียดของกิจกรรมได้อย่างครบถ้วน ไม่ว่าจะเป็น ชื่อกิจกรรม, คำอธิบายอย่างละเอียด, สถานที่จัด (พร้อมแผนที่หากมีการเชื่อมต่อ API), วันที่และเวลาเริ่มต้น, การอัปโหลดรูปภาพประกอบกิจกรรมเพื่อดึงดูดความสนใจ, การกำหนดหมวดหมู่และชุมชนที่เกี่ยวข้อง, และการระบุจำนวนผู้เข้าร่วมสูงสุด (หากมี)
    * **การแสดงผลกิจกรรมที่ชัดเจน:** กิจกรรมที่สร้างขึ้นจะปรากฏบนแพลตฟอร์มให้ผู้ใช้อื่นๆ สามารถค้นพบได้ผ่านการค้นหา, การเรียกดูตามหมวดหมู่, หรือการแนะนำกิจกรรม ทำให้กิจกรรมของผู้จัดทุกคนมีโอกาสเข้าถึงกลุ่มเป้าหมายได้กว้างขึ้น

### 3. "ฉันต้องการสร้างคอนเน็กชันใหม่ๆ หรือหาเพื่อนที่มีความสนใจในเรื่องเดียวกัน"

* **ความท้าทาย:** การขยายวงสังคมและค้นหาเพื่อนใหม่ที่มีความชอบคล้ายกันอาจเป็นเรื่องที่ต้องใช้ความพยายามและเวลา โดยเฉพาะอย่างยิ่งเมื่อมีภาระหน้าที่ในชีวิตประจำวัน
* **"ชุมชนลิงก์" แก้ปัญหานี้อย่างไร:**
    * **การจัดหมวดหมู่กิจกรรมตามความสนใจ (Categories):** นอกเหนือจากการจัดกลุ่มตาม "ชุมชน" แอปพลิเคชันยังมีการแบ่ง "หมวดหมู่กิจกรรม" ตามประเภทของความสนใจที่หลากหลาย เช่น กีฬา, ดนตรี, ศิลปะ, การทำอาหาร, เทคโนโลยี, การเรียนรู้ภาษา, การพัฒนาตนเอง เป็นต้น ผู้ใช้สามารถเลือกดูเฉพาะกิจกรรมในหมวดหมู่ที่ตนเองสนใจ ซึ่งเป็นก้าวแรกในการพบปะผู้คนที่มีความชอบคล้ายกัน
    * **ฟีเจอร์ "ควิซค้นหาผีเสื้อ":** เพื่อเพิ่มมิติใหม่ให้กับการค้นหาเพื่อนที่มีเคมีตรงกัน "ชุมชนลิงก์" ได้นำเสนอระบบ "ควิซค้นหาผีเสื้อ" ซึ่งเป็นแบบทดสอบบุคลิกภาพและความสนใจในรูปแบบที่สนุกสนานและเข้าใจง่าย
        * **กระบวนการ:** ผู้ใช้ตอบคำถามในควิซ ระบบจะประมวลผลและกำหนด "ประเภทผีเสื้อ" ที่สะท้อนถึงลักษณะนิสัย, ความชอบ, หรือแนวทางการเข้าสังคมของผู้ใช้นั้นๆ
        * **การแสดงผลบนโปรไฟล์:** "ประเภทผีเสื้อ" ที่ผู้ใช้ได้รับจะถูกแสดงอย่างเด่นชัดบนหน้าโปรไฟล์ส่วนตัว
        * **การเชื่อมโยงผู้คน:** ผู้ใช้สามารถมองเห็น "ประเภทผีเสื้อ" ของผู้ใช้คนอื่นๆ เมื่อเข้าชมโปรไฟล์หรือรายชื่อผู้เข้าร่วมกิจกรรม ทำให้เกิดการรับรู้เบื้องต้นถึงความเข้ากันได้ หรือความคล้ายคลึงกันในด้านต่างๆ ซึ่งอาจเป็นจุดเริ่มต้นของการสร้างบทสนทนาและมิตรภาพใหม่ๆ ที่ง่ายขึ้นและเป็นธรรมชาติมากขึ้น
    * **การแสดงรายชื่อผู้เข้าร่วมและผู้สนใจ:** ในหน้ารายละเอียดกิจกรรม ผู้ใช้สามารถเห็นได้ว่าใครบ้างที่ยืนยันเข้าร่วม (Attending) หรือแสดงความสนใจ (Interested) ในกิจกรรมนั้นๆ พร้อมลิงก์ไปยังโปรไฟล์ของแต่ละคน ทำให้สามารถทำความรู้จักเบื้องต้นก่อนเริ่มกิจกรรมจริงได้

## ขั้นตอนการใช้งาน
เพื่อให้เห็นภาพการทำงานของ "ชุมชนลิงก์" ได้ชัดเจนยิ่งขึ้น นี่คือขั้นตอนการใช้งานตาม User Stories ที่กล่าวมา:

### ขั้นตอนการใช้งานสำหรับ User Story 1: การรวมกลุ่มในชุมชน

1.  **ผู้ใช้ A (สมาชิกชุมชนคลองหนึ่ง):** เข้าสู่ระบบ "ชุมชนลิงก์"
2.  **ไปที่หน้า "กิจกรรม" (Event List):** จากแถบนำทาง ผู้ใช้ A คลิกที่เมนู "กิจกรรม"
3.  **กรองตาม "ชุมชน":** ผู้ใช้ A มองหาตัวกรอง "เลือกชุมชน" และเลือก "ชุมชนคนคลองหนึ่ง"
4.  **ดูกิจกรรมในชุมชน:** หน้าเว็บจะแสดงเฉพาะกิจกรรมที่ผูกกับ "ชุมชนคนคลองหนึ่ง"
5.  **ดูกรายละเอียดและเข้าร่วม:** ผู้ใช้ A คลิกดูกิจกรรมที่สนใจ อ่านรายละเอียด และหากต้องการเข้าร่วม ก็คลิกปุ่ม "เข้าร่วม" หรือ "สนใจ"

### ขั้นตอนการใช้งานสำหรับ User Story 2: การสร้างและโปรโมทกิจกรรม (โดยตัวอย่างผู้ใช้ JaneJ)

1.  **JaneJ (ผู้จัดกิจกรรม):** เข้าสู่ระบบ "ชุมชนลิงก์"
2.  **ไปที่หน้า "สร้างกิจกรรม" (Create Event):** จากแถบนำทาง JaneJ คลิกที่เมนู "สร้างกิจกรรม" (จะปรากฏเมื่อล็อกอินแล้ว)
3.  **กรอกรายละเอียดกิจกรรม(ตัวอย่าง):**
    * **ชื่อกิจกรรม:** "Jam With JaneJ: คาราโอเกะ ปลดปล่อยพลังเสียง!"
    * **รายละเอียด:** มาร้องเพลงคาราโอเกะด้วยกัน หาเพื่อนใหม่
    * **สถานที่:** "ลานกิจกรรมหน้าหอประชุมเล็ก มหาวิทยาลัยธรรมศาสตร์ ศูนย์รังสิต"
    * **วันที่และเวลา:** 2025-06-08 เวลา 15:00
    * **รูปภาพ:** อัปโหลดรูปภาพที่สื่อถึงกิจกรรมดนตรีสนุกๆ
    * **หมวดหมู่:** เลือก "ดนตรี"
    * **จำนวนผู้เข้าร่วมสูงสุด:** 25
4.  **บันทึกกิจกรรม:** JaneJ ตรวจสอบความถูกต้องแล้วคลิกปุ่ม "บันทึกกิจกรรม"
5.  **กิจกรรมปรากฏบนแพลตฟอร์ม:** กิจกรรม "Jam With JaneJ" จะปรากฏในหน้ารายการกิจกรรม และผู้ใช้อื่นๆ ที่สนใจดนตรีหรืออยู่ในชุมชน "ชาวรังสิตหัวใจดนตรี" ก็จะสามารถค้นพบกิจกรรมนี้ได้

### ขั้นตอนการใช้งานสำหรับ User Story 3: การค้นหาเพื่อนใหม่ตามความสนใจ

**วิธีที่ 1: ผ่านการค้นหากิจกรรมตามหมวดหมู่**

1.  **ผู้ใช้ B (สนใจศิลปะ):** เข้าสู่ระบบ "ชุมชนลิงก์"
2.  **ไปที่หน้า "กิจกรรม":** คลิกเมนู "กิจกรรม"
3.  **กรองตาม "หมวดหมู่":** ผู้ใช้ B เลือกตัวกรอง "เลือกหมวดหมู่กิจกรรม" และเลือก "ศิลปะและงานฝีมือ"
4.  **ค้นพบกิจกรรม:** ผู้ใช้ B เห็นกิจกรรม "Workshop วาดภาพสีน้ำนอกสถานที่ 'มนต์เสน่ห์ตลาดน้ำอัมพวา'" และสนใจเข้าร่วม
5.  **ดูผู้เข้าร่วมคนอื่น:** เมื่อเข้าไปดูรายละเอียดกิจกรรม ผู้ใช้ B สามารถเห็นรายชื่อผู้ที่ "เข้าร่วม" หรือ "สนใจ" คนอื่นๆ ซึ่งอาจมีพื้นฐานความชอบศิลปะเหมือนกัน และสามารถเริ่มทำความรู้จักกันได้ในวันงาน

**วิธีที่ 2: ผ่านฟีเจอร์ "ควิซค้นหาผีเสื้อ"**

1.  **ผู้ใช้ C (ต้องการหาเพื่อนใหม่):** สมัครสมาชิกและเข้าสู่ระบบ "ชุมชนลิงก์"
2.  **ทำควิซผีเสื้อ:** ผู้ใช้ C เห็นลิงก์หรือปุ่มชวนทำ "ควิซค้นหาผีเสื้อ" จึงคลิกเข้าไปทำแบบทดสอบ
3.  **รับผลลัพธ์:** หลังจากตอบคำถาม ระบบประมวลผลและแจ้งว่าผู้ใช้ C เป็น "ผีเสื้อนักผจญภัย" (สมมติ) พร้อมคำอธิบายลักษณะ
4.  **ผลลัพธ์แสดงบนโปรไฟล์:** "ประเภทผีเสื้อนักผจญภัย" จะปรากฏบนโปรไฟล์ของผู้ใช้ C
5.  **ดูโปรไฟล์ JaneJ:** ผู้ใช้ C อาจจะเห็นกิจกรรมที่ JaneJ จัด หรือเห็น JaneJ ในรายชื่อผู้เข้าร่วมกิจกรรมอื่น เมื่อคลิกเข้าไปดูโปรไฟล์ของ JaneJ จะเห็นว่า JaneJ เป็น "ผีเสื้อสีสันสังคม"
6.  **เชื่อมโยงความสนใจ:** ผู้ใช้ C อาจจะรู้สึกว่า "ผีเสื้อสีสันสังคม" อย่าง JaneJ น่าจะเป็นคนที่สนุกสนานและเข้ากับ "ผีเสื้อนักผจญภัย" อย่างตนเองได้ดี โดยเฉพาะถ้าทั้งคู่สนใจกิจกรรมคล้ายๆ กัน เช่น กิจกรรมกลางแจ้ง หรือกิจกรรมที่ต้องใช้ความคิดสร้างสรรค์ จึงอาจตัดสินใจทักทาย JaneJ หรือเข้าร่วมกิจกรรมที่ JaneJ จัด

## การติดตั้งและใช้งาน (สำหรับการพัฒนา)

เนื่องจาก "ชุมชนลิงก์" เป็นเว็บแอปพลิเคชันที่พัฒนาด้วย Django ผู้ใช้ทั่วไปสามารถเข้าใช้งานผ่านเว็บเบราว์เซอร์ได้โดยตรงเมื่อแอปพลิเคชันถูกนำขึ้นเซิร์ฟเวอร์ (deployed) แล้ว สำหรับนักพัฒนาที่ต้องการติดตั้งโปรเจกต์นี้ในเครื่องของตนเองเพื่อทำการพัฒนาต่อ สามารถทำตามขั้นตอนเบื้องต้นดังนี้:

**ข้อกำหนดเบื้องต้น (Prerequisites):**

* Python (เวอร์ชัน 3.8 ขึ้นไปแนะนำ)
* Pip (Python package installer)
* Git (Version control system)
* (แนะนำ) Virtual Environment (เช่น `venv` หรือ `conda`)

**ขั้นตอนการติดตั้ง:**

1.  **Clone Repository:**
    ```bash
    git clone <https://github.com/PimladaNga/dsi202_2025>
    cd <dsi202_2025>
    ```

2.  **สร้างและ Activate Virtual Environment (แนะนำ):**
    ```bash
    python -m venv venv
    # บน Windows
    venv\Scripts\activate
    # บน macOS/Linux
    source venv/bin/activate
    ```

3.  **ติดตั้ง Dependencies:**
    ไฟล์ `requirements.txt` ควรมีรายชื่อ library ที่โปรเจกต์นี้ใช้งาน (เช่น Django, Pillow, djangorestframework, django-widget-tweaks เป็นต้น)
    ```bash
    pip install -r requirements.txt
    ```
    *(หากยังไม่มีไฟล์ `requirements.txt` สามารถสร้างได้จากโปรเจกต์ที่สมบูรณ์แล้วด้วยคำสั่ง `pip freeze > requirements.txt`)*

4.  **ตั้งค่า Database:**
    โปรเจกต์นี้ใช้ SQLite เป็นฐานข้อมูลเริ่มต้น ซึ่งมีการตั้งค่าไว้ใน `settings.py` แล้ว
    ทำการ Migrate ฐานข้อมูลเพื่อสร้างตารางที่จำเป็น:
    ```bash
    python manage.py makemigrations myapp
    python manage.py migrate
    ```
    *(`myapp` คือชื่อแอปพลิเคชันของคุณ)*

5.  **สร้าง Superuser (สำหรับเข้าหน้า Admin):**
    ```bash
    python manage.py createsuperuser
    ```
    จากนั้นกรอก Username, Email (ไม่บังคับ), และ Password ตามที่ระบบแจ้ง

6.  **รวบรวม Static Files (จำเป็นสำหรับ Production แต่ควรทดสอบใน Development ด้วย):**
    ตรวจสอบว่า `STATIC_ROOT` ใน `settings.py` ถูกตั้งค่าอย่างเหมาะสม (ปกติจะตั้งค่าเมื่อจะ deploy)
    ```bash
    python manage.py collectstatic
    ```
7.  **รัน Development Server:**
    ```bash
    python manage.py runserver
    ```
    โดยปกติแล้ว เซิร์ฟเวอร์จะรันที่ `http://127.0.0.1:8000/`

**การใช้งาน:**

* **เข้าสู่หน้าเว็บ:** เปิดเว็บเบราว์เซอร์แล้วไปที่ `http://127.0.0.1:8000/`
* **เข้าสู่หน้า Admin:** ไปที่ `http://127.0.0.1:8000/admin/` แล้วล็อกอินด้วยบัญชี Superuser ที่สร้างไว้ เพื่อจัดการข้อมูลต่างๆ ผ่าน Django Admin interfaceS

## สรุปความคาดหวังของผู้จัดทำ

ทีมผู้จัดทำ **ชุมชนลิงก์ (Chum-Chon Link)** มีความมุ่งมั่นและคาดหวังเป็นอย่างยิ่งว่าแพลตฟอร์มนี้จะเป็นมากกว่าเพียงเครื่องมือในการค้นหาและจัดการกิจกรรม แต่จะเป็น **"สะพาน"** ที่เชื่อมโยงผู้คนเข้าหากันอย่างแท้จริง เราเชื่อว่าการได้ทำกิจกรรมที่รักร่วมกับผู้อื่นที่มีความสนใจคล้ายคลึงกัน เป็นหนทางที่ดีที่สุดในการสร้างมิตรภาพที่ยั่งยืนและมีความหมาย

ด้วยฟังก์ชันการจัดกลุ่มตาม "ชุมชน" และ "หมวดหมู่ความสนใจ" ผนวกกับกลไกการค้นหาคู่เหมือนผ่าน "ควิซผีเสื้อ" เราหวังเป็นอย่างยิ่งว่า "ชุมชนลิงก์" จะสามารถทำลายกำแพงของความห่างเหิน ช่วยให้ผู้คนกล้าที่จะก้าวออกมาทำความรู้จักเพื่อนใหม่ๆ และสร้างเครือข่ายทางสังคมที่แข็งแกร่งและอบอุ่นยิ่งขึ้น ท้ายที่สุดแล้ว ความปรารถนาสูงสุดของเราคือการเห็นผู้ใช้ทุกคนใน "ชุมชนลิงก์" สามารถ **"เป็นเพื่อนกันได้มากขึ้น"** ผ่านประสบการณ์และความทรงจำดีๆ ที่สร้างร่วมกันบนแพลตฟอร์มนี้.