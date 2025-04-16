Using Agent-Based Modeling (ABM) to Explore Macroeconomics from the Bottom Up

This is an early, interim step in the development of an agent-based model of macroeconomics—built from the bottom up—to help capture the complex and often unexpected behaviors that emerge in economic systems. While still in its infancy and far from perfect, the goal is to gain some insight into the non-intuitive dynamics of real-world economies.

The model is implemented in Python using the Mesa ABM library.

Its broader purpose is to explore questions such as:

What macroeconomic choices lead to greater happiness in different types of societies?

How do fiscal and monetary policies impact long-term well-being?

How does international trade between unequal countries affect both parties?

In this initial version, countries, businesses, and citizens (the “agents”) are initialized randomly. Although the simulation runs and produces output, the results are currently still mostly noise and should not yet be taken too seriously.

While the high-level design is entirely my own—something that current AI cannot yet replicate—I gratefully acknowledge the detailed coding support provided by several free AI tools. These "assistants" have been invaluable in bringing the project to this point. Special thanks to Claude, ChatGPT, Grok, and Microsoft Copilot.

First Planned Scenario for Testing
The first specific test scenario will involve two countries:

A USA-type country: rich, developed, and long committed to free trade, but with a history of undisciplined fiscal policy.

A China-type country: poorer, developing, and focused on export-led growth.

The rich country has, for decades, followed a free trade policy but neglected fiscal discipline—essentially operating under the assumption that "deficits do not matter." In the short term, this seemed sustainable, but over time government debt ballooned. Eventually, the annual deficit grew so large that debt levels became alarming. If left unchecked, interest payments on the debt could seriously harm the economy.

The model will be used to explore the effects—measured primarily in terms of citizen happiness—of two possible policy responses by the rich country:

Increase the tax rate to reduce the deficit.

Increase import duties to reduce the deficit.

In both cases, it is assumed that the government will take additional steps to boost economic growth, but these are not explicitly included in the simulation at this stage.
