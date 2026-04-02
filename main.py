import pandas as pd
import numpy as np

mentors = pd.read_csv("mentors.csv")
students = pd.read_csv("students.csv")
interactions = pd.read_csv("interactions.csv")
feedbacks = pd.read_csv("feedbacks.csv")


interactions_unique = interactions.drop_duplicates(subset=["StudentID", "MentorID"])


merged = pd.merge(
    students,
    interactions_unique[["StudentID", "MentorID"]],
    on="StudentID",
    how="left"
)


grouped = merged.groupby("MentorID").agg({
    "MilestonesCompleted": "sum",
    "TotalMilestones": "sum"
}).reset_index()

grouped.rename(columns={
    "MilestonesCompleted": "Mc_sum",
    "TotalMilestones": "Mt_sum"
}, inplace=True)


grouped["base_ratio"] = grouped["Mc_sum"] / grouped["Mt_sum"].replace(0, np.nan)
grouped["scale"] = np.log1p(grouped["Mt_sum"])
grouped["P"] = grouped["base_ratio"] * grouped["scale"]
grouped["P"] = grouped["P"].fillna(0)

k = 0.5
grouped["P_final"] = 1 - np.exp(-k * grouped["P"])


resp = interactions.groupby("MentorID").agg({
    "AvgResponseTime": "mean"
}).reset_index()

t_bar = resp["AvgResponseTime"].mean()

resp["R"] = 2 ** (-resp["AvgResponseTime"] / t_bar)
resp["R"] = resp["R"].fillna(0)


w_meet = 0.5
w_review = 0.3
w_msg = 0.2

interactions["interaction_score"] = (
    w_meet * interactions["Meetings"] +
    w_review * interactions["CodeReviews"] +
    w_msg * interactions["Messages"]
)

eng = interactions.groupby("MentorID").agg({
    "interaction_score": "sum",
    "StudentID": "nunique"
}).reset_index()

eng["E_raw"] = eng["interaction_score"] / eng["StudentID"].replace(0, np.nan)

k_e = 0.1
eng["E"] = 1 - np.exp(-k_e * eng["E_raw"])
eng["E"] = eng["E"].fillna(0)


feedbacks["rating_norm"] = (feedbacks["Rating"] - 1) / 4
mu = feedbacks["rating_norm"].mean()
C = 3


mentor_stats = feedbacks.groupby("MentorID")["rating_norm"].agg(["mean", "std"]).reset_index()
mentor_stats.columns = ["MentorID", "mentor_mean", "mentor_std"]

feedbacks = feedbacks.merge(mentor_stats, on="MentorID", how="left")
feedbacks["mentor_std"] = feedbacks["mentor_std"].fillna(0)
feedbacks["z_score"] = np.where(
    feedbacks["mentor_std"] > 0,
    np.abs(feedbacks["rating_norm"] - feedbacks["mentor_mean"]) / feedbacks["mentor_std"],
    0
)
feedbacks["zscore_suspicious"] = feedbacks["z_score"] > 2


biased_students = (
    feedbacks.groupby("StudentID")["rating_norm"]
    .apply(lambda r: (r == 1.0).all() or (r == 0.0).all())
)
biased_students = biased_students[biased_students].index
feedbacks["student_suspicious"] = feedbacks["StudentID"].isin(biased_students)


feedbacks["weight"] = np.where(
    feedbacks["zscore_suspicious"] | feedbacks["student_suspicious"],
    0.3, 1.0
)


def weighted_bayesian_f(group):
    w = group["weight"]
    r = group["rating_norm"]
    return ((w * r).sum() + C * mu) / (w.sum() + C)


fb = feedbacks.groupby("MentorID").apply(weighted_bayesian_f).reset_index()
fb.columns = ["MentorID", "F"]
fb["F"] = fb["F"].fillna(mu)



final = grouped.merge(resp, on="MentorID", how="left") \
               .merge(eng, on="MentorID", how="left") \
               .merge(fb, on="MentorID", how="left")


w1 = 0.35  
w2 = 0.30  
w3 = 0.20  
w4 = 0.15  

final["M"] = (
    w1 * final["P_final"] +
    w2 * final["R"] +
    w3 * final["E"] +
    w4 * final["F"]
)

# NOTE: Score Evolution and Activity Decay, both are described in the Ideation Document.

final = final.sort_values(by="M", ascending=False)
final["Rank"] = range(1, len(final) + 1)

final = final.merge(mentors[["MentorID", "Name"]], on="MentorID", how="left")


print(final[["MentorID", "Name", "M", "Rank"]].to_string(index=False))

final[["MentorID", "Name", "M", "Rank"]] \
    .to_csv("mentor_scores.csv", index=False)