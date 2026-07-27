# This Project
While watching the FIFA World Cup 2026, it was hard to shake the notion that bigger teams tended to get more favorable calls over smaller opponents. I also realized the potential biases I may carry, and that simply watching matches was no way to fairly determine whether referees truly gave the benefit of the doubt to only the giants. I made this as a brief project to put what I felt I saw in games into some sort of real analysis.

# How to use

Run pip install -r requirements.txt

Files that require manual input: decision.csv and match_context.csv 
Both of these files live in /data/manual

Inputs in decision.csv must follow the following format for this to work correctly:

incident_id,match,stage,minute,favored_team,underdog_team,team_benefited,team_hurt,incident_type,decision,favored_team_benefited,score,call_correctness,confidence,video_timestamp,VAR_involved,standard_fit,notes
RSA-CAN-R32-01,"South Africa Vs Canada", R32, 45, Canada, South Africa, South Africa, Canada, Potenital Penalty, No Penalty, FALSE, -2, 0.3, 0.7, 5:30, FALSE, 0.5,"Notes."

Refer to rubric.md for scoring guidelines, or else results might explode
Having more incidents for as many games as possible will produce more robust results

After decision.csv is done, click RUN ALL in 01_data_check.ipynb
This will create match_context.csv

It will populate with given data, but winner and spread need to be manually inputted. Spread is how many goals a team won by. Negative represents how many goals the favorite won by, positive how many goals the underdog won by, and 0 represents a game was decided in pens.

For example, the spread for Argentina beating Cape Verde 3-2 would be represented as -1. Norway beating Brazil 2-1 is represented as 1 etc.

Once this sheet is complete, no more manual inputs are needed. Go to 02_build_tables.ipynb and click RUN ALL. Some data checks will be run, and once validated the processed tables will be created, and some example tables to explore data will be displayed.

Afterwards, RUN ALL in 03_charts_and_analysis.ipynb and some charts will be generated and placed into /outputs/charts

04_ultimate is an AI-generated "super-chart" for fun to answer the question, do bigger teams get the whistle?

Project starts with my logged incidents in decision.csv, and my personal interpretation is located at /outputs/v1_findings.md



