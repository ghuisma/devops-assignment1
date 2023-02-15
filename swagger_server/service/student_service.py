import os
from pymongo import MongoClient, DESCENDING

mongo_uri = os.environ.get('MONGO_URI')
client = MongoClient(mongo_uri)
db = client.tutorial
students_collection = db.students


def add(student=None):
    # check if student already exists
    res = students_collection.find_one({
        "first_name": student.first_name,
        "last_name": student.last_name
    })
    if res:
        return 'already exists', 409
    # calculate student_id
    student_id = 1
    highest_student_id = students_collection.find_one(
        sort=[("student_id", DESCENDING)])
    if highest_student_id:
        student_id += highest_student_id["student_id"]
    # insert student into database
    students_collection.insert_one({
        "first_name": student.first_name,
        "last_name": student.last_name,
        "grade_records": list(map(lambda gradeRecord: gradeRecord.to_dict(), student.grade_records)),
        "student_id": student_id
    })
    return str(student_id)


def get_by_id(student_id=None, subject=None):
    student = students_collection.find_one(
        {"student_id": student_id}, {"_id": False})
    if not student:
        return 'not found', 404
    return student


def delete(student_id=None):
    result = students_collection.delete_one({"student_id": student_id})
    if result.deleted_count != 1:
        return 'not found', 404
    return student_id
