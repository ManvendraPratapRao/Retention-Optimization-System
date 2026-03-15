# Decision Engine: Economic Logic

This document details the mathematical framework used to translate Churn Probabilities ($P$) into Business Actions.

## The Objective Function
The goal of the engine is to maximize the **Expected Gain ($EG$)** from retention interventions.

$$EG = (P \times BRV \times Success\_Rate) - Intervention\_Cost$$

## Core Metrics

### 1. Base Remaining Value (BRV)
BRV represents the potential revenue lost if the customer churns today.
- **Formula**: `MonthlyCharges * Customer_Lifetime_Value_Factor`
- **Lifetime Factor**: Typically calculated as the average remaining months for a customer in that segment.

### 2. Intervention Cost
The total cost of the retention campaign for a specific customer.
- **Formula**: `ContactCost + (IncentiveCost * ParticipationRate)`

### 3. ROI (Return on Investment)
The efficiency of the retention spend.
- **Formula**: `ExpectedGain / InterventionCost`

## Decision Thresholds

| ROI Level | Action | Strategy |
| :--- | :--- | :--- |
| **> 2.0** | ✅ **High Priority** | Aggressive retention (e.g., direct call + heavy discount). |
| **1.0 - 2.0** | ⚠️ **Standard** | Automated retention (e.g., personalized email + bundle offer). |
| **< 1.0** | ❌ **Passive** | No intervention (Cost exceeds potential recovery value). |

## Implementation
The logic is isolated in `app/core/engine.py` to allow business analysts to adjust `margin_pct` or `incentive_cost` via environment variables or the Dashboard UI without requiring developer intervention.
