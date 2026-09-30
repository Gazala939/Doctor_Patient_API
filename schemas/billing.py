from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


class BillingCreate(BaseModel):

    patient_id: int = Field(gt=0)

    doctor_id: int = Field(gt=0)

    appointment_id: Optional[int] = Field(
        default=None,
        gt=0
    )

    consultation_fee: float = Field(
        ge=0
    )

    additional_charges: float = Field(
        default=0,
        ge=0
    )

    payment_status: Literal[
        "pending",
        "paid",
        "cancelled"
    ] = "pending"

    payment_mode: Optional[
        Literal[
            "cash",
            "card",
            "upi"
        ]
    ] = None


class BillingUpdate(BaseModel):

    consultation_fee: float = Field(
        ge=0
    )

    additional_charges: float = Field(
        default=0,
        ge=0
    )

    payment_status: Literal[
        "pending",
        "paid",
        "cancelled"
    ]

    payment_mode: Optional[
        Literal[
            "cash",
            "card",
            "upi"
        ]
    ] = None


class BillingPatch(BaseModel):

    consultation_fee: Optional[
        float
    ] = Field(
        default=None,
        ge=0
    )

    additional_charges: Optional[
        float
    ] = Field(
        default=None,
        ge=0
    )

    payment_status: Optional[
        Literal[
            "pending",
            "paid",
            "cancelled"
        ]
    ] = None

    payment_mode: Optional[
        Literal[
            "cash",
            "card",
            "upi"
        ]
    ] = None


class BillingResponse(BaseModel):

    id: int

    patient_id: int

    doctor_id: int

    appointment_id: Optional[int]

    consultation_fee: float

    additional_charges: float

    total_amount: float

    payment_status: str

    payment_mode: Optional[str]

    is_active: bool

    created_at: datetime

    updated_at: datetime

    class Config:
        from_attributes = True