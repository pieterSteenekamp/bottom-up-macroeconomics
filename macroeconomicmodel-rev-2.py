import mesa
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import cm
import pandas as pd
from tqdm import tqdm

class Country(mesa.Agent):
    def __init__(self, model):
        super().__init__(model)
        self.numberOfPersons = 100
        
        # Government actionable properties
        self.tax_rate = self.random.uniform(0.1, 0.4)  # Tax rate between 10% and 40%
        self.interest_rate = self.random.uniform(0.01, 0.05)  # Interest rate between 1% and 5%
        self.bonds_issued = 0
        self.social_services_spending = self.random.uniform(0.2, 0.5)  # As a fraction of tax revenue
        self.immigration_incentives = self.random.uniform(0, 0.1)  # Scale from 0 to 0.1
        
        # New import duty parameters
        self.import_duty_rate = self.random.uniform(0.05, 0.25)  # Import duty rate between 5% and 25%
        self.import_duty_revenue = 0
        self.local_manufacturing_boost = 0  # Initialized at 0, will be calculated based on import duties
        
        # Fixed given properties
        self.homogeneity = self.random.uniform(0, 1)  # 0 = diverse, 1 = homogeneous
        self.development_level = self.random.uniform(0.3, 1)  # 0.3 = developing, 1 = fully developed
        self.wealth_level = self.random.uniform(0.2, 1)  # 0.2 = poor, 1 = rich
        
        # Changing external properties
        self.external_influences = self.random.randint(-100, 100)
        
        # Emergent properties (initialized with placeholder values)
        self.inflation = self.random.uniform(0.01, 0.05)  # Starting inflation rate
        self.economic_growth = self.random.uniform(0.01, 0.03)  # Starting economic growth
        self.tax_revenue = 0
        self.interest_payments = 0
        self.bond_interest_rate = self.interest_rate + 0.01  # Slightly higher than base rate
        self.gini_coefficient = self.random.uniform(0.2, 0.6)  # Initial inequality measure
        self.citizen_happiness = 0
        self.total_revenue = 0  # Combined tax and import duty revenue
        
        # NEW: Money supply as an emergent property
        self.money_supply = self.random.uniform(800, 1200) * self.wealth_level * self.development_level
        self.money_velocity = self.random.uniform(1.5, 2.5)  # How quickly money circulates
        self.government_spending = 0  # Will be calculated based on revenue and policy
        self.central_bank_policy = self.random.uniform(-0.1, 0.1)  # Expansionary or contractionary
        
        # Lists to store citizens and businesses
        self.citizens = []
        self.businesses = []
        
        # Add an agent type identifier
        self.agent_type = "Country"
        
    def update_external_factors(self):
        # Update external influences
        self.external_influences = max(-100, min(100, 
            self.external_influences + self.random.randint(-10, 10)))
        
        # Calculate government spending based on tax revenue and policy
        self.government_spending = (
            self.total_revenue * (1 - 0.1)  # Reserve 10% for other expenses
            + self.bonds_issued * 0.2  # Use some of the issued bonds
        )
        
        # NEW: Update money supply based on central bank policy, interest rates and government actions
        money_supply_change = (
            # Lower interest rates increase money supply (central bank effect)
            (0.03 - self.interest_rate) * 100 +
            # Government spending increases money supply
            self.government_spending / 1000 +
            # Central bank policy directly affects money supply
            self.central_bank_policy * self.money_supply * 0.1 +
            # Economic growth naturally expands money supply
            self.economic_growth * self.money_supply * 0.5
        )
        
        # Update money supply with limits to prevent extreme changes
        self.money_supply = max(self.money_supply * 0.9, 
                               min(self.money_supply * 1.1, 
                                  self.money_supply + money_supply_change))
        
        # Update the central bank policy (slightly random changes)
        # High inflation leads to contractionary policy, low inflation to expansionary
        policy_adjustment = (0.02 - self.inflation) * 0.1 + self.random.uniform(-0.03, 0.03)
        self.central_bank_policy = max(-0.2, min(0.2, self.central_bank_policy + policy_adjustment))
            
        # NEW: Update interest rate based on central bank policy and inflation
        interest_rate_change = (
            self.central_bank_policy * -0.1 +  # Negative correlation with central bank policy
            (self.inflation - 0.02) * 0.2 +  # Positive correlation with inflation
            self.random.uniform(-0.002, 0.002)  # Small random factor
        )
        self.interest_rate = max(0.005, min(0.12, self.interest_rate + interest_rate_change))
        
        # NEW: Update inflation based on economic factors and money supply
        # Using a simplified Quantity Theory of Money: MV = PQ
        # Where M is money supply, V is velocity, P is price level (inflation), Q is output (related to growth)
        theoretical_inflation = (
            (self.money_supply * self.money_velocity) / 
            (self.wealth_level * 1000 * (1 + self.economic_growth))
        ) - 1
        
        # Smooth transition to theoretical inflation
        inflation_change = (theoretical_inflation - self.inflation) * 0.2 + (
            0.005 * (self.social_services_spending - 0.3) +  # Higher spending increases inflation
            0.01 * (self.interest_rate - 0.03) +  # Higher rates decrease inflation (now reversed)
            0.002 * (self.external_influences / 100) +  # External factors
            0.003 * self.import_duty_rate  # Import duties can increase inflation
        )
        self.inflation = max(0, min(0.2, self.inflation + inflation_change))
        
        # Calculate local manufacturing boost based on import duties
        self.local_manufacturing_boost = self.import_duty_rate * 2  # Simple linear relationship
        
        # Update economic growth, now including impact of money supply
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
        
        # Reset revenue counters
        self.tax_revenue = 0
        self.import_duty_revenue = 0
        
        # Calculate tax revenue from citizens and businesses
        for citizen in self.citizens:
            if citizen.employed:
                self.tax_revenue += citizen.salary * self.tax_rate
        
        for business in self.businesses:
            self.tax_revenue += business.tax_payable
            
            # Calculate import duty revenue
            if business.business_type.startswith("import"):
                # Import duties are calculated based on business revenue before costs
                self.import_duty_revenue += business.revenue * self.import_duty_rate
                
        # Calculate total government revenue
        self.total_revenue = self.tax_revenue + self.import_duty_revenue
        
        # Update bond interest rate
        self.bond_interest_rate = self.interest_rate + max(0.01, self.inflation * 0.5)
        
        # Calculate interest payments on bonds
        self.interest_payments = self.bonds_issued * self.bond_interest_rate
        
        # Calculate average citizen happiness
        if self.citizens:
            self.citizen_happiness = sum(c.happiness for c in self.citizens) / len(self.citizens)
        else:
            self.citizen_happiness = 50  # Default value
            
        # Update money velocity based on economic growth and interest rates
        velocity_change = (
            self.economic_growth * 0.5 +  # Higher growth increases velocity
            (self.interest_rate - 0.03) * 0.2 +  # Higher interest rates increase velocity
            self.random.uniform(-0.05, 0.05)  # Random factor
        )
        self.money_velocity = max(1.2, min(3.0, self.money_velocity + velocity_change))

    def collect_statistics(self):
        # Print some basic statistics about the country
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
    def __init__(self, model, country=None):
        super().__init__(model)
        self.country = country
        self.salary = self.random.randint(40, 60)
        self.happiness = self.random.randint(40, 60)
        
        # Fixed given properties
        self.expertise = self.random.choice(["low", "medium", "high", "expert"])
        self.values_social_services = self.random.uniform(0, 1)
        self.values_economic_freedom = self.random.uniform(0, 1)
        self.trust_in_government = self.random.uniform(0, 1)
        
        # New properties for import duty effects
        self.import_goods_preference = self.random.uniform(0.2, 0.8)  # How much they prefer imported goods
        self.import_price_sensitivity = self.random.uniform(0.3, 1.0)  # How sensitive they are to import prices
        
        # NEW: Properties related to money supply and inflation
        self.inflation_sensitivity = self.random.uniform(0.3, 1.0)  # How much inflation affects them
        self.savings = self.random.uniform(10, 100)  # Initial savings
        
        # Emergent properties
        self.employed = self.random.random() < 0.8  # 80% initial employment
        self.employer = None
        self.employment_matches_expertise = False
        
        # Add an agent type identifier
        self.agent_type = "Citizen"
        
    def update_happiness(self):
        # Skip if not assigned to a country yet
        if self.country is None:
            return
            
        # Basic economic factor
        economic_factor = 0
        if self.employed:
            economic_factor = min(100, self.salary * (1 - self.country.tax_rate))
        else:
            economic_factor = min(50, self.country.social_services_spending * 100)
        
        # Social services satisfaction
        social_services_satisfaction = (
            self.values_social_services * self.country.social_services_spending * 100
        )
        
        # Economic freedom satisfaction
        economic_freedom_satisfaction = (
            self.values_economic_freedom * (1 - self.country.tax_rate) * 100
        )
        
        # Trust factor
        trust_factor = self.trust_in_government * 20
        
        # Import factors
        import_price_impact = -self.import_goods_preference * self.import_price_sensitivity * self.country.import_duty_rate * 100
        
        # Employment opportunity impact from local manufacturing boost
        employment_opportunity_impact = 0
        if not self.employed:
            # Unemployed citizens benefit more from increased local manufacturing
            employment_opportunity_impact = self.country.local_manufacturing_boost * 20
        else:
            # Employed citizens benefit less, but still positively
            employment_opportunity_impact = self.country.local_manufacturing_boost * 5
        
        # NEW: Inflation impact on happiness
        # High inflation erodes savings and purchasing power
        inflation_impact = -self.inflation_sensitivity * self.country.inflation * 200
        
        # NEW: Interest rate impact on savings
        interest_impact = self.country.interest_rate * self.savings * 0.2
        
        # Calculate new happiness with all effects
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
        
        # Happiness is more sticky than rapidly changing
        self.happiness = 0.7 * self.happiness + 0.3 * new_happiness
        self.happiness = max(0, min(100, self.happiness))
        
        # NEW: Update savings based on interest rate, inflation, and income
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
        
    def seek_employment(self):
        if self.country is None or self.employed:
            return
            
        # Simple job seeking - try to find a business that needs employees
        available_businesses = [b for b in self.country.businesses if b.has_openings()]
        if available_businesses:
            # Prioritize local manufacturing businesses if there's a boost
            if self.country.local_manufacturing_boost > 0.1:
                local_manufacturing = [b for b in available_businesses if b.business_type.startswith("manufacturing")]
                if local_manufacturing:
                    available_businesses = local_manufacturing
            
            potential_employer = self.random.choice(available_businesses)
            hired = potential_employer.hire_employee(self)
            if hired:
                self.employed = True
                self.employer = potential_employer
                # Check if employment matches expertise
                if self.expertise == "expert" and potential_employer.expert_employees > 0:
                    self.employment_matches_expertise = True
                elif self.expertise == "high" and potential_employer.white_collar_employees > 0:
                    self.employment_matches_expertise = True
                elif self.expertise in ["medium", "low"] and potential_employer.blue_collar_employees > 0:
                    self.employment_matches_expertise = True

class Business(mesa.Agent):
    def __init__(self, model, country=None):
        super().__init__(model)
        self.country = country
        
        # Business properties
        self.business_type = self.random.choice([
            "manufacturing_local_consumers",
            "manufacturing_local_businesses",
            "manufacturing_export",
            "import_citizens_consumers",
            "import_business_customers",
            "ai"
        ])
        
        self.automation_level = self.random.uniform(0.1, 0.9)
        
        # Initialize employee counts based on business type and size
        self.size_factor = self.random.uniform(0.5, 2.0)
        self.blue_collar_employees = 0
        self.white_collar_employees = 0
        self.expert_employees = 0
        
        # Initialize financial metrics
        self.revenue = 0
        self.costs = 0
        self.profit = 0
        self.tax_payable = 0
        self.import_duty_payable = 0
        
        # NEW: Business properties related to money supply
        self.borrowing = 0  # Amount borrowed from banks
        self.investment_rate = self.random.uniform(0.1, 0.4)  # Rate of reinvestment of profits
        self.interest_rate_sensitivity = self.random.uniform(0.5, 1.5)  # How sensitive to interest rates
        
        # Employee lists
        self.employees = []
        
        # Set initial max employees based on business type
        self.max_employees = int(10 * self.size_factor)
        if self.business_type == "ai":
            self.max_employees = int(2 * self.size_factor)  # AI businesses need fewer employees
        
        # Add an agent type identifier
        self.agent_type = "Business"
        
    def update_business(self):
        if self.country is None:
            return
            
        # Update business performance based on economic conditions
        base_revenue_factor = 1.0
        
        # Different business types react differently to economic factors
        if self.business_type.startswith("manufacturing"):
            base_revenue_factor += self.country.economic_growth * 2
            # Local manufacturing gets a boost from import duties
            base_revenue_factor += self.country.local_manufacturing_boost
            
            if self.business_type == "manufacturing_export":
                base_revenue_factor += self.country.external_influences / 200  # External influences affect exports
        
        elif self.business_type.startswith("import"):
            base_revenue_factor += self.country.economic_growth
            # Import businesses are negatively affected by import duties
            base_revenue_factor -= self.country.import_duty_rate * 2
            base_revenue_factor -= self.country.external_influences / 300  # External influences can affect imports
        
        elif self.business_type == "ai":
            base_revenue_factor += self.country.economic_growth * 3  # AI businesses benefit more from growth
            base_revenue_factor += self.country.development_level * 0.5  # More developed countries have better AI businesses
        
        # NEW: Money supply effect on business revenue
        # More money in the economy generally means more spending
        money_supply_effect = (self.country.money_supply / 1000) * 0.2
        base_revenue_factor += money_supply_effect
        
        # NEW: Interest rate effect on business investment and growth
        interest_rate_effect = (0.05 - self.country.interest_rate) * self.interest_rate_sensitivity
        base_revenue_factor += interest_rate_effect
        
        # Calculate revenue
        employee_factor = len(self.employees) / max(1, self.max_employees)
        self.revenue = 100 * self.size_factor * base_revenue_factor * (0.5 + 0.5 * employee_factor)
        
        # Calculate costs
        employee_costs = sum(employee.salary for employee in self.employees)
        operating_costs = 20 * self.size_factor * (1 - 0.5 * self.automation_level)
        
        # NEW: Interest payments on borrowed money
        interest_costs = self.borrowing * self.country.interest_rate
        
        # Additional costs for import businesses due to import duties
        import_duty_costs = 0
        if self.business_type.startswith("import"):
            import_duty_costs = self.revenue * self.country.import_duty_rate
            self.import_duty_payable = import_duty_costs
        
        # NEW: Inflation increases operating costs
        inflation_cost_increase = operating_costs * self.country.inflation * 2
        
        self.costs = employee_costs + operating_costs + import_duty_costs + interest_costs + inflation_cost_increase
        
        # Calculate profit and tax
        self.profit = self.revenue - self.costs
        if self.profit > 0:
            self.tax_payable = self.profit * self.country.tax_rate
        else:
            self.tax_payable = 0
            
        # NEW: Update borrowing based on interest rates and business performance
        if self.country.interest_rate < 0.04 and self.profit > 0:
            # Low interest rates encourage borrowing for expansion
            new_borrowing = self.revenue * 0.1 * (1 - self.country.interest_rate * 10)
            self.borrowing += new_borrowing
        else:
            # High interest rates or poor performance lead to debt reduction
            self.borrowing = max(0, self.borrowing * 0.95)
            
        # Adjust size based on profitability and borrowing capacity
        size_change_factor = 0
        if self.profit > 50 * self.size_factor and len(self.employees) >= self.max_employees * 0.9:
            size_change_factor = 0.1
        elif self.profit < -20 * self.size_factor:
            size_change_factor = -0.1
            
        # NEW: Interest rates affect expansion capacity
        interest_expansion_factor = (0.05 - self.country.interest_rate) * self.interest_rate_sensitivity * 0.5
        size_change_factor += interest_expansion_factor
        
        # Apply size change
        if size_change_factor > 0:
            self.max_employees = min(100, int(self.max_employees * (1 + size_change_factor)))
        elif size_change_factor < 0:
            self.max_employees = max(1, int(self.max_employees * (1 + size_change_factor)))
            # Layoff employees if necessary
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
            
        # Add employee to the business
        self.employees.append(citizen)
        
        # Determine job type based on citizen expertise
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
    def __init__(self, num_countries=None, citizens_per_country=100, businesses_per_country=10, import_duty_rates=None):
        super().__init__()
        self.num_countries = num_countries if num_countries is not None else self.random.randint(2, 5)
        self.citizens_per_country = citizens_per_country
        self.businesses_per_country = businesses_per_country
        self.countries = []
        
        # Initialize data storage for visualization
        self.data = {
            'inflation': [[] for _ in range(self.num_countries)],
            'economic_growth': [[] for _ in range(self.num_countries)],
            'tax_revenue': [[] for _ in range(self.num_countries)],
            'import_duty_revenue': [[] for _ in range(self.num_countries)],
            'total_revenue': [[] for _ in range(self.num_countries)],
            'citizen_happiness': [[] for _ in range(self.num_countries)],
            'local_manufacturing_boost': [[] for _ in range(self.num_countries)],
            'money_supply': [[] for _ in range(self.num_countries)],  # NEW
            'interest_rate': [[] for _ in range(self.num_countries)],  # NEW
            'central_bank_policy': [[] for _ in range(self.num_countries)]  # NEW
        }
        
        # Create country agents directly
        for i in range(self.num_countries):
            country = Country(self)  # Instantiate Country agent
            
            # Set specific import duty rate if provided
            if import_duty_rates is not None and i < len(import_duty_rates):
                country.import_duty_rate = import_duty_rates[i]
                
            self.countries.append(country)
        
        # Create citizens and businesses for each country
        for country in self.countries:
            for _ in range(self.citizens_per_country):
                citizen = Citizen(self, country)
                country.citizens.append(citizen)
            for _ in range(self.businesses_per_country):
                business = Business(self, country)
                country.businesses.append(business)
        
        print(f"Created {len(self.countries)} countries with {self.citizens_per_country} citizens and {self.businesses_per_country} businesses each")
    
    def step(self):
        """Advance the model by one step."""
        # Update businesses
        for country in self.countries:
            for business in country.businesses:
                business.update_business()
        
        # Update citizens
        for country in self.countries:
            for citizen in country.citizens:
                citizen.seek_employment()
                citizen.update_happiness()
        
        # Update countries and collect data
        for i, country in enumerate(self.countries):
            country.update_external_factors()
            # Store data for visualization
            self.data['inflation'][i].append(country.inflation)
            self.data['economic_growth'][i].append(country.economic_growth)
            self.data['tax_revenue'][i].append(country.tax_revenue)
            self.data['import_duty_revenue'][i].append(country.import_duty_revenue)
            self.data['total_revenue'][i].append(country.total_revenue)
            self.data['citizen_happiness'][i].append(country.citizen_happiness)
            self.data['local_manufacturing_boost'][i].append(country.local_manufacturing_boost)
            self.data['money_supply'][i].append(country.money_supply)  # NEW
            self.data['interest_rate'][i].append(country.interest_rate)  # NEW
            self.data['central_bank_policy'][i].append(country.central_bank_policy)  # NEW
    
    def collect_statistics(self):
        for i, country in enumerate(self.countries):
            print(f"\nCountry {i+1}:")
            country.collect_statistics()
    
    def plot_results(self):
        """Generate plots for key metrics."""
        steps = range(1, len(self.data['inflation'][0]) + 1)
        num_countries = len(self.countries)
        
        # Create a figure with subplots (3x3 grid to include money supply metrics)
        fig, axs = plt.subplots(3, 3, figsize=(18, 15))
        fig.suptitle('Economic Model Simulation Results', fontsize=16)
        
        # Plot inflation
        for i in range(num_countries):
            axs[0, 0].plot(steps, self.data['inflation'][i], label=f'Country {i+1} (Duty: {self.countries[i].import_duty_rate:.2f})')
        axs[0, 0].set_title('Inflation')
        axs[0, 0].set_xlabel('Step')
        axs[0, 0].set_ylabel('Inflation Rate')
        axs[0, 0].legend()
        axs[0, 0].grid(True)
        
        # Plot economic growth
        for i in range(num_countries):
            axs[0, 1].plot(steps, self.data['economic_growth'][i], label=f'Country {i+1} (Duty: {self.countries[i].import_duty_rate:.2f})')
        axs[0, 1].set_title('Economic Growth')
        axs[0, 1].set_xlabel('Step')
        axs[0, 1].set_ylabel('Growth Rate')
        axs[0, 1].legend()
        axs[0, 1].grid(True)
        
        # Plot money supply (NEW)
        for i in range(num_countries):
            axs[0, 2].plot(steps, self.data['money_supply'][i], label=f'Country {i+1} (Duty: {self.countries[i].import_duty_rate:.2f})')
        axs[0, 2].set_title('Money Supply')
        axs[0, 2].set_xlabel('Step')
        axs[0, 2].set_ylabel('Money Supply')
        axs[0, 2].legend()
        axs[0, 2].grid(True)
        
        # Plot interest rate (NEW)
        for i in range(num_countries):
            axs[1, 0].plot(steps, self.data['interest_rate'][i], label=f'Country {i+1} (Duty: {self.countries[i].import_duty_rate:.2f})')
        axs[1, 0].set_title('Interest Rate')
        axs[1, 0].set_xlabel('Step')
        axs[1, 0].set_ylabel('Rate')
        axs[1, 0].legend()
        axs[1, 0].grid(True)
        
        # Plot central bank policy (NEW)
        for i in range(num_countries):
            axs[1, 1].plot(steps, self.data['central_bank_policy'][i], label=f'Country {i+1} (Duty: {self.countries[i].import_duty_rate:.2f})')
        axs[1, 1].set_title('Central Bank Policy')
        axs[1, 1].set_xlabel('Step')
        axs[1, 1].set_ylabel('Policy (-: Contractionary, +: Expansionary)')
        axs[1, 1].legend()
        axs[1, 1].grid(True)
        
# Plot total revenue
        for i in range(num_countries):
            axs[1, 2].plot(steps, self.data['total_revenue'][i], label=f'Country {i+1} (Duty: {self.countries[i].import_duty_rate:.2f})')
        axs[1, 2].set_title('Total Government Revenue')
        axs[1, 2].set_xlabel('Step')
        axs[1, 2].set_ylabel('Revenue')
        axs[1, 2].legend()
        axs[1, 2].grid(True)
        
        # Plot tax revenue
        for i in range(num_countries):
            axs[2, 0].plot(steps, self.data['tax_revenue'][i], label=f'Country {i+1} (Duty: {self.countries[i].import_duty_rate:.2f})')
        axs[2, 0].set_title('Tax Revenue')
        axs[2, 0].set_xlabel('Step')
        axs[2, 0].set_ylabel('Revenue')
        axs[2, 0].legend()
        axs[2, 0].grid(True)
        
        # Plot import duty revenue
        for i in range(num_countries):
            axs[2, 1].plot(steps, self.data['import_duty_revenue'][i], label=f'Country {i+1} (Duty: {self.countries[i].import_duty_rate:.2f})')
        axs[2, 1].set_title('Import Duty Revenue')
        axs[2, 1].set_xlabel('Step')
        axs[2, 1].set_ylabel('Revenue')
        axs[2, 1].legend()
        axs[2, 1].grid(True)
        
        # Plot citizen happiness
        for i in range(num_countries):
            axs[2, 2].plot(steps, self.data['citizen_happiness'][i], label=f'Country {i+1} (Duty: {self.countries[i].import_duty_rate:.2f})')
        axs[2, 2].set_title('Citizen Happiness')
        axs[2, 2].set_xlabel('Step')
        axs[2, 2].set_ylabel('Happiness')
        axs[2, 2].legend()
        axs[2, 2].grid(True)
        
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.show()

def run_multiple_simulations(num_runs=10, num_countries=2, duty_rates=None, steps=20):
    """Run multiple simulations and average the results."""
    all_results = []
    
    if duty_rates is None:
        # Default set of import duty rates to test
        duty_rates = np.linspace(0.0, 0.5, 6)  # 0%, 10%, 20%, 30%, 40%, 50%
    
    # Create a progress bar
    pbar = tqdm(total=num_runs * len(duty_rates), desc="Running simulations")
    
    # For each import duty rate
    for duty_rate in duty_rates:
        duty_results = []
        
        # Run multiple simulations
        for _ in range(num_runs):
            # Create model with the same duty rate for all countries
            model = EconomicModel(
                num_countries=num_countries, 
                citizens_per_country=100, 
                businesses_per_country=10,
                import_duty_rates=[duty_rate] * num_countries
            )
            
            # Run for specified steps
            for _ in range(steps):
                model.step()
            
            # Calculate average for last 5 steps
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
    
    # Convert to DataFrame for easier analysis
    df = pd.DataFrame(all_results)
    
    # Group by duty rate and calculate averages
    grouped = df.groupby('duty_rate').mean().reset_index()
    
    # Plot the results with monetary factors included
    plt.figure(figsize=(15, 10))
    
    # Plot happiness vs duty rate
    plt.subplot(2, 3, 1)
    plt.plot(grouped['duty_rate'], grouped['avg_happiness'], 'o-', linewidth=2)
    plt.title('Average Happiness vs Import Duty Rate')
    plt.xlabel('Import Duty Rate')
    plt.ylabel('Average Happiness')
    plt.grid(True)
    
    # Plot growth vs duty rate
    plt.subplot(2, 3, 2)
    plt.plot(grouped['duty_rate'], grouped['avg_growth'], 'o-', linewidth=2)
    plt.title('Average Economic Growth vs Import Duty Rate')
    plt.xlabel('Import Duty Rate')
    plt.ylabel('Average Growth')
    plt.grid(True)
    
    # Plot total revenue vs duty rate
    plt.subplot(2, 3, 3)
    plt.plot(grouped['duty_rate'], grouped['avg_revenue'], 'o-', linewidth=2)
    plt.title('Average Government Revenue vs Import Duty Rate')
    plt.xlabel('Import Duty Rate')
    plt.ylabel('Average Revenue')
    plt.grid(True)
    
    # Plot inflation vs duty rate (NEW)
    plt.subplot(2, 3, 4)
    plt.plot(grouped['duty_rate'], grouped['avg_inflation'], 'o-', linewidth=2)
    plt.title('Average Inflation vs Import Duty Rate')
    plt.xlabel('Import Duty Rate')
    plt.ylabel('Average Inflation')
    plt.grid(True)
    
    # Plot money supply vs duty rate (NEW)
    plt.subplot(2, 3, 5)
    plt.plot(grouped['duty_rate'], grouped['avg_money_supply'], 'o-', linewidth=2)
    plt.title('Average Money Supply vs Import Duty Rate')
    plt.xlabel('Import Duty Rate')
    plt.ylabel('Average Money Supply')
    plt.grid(True)
    
    # Plot interest rate vs duty rate (NEW)
    plt.subplot(2, 3, 6)
    plt.plot(grouped['duty_rate'], grouped['avg_interest_rate'], 'o-', linewidth=2)
    plt.title('Average Interest Rate vs Import Duty Rate')
    plt.xlabel('Import Duty Rate')
    plt.ylabel('Average Interest Rate')
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()
    
    return grouped

def run_monetary_policy_analysis(base_duty_rate=0.2, interest_rates=None, num_runs=5):
    """Run analysis specifically focused on monetary policy effects."""
    all_results = []
    
    if interest_rates is None:
        # Default set of interest rates to test
        interest_rates = np.linspace(0.01, 0.10, 5)  # 1% to 10%
    
    # Create a progress bar
    pbar = tqdm(total=num_runs * len(interest_rates), desc="Running monetary policy simulations")
    
    # For each interest rate
    for interest_rate in interest_rates:
        rate_results = []
        
        # Run multiple simulations
        for _ in range(num_runs):
            # Create model with the same parameters
            model = EconomicModel(
                num_countries=1,  # For simplicity
                citizens_per_country=100, 
                businesses_per_country=10,
                import_duty_rates=[base_duty_rate]
            )
            
            # Set specific interest rate for the country
            model.countries[0].interest_rate = interest_rate
            
            # Run for specified steps
            for _ in range(20):
                model.step()
            
            # Calculate average for last 5 steps
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
    
    # Convert to DataFrame for easier analysis
    df = pd.DataFrame(all_results)
    
    # Group by interest rate and calculate averages
    grouped = df.groupby('interest_rate').mean().reset_index()
    
    # Plot the results
    plt.figure(figsize=(15, 10))
    
    # Plot happiness vs interest rate
    plt.subplot(2, 2, 1)
    plt.plot(grouped['interest_rate'], grouped['avg_happiness'], 'o-', linewidth=2)
    plt.title('Average Happiness vs Interest Rate')
    plt.xlabel('Interest Rate')
    plt.ylabel('Average Happiness')
    plt.grid(True)
    
    # Plot growth vs interest rate
    plt.subplot(2, 2, 2)
    plt.plot(grouped['interest_rate'], grouped['avg_growth'], 'o-', linewidth=2)
    plt.title('Average Economic Growth vs Interest Rate')
    plt.xlabel('Interest Rate')
    plt.ylabel('Average Growth')
    plt.grid(True)
    
    # Plot inflation vs interest rate
    plt.subplot(2, 2, 3)
    plt.plot(grouped['interest_rate'], grouped['avg_inflation'], 'o-', linewidth=2)
    plt.title('Average Inflation vs Interest Rate')
    plt.xlabel('Interest Rate')
    plt.ylabel('Average Inflation')
    plt.grid(True)
    
    # Plot money supply vs interest rate
    plt.subplot(2, 2, 4)
    plt.plot(grouped['interest_rate'], grouped['avg_money_supply'], 'o-', linewidth=2)
    plt.title('Average Money Supply vs Interest Rate')
    plt.xlabel('Interest Rate')
    plt.ylabel('Average Money Supply')
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()
    
    return grouped

def run_sensitivity_analysis(base_duty_rate=0.2, variation=0.1, num_runs=5):
    """Run a sensitivity analysis by varying import duty rates."""
    # Create a range of duty rates around the base rate
    duty_rates = np.linspace(max(0, base_duty_rate - variation), 
                            min(1, base_duty_rate + variation), 
                            5)
    
    # Run simulations with these duty rates
    results = run_multiple_simulations(num_runs=num_runs, duty_rates=duty_rates)
    return results

# Run the simulation
if __name__ == "__main__":
    # Run a single simulation with default parameters
    print("Running single simulation...")
    model = EconomicModel(num_countries=2, citizens_per_country=100, businesses_per_country=10)
    
    # Run for 20 steps
    for i in range(20):
        print(f"\n--- Step {i+1} ---")
        model.step()
        if (i+1) % 5 == 0:
            model.collect_statistics()
    
    # Generate and display plots
    model.plot_results()
    
    # Run multiple simulations with different import duty rates
    print("\nRunning multiple simulations with varying import duty rates...")
    avg_results = run_multiple_simulations(num_runs=5)
    
    # Run sensitivity analysis around a base import duty rate
    print("\nRunning sensitivity analysis...")
    sensitivity_results = run_sensitivity_analysis(base_duty_rate=0.2, variation=0.1)
    
    # Run monetary policy analysis (NEW)
    print("\nRunning monetary policy analysis...")
    monetary_results = run_monetary_policy_analysis()
    
    print("\nSimulation complete!")
