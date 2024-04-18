import fastapi
import pandas as pd
from .model import DelayModel
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request
from pydantic import BaseModel, Field, validator
from typing import List

app = fastapi.FastAPI()
model = DelayModel()


class Flight(BaseModel):
    OPERA: str
    TIPOVUELO: str = Field(..., regex="^[IN]$",
                           description="Allowed values are 'I' or 'N'")
    MES: int = Field(..., ge=1, le=12,
                     description="Must be an integer between 1 and 12 (inclusive)")

    @validator("TIPOVUELO")
    def validate_TIPOVUELO(cls, v):
        if v not in ["N", "I"]:
            raise ValueError("Invalid flight type")
        return v

    @validator("MES")
    def validate_MES(cls, v):
        if v not in range(1, 13):
            raise ValueError("Invalid month")
        return v


class FlightList(BaseModel):
    flights: List[Flight]


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"detail": "Validation error", "errors": exc.errors()},
    )


@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {"status": "OK"}


@app.post("/predict", status_code=200)
async def post_predict(data: FlightList) -> dict:
    try:
        df = pd.DataFrame([flight.dict() for flight in data.flights])
        features = model.preprocess(df)
        predictions = model.predict(features)
        return {"predict": predictions}
    except Exception as e:
        return {"error": "An error occurred during prediction.", "detail": str(e)}
