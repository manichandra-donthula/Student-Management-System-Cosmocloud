from fastapi import APIRouter, HTTPException, Query, Path
from bson import ObjectId
from .models import students_collection
from .schemas import StudentCreateModel, StudentUpdateModel

router = APIRouter()

# Utility function to format MongoDB document
def format_student(student):
    student["id"] = str(student["_id"])
    del student["_id"]
    return student

@router.post("/students", status_code=201)
async def create_student(student: StudentCreateModel):
    new_student = student.dict()
    result = await students_collection.insert_one(new_student)
    return {"id": str(result.inserted_id)}

@router.get("/students", status_code=200)
async def list_students(
    country: str | None = Query(default=None),
    age: int | None = Query(default=None),
):
    query = {}
    if country:
        query["address.country"] = country
    if age:
        query["age"] = {"$gte": age}
    students = await students_collection.find(query).to_list(100)
    return {"data": [format_student(student) for student in students]}

@router.get("/students/{id}", status_code=200)
async def fetch_student(id: str = Path(...)):
    student = await students_collection.find_one({"_id": ObjectId(id)})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return format_student(student)

@router.patch("/students/{id}", status_code=204)
async def update_student(id: str, student: StudentUpdateModel):
    update_data = {k: v for k, v in student.dict(exclude_unset=True).items()}
    result = await students_collection.update_one(
        {"_id": ObjectId(id)}, {"$set": update_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return

@router.delete("/students/{id}", status_code=200)
async def delete_student(id: str = Path(...)):
    result = await students_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"detail": "Student deleted successfully"}
