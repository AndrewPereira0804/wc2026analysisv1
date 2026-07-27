# Project

I created this project mainly as an exercise in Pandas and working with a CSV pipeline. I wanted to take the notion that "Bigger teams get the whistle" in international soccer and put it to numbers, and see if the claim holds any weight. I designed a scoring system (outlined in rubric.md) and watched the FOX extended highlights of all KO matches of FIFA WC 26, and then drew comparisons across the whole tournament. What I found (maybe conveniently) mostly matched my expectations, but it still made me realize how strong confirmation bias can be when you just observe with your eyes, and how many inconsistencies in refereeing appear even in small-ticket games. Calls that are assisted with technology (such as offsides) are ignored. Below, I'll outline some of my favorite finds.

# Addressing bias and limitations

The two strongest caveats to this entire project are: 
1. I am not a referee, I am one fan with my own internal biases and potential misunderstandings. I tried my best to be as fair as possible and watched the extended highlights of every match, but I recognize that one person rating what he deems to be a controversial call is far from the most fair and impartial system.
2. Only FOX extended highlights are used as pools to sample incidents from. This introduces massive selection bias throughout every match. The only incidents that appear are the ones FOX Sports decided were worth showing in their uploaded highlights. I consistently watched only FOX highlights to try and make this issue affect all games somewhat equally, but again this bias is very present

The current analysis reduces each match to a single net bias score. This makes comparison straightforward, but it can hide matches where several significant decisions benefited both teams and largely canceled each other out. The normalized favorite-advantage measure also describes the direction of the logged impact, not the frequency of ordinary favorable calls or the referee’s overall level of strictness throughout all the games they officiate.

The model treats the team with the higher FIFA ELO/World Ranking as the “bigger team,” although ELO Rank and team stature are not always equivalent. It also assumes that weighted incident scores can be added and compared directly, even though the practical effect of two separate decisions may not be perfectly cumulative.

A more robust version would incorporate an independent measure of team stature, test the sensitivity of results to different scoring formulas, and also take more statistical certainties into account, such as ELO-gap, yellow cards per foul for, yellow cards per foul against, penalties per foul for/against, xG from incidents, minute, score line, etc.

Better data collection would entail an expanded version of what I did myself. Logging every incident over the course of entire matches, rather than just extended highlights, logging all routine/minor calls that are correct, having multiple opinions decide the rankings (such as call correctness, impact score, and consistency boost), and even having legitimate referees do the scoring of incidents would lead to more meaningful data.

With all that aside, here is the summary of what I found.

# Summarizing Findings
I personally logged 55 incidents in 28 matches spanning 30/32 teams.
Favorites received 58.5% of total weighted bias significance.
Underdogs received 41.5% of total weighted bias significance.
Net favorite advantage: +17.1%.
95% match-bootstrap interval: -25.9% to +59.8%.

What this suggests is that over the course of the KO round of the tournament, the whistle leaned toward favorited teams. However, the 95% CI going negative suggests there might be too much noise to say with certainty that favorited teams were systemically benefitted by controversial calls over the course of the entire bracket, as underdog teams saw a significant amount of beneficial calls as well.

Overall match direction found 7 favorite-leaning, 5 underdog-leaning, 16 mixed/neutral after incidents are weighted. So the favorite advantage is not from more favorite-leaning matches; it comes from larger favorite-side swings in key matches.

# Match Summaries
![alt text](./charts/matches_by_impact.png)

This chart ranks matches by the sum of the scores, ignoring bias direction. This can be interpreted as my personal ranking of the most controversial/worst-managed matches without considering which side benefited more or less. Some matches (e.g. France V Paraguay) had many small incidents that compiled, while others had few, but high impact incidents (e.g. Argentina Vs Egypt). Lower absolute match bias directly points to a overall less controversial match. If a match isn't listed at all, that means I found no incidents worth logging in that match.

![alt text](./charts/matches_by_bias.png)

This chart ranks matches by the overall bias seen, with the middle cutoffs showing where the score is >0.75 in either direction representing an overall neutral match. This graph much more clearly shows where bias actually falls and how much. Negative values representing the underdog receiving more favorable calls and positive values representing the favorite receiving more favorable calls. The "neutral" cutoff is more of a made-up boundary rather than a mathematical statement.

![alt text](./charts/match_score_vs_spread.png)

There is not a clear correlation between refereeing bias and the spread of a game (negative values representing how many the favorite won by, positive underdog), but its still interesting anyway. Only two underdog teams won in spite of the calls drifting towards the direction of the favorite.

# Team Summaries
![alt text](./charts/total_benefit.png)
![alt text](./charts/total_harm.png)

Looking at total benefit and harm does not tell the whole story, as teams that make it farther tend to have more extreme values, as expected, but it does show some interesting outliers. Cape Verde despite having only one KO match experienced the most total harm from refeering calls, simply because in their match against Argentina, they saw no meaningful calls going their way. Argentina saw the highest total benefit, but with the caveat they made it to the finals. England and France actually saw a large amount of harm from calls over the course of the tournament, but again they also saw more matches. 

![alt text](./charts/impact_per_match.png)

Looking at benefit/harm over matches paints a clearer picture. Paraguay actually tops the chart of per-match calls going their way, but the score is pushed heavily by Germany's huge disallowed goal, which ultimately led to their advancing to R16, and the poor game management seen in their R16 game against France; where despite their unsporting behavior, not a single yellow card was shown. Interestingly, because of Paraguay, France and Germany in turn fall down to having a significant amount of harm against them. Argentina, despite making it to the finals, is a clear second place for most benefitted teams. The case for controversial calls going Argentina's way is stronger, as they played in more matches and consistently saw beneficial calls. 

The fact that the impact per match seems to lean more heavily towards harm than benefit, and that many of the teams who saw the most impact either way were eliminated early, suggests that over the course of the tournament, controversial refereeing may have helped in deciding games but teams that made it far tended to be on both beneficial and hurtful ends of biased calls, therefor evening out, with the exception of Argentina. 

# Other Summaries

![alt text](./charts/impact_by_stage.png)

This chart measures the total of bias direction in each stage of the the KO Tournament. We can see that in no stage did the overall bias favor the underdog (3P match saw insignifcant bias toward the under), with R32 seeing the most total bias toward the favorite, with the caveat that R32 also had the most logged matches. Interestingly, the QF saw less total favoritism than the SF despite more QF matches being logged.

![alt text](./charts/incident_count_vs_impact.png)

Shows a sort of obvious trend that matches with more incidents tend to have a higher overall display of bias in either direction

![alt text](./charts/impact_by_incident_type.png)

Disallowed goals are understandably the most impactful, and controversial types of calls in this tournament. Because it is not the most common, it is also pushed heavily by the most controversial incidents. No Free Kick and No Penalty show a significant amount of controversy despite being more common incident types, suggesting that unfairness may arise more significantly in missed calls rather than calls given. 


# Ultimate Summaries

![alt text](./charts/ultimate_do_bigger_teams_get_the_whistle.png)
![alt text](./charts/ultimate_whistle_evidence_map.png)

For fun, I had Codex generate two graphs that combine all the data to try and answer the ultimate question, "Do bigger teams get the whistle?"

The headline stats are: Favorites received 58.5% of total weighted bias significance.
Underdogs received 41.5% of total weighted bias significance.
Net favorite advantage: +17.0%.
95% match-bootstrap interval: -25.9% to +59.7%.

This is the share of the weighted evidence, not the percentage of all referee calls. It does not mean that 58.5% of decisions favored the favorite.

Because the 95% bootstrap interval crosses 0 by a significant amount, the evidence does not conclusively say that in the KO tournament that bigger teams systemically received more favorable calls. However, it does weakly suggest that it may lean toward the favorite. 

The match-level whistle direction graph is not incredibly meaningful. Many matches saw single, or low amounts of controversial calls that may only go one way, pushing lots of matches to 100 percent in one direction or the other, but does not suggest enormous bias. 

The most impactful decisions are also listed, which is certainly an interesting graph but does not contribute to the point overall. We do see that on either end of the bias, the most significant calls were disallowed goals. 

The sensitivity graph shows the estimated higher-Elo advantage remains positive across a range of correctness-discount exponents, declining from approximately 18.5% to 14.5%. This suggests that the result is reasonably stable to this particular scoring choice, although it does not address uncertainty in incident selection or subjective ratings.

On the whistle evidence map, the diagonal boundaries indicate the maximum possible one-sidedness. A point on or near a diagonal means nearly all the evidence in that match points in one direction. A point closer to the center has calls pointing both ways. Most matches are clustered near the bottom, meaning they contain relatively little evidence. Therefore, a handful of higher-evidence matches have considerable influence on the tournament-wide result.

The cumulative whistle ledger shows the cumulative net favorite advantage is jumpy and influenced by a few large incidents. It is clearly unstable, but does again lean toward the favorite over the course of the tournament

# Leave-one-out Filter

Leaving out just one team can significantly swing the final totals. Excluding Argentina gives the net favorite advantage to underdogs, at -11.8%, showing Argentina pushes a huge amount of points toward the favorite advantage. Removing Paraguay shifts the final percentages so far towards the favorite, that the 95% interval barely contains any underdog advantage at all, suggesting Paraguay's matches represent a massive amount of all underdog advantage seen. Although I have not tested results for leaving out each individual team, this further suggests that the findings are influenced majorly by team and match clusters.

# Overall

All in all, this project suffers the most from data collection and bias limitations, leaving uncertainty wide. This exercise does not remarkably prove systemic bias in either direction, and despite data leaning towards favorites it does not prove that they benefitted so consistently over the course of the whole tournament that some conspiracy emerges. What this does more strongly suggest is that some matches may not have been managed clearly and correctly, and certain teams received a large sum of biased calls in their favor, which majorly pushes the needle away from complete fairness. Despite some interesting points and outliers, the finding is pretty consistent with the most reasonable interpretation of referee impact on this particular tournament.









