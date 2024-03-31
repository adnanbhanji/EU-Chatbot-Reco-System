# Data Schema

## Overview

The database schema for the dairy farmers' carbon emission reporting project utilizes a relational model optimized for data collection through a WhatsApp chatbot and secure storage on Azure's cloud infrastructure. It includes key tables for managing user profiles, emission reports, and associated data to ensure comprehensive tracking and analysis of carbon emission data.

## Tables

### Table 1: Users

| Field          | Type          | Description                                         |
|----------------|---------------|-----------------------------------------------------|
| **FarmerID**   | `VARCHAR(255)` | Unique identifier for each farmer.                 |
| **Name**       | `VARCHAR(255)` | Farmer's full name.                                 |
| **WhatsAppNumber** | `VARCHAR(15)`  | Contact number used for WhatsApp communication.    |
| **FarmLocation**   | `VARCHAR(255)` | Geographical location of the farm.                 |
| **FarmSize**       | `DECIMAL`      | Size of the farm (e.g., in hectares).              |

### Table 2: Emission Report

| Field            | Type           | Description                                             |
|------------------|----------------|---------------------------------------------------------|
| **ReportID**     | `VARCHAR(255)` | Unique identifier for each emission report.            |
| **FarmerID**     | `VARCHAR(255)` | Links to Farmer Information.                           |
| **ReportDate**   | `DATE`         | Date when the report was submitted.                    |
| **EmissionType** | `VARCHAR(50)`  | Type of emission (e.g., methane, CO2).                 |
| **EmissionSource** | `VARCHAR(255)` | Source of emission within the farm (e.g., livestock, machinery). |
| **Quantity**       | `DECIMAL`      | Quantified emission (e.g., in kilograms of CO2 equivalent). |
| **CalculationMethod**| `VARCHAR(255)` | Method or model used for emission calculation |
