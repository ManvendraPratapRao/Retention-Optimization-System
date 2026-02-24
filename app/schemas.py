from pydantic import BaseModel, Field, ConfigDict


# ==========================================
# Customer Features (Used ONLY for single prediction)
# ==========================================

class CustomerInput(BaseModel):
    """
    Features required by the ML pipeline.
    Extra fields (like gender, PhoneService, etc.)
    will be ignored automatically.
    """

    model_config = ConfigDict(extra="ignore")

    # -------- Numeric --------
    tenure: float = Field(..., ge=0)
    MonthlyCharges: float = Field(..., ge=0)

    # -------- Categorical --------
    SeniorCitizen: int
    Partner: str
    Dependents: str
    Contract: str
    PaymentMethod: str
    PaperlessBilling: str
    InternetService: str
    TechSupport: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    StreamingTV: str
    StreamingMovies: str


# ==========================================
# Business Configuration Schema
# ==========================================

class BusinessConfigSchema(BaseModel):
    """
    Economic assumptions for retention calculations.
    Used in both single and batch modes.
    """

    avg_lifetime: int = Field(36, ge=1)
    floor_months: int = Field(6, ge=0)

    margin_pct: float = Field(0.5, ge=0, le=1)
    retention_success_rate: float = Field(0.2, ge=0, le=1)

    contact_cost: float = Field(5.0, ge=0)
    incentive_cost: float = Field(20.0, ge=0)


# ==========================================
# Single Prediction Request
# ==========================================

class SingleRequest(BaseModel):
    """
    Strictly validated request for single customer prediction.
    """

    customer: CustomerInput
    business_config: BusinessConfigSchema
    include_explanation: bool = False