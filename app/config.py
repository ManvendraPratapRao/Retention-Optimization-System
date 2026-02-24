from pydantic import BaseModel

class BusinessConfig(BaseModel):
    """
    Business economic assumptions.
    All percentages are in decimal form (0.5 = 50%)
    """

    avg_lifetime: int = 36
    floor_months: int = 6
    margin_pct: float = 0.5
    retention_success_rate: float = 0.2

    contact_cost: float = 5.0
    incentive_cost: float = 20.0

    @property
    def retention_cost(self) -> float:
        return self.contact_cost + self.incentive_cost

    def validate_config(self):
        if self.avg_lifetime < self.floor_months:
            raise ValueError("avg_lifetime must be >= floor_months")

        if not 0 <= self.margin_pct <= 1:
            raise ValueError("margin_pct must be between 0 and 1")

        if not 0 <= self.retention_success_rate <= 1:
            raise ValueError("retention_success_rate must be between 0 and 1")

        if self.contact_cost < 0 or self.incentive_cost < 0:
            raise ValueError("Costs cannot be negative")