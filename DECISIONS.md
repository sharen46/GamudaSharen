Direct CSV Analysis: I decided to use the LangChain Pandas Agent rather than converting CSVs to text. This allows the system to perform actual mathematical calculations on project budgets.


Stateless Storage: For this MVP, files are stored in memory/temporary local storage to meet the 3-day development window.


LLM Choice: Gemini 2.5 Flash was selected to leverage its large context window for long project status reports.


Error Handling: Implemented df.fillna(0) to handle the "intentional messiness" of the synthetic financial data.