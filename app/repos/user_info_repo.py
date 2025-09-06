from sqlalchemy import Table, MetaData, Column, String, Integer, Date, DateTime, text
from app.repos.base_repo import BaseRepo

table = Table(
    "t_user_info",
    MetaData(),
    Column("id", Integer, primary_key=True, autoincrement=True, comment="고유 PK"),
    Column("user_id", String(50), index=True, comment="t_user 고유 PK"),
    Column("nickname", String(50), comment="닉네임"),
    Column("fullname", String(100), comment="이름"),
    Column("birth_date", Date, comment="생년월일"),
    Column("mobile", String(20), comment="휴대폰"),
    Column("telephone", String(20), comment="전화번호"),
    Column("zipcode", String(10), comment="우편번호"),
    Column("address1", String(200), comment="주소"),
    Column("address2", String(200), comment="상세주소"),
    Column("email", String(100), comment="이메일"),
    Column("email_consent", String(1), server_default=text("F"), comment="이메일 수신"),
    Column("sms_consent", String(1), server_default=text("F"), comment="SMS 수신"),
    Column("referrer_username", String(50), comment="추천인 아이디"),
    Column("company_name", String(50), comment="업체명"),
    Column("ceo_name", String(50), comment="대표자명"),
    Column("company_tel", String(50), comment="업체전화번호"),
    Column("business_type", String(50), comment="업태"),
    Column("business_item", String(50), comment="업종"),
    Column("company_zipcode", String(50), comment="업체 우편번호"),
    Column("company_address1", String(50), comment="업체 주소"),
    Column("company_address2", String(50), comment="업체 상세주소"),
    Column("business_number", String(50), comment="사업자번호"),
    Column("business_license", String(50), comment="사업자등록증"),
    Column("power_of_attorney", String(50), comment="위임장"),
    Column("last_login_at", String(50), comment="마지막 접속일시"),
    Column("pobox_code", String(50), comment="사서함 번호"),
    Column("created_at", DateTime, comment="생성일시"),
    Column("updated_at", DateTime, comment="수정일시"),
    Column("is_deleted", String(1), server_default=text("F"), comment="삭제 여부"),
    mysql_engine="InnoDB",
    mysql_charset="utf8mb4",
    comment="회원 추가 정보"
)


class UserInfoRepo(BaseRepo):
    @property
    def table(self):
        return table

    async def get_by_user_id(self, user_id: int):
        query = self.table.select().where(self.table.c.user_id == user_id)
        row = await self.db.fetch_one(query)
        return dict(row) if row else None
