/*============================================================
 은행24 데이터베이스 생성 SQL
 주석은 송정근이 작성 히히히히히히히히히히히히히히히히히
============================================================*/


/*이건 기존의 있던  데이터베이스의 테이블, 데이터를 삭제하는 코드임 
(예를 들어 내가 이 데이터 베이스를 테스트해보려고 
신청하기 계속 누르고 막 데이터 넣고 해서 지저분해진걸 정리하는 코드임)
삭제 순서: 외래 키를 가진 테이블 먼저 삭제
왜래 키 란 기본 키에서 레퍼런스 명령어를 써서 다른 테이블에 적용하는 키
한마디로 다른테이블의 기본키를 가져와서 쓰는 키다 */

DROP TABLE IF EXISTS applications;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;


-- ============================================================
-- 1. customers 테이블
/* INTEGER 정수값 PRIMARY KEY 기본 키 
 AUTOINCREMENT 사람명수에 따라 id를 자동으로 늘려서 저장해준다는거 
 UNIQUE 는 고유값으로 다른 겹치는 값이 있을 수 없다는 뜻
 데이터 베이스에 저장될때 고객의 이름이나 전화번호 나이는 무조건 입력해야한다
 0은 기본값이 0이라는게 아니라 True아님 False라고 생각하면됨*/
CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    customer_phone TEXT UNIQUE NOT NULL,
    customer_age INTEGER NOT NULL,
    customer_monthly_income INTEGER,
    customer_credit_grade INTEGER,
    customer_has_overdue INTEGER DEFAULT 0,
    customer_existing_loan_count INTEGER DEFAULT 0,
    customer_is_employed INTEGER DEFAULT 0,
    customer_has_salary_transfer INTEGER DEFAULT 0
);

/*인덱스 생성 고객이 1,000만 명인데 인덱스가 없으면
파이썬 서버에서 "전화번호가 '010-1234-5678'인 사람 찾아줘!"라고 명령했을 때, 
데이터베이스는 1번 고객부터 1,000만 번 고객까지 하나하나 전부 다 뒤져야 함. 
(이걸 개발 용어로 풀 스캔, Full Scan이라고 함. 개느림)
그래서 약간 전화번호부 같은 거임 다 얘가 미리 정렬해 놓는거임 컴퓨터가 바로바로 찾을 수 있게
절반 절반 나눠 업다운 형식으로 찾는듯 이진탐색이라고 함 그걸
단점은 책장 하나 만드는거라 고객정보 들어오면 바로 못넣어서 좀 느림 그래서 남발하면 안됨 진짜 중요한것만*/
CREATE INDEX idx_customer_phone ON customers(customer_phone);
CREATE INDEX idx_customer_age ON customers(customer_age);


-- ============================================================
-- 2. products 테이블
-- ============================================================
-- REAL 은 정수말고 소수점 미세한값 다룰때 
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    product_description TEXT,
    product_interest_rate REAL,
    product_loan_limit_amount INTEGER,
    product_min_age_requirement INTEGER,
    product_max_age_requirement INTEGER,
    product_min_income_requirement INTEGER,
    product_min_credit_score_requirement INTEGER,
    product_max_dti_ratio REAL,
    product_required_documents TEXT,
    product_requires_manual_review INTEGER DEFAULT 0
);

-- 인덱스 생성
CREATE INDEX idx_product_name ON products(product_name);


-- ============================================================
-- 3. applications 테이블
-- ============================================================
CREATE TABLE applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    application_number TEXT UNIQUE NOT NULL,
    applicant_customer_id INTEGER NOT NULL,
    applied_product_id INTEGER NOT NULL,
    application_status TEXT DEFAULT '신청완료',
    application_documents_submitted INTEGER DEFAULT 0,
    application_submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    application_signature_image_data TEXT,
    FOREIGN KEY (applicant_customer_id) REFERENCES customers(id),
    FOREIGN KEY (applied_product_id) REFERENCES products(id)
);

-- 인덱스 생성
CREATE INDEX idx_application_status ON applications(application_status);
CREATE INDEX idx_application_customer ON applications(applicant_customer_id);
CREATE INDEX idx_application_product ON applications(applied_product_id);
CREATE INDEX idx_application_submitted_at ON applications(application_submitted_at);



-- ============================================================
-- 데이터 입력
-- ============================================================

-- customers 데이터 (15명) 이거 순서대로 넣어야함 선언한 테이블대로
INSERT INTO customers VALUES (1, '김민준', '010-1234-5678', 28, 3500, 3, 0, 0, 1, 300);
INSERT INTO customers VALUES (2, '이서연', '010-2345-6789', 35, 4200, 2, 0, 1, 0, 0);
INSERT INTO customers VALUES (3, '박지훈', '010-3456-7890', 42, 5000, 1, 0, 2, 0, 0);
INSERT INTO customers VALUES (4, '최수아', '010-4567-8901', 24, 1800, 5, 0, 0, 0, 0);
INSERT INTO customers VALUES (5, '정우진', '010-5678-9012', 31, 3000, 4, 1, 1, 0, 0);
INSERT INTO customers VALUES (6, '한예린', '010-6789-0123', 55, 2500, 6, 0, 3, 0, 0);
INSERT INTO customers VALUES (7, '오승현', '010-7890-1234', 29, 2200, 7, 1, 2, 0, 0);
INSERT INTO customers VALUES (8, '임나은', '010-8901-2345', 45, 6000, 2, 0, 1, 0, 0);
INSERT INTO customers VALUES (9, '강도현', '010-9012-3456', 22, 1200, 8, 0, 0, 0, 0);
INSERT INTO customers VALUES (10, '윤서진', '010-0123-4567', 60, 3800, 3, 0, 2, 0, 0);
INSERT INTO customers VALUES (11, '이강인', '01012345678', 27, 300, 6, 1, 3, 0, 0);
INSERT INTO customers VALUES (12, '송정근', '01012345697', 30, 3000, 1, 0, 0, 0, 0);
INSERT INTO customers VALUES (13, 'thdwjdrms', '58466165161651', 30, 3000, 1, 0, 0, 0, 0);
INSERT INTO customers VALUES (15, '김철수', '010-9876-5432', 35, 500, 3, 0, 0, 0, 0);
INSERT INTO customers VALUES (16, '이영희', '010-5555-1234', 28, 400, 4, 0, 0, 0, 0);

-- products 데이터 (36개)
INSERT INTO products VALUES (2, '시니어 안심 예금', '만 55세 이상 어르신을 위한 안전한 예금', 4.2, NULL, 55, 80, 500, 0, 100.0, '신분증,건강보험료납부확인서', 0);
INSERT INTO products VALUES (3, '직장인 플러스 통장', '재직자 전용 고금리 입출금 통장', 3.8, NULL, 20, 60, 2000, 0, 100.0, '신분증,재직증명서,소득증명서', 0);
INSERT INTO products VALUES (4, '신용 대출 스탠다드', '직장인 대상 무담보 신용대출', 6.5, 5000, 20, 60, 2500, 0, 100.0, '신분증,소득증명서,재직증명서', 0);
INSERT INTO products VALUES (5, '서민 금융 대출', '저소득층을 위한 정부 지원 저금리 대출', 3.0, 2000, 19, 65, 500, 0, 100.0, '신분증,소득증명서', 0);
INSERT INTO products VALUES (6, '전세 자금 대출', '전세 보증금 마련을 위한 주거 안정 대출', 4.5, 30000, 19, 50, 3000, 0, 100.0, '신분증,소득증명서,주민등록등본', 0);
INSERT INTO products VALUES (7, '햇살론 청년 대출', '취업 준비 청년을 위한 생활비 지원 대출', 2.5, 1200, 19, 34, 0, 0, 100.0, '신분증,주민등록등본', 0);
INSERT INTO products VALUES (8, '일반 체크카드', '누구나 사용 가능한 기본 체크카드입니다.', 0.0, 0, 19, 100, 0, 0, 100.0, '신분증', 0);
INSERT INTO products VALUES (9, '청년 우대 체크카드', '만 19-34세 청년을 위한 우대 혜택 체크카드입니다.', 0.0, 0, 19, 34, 0, 0, 100.0, '신분증', 0);
INSERT INTO products VALUES (10, '일반 신용카드', '기본적인 신용카드 서비스를 제공합니다.', 12000.0, 300, 19, 100, 100, 0, 100.0, '신분증, 소득증빙서류', 0);
INSERT INTO products VALUES (11, '골드 신용카드', '프리미엄 혜택이 제공되는 골드 등급 신용카드입니다.', 30000.0, 1000, 19, 100, 300, 0, 100.0, '신분증, 소득증빙서류', 0);
INSERT INTO products VALUES (12, '청년 우대 신용카드', '만 19-34세 청년을 위한 우대 신용카드입니다.', 0.0, 300, 19, 34, 100, 0, 100.0, '신분증, 소득증빙서류', 0);
INSERT INTO products VALUES (13, '캐시백 신용카드', '결제 금액의 일부를 캐시백으로 돌려드립니다.', 15000.0, 500, 19, 100, 150, 0, 100.0, '신분증, 소득증빙서류', 0);
INSERT INTO products VALUES (14, '마일리지 신용카드', '항공 마일리지 적립 혜택이 있는 신용카드입니다.', 20000.0, 500, 19, 100, 200, 0, 100.0, '신분증, 소득증빙서류', 0);
INSERT INTO products VALUES (15, '기업 신용카드', '사업자를 위한 법인 신용카드입니다.', 10000.0, 1000, 19, 100, 0, 0, 100.0, '신분증, 사업자등록증', 0);
INSERT INTO products VALUES (16, '일반 정기예금', '누구나 가입 가능한 기본 정기예금입니다.', 3.5, 0, 19, 100, 0, 0, 100.0, '신분증', 0);
INSERT INTO products VALUES (17, '일반 정기적금', '매월 일정 금액을 적립하는 정기적금입니다.', 3.3, 0, 19, 100, 0, 0, 100.0, '신분증', 0);
INSERT INTO products VALUES (18, '파킹통장', '자유롭게 입출금이 가능한 통장입니다.', 2.0, 0, 19, 100, 0, 0, 100.0, '신분증', 0);
INSERT INTO products VALUES (19, '저축예금', '장기 저축을 위한 예금 상품입니다.', 3.0, 0, 19, 100, 0, 0, 100.0, '신분증', 0);
INSERT INTO products VALUES (20, '아동 적금', '만 18세 미만 아동을 위한 적금 상품입니다.', 4.0, 0, 0, 18, 0, 0, 100.0, '신분증(법정대리인), 가족관계증명서', 0);
INSERT INTO products VALUES (21, '고령자 우대 예금', '만 65세 이상 고령자를 위한 우대 예금입니다.', 4.0, 0, 65, 100, 0, 0, 100.0, '신분증', 0);
INSERT INTO products VALUES (22, '청년 우대 예금', '만 19-34세 청년을 위한 우대 예금입니다.', 4.2, 0, 19, 34, 100, 0, 100.0, '신분증, 재직증명서, 소득증명원', 0);
INSERT INTO products VALUES (23, '청년 우대 적금', '만 19-34세 청년을 위한 우대 적금입니다.', 4.0, 0, 19, 34, 100, 0, 100.0, '신분증, 재직증명서', 0);
INSERT INTO products VALUES (24, '직장인 우대 예금', '급여이체 고객을 위한 우대 예금입니다.', 4.0, 0, 19, 65, 50, 0, 100.0, '신분증, 재직증명서, 급여명세서', 0);
INSERT INTO products VALUES (25, '군인 우대 적금', '현역 군인을 위한 우대 적금입니다.', 5.0, 0, 19, 35, 0, 0, 100.0, '신분증, 군복무확인서', 0);
INSERT INTO products VALUES (26, '주택청약 우대 예금', '주택청약을 위한 우대 예금입니다.', 3.8, 0, 19, 100, 0, 0, 100.0, '신분증', 0);
INSERT INTO products VALUES (27, '자유적금', '자유롭게 입금할 수 있는 적금입니다.', 3.2, 0, 19, 100, 0, 0, 100.0, '신분증', 0);
INSERT INTO products VALUES (28, '신용대출', '담보 없이 신용도로 대출받는 상품입니다.', 4.5, 5000, 19, 65, 0, 700, 100.0, '신분증, 소득증빙서류', 0);
INSERT INTO products VALUES (29, '마이너스 통장', '필요할 때 자유롭게 인출 가능한 한도대출입니다.', 5.0, 1000, 19, 65, 150, 680, 100.0, '신분증, 소득증빙서류', 0);
INSERT INTO products VALUES (30, '학자금 대출', '대학생을 위한 학자금 대출입니다.', 1.7, 5000, 19, 35, 0, 0, 100.0, '신분증, 재학증명서', 0);
INSERT INTO products VALUES (31, '생활안정자금 대출', '저소득층을 위한 생활안정자금 대출입니다.', 3.5, 1000, 19, 100, 0, 350, 100.0, '신분증, 소득증빙서류', 0);
INSERT INTO products VALUES (32, '긴급생계비 대출', '긴급한 생계비가 필요한 분을 위한 대출입니다.', 4.0, 300, 19, 100, 0, 300, 100.0, '신분증', 0);
INSERT INTO products VALUES (33, '주택담보대출', '주택을 담보로 한 대출입니다. 은행원이 등기부등본 확인 및 담보가치를 평가합니다.', 3.5, 50000, 19, 100, 0, 600, 100.0, '신분증, 등기부등본, 소득증빙서류', 1);
INSERT INTO products VALUES (34, '전세자금대출', '전세 계약을 위한 대출입니다. 은행원이 전세계약서 확인 및 임대인 신원을 확인합니다.', 2.8, 30000, 19, 100, 0, 650, 100.0, '신분증, 전세계약서, 등기부등본, 소득증빙서류', 1);
INSERT INTO products VALUES (35, '주택구입자금 대출', '주택 구입을 위한 대출입니다. 은행원이 매매계약서 확인 및 등기 절차를 검토합니다.', 3.2, 50000, 19, 100, 0, 650, 100.0, '신분증, 매매계약서, 등기부등본, 소득증빙서류', 1);
INSERT INTO products VALUES (36, '자동차담보대출', '자동차를 담보로 한 대출입니다. 은행원이 차량등록증 확인 및 차량가치를 평가합니다.', 6.5, 5000, 19, 100, 0, 600, 100.0, '신분증, 차량등록증, 소득증빙서류', 1);
INSERT INTO products VALUES (37, '사업자 대출', '사업자를 위한 운영자금 대출입니다. 은행원이 사업 안정성 및 매출을 평가합니다.', 4.5, 10000, 19, 100, 0, 600, 100.0, '신분증, 사업자등록증, 재무제표', 1);

-- applications 데이터 (6건)
INSERT INTO applications VALUES (1, 'C3DAB92E', 11, 2, '심사중', 0, '2026-04-17 18:09:23', NULL);
INSERT INTO applications VALUES (2, '86DCD0FE', 12, 1, '심사중', 0, '2026-04-18 16:51:53', NULL);
INSERT INTO applications VALUES (3, 'B601AE71', 13, 1, '심사중', 0, '2026-04-18 16:53:28', NULL);
INSERT INTO applications VALUES (4, 'APP89884', 1, 1, '심사중', 0, '2024-05-10 14:30:00', NULL);
INSERT INTO applications VALUES (5, 'APP49152', 1, 2, '승인', 0, '2024-05-05 10:15:00', NULL);
INSERT INTO applications VALUES (6, 'APP86483', 1, 3, '신청중', 0, '2024-05-12 09:00:00', NULL);


-- ============================================================
-- JOIN 예제
-- ============================================================

-- INNER JOIN 예제: 모든 신청 내역 조회
/*
SELECT 
    a.id,
    a.application_number,
    c.customer_name,
    c.customer_phone,
    p.product_name,
    p.product_interest_rate,
    a.application_status,
    a.application_submitted_at
FROM applications a
INNER JOIN customers c ON a.applicant_customer_id = c.id
INNER JOIN products p ON a.applied_product_id = p.id
ORDER BY a.application_submitted_at DESC;
*/

-- LEFT JOIN 예제: 모든 고객 (신청 여부 포함)
/*
SELECT 
    c.id,
    c.customer_name,
    c.customer_phone,
    COUNT(a.id) as application_count
FROM customers c
LEFT JOIN applications a ON c.id = a.applicant_customer_id
GROUP BY c.id, c.customer_name, c.customer_phone
ORDER BY application_count DESC;
*/

-- ============================================================
-- 완료!
-- ============================================================
