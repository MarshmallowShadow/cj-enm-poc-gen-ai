# CJ E&M Gen AI POC :books:

## Specifications :computer:
- Language: Python 3.12
- Framework: Django 5.0.6
- Frontend: HTML, CSS, JS
- Database: MySQL 8.0
- JS Libraries: Showdown, Jquery, Bootstrap, Ajax
- Others: Google Cloud Storage, Gemini API (Vertex AI)

## Required Environment Variables :key:
- **SECRET_KEY** (파이썬 시크릿 키)
- **BUCKET_NAME** (Google Cloud Storage 버킷 이름)
- **BLOB_PREFIX** (파일 저장 경로)
- **DB_NAME** (데이터베이스명)
- **DB_HOST** (데이터베이스 IP 주소)
- **DB_USER** (DB 사용자명)
- **DB_PASSWORD** (사용자 비밀번호)

## Libraries to Install :snake:
```shell
pip install django
pip install venv
pip install google-cloud-storage
pip install google-cloud-aiplatform
pip install mysqlclient
```
