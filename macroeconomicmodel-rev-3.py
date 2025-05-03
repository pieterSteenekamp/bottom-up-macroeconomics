import mesa
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tqdm import tqdm
import random
import os
import csv

class ConfigManager:
    def __init__(self, config_dir="config"):
        self.config_dir = config_dir
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        self.country_params_file = os.path.join(config_dir, "country_parameters.csv")
        self.citizen_params_file = os.path.join(config_dir, "citizen_parameters.csv")
        self.business_params_file = os.path.join(config_dir, "business_parameters.csv")    
    def generate_template_files(self):
        self._generate_country_params_template()
        self._generate_citizen_params_template()
        self._generate_business_params_template()
    def _generate_country_params_template(self):
        countries = [
            {
                "country_id": 1,
                "name": "Developed Country",
                # Fixed parameters
                "development_level": 0.9,
                "wealth_level": 0.85,
                "homogeneity": 0.7,
                # Government actionable properties
                "tax_rate": 0.35,
                "interest_rate": 0.02,
                "social_services_spending": 0.4,
                "immigration_incentives": 0.05,
                # Import duty parameters
                "import_duty_rate": 0.1,
                # External properties
                "external_influences": 50
            },
            {
                "country_id": 3,
                "name": "Developing Country",
                # Fixed parameters
                "development_level": 0.3,
                "wealth_level": 0.2,
                "homogeneity": 0.9,
                # Government actionable properties
                "tax_rate": 0.15,
                "interest_rate": 0.08,
                "social_services_spending": 0.25,
                "immigration_incentives": 0.08,
                # Import duty parameters
                "import_duty_rate": 0.25,
                # External properties
                "external_influences": -30
            }
        ]
        df = pd.DataFrame(countries)
        df.to_csv(self.country_params_file, index=False)    
    def _generate_citizen_params_template(self):
        params = [
            {
                "development_level": "high",  # Development level > 0.7
                "min_salary": 60,
                "max_salary": 120,
                "expertise_low_pct": 0.1,
                "expertise_medium_pct": 0.3,
                "expertise_high_pct": 0.4,
                "expertise_expert_pct": 0.2,
                "min_savings": 50,
                "max_savings": 200,
                "min_values_social_services": 0.3,
                "max_values_social_services": 0.8,
                "min_values_economic_freedom": 0.4,
                "max_values_economic_freedom": 0.9,
                "min_trust_in_government": 0.4,
                "max_trust_in_government": 0.8,
                "min_import_goods_preference": 0.3,
                "max_import_goods_preference": 0.7,
                "min_import_price_sensitivity": 0.2,
                "max_import_price_sensitivity": 0.6,
                "min_inflation_sensitivity": 0.4,
                "max_inflation_sensitivity": 0.8,
                "initial_employment_rate": 0.95
            },
            {
                "development_level": "low",  # Development level < 0.4
                "min_salary": 20,
                "max_salary": 60,
                "expertise_low_pct": 0.4,
                "expertise_medium_pct": 0.4,
                "expertise_high_pct": 0.15,
                "expertise_expert_pct": 0.05,
                "min_savings": 5,
                "max_savings": 50,
                "min_values_social_services": 0.5,
                "max_values_social_services": 1.0,
                "min_values_economic_freedom": 0.2,
                "max_values_economic_freedom": 0.6,
                "min_trust_in_government": 0.1,
                "max_trust_in_government": 0.5,
                "min_import_goods_preference": 0.5,
                "max_import_goods_preference": 0.9,
                "min_import_price_sensitivity": 0.6,
                "max_import_price_sensitivity": 1.0,
                "min_inflation_sensitivity": 0.7,
                "max_inflation_sensitivity": 1.0,
                "initial_employment_rate": 0.6
            }
        ]
        df = pd.DataFrame(params)
        df.to_csv(self.citizen_params_file, index=False)    
    def _generate_business_params_template(self):
        params = [
            {
                "development_level": "high",  # Development level > 0.7
                "manufacturing_local_consumers_pct": 0.2,
                "manufacturing_local_businesses_pct": 0.15,
                "manufacturing_export_pct": 0.25,
                "import_citizens_consumers_pct": 0.15,
                "import_business_customers_pct": 0.1,
                "ai_pct": 0.15,
                "min_automation_level": 0.4,
                "max_automation_level": 0.9,
                "min_size_factor": 0.8,
                "max_size_factor": 2.5,
                "min_investment_rate": 0.2,
                "max_investment_rate": 0.5,
                "min_interest_rate_sensitivity": 0.7,
                "max_interest_rate_sensitivity": 1.2
            },
            {
                "development_level": "low",  # Development level < 0.4
                "manufacturing_local_consumers_pct": 0.3,
                "manufacturing_local_businesses_pct": 0.25,
                "manufacturing_export_pct": 0.15,
                "import_citizens_consumers_pct": 0.2,
                "import_business_customers_pct": 0.1,
                "ai_pct": 0.0,
                "min_automation_level": 0.1,
                "max_automation_level": 0.5,
                "min_size_factor": 0.4,
                "max_size_factor": 1.5,
                "min_investment_rate": 0.1,
                "max_investment_rate": 0.3,
                "min_interest_rate_sensitivity": 0.9,
                "max_interest_rate_sensitivity": 1.5
            }
        ]
        df = pd.DataFrame(params)
        df.to_csv(self.business_params_file, index=False)    
    def load_country_parameters(self):
        if not os.path.exists(self.country_params_file):
            print(f"Country parameters file not found: {self.country_params_file}")
            print("Generating template files...")
            self.generate_template_files()        
        try:
            df = pd.read_csv(self.country_params_file)
            return df.to_dict('records')
        except Exception as e:
            print(f"Error loading country parameters: {e}")
            return None    
    def load_citizen_parameters(self):
        if not os.path.exists(self.citizen_params_file):
            print(f"Citizen parameters file not found: {self.citizen_params_file}")
            print("Generating template files...")
            self.generate_template_files()        
        try:
            df = pd.read_csv(self.citizen_params_file)
            return {row["development_level"]: row.to_dict() for _, row in df.iterrows()}
        except Exception as e:
            print(f"Error loading citizen parameters: {e}")
            return None
    def load_business_parameters(self):
        if not os.path.exists(self.business_params_file):
            print(f"Business parameters file not found: {self.business_params_file}")
            print("Generating template files...")
            self.generate_template_files()        
        try:
            df = pd.read_csv(self.business_params_file)
            return {row["development_level"]: row.to_dict() for _, row in df.iterrows()}
        except Exception as e:
            print(f"Error loading business parameters: {e}")
            return None
    def get_development_level_category(self, development_level):
        if development_level > 0.7:
            return "high"
        elif development_level > 0.4:
            return "medium"
        else:
            return "low"

class Country(mesa.Agent):
    def __init__(self, model, country_config=None):
        super().__init__(model)
        self.numberOfPersons = 100        
        if country_config:
            self.country_id = country_config.get("country_id", random.randint(1, 1000))
            self.name = country_config.get("name", f"Country {self.country_id}")
            self.homogeneity = country_config.get("homogeneity", self.random.uniform(0, 1))
            self.development_level = country_config.get("development_level", self.random.uniform(0.3, 1))
            self.wealth_level = country_config.get("wealth_level", self.random.uniform(0.2, 1))
            self.tax_rate = country_config.get("tax_rate", self.random.uniform(0.1, 0.4))
            self.interest_rate = country_config.get("interest_rate", self.random.uniform(0.01, 0.05))
            self.social_services_spending = country_config.get("social_services_spending", self.random.uniform(0.2, 0.5))
            self.immigration_incentives = country_config.get("immigration_incentives", self.random.uniform(0, 0.1))
            self.import_duty_rate = country_config.get("import_duty_rate", self.random.uniform(0.05, 0.25))
            self.external_influences = country_config.get("external_influences", self.random.randint(-100, 100))
        else:
            # Use random defaults (same as original code)
            self.homogeneity = self.random.uniform(0, 1)
            self.development_level = self.random.uniform(0.3, 1)
            self.wealth_level = self.random.uniform(0.2, 1)
            self.tax_rate = self.random.uniform(0.1, 0.4)
            self.interest_rate = self.random.uniform(0.01, 0.05)
            self.social_services_spending = self.random.uniform(0.2, 0.5)
            self.immigration_incentives = self.random.uniform(0, 0.1)
            self.import_duty_rate = self.random.uniform(0.05, 0.25)
            self.external_influences = self.random.randint(-100, 100)
        self.bonds_issued = 0
        self.import_duty_revenue = 0
        self.local_manufacturing_boost = 0
        self.inflation = self.random.uniform(0.01, 0.05)
        self.economic_growth = self.random.uniform(0.01, 0.03)
        self.tax_revenue = 0
        self.interest_payments = 0
        self.bond_interest_rate = self.interest_rate + 0.01
        self.gini_coefficient = self.random.uniform(0.2, 0.6)
        self.citizen_happiness = 0
        self.total_revenue = 0
        self.money_supply = self.random.uniform(800, 1200) * self.wealth_level * self.development_level
        self.money_velocity = self.random.uniform(1.5, 2.5)
        self.government_spending = 0
        self.central_bank_policy = self.random.uniform(-0.1, 0.1)
        self.citizens = []
        self.businesses = []
        self.agent_type = "Country"
    def update_external_factors(self):
        self.external_influences = max(-100, min(100, 
            self.external_influences + self.random.randint(-10, 10)))
        self.government_spending = (
            self.total_revenue * (1 - 0.1)  # Reserve 10% for other expenses
            + self.bonds_issued * 0.2  # Use some of the issued bonds
        )        
        money_supply_change = (
            (0.03 - self.interest_rate) * 100 +
            self.government_spending / 1000 +
            self.central_bank_policy * self.money_supply * 0.1 +
            self.economic_growth * self.money_supply * 0.5
        )
        self.money_supply = max(self.money_supply * 0.9, 
                               min(self.money_supply * 1.1, 
                                  self.money_supply + money_supply_change))
        
        policy_adjustment = (0.02 - self.inflation) * 0.1 + self.random.uniform(-0.03, 0.03)
        self.central_bank_policy = max(-0.2, min(0.2, self.central_bank_policy + policy_adjustment))
        interest_rate_change = (
            self.central_bank_policy * -0.1 +  # Negative correlation with central bank policy
            (self.inflation - 0.02) * 0.2 +  # Positive correlation with inflation
            self.random.uniform(-0.002, 0.002)  # Small random factor
        )
        self.interest_rate = max(0.005, min(0.12, self.interest_rate + interest_rate_change))
        theoretical_inflation = (
            (self.money_supply * self.money_velocity) / 
            (self.wealth_level * 1000 * (1 + self.economic_growth))
        ) - 1
        inflation_change = (theoretical_inflation - self.inflation) * 0.2 + (
            0.005 * (self.social_services_spending - 0.3) +  # Higher spending increases inflation
            0.01 * (self.interest_rate - 0.03) +  # Higher rates decrease inflation (now reversed)
            0.002 * (self.external_influences / 100) +  # External factors
            0.003 * self.import_duty_rate  # Import duties can increase inflation
        )
        self.inflation = max(0, min(0.2, self.inflation + inflation_change))
        self.local_manufacturing_boost = self.import_duty_rate * 2  # Simple linear relationship
        growth_change = (
            0.005 * (0.03 - self.interest_rate) +  # Lower rates increase growth
            0.002 * (self.external_influences / 100) +  # External factors
            0.003 * (0.3 - self.tax_rate) +  # Lower taxes increase growth
            0.004 * self.local_manufacturing_boost -  # Local manufacturing boost helps growth
            0.006 * self.import_duty_rate +  # But high import duties can hurt overall growth
            0.003 * (self.money_supply / 1000 - 1) -  # Moderate money supply growth helps
            0.01 * max(0, self.inflation - 0.03)  # High inflation hurts growth
        )
        self.economic_growth = max(-0.05, min(0.1, self.economic_growth + growth_change))
        self.tax_revenue = 0
        self.import_duty_revenue = 0
        for citizen in self.citizens:
            if citizen.employed:
                self.tax_revenue += citizen.salary * self.tax_rate
        
        for business in self.businesses:
            self.tax_revenue += business.tax_payable
            if business.business_type.startswith("import"):
                self.import_duty_revenue += business.revenue * self.import_duty_rate
        self.total_revenue = self.tax_revenue + self.import_duty_revenue
        self.bond_interest_rate = self.interest_rate + max(0.01, self.inflation * 0.5)
        self.interest_payments = self.bonds_issued * self.bond_interest_rate
        if self.citizens:
            self.citizen_happiness = sum(c.happiness for c in self.citizens) / len(self.citizens)
        else:
            self.citizen_happiness = 50  # Default value
        velocity_change = (
            self.economic_growth * 0.5 +  # Higher growth increases velocity
            (self.interest_rate - 0.03) * 0.2 +  # Higher interest rates increase velocity
            self.random.uniform(-0.05, 0.05)  # Random factor
        )
        self.money_velocity = max(1.2, min(3.0, self.money_velocity + velocity_change))
    def collect_statistics(self):
        print(f"Country statistics:")
        print(f"  Tax rate: {self.tax_rate:.2f}")
        print(f"  Import duty rate: {self.import_duty_rate:.2f}")
        print(f"  Interest rate: {self.interest_rate:.2f}")
        print(f"  Inflation: {self.inflation:.2f}")
        print(f"  Economic growth: {self.economic_growth:.2f}")
        print(f"  Tax revenue: {self.tax_revenue:.2f}")
        print(f"  Import duty revenue: {self.import_duty_revenue:.2f}")
        print(f"  Total government revenue: {self.total_revenue:.2f}")
        print(f"  Local manufacturing boost: {self.local_manufacturing_boost:.2f}")
        print(f"  Money supply: {self.money_supply:.2f}")
        print(f"  Money velocity: {self.money_velocity:.2f}")
        print(f"  Government spending: {self.government_spending:.2f}")
        print(f"  Central bank policy: {self.central_bank_policy:.2f}")
        print(f"  Citizen happiness: {self.citizen_happiness:.2f}")
        print(f"  Number of citizens: {len(self.citizens)}")
        print(f"  Number of businesses: {len(self.businesses)}")

class Citizen(mesa.Agent):
    def __init__(self, model, country=None, citizen_params=None):
        super().__init__(model)
        self.country = country
        development_level_category = "medium"
        params = None
        if country and citizen_params:
            dev_level = country.development_level
            if dev_level > 0.7:
                development_level_category = "high"
            elif dev_level > 0.4:
                development_level_category = "medium"
            else:
                development_level_category = "low"                
            if development_level_category in citizen_params:
                params = citizen_params[development_level_category]
        if params:
            self.salary = self.random.randint(
                int(params["min_salary"]), 
                int(params["max_salary"])
            )
            expertise_distribution = [
                params["expertise_low_pct"],
                params["expertise_medium_pct"],
                params["expertise_high_pct"],
                params["expertise_expert_pct"]
            ]
            expertise_levels = ["low", "medium", "high", "expert"]
            total = sum(expertise_distribution)
            expertise_distribution = [p/total for p in expertise_distribution]
            self.expertise = self.random.choices(
                expertise_levels, 
                weights=expertise_distribution, 
                k=1
            )[0]
            self.values_social_services = self.random.uniform(
                params["min_values_social_services"],
                params["max_values_social_services"]
            )
            self.values_economic_freedom = self.random.uniform(
                params["min_values_economic_freedom"],
                params["max_values_economic_freedom"]
            )
            self.trust_in_government = self.random.uniform(
                params["min_trust_in_government"], 
                params["max_trust_in_government"]
            )
            self.import_goods_preference = self.random.uniform(
                params["min_import_goods_preference"],
                params["max_import_goods_preference"]
            )
            self.import_price_sensitivity = self.random.uniform(
                params["min_import_price_sensitivity"],
                params["max_import_price_sensitivity"]
            )
            self.inflation_sensitivity = self.random.uniform(
                params["min_inflation_sensitivity"],
                params["max_inflation_sensitivity"]
            )
            self.savings = self.random.uniform(
                params["min_savings"],
                params["max_savings"]
            )
            self.employed = self.random.random() < params["initial_employment_rate"]
        else:
            # Use default values as in original code
            self.salary = self.random.randint(40, 60)
            self.expertise = self.random.choice(["low", "medium", "high", "expert"])
            self.values_social_services = self.random.uniform(0, 1)
            self.values_economic_freedom = self.random.uniform(0, 1)
            self.trust_in_government = self.random.uniform(0, 1)
            self.import_goods_preference = self.random.uniform(0.2, 0.8)
            self.import_price_sensitivity = self.random.uniform(0.3, 1.0)
            self.inflation_sensitivity = self.random.uniform(0.3, 1.0)
            self.savings = self.random.uniform(10, 100)
            self.employed = self.random.random() < 0.8
        self.happiness = self.random.randint(40, 60)
        self.employer = None
        self.employment_matches_expertise = False
        self.agent_type = "Citizen"
    def seek_employment(self):
        if self.country is None or self.employed:
            return
        available_businesses = [b for b in self.country.businesses if b.has_openings()]
        if available_businesses:
            if self.country.local_manufacturing_boost > 0.1:
                local_manufacturing = [b for b in available_businesses if b.business_type.startswith("manufacturing")]
                if local_manufacturing:
                    available_businesses = local_manufacturing
            potential_employer = self.random.choice(available_businesses)
            hired = potential_employer.hire_employee(self)
            if hired:
                self.employed = True
                self.employer = potential_employer
                if self.expertise == "expert" and potential_employer.expert_employees > 0:
                    self.employment_matches_expertise = True
                elif self.expertise == "high" and potential_employer.white_collar_employees > 0:
                    self.employment_matches_expertise = True
                elif self.expertise in ["medium", "low"] and potential_employer.blue_collar_employees > 0:
                    self.employment_matches_expertise = True
    def update_happiness(self):
        if self.country is None:
            return            
        economic_factor = 0
        if self.employed:
            economic_factor = min(100, self.salary * (1 - self.country.tax_rate))
        else:
            economic_factor = min(50, self.country.social_services_spending * 100)        
        social_services_satisfaction = (
            self.values_social_services * self.country.social_services_spending * 100
        )
        economic_freedom_satisfaction = (
            self.values_economic_freedom * (1 - self.country.tax_rate) * 100
        )
        trust_factor = self.trust_in_government * 20        
        import_price_impact = -self.import_goods_preference * self.import_price_sensitivity * self.country.import_duty_rate * 100
        employment_opportunity_impact = 0
        if not self.employed:
            employment_opportunity_impact = self.country.local_manufacturing_boost * 20
        else:
            employment_opportunity_impact = self.country.local_manufacturing_boost * 5
        inflation_impact = -self.inflation_sensitivity * self.country.inflation * 200
        interest_impact = self.country.interest_rate * self.savings * 0.2
        new_happiness = (
            0.30 * economic_factor +
            0.15 * social_services_satisfaction +
            0.15 * economic_freedom_satisfaction +
            0.08 * trust_factor +
            0.08 * import_price_impact +
            0.08 * employment_opportunity_impact +
            0.08 * inflation_impact +  # NEW
            0.05 * interest_impact +   # NEW
            0.03 * self.random.uniform(-10, 10)  # Random factor
        )
        self.happiness = 0.7 * self.happiness + 0.3 * new_happiness
        self.happiness = max(0, min(100, self.happiness))
        if self.employed:
            savings_change = (
                self.salary * 0.1 +  # Save 10% of salary
                self.savings * self.country.interest_rate -  # Interest earned
                self.savings * self.country.inflation      # Eroded by inflation
            )
            self.savings = max(0, self.savings + savings_change)
        else:
            # Unemployed citizens spend savings
            self.savings = max(0, self.savings * (1 - self.country.inflation - 0.05))

class Business(mesa.Agent):
    def __init__(self, model, country=None, business_params=None):
        super().__init__(model)
        self.country = country
        development_level_category = "medium"
        params = None
        if country and business_params:
            dev_level = country.development_level
            if dev_level > 0.7:
                development_level_category = "high"
            elif dev_level > 0.4:
                development_level_category = "medium"
            else:
                development_level_category = "low"
                
            if development_level_category in business_params:
                params = business_params[development_level_category]
        if params:
            business_types = [
                "manufacturing_local_consumers",
                "manufacturing_local_businesses",
                "manufacturing_export",
                "import_citizens_consumers",
                "import_business_customers",
                "ai"
            ]
            business_weights = [
                params["manufacturing_local_consumers_pct"],
                params["manufacturing_local_businesses_pct"],
                params["manufacturing_export_pct"],
                params["import_citizens_consumers_pct"],
                params["import_business_customers_pct"],
                params["ai_pct"]
            ]
            total = sum(business_weights)
            business_weights = [w/total for w in business_weights]
            self.business_type = self.random.choices(
                business_types, 
                weights=business_weights, 
                k=1
            )[0]
            self.automation_level = self.random.uniform(
                params["min_automation_level"],
                params["max_automation_level"]
            )
            self.size_factor = self.random.uniform(
                params["min_size_factor"],
                params["max_size_factor"]
            )
            self.investment_rate = self.random.uniform(
                params["min_investment_rate"],
                params["max_investment_rate"]
            )
            self.interest_rate_sensitivity = self.random.uniform(
                params["min_interest_rate_sensitivity"],
                params["max_interest_rate_sensitivity"]
            )
        else:
            self.business_type = self.random.choice([
                "manufacturing_local_consumers",
                "manufacturing_local_businesses",
                "manufacturing_export",
                "import_citizens_consumers",
                "import_business_customers",
                "ai"
            ])
            self.automation_level = self.random.uniform(0.1, 0.9)
            self.size_factor = self.random.uniform(0.5, 2.0)
            self.investment_rate = self.random.uniform(0.1, 0.4)
            self.interest_rate_sensitivity = self.random.uniform(0.5, 1.5)
        self.blue_collar_employees = 0
        self.white_collar_employees = 0
        self.expert_employees = 0
        self.revenue = 0
        self.costs = 0
        self.profit = 0
        self.tax_payable = 0
        self.import_duty_payable = 0
        self.borrowing = 0
        self.employees = []
        self.max_employees = int(10 * self.size_factor)
        if self.business_type == "ai":
            self.max_employees = int(2 * self.size_factor)  # AI businesses need fewer employees
        self.agent_type = "Business"
    def update_business(self):
        if self.country is None:
            return
        base_revenue_factor = 1.0
        if self.business_type.startswith("manufacturing"):
            base_revenue_factor += self.country.economic_growth * 2
            # Local manufacturing gets a boost from import duties
            base_revenue_factor += self.country.local_manufacturing_boost            
            if self.business_type == "manufacturing_export":
                base_revenue_factor += self.country.external_influences / 200  # External influences affect exports        
        elif self.business_type.startswith("import"):
            base_revenue_factor += self.country.economic_growth
            base_revenue_factor -= self.country.import_duty_rate * 2
            base_revenue_factor -= self.country.external_influences / 300  # External influences can affect imports        
        elif self.business_type == "ai":
            base_revenue_factor += self.country.economic_growth * 3  # AI businesses benefit more from growth
            base_revenue_factor += self.country.development_level * 0.5  # More developed countries have better AI businesses
        money_supply_effect = (self.country.money_supply / 1000) * 0.2
        base_revenue_factor += money_supply_effect
        interest_rate_effect = (0.05 - self.country.interest_rate) * self.interest_rate_sensitivity
        base_revenue_factor += interest_rate_effect
        employee_factor = len(self.employees) / max(1, self.max_employees)
        self.revenue = 100 * self.size_factor * base_revenue_factor * (0.5 + 0.5 * employee_factor)
        employee_costs = sum(employee.salary for employee in self.employees)
        operating_costs = 20 * self.size_factor * (1 - 0.5 * self.automation_level)
        interest_costs = self.borrowing * self.country.interest_rate
        import_duty_costs = 0
        if self.business_type.startswith("import"):
            import_duty_costs = self.revenue * self.country.import_duty_rate
            self.import_duty_payable = import_duty_costs
        inflation_cost_increase = operating_costs * self.country.inflation * 2        
        self.costs = employee_costs + operating_costs + import_duty_costs + interest_costs + inflation_cost_increase
        self.profit = self.revenue - self.costs
        if self.profit > 0:
            self.tax_payable = self.profit * self.country.tax_rate
        else:
            self.tax_payable = 0
        if self.country.interest_rate < 0.04 and self.profit > 0:
            new_borrowing = self.revenue * 0.1 * (1 - self.country.interest_rate * 10)
            self.borrowing += new_borrowing
        else:
            self.borrowing = max(0, self.borrowing * 0.95)
        size_change_factor = 0
        if self.profit > 50 * self.size_factor and len(self.employees) >= self.max_employees * 0.9:
            size_change_factor = 0.1
        elif self.profit < -20 * self.size_factor:
            size_change_factor = -0.1
        interest_expansion_factor = (0.05 - self.country.interest_rate) * self.interest_rate_sensitivity * 0.5
        size_change_factor += interest_expansion_factor
        if size_change_factor > 0:
            self.max_employees = min(100, int(self.max_employees * (1 + size_change_factor)))
        elif size_change_factor < 0:
            self.max_employees = max(1, int(self.max_employees * (1 + size_change_factor)))
            while len(self.employees) > self.max_employees:
                employee = self.random.choice(self.employees)
                employee.employed = False
                employee.employer = None
                self.employees.remove(employee)    
    def has_openings(self):
        return len(self.employees) < self.max_employees
    
    def hire_employee(self, citizen):
        if not self.has_openings():
            return False
        self.employees.append(citizen)
        if citizen.expertise == "expert":
            self.expert_employees += 1
            citizen.salary = self.random.randint(80, 100)
        elif citizen.expertise == "high":
            self.white_collar_employees += 1
            citizen.salary = self.random.randint(60, 80)
        else:  # "medium" or "low"
            self.blue_collar_employees += 1
            citizen.salary = self.random.randint(40, 60)            
        return True

class EconomicModel(mesa.Model):
    def __init__(self, config_manager=None, num_countries=1, citizens_per_country=100, 
                 businesses_per_country=10, policy_params=None):
        super().__init__()
        self.config_manager = config_manager
        country_configs = None
        citizen_params = None
        business_params = None
        if self.config_manager:
            country_configs = self.config_manager.load_country_parameters()
            citizen_params = self.config_manager.load_citizen_parameters()
            business_params = self.config_manager.load_business_parameters()
        
        self.num_countries = num_countries
        self.citizens_per_country = citizens_per_country
        self.businesses_per_country = businesses_per_country
        self.countries = []
        self.data = {
            'inflation': [[] for _ in range(self.num_countries)],
            'economic_growth': [[] for _ in range(self.num_countries)],
            'tax_revenue': [[] for _ in range(self.num_countries)],
            'import_duty_revenue': [[] for _ in range(self.num_countries)],
            'total_revenue': [[] for _ in range(self.num_countries)],
            'citizen_happiness': [[] for _ in range(self.num_countries)],
            'local_manufacturing_boost': [[] for _ in range(self.num_countries)],
            'money_supply': [[] for _ in range(self.num_countries)],
            'interest_rate': [[] for _ in range(self.num_countries)],
            'central_bank_policy': [[] for _ in range(self.num_countries)],
            'government_spending': [[] for _ in range(self.num_countries)]  # NEW
        }
        
        # Use rich country configuration (development_level > 0.7)
        country_config = {
            "country_id": 1,
            "name": "Rich Country",
            "development_level": 0.9,
            "wealth_level": 0.85,
            "homogeneity": 0.7,
            "tax_rate": policy_params.get("tax_rate", 0.35) if policy_params else 0.35,
            "interest_rate": policy_params.get("interest_rate", 0.02) if policy_params else 0.02,
            "social_services_spending": policy_params.get("social_services_spending", 0.4) if policy_params else 0.4,
            "immigration_incentives": policy_params.get("immigration_incentives", 0.05) if policy_params else 0.05,
            "import_duty_rate": policy_params.get("import_duty_rate", 0.1) if policy_params else 0.1,
            "external_influences": 50
        }
        country = Country(self, country_config)
        self.countries.append(country)
        
        for country in self.countries:
            dev_level_category = self.config_manager.get_development_level_category(country.development_level) if self.config_manager else None
            for _ in range(self.citizens_per_country):
                citizen = Citizen(self, country, citizen_params)
                country.citizens.append(citizen)
            for _ in range(self.businesses_per_country):
                business = Business(self, country, business_params)
                country.businesses.append(business)
        
        print(f"Created {len(self.countries)} countries with {self.citizens_per_country} citizens and {self.businesses_per_country} businesses each")

    def step(self):
        for country in self.countries:
            for business in country.businesses:
                business.update_business()
        for country in self.countries:
            for citizen in country.citizens:
                citizen.seek_employment()
                citizen.update_happiness()
        for i, country in enumerate(self.countries):
            country.update_external_factors()
            self.data['inflation'][i].append(country.inflation)
            self.data['economic_growth'][i].append(country.economic_growth)
            self.data['tax_revenue'][i].append(country.tax_revenue)
            self.data['import_duty_revenue'][i].append(country.import_duty_revenue)
            self.data['total_revenue'][i].append(country.total_revenue)
            self.data['citizen_happiness'][i].append(country.citizen_happiness)
            self.data['local_manufacturing_boost'][i].append(country.local_manufacturing_boost)
            self.data['money_supply'][i].append(country.money_supply)
            self.data['interest_rate'][i].append(country.interest_rate)
            self.data['central_bank_policy'][i].append(country.central_bank_policy)
            self.data['government_spending'][i].append(country.government_spending)  # NEW

    def collect_statistics(self):
        for i, country in enumerate(self.countries):
            print(f"\nCountry {i+1}:")
            country.collect_statistics()

def run_multiple_simulations(num_runs=10, num_countries=2, duty_rates=None, steps=20):
    all_results = []    
    if duty_rates is None:
        duty_rates = np.linspace(0.0, 0.5, 6)  # 0%, 10%, 20%, 30%, 40%, 50%
    pbar = tqdm(total=num_runs * len(duty_rates), desc="Running simulations")
    for duty_rate in duty_rates:
        duty_results = []
        for _ in range(num_runs):
            model = EconomicModel(
                num_countries=num_countries, 
                citizens_per_country=100, 
                businesses_per_country=10,
                import_duty_rates=[duty_rate] * num_countries
            )
            for _ in range(steps):
                model.step()
            avg_happiness = np.mean([np.mean(model.data['citizen_happiness'][i][-5:]) for i in range(num_countries)])
            avg_growth = np.mean([np.mean(model.data['economic_growth'][i][-5:]) for i in range(num_countries)])
            avg_revenue = np.mean([np.mean(model.data['total_revenue'][i][-5:]) for i in range(num_countries)])
            avg_inflation = np.mean([np.mean(model.data['inflation'][i][-5:]) for i in range(num_countries)])
            avg_money_supply = np.mean([np.mean(model.data['money_supply'][i][-5:]) for i in range(num_countries)])
            avg_interest_rate = np.mean([np.mean(model.data['interest_rate'][i][-5:]) for i in range(num_countries)])            
            duty_results.append({
                'duty_rate': duty_rate,
                'avg_happiness': avg_happiness,
                'avg_growth': avg_growth,
                'avg_revenue': avg_revenue,
                'avg_inflation': avg_inflation,
                'avg_money_supply': avg_money_supply,
                'avg_interest_rate': avg_interest_rate
            })
            pbar.update(1)        
        all_results.extend(duty_results)    
    pbar.close()
    df = pd.DataFrame(all_results)
    grouped = df.groupby('duty_rate').mean().reset_index()
    return grouped

def run_monetary_policy_analysis(base_duty_rate=0.2, interest_rates=None, num_runs=5):
    all_results = []    
    if interest_rates is None:
        # Default set of interest rates to test
        interest_rates = np.linspace(0.01, 0.10, 5)  # 1% to 10%
    pbar = tqdm(total=num_runs * len(interest_rates), desc="Running monetary policy simulations")
    for interest_rate in interest_rates:
        rate_results = []
        for _ in range(num_runs):
            model = EconomicModel(
                num_countries=1,  # For simplicity
                citizens_per_country=100, 
                businesses_per_country=10,
                import_duty_rates=[base_duty_rate]
            )
            model.countries[0].interest_rate = interest_rate
            for _ in range(20):
                model.step()
            avg_happiness = np.mean(model.data['citizen_happiness'][0][-5:])
            avg_growth = np.mean(model.data['economic_growth'][0][-5:])
            avg_inflation = np.mean(model.data['inflation'][0][-5:])
            avg_money_supply = np.mean(model.data['money_supply'][0][-5:])            
            rate_results.append({
                'interest_rate': interest_rate,
                'avg_happiness': avg_happiness,
                'avg_growth': avg_growth,
                'avg_inflation': avg_inflation,
                'avg_money_supply': avg_money_supply
            })            
            pbar.update(1)        
        all_results.extend(rate_results)    
    pbar.close()
    df = pd.DataFrame(all_results)
    grouped = df.groupby('interest_rate').mean().reset_index()
    return grouped

def run_sensitivity_analysis(base_duty_rate=0.2, variation=0.1, num_runs=5):
    """Run a sensitivity analysis by varying import duty rates."""
    # Create a range of duty rates around the base rate
    duty_rates = np.linspace(max(0, base_duty_rate - variation), 
                            min(1, base_duty_rate + variation), 
                            5)
    results = run_multiple_simulations(num_runs=num_runs, duty_rates=duty_rates)
    return results

def balance_budget(model, policy_params, max_iterations=10, tolerance=0.1):
    """
    Adjust policy parameters to ensure government spending is within tolerance of revenue.
    Tolerance is a fraction (e.g., 0.1 for ±10%).
    """
    country = model.countries[0]
    for iteration in range(max_iterations):
        # Run a short simulation to estimate revenue and spending
        model = EconomicModel(
            config_manager=model.config_manager,
            num_countries=1,
            citizens_per_country=model.citizens_per_country,
            businesses_per_country=model.businesses_per_country,
            policy_params=policy_params
        )
        for _ in range(5):  # Short simulation to stabilize
            model.step()
        
        avg_revenue = np.mean(model.data['total_revenue'][0][-3:])
        avg_spending = np.mean(model.data['government_spending'][0][-3:])
        
        # Check if budget is balanced within tolerance
        if abs(avg_spending - avg_revenue) / avg_revenue <= tolerance:
            return policy_params, avg_revenue, avg_spending
        
        # Adjust parameters to balance budget
        deficit = avg_spending - avg_revenue
        if deficit > 0:
            # Reduce spending or increase revenue
            if policy_params['social_services_spending'] > 0.2:
                policy_params['social_services_spending'] = max(0.2, policy_params['social_services_spending'] - 0.05)
            elif policy_params['tax_rate'] < 0.5:
                policy_params['tax_rate'] = min(0.5, policy_params['tax_rate'] + 0.05)
            elif policy_params['import_duty_rate'] < 0.3:
                policy_params['import_duty_rate'] = min(0.3, policy_params['import_duty_rate'] + 0.05)
        else:
            # Increase spending or reduce revenue
            if policy_params['social_services_spending'] < 0.6:
                policy_params['social_services_spending'] = min(0.6, policy_params['social_services_spending'] + 0.05)
            elif policy_params['tax_rate'] > 0.2:
                policy_params['tax_rate'] = max(0.2, policy_params['tax_rate'] - 0.05)
            elif policy_params['import_duty_rate'] > 0.05:
                policy_params['import_duty_rate'] = max(0.05, policy_params['import_duty_rate'] - 0.05)
    
    # If max iterations reached, return best effort
    return policy_params, avg_revenue, avg_spending

def run_policy_combinations(num_runs=5, steps=20, output_file="policy_results.csv"):
    config_manager = ConfigManager(config_dir="my_config")
    
    # Define ranges for policy parameters
    tax_rates = np.linspace(0.2, 0.5, 4)  # 20% to 50%
    interest_rates = np.linspace(0.01, 0.05, 3)  # 1% to 5%
    social_services_spendings = np.linspace(0.2, 0.6, 3)  # 20% to 60%
    immigration_incentives = np.linspace(0.0, 0.1, 3)  # 0% to 10%
    import_duty_rates = np.linspace(0.05, 0.3, 3)  # 5% to 30%
    
    all_results = []
    pbar = tqdm(total=num_runs * len(tax_rates) * len(interest_rates) * 
                len(social_services_spendings) * len(immigration_incentives) * 
                len(import_duty_rates), desc="Running policy simulations")
    
    for tax_rate in tax_rates:
        for interest_rate in interest_rates:
            for social_spending in social_services_spendings:
                for immigration_incentive in immigration_incentives:
                    for import_duty_rate in import_duty_rates:
                        policy_params = {
                            'tax_rate': tax_rate,
                            'interest_rate': interest_rate,
                            'social_services_spending': social_spending,
                            'immigration_incentives': immigration_incentive,
                            'import_duty_rate': import_duty_rate
                        }
                        
                        for _ in range(num_runs):
                            # Balance the budget for this policy combination
                            balanced_params, avg_revenue, avg_spending = balance_budget(
                                EconomicModel(config_manager=config_manager),
                                policy_params.copy()
                            )
                            
                            # Run full simulation with balanced parameters
                            model = EconomicModel(
                                config_manager=config_manager,
                                num_countries=1,
                                citizens_per_country=100,
                                businesses_per_country=10,
                                policy_params=balanced_params
                            )
                            for _ in range(steps):
                                model.step()
                            
                            # Collect results (average of last 5 steps for stability)
                            result = {
                                'tax_rate': balanced_params['tax_rate'],
                                'interest_rate': balanced_params['interest_rate'],
                                'social_services_spending': balanced_params['social_services_spending'],
                                'immigration_incentives': balanced_params['immigration_incentives'],
                                'import_duty_rate': balanced_params['import_duty_rate'],
                                'avg_happiness': np.mean(model.data['citizen_happiness'][0][-5:]),
                                'avg_growth': np.mean(model.data['economic_growth'][0][-5:]),
                                'avg_revenue': np.mean(model.data['total_revenue'][0][-5:]),
                                'avg_spending': np.mean(model.data['government_spending'][0][-5:]),
                                'avg_inflation': np.mean(model.data['inflation'][0][-5:]),
                                'avg_money_supply': np.mean(model.data['money_supply'][0][-5:])
                            }
                            all_results.append(result)
                            pbar.update(1)
    
    pbar.close()
    
    # Save results to CSV
    df = pd.DataFrame(all_results)
    df.to_csv(output_file, index=False)
    print(f"Results saved to {output_file}")
    
    # Return grouped results for analysis
    grouped = df.groupby(['tax_rate', 'interest_rate', 'social_services_spending', 
                         'immigration_incentives', 'import_duty_rate']).mean().reset_index()
    return grouped

if __name__ == "__main__":
    config_manager = ConfigManager(config_dir="my_config")
    choice = input("Enter 1 if you wish to create template csv configuration files, 2 if not: ")
    if choice == "1":
        config_manager.generate_template_files()
    
    print("\nRunning policy combinations analysis...")
    results = run_policy_combinations(num_runs=3, steps=20, output_file="policy_results.csv")
    
    print("\nSimulation complete!")
    print("\nSummary of Results:")
    print(results[['tax_rate', 'interest_rate', 'social_services_spending', 
                   'immigration_incentives', 'import_duty_rate', 
                   'avg_happiness', 'avg_growth']])
