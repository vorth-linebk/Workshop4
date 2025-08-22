from fastapi import FastAPI
from sqlalchemy.orm import Session

from database import engine
from models import Base
from auth import router as auth_router
from profile import router as profile_router

app = FastAPI(
    title="Workshop4 API",
    version="0.1.0",
    description=(
        "API สำหรับการสมัครสมาชิก ล็อกอิน และจัดการโปรไฟล์ (ดู/แก้ไข).\n\n"
        "- Authentication: สมัคร, ล็อกอิน (JWT)\n"
        "- Profile: ดูโปรไฟล์ตนเอง, แก้ไขชื่อ-นามสกุล-เบอร์โทร"
    ),
    contact={
        "name": "Workshop4",
        "url": "https://example.com",
        "email": "support@example.com",
    },
    license_info={"name": "MIT"},
    openapi_tags=[
        {"name": "auth", "description": "ลงทะเบียนผู้ใช้ใหม่ และรับโทเค็นสำหรับเข้าสู่ระบบ."},
        {"name": "profile", "description": "ดู/แก้ไขข้อมูลโปรไฟล์ของผู้ใช้ที่กำลังล็อกอิน."},
    ],
)

# Create tables on startup if they don't exist
Base.metadata.create_all(bind=engine)


@app.get("/", summary="Healthcheck / Hello", description="ทดสอบการทำงานของเซิร์ฟเวอร์อย่างง่าย")
async def read_root():
	return {"message": "Hello, World!"}


# Routers
app.include_router(auth_router)
app.include_router(profile_router)
