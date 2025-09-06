import sqlalchemy

from app.repos.base_repo import BaseRepo

table = sqlalchemy.Table(
    "t_user",
    sqlalchemy.MetaData(),
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, comment="고유 PK"),
    sqlalchemy.Column("username", sqlalchemy.String(50), nullable=False, unique=True, index=True, comment="아이디"),
    sqlalchemy.Column("username_type", sqlalchemy.String(50), nullable=False, unique=True, index=True,
                      comment="아이디 타입"),
    sqlalchemy.Column("password", sqlalchemy.String(200), nullable=False, comment="비밀번호"),
    sqlalchemy.Column("nickname", sqlalchemy.String(50), comment="닉네임"),
    sqlalchemy.Column("fullname", sqlalchemy.String(100), comment="이름"),
    sqlalchemy.Column("birth_date", sqlalchemy.Date, comment="생년월일"),
    sqlalchemy.Column("mobile", sqlalchemy.String(20), comment="휴대폰"),
    sqlalchemy.Column("telephone", sqlalchemy.String(20), comment="전화번호"),
    sqlalchemy.Column("zipcode", sqlalchemy.String(10), comment="우편번호"),
    sqlalchemy.Column("address1", sqlalchemy.String(200), comment="주소"),
    sqlalchemy.Column("address2", sqlalchemy.String(200), comment="상세주소"),
    sqlalchemy.Column("email", sqlalchemy.String(100), comment="이메일"),
    sqlalchemy.Column("email_consent", sqlalchemy.String(1), server_default=sqlalchemy.text("F"),
                      comment="이메일 수신 동의 여부"),
    sqlalchemy.Column("sms_consent", sqlalchemy.String(1), server_default=sqlalchemy.text("F"), comment="SMS 수신 동의 여부"),
    sqlalchemy.Column("referrer_username", sqlalchemy.String(50), comment="추천인 아이디"),
    sqlalchemy.Column("company_name", sqlalchemy.String(50), comment="업체명"),
    sqlalchemy.Column("ceo_name", sqlalchemy.String(50), comment="대표자명"),
    sqlalchemy.Column("company_tel", sqlalchemy.String(50), comment="업체전화번호"),
    sqlalchemy.Column("business_type", sqlalchemy.String(50), comment="업태"),
    sqlalchemy.Column("business_item", sqlalchemy.String(50), comment="업종"),
    sqlalchemy.Column("company_zipcode", sqlalchemy.String(50), comment="업체 우편번호"),
    sqlalchemy.Column("company_address1", sqlalchemy.String(50), comment="업체 주소"),
    sqlalchemy.Column("company_address2", sqlalchemy.String(50), comment="업체 상세주소"),
    sqlalchemy.Column("business_number", sqlalchemy.String(50), comment="사업자번호"),
    sqlalchemy.Column("business_license", sqlalchemy.String(50), comment="사업자등록증"),
    sqlalchemy.Column("power_of_attorney", sqlalchemy.String(50), comment="위임장"),
    sqlalchemy.Column("last_login_at", sqlalchemy.String(50), comment="마지막 접속일시"),
    sqlalchemy.Column("pobox_code", sqlalchemy.String(50), comment="사서함 번호 "),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, comment="생성일시"),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime, comment="수정일시"),
    sqlalchemy.Column("is_deleted", sqlalchemy.String(1), server_default=sqlalchemy.text("F"), comment="삭제 여부"),
    mysql_engine="InnoDB",
    mysql_charset="utf8mb4",
    comment="회원 정보"
)


class UserRepo(BaseRepo):
    @property
    def table(self):
        return User.__table__

    async def get_by_username(self, username: str):
        query = self.table.select().where(self.table.c.username == username)
        row = await self.db.fetch_one(query)
        return dict(row) if row else None
