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
            0.002 * (self.external_influences / 100) +  # External factors
            0.003 * self.import_duty_rate  # Import duties can increase inflation
        )
        self.inflation = max(0, min(0.2, self.inflation + inflation_change))
        
        # Calculate local manufacturing boost based on import duties
        self.local_manufacturing_boost = self.import_duty_rate * 2  # Simple linear relationship
        
        # Update economic growth, now including impact of import duties
        growth_change = (
            0.005 * (0.03 - self.interest_rate) +  # Lower rates increase growth
            0.002 * (self.external_influences / 100) +  # External factors
            0.003 * (0.3 - self.tax_rate) +  # Lower taxes increase growth
            0.004 * self.local_manufacturing_boost -  # Local manufacturing boost helps growth
            0.006 * self.import_duty_rate  # But high import duties can hurt overall growth
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
        
        # New factors related to import duties
        
        # Import goods price impact - higher duties make imported goods more expensive
        import_price_impact = -self.import_goods_preference * self.import_price_sensitivity * self.country.import_duty_rate * 100
        
        # Employment opportunity impact from local manufacturing boost
        employment_opportunity_impact = 0
        if not self.employed:
            # Unemployed citizens benefit more from increased local manufacturing
            employment_opportunity_impact = self.country.local_manufacturing_boost * 20
        else:
            # Employed citizens benefit less, but still positively
            employment_opportunity_impact = self.country.local_manufacturing_boost * 5
        
        # Calculate new happiness with import duty effects
        new_happiness = (
            0.35 * economic_factor +
            0.15 * social_services_satisfaction +
            0.15 * economic_freedom_satisfaction +
            0.1 * trust_factor +
            0.1 * import_price_impact +
            0.1 * employment_opportunity_impact +
            0.05 * self.random.uniform(-10, 10)  # Random factor
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
        
        # Calculate revenue
        employee_factor = len(self.employees) / max(1, self.max_employees)
        self.revenue = 100 * self.size_factor * base_revenue_factor * (0.5 + 0.5 * employee_factor)
        
        # Calculate costs
        employee_costs = sum(employee.salary for employee in self.employees)
        operating_costs = 20 * self.size_factor * (1 - 0.5 * self.automation_level)
        
        # Additional costs for import businesses due to import duties
        import_duty_costs = 0
        if self.business_type.startswith("import"):
            import_duty_costs = self.revenue * self.country.import_duty_rate
            self.import_duty_payable = import_duty_costs
        
        self.costs = employee_costs + operating_costs + import_duty_costs
        
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
            'local_manufacturing_boost': [[] for _ in range(self.num_countries)]
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
    
    def collect_statistics(self):
        for i, country in enumerate(self.countries):
            print(f"\nCountry {i+1}:")
            country.collect_statistics()
    
    def plot_results(self):
        """Generate plots for key metrics."""
        steps = range(1, len(self.data['inflation'][0]) + 1)
        num_countries = len(self.countries)
        
        # Create a figure with subplots (3x2 grid)
        fig, axs = plt.subplots(3, 2, figsize=(15, 15))
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
        
        # Plot tax revenue
        for i in range(num_countries):
            axs[1, 0].plot(steps, self.data['tax_revenue'][i], label=f'Country {i+1} (Duty: {self.countries[i].import_duty_rate:.2f})')
        axs[1, 0].set_title('Tax Revenue')
        axs[1, 0].set_xlabel('Step')
        axs[1, 0].set_ylabel('Revenue')
        axs[1, 0].legend()
        axs[1, 0].grid(True)
        
        # Plot import duty revenue
        for i in range(num_countries):
            axs[1, 1].plot(steps, self.data['import_duty_revenue'][i], label=f'Country {i+1} (Duty: {self.countries[i].import_duty_rate:.2f})')
        axs[1, 1].set_title('Import Duty Revenue')
        axs[1, 1].set_xlabel('Step')
        axs[1, 1].set_ylabel('Revenue')
        axs[1, 1].legend()
        axs[1, 1].grid(True)
        
        # Plot citizen happiness
        for i in range(num_countries):
            axs[2, 0].plot(steps, self.data['citizen_happiness'][i], label=f'Country {i+1} (Duty: {self.countries[i].import_duty_rate:.2f})')
        axs[2, 0].set_title('Citizen Happiness')
        axs[2, 0].set_xlabel('Step')
        axs[2, 0].set_ylabel('Happiness')
        axs[2, 0].legend()
        axs[2, 0].grid(True)
        
        # Plot local manufacturing boost
        for i in range(num_countries):
            axs[2, 1].plot(steps, self.data['local_manufacturing_boost'][i], label=f'Country {i+1} (Duty: {self.countries[i].import_duty_rate:.2f})')
        axs[2, 1].set_title('Local Manufacturing Boost')
        axs[2, 1].set_xlabel('Step')
        axs[2, 1].set_ylabel('Boost Factor')
        axs[2, 1].legend()
        axs[2, 1].grid(True)
        
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
            
            # Calculate average happiness for the last 5 steps
            avg_happiness = np.mean([np.mean(model.data['citizen_happiness'][i][-5:]) for i in range(num_countries)])
            avg_growth = np.mean([np.mean(model.data['economic_growth'][i][-5:]) for i in range(num_countries)])
            avg_revenue = np.mean([np.mean(model.data['total_revenue'][i][-5:]) for i in range(num_countries)])
#            avg_happiness = np.mean([np.mean([model.data['citizen_happiness'][i][-5:]) for i in range(num_countries)])
#            avg_growth = np.mean([np.mean([model.data['economic_growth'][i][-5:]) for i in range(num_countries)])
#            avg_revenue = np.mean([np.mean([model.data['total_revenue'][i][-5:]) for i in range(num_countries)])
            
            duty_results.append({
                'duty_rate': duty_rate,
                'avg_happiness': avg_happiness,
                'avg_growth': avg_growth,
                'avg_revenue': avg_revenue
            })
            
            pbar.update(1)
        
        all_results.extend(duty_results)
    
    pbar.close()
    
    # Convert to DataFrame for easier analysis
    df = pd.DataFrame(all_results)
    
    # Group by duty rate and calculate averages
    grouped = df.groupby('duty_rate').mean().reset_index()
    
    # Plot the results
    plt.figure(figsize=(15, 5))
    
    # Plot happiness vs duty rate
    plt.subplot(1, 3, 1)
    plt.plot(grouped['duty_rate'], grouped['avg_happiness'], 'o-', linewidth=2)
    plt.title('Average Happiness vs Import Duty Rate')
    plt.xlabel('Import Duty Rate')
    plt.ylabel('Average Happiness')
    plt.grid(True)
    
    # Plot growth vs duty rate
    plt.subplot(1, 3, 2)
    plt.plot(grouped['duty_rate'], grouped['avg_growth'], 'o-', linewidth=2)
    plt.title('Average Economic Growth vs Import Duty Rate')
    plt.xlabel('Import Duty Rate')
    plt.ylabel('Average Growth')
    plt.grid(True)
    
    # Plot total revenue vs duty rate
    plt.subplot(1, 3, 3)
    plt.plot(grouped['duty_rate'], grouped['avg_revenue'], 'o-', linewidth=2)
    plt.title('Average Government Revenue vs Import Duty Rate')
    plt.xlabel('Import Duty Rate')
    plt.ylabel('Average Revenue')
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
    
    print("\nSimulation complete!")
