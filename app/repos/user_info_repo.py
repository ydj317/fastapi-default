from sqlalchemy import Column, String, Integer, Date, DateTime, text
from app.repos.base import Base, BaseRepo

class UserInfo(Base):
    __tablename__ = "t_user_info"
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8mb4",
        "comment": "회원 추가정보"
    }


    id = Column(Integer, primary_key=True, autoincrement=True, comment="고유 PK")
    user_id = Column(String(50), index=True, comment="t_user 고유 PK")
    nickname = Column(String(50), comment="닉네임")
    fullname = Column(String(100), comment="이름")
    birth_date = Column(Date, comment="생년월일")
    mobile = Column(String(20), comment="휴대폰")
    telephone = Column(String(20), comment="전화번호")
    zipcode = Column(String(10), comment="우편번호")
    address1 = Column(String(200), comment="주소")
    address2 = Column(String(200), comment="상세주소")
    email = Column(String(100), comment="이메일")
    email_consent = Column(String(1), server_default=text("'F'"), comment="이메일 수신")
    sms_consent = Column(String(1), server_default=text("'F'"), comment="SMS 수신")
    referrer_username = Column(String(50), comment="추천인 아이디")
    company_name = Column(String(50), comment="업체명")
    ceo_name = Column(String(50), comment="대표자명")
    company_tel = Column(String(50), comment="업체전화번호")
    business_type = Column(String(50), comment="업태")
    business_item = Column(String(50), comment="업종")
    company_zipcode = Column(String(50), comment="업체 우편번호")
    company_address1 = Column(String(50), comment="업체 주소")
    company_address2 = Column(String(50), comment="업체 상세주소")
    business_number = Column(String(50), comment="사업자번호")
    business_license = Column(String(50), comment="사업자등록증")
    power_of_attorney = Column(String(50), comment="위임장")
    last_login_at = Column(String(50), comment="마지막 접속일시")
    pobox_code = Column(String(50), comment="사서함 번호")
    created_at = Column(DateTime, comment="생성일시")
    updated_at = Column(DateTime, comment="수정일시")
    is_deleted = Column(String(1), server_default=text("'F'"), comment="삭제 여부")


class UserInfoRepo(BaseRepo):
    @property
    def table(self):
        return UserInfo.__table__

    async def get_by_user_id(self, user_id: int):
        query = self.table.select().where(self.table.c.user_id == user_id)
        row = await self.db.fetch_one(query)
        return dict(row) if row else None
