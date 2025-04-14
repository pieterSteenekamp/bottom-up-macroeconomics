print("starting my macroeconomics project")
import mesa
import matplotlib.pyplot as plt
import numpy as np

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
        self.import_duty_revenue = 0
        self.interest_payments = 0
        self.bond_interest_rate = self.interest_rate + 0.01  # Slightly higher than base rate
        self.gini_coefficient = self.random.uniform(0.2, 0.6)  # Initial inequality measure
        self.citizen_happiness = 0
        
        # Lists to store citizens and businesses
        self.citizens = []
        self.businesses = []
        
        # Add an agent type identifier
        self.agent_type = "Country"
        
    def update_external_factors(self):
        # Update external influences
        self.external_influences = max(-100, min(100, 
            self.external_influences + self.random.randint(-10, 10)))
            
        # Update inflation based on economic factors
        inflation_change = (
            0.005 * (self.social_services_spending - 0.3) +  # Higher spending increases inflation
            0.01 * (self.interest_rate - 0.03) +  # Lower rates increase inflation
            0.002 * (self.external_influences / 100)  # External factors
        )
        self.inflation = max(0, min(0.2, self.inflation + inflation_change))
        
        # Update economic growth
        growth_change = (
            0.005 * (0.03 - self.interest_rate) +  # Lower rates increase growth
            0.002 * (self.external_influences / 100) +  # External factors
            0.003 * (0.3 - self.tax_rate)  # Lower taxes increase growth
        )
        self.economic_growth = max(-0.05, min(0.1, self.economic_growth + growth_change))
        
        # Calculate tax revenue
        self.tax_revenue = 0
        for citizen in self.citizens:
            if citizen.employed:
                self.tax_revenue += citizen.salary * self.tax_rate
        
        for business in self.businesses:
            self.tax_revenue += business.tax_payable
        
        # Update bond interest rate
        self.bond_interest_rate = self.interest_rate + max(0.01, self.inflation * 0.5)
        
        # Calculate interest payments on bonds
        self.interest_payments = self.bonds_issued * self.bond_interest_rate
        
        # Calculate average citizen happiness
        if self.citizens:
            self.citizen_happiness = sum(c.happiness for c in self.citizens) / len(self.citizens)
        else:
            self.citizen_happiness = 50  # Default value

    def collect_statistics(self):
        # Print some basic statistics about the country
        print(f"Country statistics:")
        print(f"  Tax rate: {self.tax_rate:.2f}")
        print(f"  Interest rate: {self.interest_rate:.2f}")
        print(f"  Inflation: {self.inflation:.2f}")
        print(f"  Economic growth: {self.economic_growth:.2f}")
        print(f"  Tax revenue: {self.tax_revenue:.2f}")
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
            
        # Update happiness based on various factors
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
        
        # Calculate new happiness
        new_happiness = (
            0.4 * economic_factor +
            0.2 * social_services_satisfaction +
            0.2 * economic_freedom_satisfaction +
            0.1 * trust_factor +
            0.1 * self.random.uniform(-10, 10)  # Random factor
        )
        
        # Happiness is more sticky than rapidly changing
        self.happiness = 0.7 * self.happiness + 0.3 * new_happiness
        self.happiness = max(0, min(100, self.happiness))
        
    def seek_employment(self):
        if self.country is None or self.employed:
            return
            
        # Simple job seeking - try to find a business that needs employees
        available_businesses = [b for b in self.country.businesses if b.has_openings()]
        if available_businesses:
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
            if self.business_type == "manufacturing_export":
                base_revenue_factor += self.country.external_influences / 200  # External influences affect exports
        
        elif self.business_type.startswith("import"):
            base_revenue_factor += self.country.economic_growth
            base_revenue_factor -= self.country.external_influences / 300  # External influences can affect imports
        
        elif self.business_type == "ai":
            base_revenue_factor += self.country.economic_growth * 3  # AI businesses benefit more from growth
            base_revenue_factor += self.country.development_level * 0.5  # More developed countries have better AI businesses
        
        # Calculate revenue
        employee_factor = len(self.employees) / max(1, self.max_employees)
        self.revenue = 100 * self.size_factor * base_revenue_factor * (0.5 + 0.5 * employee_factor)
        
        # Calculate costs
        employee_costs = sum(employee.salary for employee in self.employees)
        operating_costs = 20 * self.size_factor * (1 - 0.5 * self.automation_level)
        self.costs = employee_costs + operating_costs
        
        # Calculate profit and tax
        self.profit = self.revenue - self.costs
        if self.profit > 0:
            self.tax_payable = self.profit * self.country.tax_rate
        else:
            self.tax_payable = 0
            
        # Adjust size based on profitability
        if self.profit > 50 * self.size_factor and len(self.employees) >= self.max_employees * 0.9:
            self.max_employees = min(100, int(self.max_employees * 1.1))
        elif self.profit < -20 * self.size_factor:
            self.max_employees = max(1, int(self.max_employees * 0.9))
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
    def __init__(self, num_countries=None, citizens_per_country=100, businesses_per_country=10):
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
            'citizen_happiness': [[] for _ in range(self.num_countries)]
        }
        
        # Create country agents directly
        for _ in range(self.num_countries):
            country = Country(self)  # Instantiate Country agent
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
            self.data['citizen_happiness'][i].append(country.citizen_happiness)
    
    def collect_statistics(self):
        for i, country in enumerate(self.countries):
            print(f"\nCountry {i+1}:")
            country.collect_statistics()
    
    def plot_results(self):
        """Generate plots for key metrics."""
        steps = range(1, len(self.data['inflation'][0]) + 1)
        num_countries = len(self.countries)
        
        # Create a figure with subplots
        fig, axs = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Economic Model Simulation Results', fontsize=16)
        
        # Plot inflation
        for i in range(num_countries):
            axs[0, 0].plot(steps, self.data['inflation'][i], label=f'Country {i+1}')
        axs[0, 0].set_title('Inflation')
        axs[0, 0].set_xlabel('Step')
        axs[0, 0].set_ylabel('Inflation Rate')
        axs[0, 0].legend()
        axs[0, 0].grid(True)
        
        # Plot economic growth
        for i in range(num_countries):
            axs[0, 1].plot(steps, self.data['economic_growth'][i], label=f'Country {i+1}')
        axs[0, 1].set_title('Economic Growth')
        axs[0, 1].set_xlabel('Step')
        axs[0, 1].set_ylabel('Growth Rate')
        axs[0, 1].legend()
        axs[0, 1].grid(True)
        
        # Plot tax revenue
        for i in range(num_countries):
            axs[1, 0].plot(steps, self.data['tax_revenue'][i], label=f'Country {i+1}')
        axs[1, 0].set_title('Tax Revenue')
        axs[1, 0].set_xlabel('Step')
        axs[1, 0].set_ylabel('Revenue')
        axs[1, 0].legend()
        axs[1, 0].grid(True)
        
        # Plot citizen happiness
        for i in range(num_countries):
            axs[1, 1].plot(steps, self.data['citizen_happiness'][i], label=f'Country {i+1}')
        axs[1, 1].set_title('Citizen Happiness')
        axs[1, 1].set_xlabel('Step')
        axs[1, 1].set_ylabel('Happiness')
        axs[1, 1].legend()
        axs[1, 1].grid(True)
        
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.show()

# Run the simulation
if __name__ == "__main__":
    model = EconomicModel(num_countries=2, citizens_per_country=100, businesses_per_country=10)
    
    # Run for 20 steps
    for i in range(20):
        print(f"\n--- Step {i+1} ---")
        model.step()
        if (i+1) % 5 == 0:
            model.collect_statistics()
    
    # Generate and display plots
    model.plot_results()
