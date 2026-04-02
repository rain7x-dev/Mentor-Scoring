## Progress Score


Formula -:

P = (Mc / Mt) * log(1 + Mt)
P_final = 1 - exp(-0.5 * P)

Mc is total milestones completed by a mentor's mentees.
Mt is total milestones assigned.

- The base ratio Mc / Mt captures how well mentees are completing their work — a direct measure of
 mentor effectiveness.

- The log(1 + Mt) scaling factor gives a slight reward to mentors managing heavier workloads. A 
mentor overseeing 10 milestones who achieves the same ratio as one overseeing 3 is doing more 
overall. The log ensures this bonus grows slowly and does not dominate.

- The exponential normalization 1 - exp(-0.5 * P) maps the score into [0, 1] and ensures diminishing
 returns — a mentor cannot inflate their score indefinitely just by having more milestones.

- k = 0.5 was chosen so that a mentor with a perfect ratio and a typical workload sits comfortably
 above 0.5, leaving room to differentiate between mentors.


## Responsiveness Score 


Formula -:

R(t) = 2^(-t / t_bar)

where t is the mentor's average response time and t_bar is the global average response time across 
all mentors.

- It is bounded in [0, 1].

- It is adaptive, A 10-hour response is not inherently bad or good; it depends on whether everyone 
else responds in 2 hours or 20.

- The score halves every t_bar hours, so a mentor who takes twice the average time scores 0.5 — 
intuitively fair.

- Very slow responders are heavily penalised (the function decays exponentially)

## Engagement Score


Formula -:

E_raw = (0.4 * Meetings + 0.4 * CodeReviews + 0.2 * Messages) / num_mentees
E = 1 - exp(-0.1 * E_raw)


- Meetings (0.4) and Code Reviews (0.4) are weighted equally and highest because they represent 
deep, structured interactions.

- Messages (0.2) are weighted lower because they are the easiest to inflate.

- A mentor with 6 mentees naturally accumulates more meetings and messages in total than one with 2.
 so per mentee normalisation is important.
 
- E_raw is unbounded. The 1 - exp(-0.1 * E_raw) keeps it bounded between [0, 1].
 

## Feedback


Method -:

Bayesian Model averaging

F = (sum of ratings + C * global_mean) / (n + C)

where n is the number of students who rated the mentor and C is a confidence parameter.


- When a mentor has very few ratings (e.g., n = 1), the formula pulls the score strongly toward the 
global mean, preventing a single extreme rating from being taken at face value.

- As more students rate the mentor, the actual ratings dominate and the global mean has less 
influence.

- C = 3 means a mentor needs at least 3 ratings before their score drifts significantly from the 
global average 


## Weight Justification


w1 = 0.35 

Mentee outcomes are the primary purpose of SoC. A mentor whose mentees consistently complete 
milestones is objectively effective.

w2 = 0.30

Timely support directly determines whether a mentee gets unblocked or drops out. Second most 
impactful factor.

w3 = 0.20

Depth of interaction (meetings, code reviews, messages) reflects quality of guidance beyond just 
answering queries. Equal to R because both are important.

w4 = 0.15

Subjective ratings are valuable but susceptible to bias. Weighted lowest to prevent a few extreme 
ratings from dominating the score.


## Score Evolution Over


Formula -: 

M_t+1 = (3*M_t + 2*M_t-1 + 1*M_t-2) / 6

Week 1 M_1 = M_current directly, no smoothing.
Week 2 M_2 = (2*M_current + 1*M_t-1) / 3
Week 3 Full formula applies.


## 6. Activity Decay


Inactivity is defined as zero meetings, code reviews, and messages in a given week. Decay is 
triggered only after two consecutive inactive periods.

M_new = M_old * (1 - d),    d = 0.15

- Only trigger after 2 consecutive inactivity period.

- A 15% reduction per inactive period.

- A mentor at score 0.8 who remains inactive for 2 additional weeks would fall to approximately 0.58.