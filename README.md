This neuro heuristics project is a part of a larger passion project where I map human cognitive traits onto machine behaviour. It aims to be equal parts model evaluation and behavioural science, even though I lack formal training in the latter. My love and fascination for langauges and human cognition pulled me towards the emerging frontier of LLM cognition. Specifically in this project, I wanted to explore how large langauge models exhibit cognitive biases like anchoring, satisficing, and recency.

Heuristics used:
1. Anchoring - Does a strong numerical or semantic anchor in the prompt skew the model's prompt?
2. Satisficing - Will the model settle for a "good enough" answer if the prompt implies speed or a cognitive constraint?
3. Recency - Does providing recent information influence the model's prediction even when older information is more relevant?

I tested outputs against high/low anchors to measure response drift. I also employed framing to trigger satisficing behavior and compared outputs across manipulated prompt histories.

I ran experiments across 3 levels of difficulty for both the analogies and heuristics, the code for which can be found in experiments. The analogies and heuristics are in the tasks and heuristics folders respectively. Plots and combined files of results from each level can be found in outputs. 
