I've made extensive use of AI throughout this project. While the overall framework and concept are my own, many of the finer details were refined with the help of various AI tools.
Special thanks to:
ChatGPT
Claude
Grok
Microsoft Copilot

I used only the free versions of these platforms, iterating across them to improve different parts of the project.
How to use it:
Simply run the included .py Python file.

Note:
This is an early proof-of-concept—a quick and dirty first version. It doesn't produce meaningful results yet, and there's still a lot of work to be done.

# bottom-up-macroeconomics
Macroeconomics Agent Based Modeling (ABM). Evaluate how governments actions influence different economic attributes that ultimately affects citizens'happiness 

Project Specification: Agent-Based Model of Macroeconomic Choices and Citizen Happiness
1. Purpose of the Model
To simulate and explore the dynamic relationships between macroeconomic policy decisions, international trade, cultural variables, and citizen happiness. The model aims to assist in answering complex questions such as:
•	What macroeconomic choices lead to greater happiness in different kinds of societies?
•	How do fiscal and monetary decisions affect long-term well-being?
•	How does international trade between unequal countries affect both parties?
•	How does citizen trust influence optimal policy decisions?
________________________________________
2. Core Conceptual Framework
Citizen Happiness is the central outcome variable, modelled as a function of how well Maslow’s hierarchy of needs are fulfilled:
1.	Physiological Needs – food, housing, health
2.	Safety Needs – job security, public order, savings
3.	Belonging – social integration, family cohesion
4.	Esteem – recognition, purpose, quality of employment
5.	Self-Actualization / Meaning – life purpose, freedom, creative expression (drawing on Viktor Frankl)
These needs are satisfied through:
•	Economic participation (jobs, income)
•	Access to services (health, education, safety)
•	Cultural context (social justice, inclusion, dignity)
•	Government and societal structure (trust, fairness, opportunity)
________________________________________
3. Key Entities and Attributes
3.1 Countries
Each country is a macro-agent with the following:
•	Government
o	Tax policies (progressive/flat; on income bands)
o	Infrastructure and social spending levels
o	Trade policies (tariffs, quotas, subsidies)
o	Immigration policies (e.g., skills or capital-based)
o	Bond issuance to finance deficits
•	Central Bank
o	Interest rate policies
o	Inflation targeting or employment targeting
o	Quantitative easing or tightening
•	Culture
o	Citizen trust level (affects tolerance for government size and interventions)
o	Value weights (e.g., individualism vs collectivism)
•	Development Status
o	GDP per capita, infrastructure quality, human development index, etc.
o	Determines baseline expectations and needs
3.2 Citizens (Agents)
Randomly instantiated individuals with:
•	Demographics – age, education, wealth, location
•	Psychological Traits – risk aversion, trust in government, purpose-orientation
•	Needs Status – satisfaction scores across Maslow’s levels
•	Employment – job, income, job quality (meaning, creativity, autonomy)
•	Migration Propensity – willingness to emigrate for better life
3.3 Businesses
•	Type (manufacturing, services, tech, agriculture)
•	Size and productivity
•	Dependence on interest rates, trade, government incentives
•	Labor demand and wages
•	Innovation and quality of jobs offered
•	Can be domestic or foreign-owned (multinationals)
________________________________________
4. Economic Mechanisms and Interactions
4.1 Government Policy Actions
•	Changes to tax rates by income class
•	Adjustments to public spending (infra vs social services)
•	Issuing bonds to finance spending
•	Regulatory changes to support/penalize specific industries
•	Immigration and visa programs (e.g., Golden Visa)
4.2 Central Bank Policy Actions
•	Set interest rates affecting:
o	Consumer borrowing/saving
o	Business investment and hiring
o	Inflation and currency strength
4.3 Trade and Global Interactions
•	Countries exchange goods/services based on comparative advantages
•	Tariffs and quotas affect prices and competitiveness
•	Exchange rate influenced by trade balance and interest rate differentials
•	Debt in one country can impact global markets
•	Policy contagion: one country’s policy may trigger others to respond
________________________________________
5. Model Dynamics and Feedback Loops
•	Citizens’ happiness → social pressure → government policy change
•	Government spending → business environment → job creation → happiness
•	Trust → acceptance of taxes → budget size → happiness via services
•	Poor country exports → rich country consumption → debt cycles
•	Long-term debt → fiscal pressure → austerity → changes in happiness
•	High inequality → social unrest or trust erosion → policy instability
________________________________________
6. Output Metrics and Visualizations
•	Happiness Index over Time per country
•	Needs Satisfaction Breakdown (Maslow levels)
•	Trust and Social Cohesion
•	Gini Coefficient and Inequality Measures
•	Employment, Wages, and Job Quality Metrics
•	Government Debt and Deficit Trends
•	Trade Flows and Balances
•	Policy Effectiveness Scores (measured by Δ in happiness and economic indicators)
________________________________________
7. Scenarios and Experiments
You can use the model to simulate:
•	Introduction of Universal Basic Income in a rich, high-trust country
•	Collapse of trust in a previously stable country
•	Large-scale immigration of high-skill workers
•	Infrastructure boom funded by debt
•	Global trade wars
•	Austerity vs stimulus policies post-debt crisis
•	Cultural shift toward collectivism or individualism
________________________________________
8. Model Extensibility
•	Future integration of climate change effects on economies
•	Resource constraints and energy cost shocks
•	Technological change and AI-induced unemployment
•	Shocks such as pandemics, wars, or natural disasters
•	Long-term emergence of new cultures (e.g., post-growth societies)


