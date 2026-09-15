"""
╔════════════════════════════════════════════════════════════════════════════╗
║                     NEO CYBORG - ID GENERATOR FF                           ║
║                         ZACH CYBORG PROTOCOL v1.0                          ║
║                         Versi Nando | MT Manager                           ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

import uuid
import random
import string
import time
from datetime import datetime
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI(
    title="NEO CYBORG ID Generator FF",
    description="API ID Generator - Versi Nando | ZACH CYBORG Protocol",
    version="1.0.0"
)

# ═══════════════════════════════════════════════════════════════════════════
# MODELS
# ═══════════════════════════════════════════════════════════════════════════

class IDResponse(BaseModel):
    """Response model untuk single ID generation"""
    id: str
    type: str
    timestamp: str
    status: str

class BatchIDResponse(BaseModel):
    """Response model untuk batch ID generation"""
    ids: List[str]
    count: int
    type: str
    timestamp: str
    status: str

class ValidateResponse(BaseModel):
    """Response model untuk ID validation"""
    id: str
    valid: bool
    type: str
    message: str

# ═══════════════════════════════════════════════════════════════════════════
# ID GENERATORS
# ═══════════════════════════════════════════════════════════════════════════

class IDGeneratorFF:
    """
    ZACH CYBORG ID Generator Protocol
    - Supports: UUID, ULID, Custom Format
    """
    
    @staticmethod
    def generate_uuid() -> str:
        """Generate standard UUID v4"""
        return str(uuid.uuid4())
    
    @staticmethod
    def generate_ulid() -> str:
        """Generate ULID format (timestamp-based)"""
        timestamp = int(time.time() * 1000)
        random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
        return f"{timestamp:x}{random_part}"
    
    @staticmethod
    def generate_custom(prefix: str = "FF", length: int = 12) -> str:
        """Generate custom ID dengan prefix dan random string"""
        random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        return f"{prefix}-{int(time.time())}-{random_part}"
    
    @staticmethod
    def generate_sequential(start: int = 1000, end: int = 999999) -> str:
        """Generate sequential numeric ID"""
        return f"ID-{random.randint(start, end)}"

# ═══════════════════════════════════════════════════════════════════════════
# ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════

@app.get("/", tags=["Status"])
async def root():
    """Status check - ZACH CYBORG ONLINE"""
    return {
        "status": "ZACH CYBORG ONLINE",
        "message": "NEO CYBORG ID Generator FF Ready",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health", tags=["Status"])
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/generate/uuid", response_model=IDResponse, tags=["Generate"])
async def generate_uuid():
    """
    Generate UUID v4
    
    **Protocol**: Standard UUID Generation
    """
    try:
        generated_id = IDGeneratorFF.generate_uuid()
        return {
            "id": generated_id,
            "type": "uuid",
            "timestamp": datetime.now().isoformat(),
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate/ulid", response_model=IDResponse, tags=["Generate"])
async def generate_ulid():
    """
    Generate ULID (Time-based ID)
    
    **Protocol**: ULID Generation
    """
    try:
        generated_id = IDGeneratorFF.generate_ulid()
        return {
            "id": generated_id,
            "type": "ulid",
            "timestamp": datetime.now().isoformat(),
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate/custom", response_model=IDResponse, tags=["Generate"])
async def generate_custom(prefix: str = "FF", length: int = 12):
    """
    Generate Custom Format ID
    
    **Parameters**:
    - `prefix`: Custom prefix (default: FF)
    - `length`: Random string length (default: 12)
    
    **Protocol**: Custom Format Generation
    """
    try:
        if length < 1 or length > 32:
            raise ValueError("Length must be between 1-32")
        
        generated_id = IDGeneratorFF.generate_custom(prefix, length)
        return {
            "id": generated_id,
            "type": "custom",
            "timestamp": datetime.now().isoformat(),
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/generate/sequential", response_model=IDResponse, tags=["Generate"])
async def generate_sequential(start: int = 1000, end: int = 999999):
    """
    Generate Sequential Numeric ID
    
    **Parameters**:
    - `start`: Range start (default: 1000)
    - `end`: Range end (default: 999999)
    
    **Protocol**: Sequential Generation
    """
    try:
        if start >= end:
            raise ValueError("Start must be less than end")
        
        generated_id = IDGeneratorFF.generate_sequential(start, end)
        return {
            "id": generated_id,
            "type": "sequential",
            "timestamp": datetime.now().isoformat(),
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/generate/batch", response_model=BatchIDResponse, tags=["Generate"])
async def generate_batch(count: int = 10, id_type: str = "uuid"):
    """
    Generate Batch IDs
    
    **Parameters**:
    - `count`: Number of IDs to generate (max: 1000)
    - `id_type`: Type of ID (uuid, ulid, custom, sequential)
    
    **Protocol**: Batch Generation
    """
    try:
        if count < 1 or count > 1000:
            raise ValueError("Count must be between 1-1000")
        
        ids = []
        
        if id_type == "uuid":
            ids = [IDGeneratorFF.generate_uuid() for _ in range(count)]
        elif id_type == "ulid":
            ids = [IDGeneratorFF.generate_ulid() for _ in range(count)]
        elif id_type == "custom":
            ids = [IDGeneratorFF.generate_custom() for _ in range(count)]
        elif id_type == "sequential":
            ids = [IDGeneratorFF.generate_sequential() for _ in range(count)]
        else:
            raise ValueError(f"Unknown ID type: {id_type}")
        
        return {
            "ids": ids,
            "count": len(ids),
            "type": id_type,
            "timestamp": datetime.now().isoformat(),
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/validate", response_model=ValidateResponse, tags=["Validate"])
async def validate_id(id_value: str):
    """
    Validate ID Format
    
    **Parameters**:
    - `id_value`: ID string to validate
    
    **Protocol**: ID Validation
    """
    try:
        # UUID validation
        try:
            uuid.UUID(id_value)
            return {
                "id": id_value,
                "valid": True,
                "type": "uuid",
                "message": "Valid UUID format"
            }
        except ValueError:
            pass
        
        # ULID validation
        if len(id_value) == 24 and all(c in string.ascii_uppercase + string.digits for c in id_value):
            return {
                "id": id_value,
                "valid": True,
                "type": "ulid",
                "message": "Valid ULID format"
            }
        
        # Custom format validation
        if "-" in id_value and id_value.startswith("FF-"):
            return {
                "id": id_value,
                "valid": True,
                "type": "custom",
                "message": "Valid custom format"
            }
        
        # Sequential validation
        if id_value.startswith("ID-") and id_value[3:].isdigit():
            return {
                "id": id_value,
                "valid": True,
                "type": "sequential",
                "message": "Valid sequential format"
            }
        
        return {
            "id": id_value,
            "valid": False,
            "type": "unknown",
            "message": "ID format not recognized"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ═══════════════════════════════════════════════════════════════════════════
# RUN
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════════════════════════════╗
    ║                     NEO CYBORG - ID GENERATOR FF                           ║
    ║                         ZACH CYBORG PROTOCOL v1.0                          ║
    ║                     Versi Nando | MT Manager Online                        ║
    ╚════════════════════════════════════════════════════════════════════════════╝
    """)
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
