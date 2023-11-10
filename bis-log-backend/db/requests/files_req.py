from sqlalchemy.orm import Session
from sqlalchemy.sql import text


def create_file_row(db: Session, filename: str, owner_id: int) -> int:
    sql_query = "INSERT INTO files (filename,owner_id) VALUES (:filename, :owner_id) RETURNING id"
    params = {"filename": filename, "owner_id": owner_id}
    result = db.execute(text(sql_query), params)
    created_id = result.scalar()
    db.commit()
    return created_id

def get_all_users_files(db: Session, owner_id: int) -> dict:
    sql_query = "SELECT * FROM files WHERE owner_id = :owner_id"
    params = {"owner_id": owner_id}
    result = db.execute(text(sql_query), params)
    files = result.fetchall()
    result = []
    for row in files:
        file_name = row[1].split("/")[1]
        curent_result = {"id":row[0],"file_name":file_name,"owner_id":row[2]}
        result.append(curent_result)
    return result


def check_owner_file(db: Session, filename: str, owner_id: int) -> bool:
    sql_query = "SELECT count(*) FROM files WHERE owner_id = :owner_id AND file_name = :filename"
    params = {"filename": filename, "owner_id": owner_id}
    result = db.execute(text(sql_query), params)
    return True if result.scalar() > 0 else False

def get_username(db: Session, user_id: int)-> str:
    sql_query = "SELECT username FROM users WHERE id = :user_id"
    params = {"user_id": user_id}
    result = db.execute(text(sql_query), params)
    username = result.fetchone()[0]
    return username