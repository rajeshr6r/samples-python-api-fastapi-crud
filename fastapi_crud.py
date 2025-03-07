from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Sample data (in-memory storage)
records = [
    {"id": 1, "name": "Record One", "value": 100},
    {"id": 2, "name": "Record Two", "value": 200},
    {"id": 3, "name": "Record Three", "value": 300},
]

class Record(BaseModel):
    id: int
    name: str
    value: int

class RecordUpdate(BaseModel):
    name: str | None = None
    value: int | None = None

@app.get("/records", response_model=list)
def get_records():
    """Get all records."""
    return records

@app.get("/records/{record_id}")
def get_record_by_id(record_id: int):
    """Get a record by its ID."""
    for record in records:
        if record["id"] == record_id:
            return record
    raise HTTPException(status_code=404, detail="Record not found")

@app.post("/records")
def create_record(new_record: Record):
    """Insert a new record."""
    for record in records:
        if record["id"] == new_record.id:
            raise HTTPException(status_code=400, detail="Record with this ID already exists")
    records.append(new_record.dict())
    return new_record

@app.put("/records/{record_id}")
def update_record(record_id: int, updated_record: RecordUpdate):
    """Update a record completely."""
    for record in records:
        if record["id"] == record_id:
            if updated_record.name is not None:
                record["name"] = updated_record.name
            if updated_record.value is not None:
                record["value"] = updated_record.value
            return record
    raise HTTPException(status_code=404, detail="Record not found")

@app.patch("/records/{record_id}")
def partial_update_record(record_id: int, updated_record: RecordUpdate):
    """Partially update a record."""
    for record in records:
        if record["id"] == record_id:
            if updated_record.name is not None:
                record["name"] = updated_record.name
            if updated_record.value is not None:
                record["value"] = updated_record.value
            return record
    raise HTTPException(status_code=404, detail="Record not found")

@app.delete("/records/{record_id}")
def delete_record(record_id: int):
    """Delete a record by its ID."""
    global records
    records = [record for record in records if record["id"] != record_id]
    return {"message": "Record deleted successfully"}
