class RetentionConfig:
    def __init__(self, avg_lifetime, floor_months, margin_pct):
        self.avg_lifetime = avg_lifetime
        self.floor_months = floor_months
        self.margin_pct = margin_pct