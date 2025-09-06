from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class JoinRequest(BaseModel):
    # t_user
    username: str                      # 아이디
    password: str                      # 비밀번호

    # t_user_info
    nickname: Optional[str] = None     # 닉네임
    fullname: Optional[str] = None     # 이름
    birth_date: Optional[date] = None  # 생년월일
    mobile: Optional[str] = None       # 휴대폰
    telephone: Optional[str] = None    # 전화번호
    zipcode: Optional[str] = None      # 우편번호
    address1: Optional[str] = None     # 주소
    address2: Optional[str] = None     # 상세주소
    email: Optional[str] = None        # 이메일
    email_consent: Optional[str] = "F" # 이메일 수신 (기본 F)
    sms_consent: Optional[str] = "F"   # SMS 수신 (기본 F)
    referrer_username: Optional[str] = None  # 추천인 아이디
    company_name: Optional[str] = None       # 업체명
    ceo_name: Optional[str] = None           # 대표자명
    company_tel: Optional[str] = None        # 업체전화번호
    business_type: Optional[str] = None      # 업태
    business_item: Optional[str] = None      # 업종
    company_zipcode: Optional[str] = None    # 업체 우편번호
    company_address1: Optional[str] = None   # 업체 주소
    company_address2: Optional[str] = None   # 업체 상세주소
    business_number: Optional[str] = None    # 사업자번호
    business_license: Optional[str] = None   # 사업자등록증
    power_of_attorney: Optional[str] = None  # 위임장
    last_login_at: Optional[datetime] = None # 마지막 접속일시
    pobox_code: Optional[str] = None         # 사서함 번호

class LoginRequest(BaseModel):
    username: str
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    nickname: str