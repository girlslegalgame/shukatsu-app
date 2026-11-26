from sqlalchemy import Column, Date, Enum, ForeignKey, Integer, String, Text

from .database import Base


# 1. 学部テーブル
class Faculty(Base):
    __tablename__ = "FACULTY"

    faculty_id = Column(Integer, primary_key=True, autoincrement=True, comment="学部ID")
    faculty_name = Column(String(100), nullable=False, comment="学部名")


# 2. 学科テーブル
class Department(Base):
    __tablename__ = "DEPARTMENT"

    department_id = Column(Integer, primary_key=True, autoincrement=True, comment="学科ID")
    faculty_id = Column(Integer, ForeignKey("FACULTY.faculty_id"), nullable=False, comment="学部ID")
    department_name = Column(String(100), nullable=False, comment="学科名")


# 3. 教員テーブル
class Teacher(Base):
    __tablename__ = "TEACHER"

    teacher_id = Column(Integer, primary_key=True, autoincrement=True, comment="教員ID")
    login_id = Column(String(50), nullable=False, unique=True, comment="ログインID")
    email = Column(String(255), nullable=False, unique=True, comment="メールアドレス")
    phone_number = Column(String(20), nullable=False, comment="電話番号")
    teacher_name = Column(String(100), nullable=False, comment="氏名")
    password_hash = Column(String(255), nullable=False, comment="ログインパスワードのハッシュ値")


# 4. クラステーブル
class Class(Base):
    __tablename__ = "CLASS"

    class_id = Column(Integer, primary_key=True, autoincrement=True, comment="クラスID")
    class_name = Column(String(50), nullable=False, comment="クラス名")
    department_id = Column(Integer, ForeignKey("DEPARTMENT.department_id"), nullable=False, comment="学科ID")
    teacher_id = Column(Integer, ForeignKey("TEACHER.teacher_id"), nullable=False, comment="教員ID")


# 5. 学生テーブル
class Student(Base):
    __tablename__ = "STUDENT"

    student_id = Column(String(20), primary_key=True, comment="学籍番号")
    student_name = Column(String(100), nullable=False, comment="学生の氏名")
    class_id = Column(Integer, ForeignKey("CLASS.class_id"), nullable=False, comment="クラスID")
    password_hash = Column(String(255), nullable=False, comment="ログインパスワードのハッシュ値")
    enrollment_date = Column(Date, nullable=False, comment="入学年月")
    expected_graduation_date = Column(Date, nullable=False, comment="卒業予定年月")


# 6. 職種テーブル
class Job(Base):
    __tablename__ = "JOB"

    job_id = Column(Integer, primary_key=True, autoincrement=True, comment="職種ID")
    job_name = Column(String(100), nullable=False, comment="職種名")


# 7. 資格テーブル
class Qualification(Base):
    __tablename__ = "QUALIFICATION"

    qualification_id = Column(Integer, primary_key=True, autoincrement=True, comment="資格ID")
    qualification_name = Column(String(150), nullable=False, comment="資格名")
    qualification_type = Column(
        Enum("国家試験", "ベンダー試験", "民間検定", name="qualification_type_enum"),
        nullable=False,
        comment="資格種類",
    )


# 8. 学生_資格テーブル
class StudentQualification(Base):
    __tablename__ = "STUDENT_QUALIFICATION"

    student_id = Column(String(20), ForeignKey("STUDENT.student_id"), primary_key=True, comment="学籍番号")
    qualification_id = Column(
        Integer, ForeignKey("QUALIFICATION.qualification_id"), primary_key=True, comment="資格ID"
    )
    acquired_date = Column(Date, nullable=False, comment="取得年月")


# 9. 学生_志望職種テーブル
class StudentDesiredJob(Base):
    __tablename__ = "STUDENT_DESIRED_JOB"

    student_id = Column(String(20), ForeignKey("STUDENT.student_id"), primary_key=True, comment="学籍番号")
    job_id = Column(Integer, ForeignKey("JOB.job_id"), primary_key=True, comment="職種ID")
    priority = Column(Integer, nullable=False, comment="優先順位")


# 10. 企業テーブル
class Company(Base):
    __tablename__ = "COMPANY"

    company_id = Column(Integer, primary_key=True, autoincrement=True, comment="企業ID")
    company_name = Column(String(255), nullable=False, comment="企業名")
    location = Column(String(255), nullable=False, comment="所在地")
    recruit_url = Column(String(2083), nullable=True, comment="採用ページのURL")


# 11. 企業_職種テーブル
class CompanyJob(Base):
    __tablename__ = "COMPANY_JOB"

    company_id = Column(Integer, ForeignKey("COMPANY.company_id"), primary_key=True, comment="企業ID")
    job_id = Column(Integer, ForeignKey("JOB.job_id"), primary_key=True, comment="職種ID")


# 12. 企業_イベントテーブル
class CompanyEvent(Base):
    __tablename__ = "COMPANY_EVENT"

    event_id = Column(Integer, primary_key=True, autoincrement=True, comment="イベントID")
    company_id = Column(Integer, ForeignKey("COMPANY.company_id"), nullable=False, comment="企業ID")
    event_name = Column(String(255), nullable=False, comment="イベント名")
    event_date = Column(Date, nullable=False, comment="開催日")
    application_start_date = Column(Date, nullable=False, comment="応募開始日")
    application_end_date = Column(Date, nullable=False, comment="応募終了日")


# 13. 履歴書テーブル
class Resume(Base):
    __tablename__ = "RESUME"

    resume_id = Column(Integer, primary_key=True, autoincrement=True, comment="履歴書ID")
    student_id = Column(String(20), ForeignKey("STUDENT.student_id"), nullable=False, comment="学籍番号")
    self_pr = Column(Text, nullable=True, comment="自己PR")
    personal_requests = Column(Text, nullable=True, comment="本人希望欄")
    created_date = Column(Date, nullable=False, comment="作成日")
    updated_date = Column(Date, nullable=False, comment="最終更新日")


# 14. 学生_応募企業テーブル
class Application(Base):
    __tablename__ = "APPLICATION"

    application_id = Column(Integer, primary_key=True, autoincrement=True, comment="応募ID")
    resume_id = Column(Integer, ForeignKey("RESUME.resume_id"), nullable=True, comment="履歴書ID")
    student_id = Column(String(20), ForeignKey("STUDENT.student_id"), nullable=False, comment="学籍番号")
    company_id = Column(Integer, ForeignKey("COMPANY.company_id"), nullable=False, comment="企業ID")
    job_id = Column(Integer, ForeignKey("JOB.job_id"), nullable=False, comment="職種ID")
    application_type = Column(
        Enum("インターン", "本選考", name="application_type_enum"),
        nullable=False,
        comment="応募種類",
    )
    status = Column(
        Enum("エントリー済", "選考中", "内定", "不合格", "辞退", name="application_status_enum"),
        nullable=False,
        comment="状況",
    )


# 15. 面接記録テーブル
class InterviewRecord(Base):
    __tablename__ = "INTERVIEW_RECORD"

    interview_id = Column(Integer, primary_key=True, autoincrement=True, comment="面接ID")
    application_id = Column(Integer, ForeignKey("APPLICATION.application_id"), nullable=False, comment="応募ID")
    interview_date = Column(Date, nullable=False, comment="面接日")
    selection_stage = Column(String(100), nullable=False, comment="選考段階")
    questions = Column(Text, nullable=True, comment="質問内容")
    reflection_memo = Column(Text, nullable=True, comment="振り返りメモ")