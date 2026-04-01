#   UserCycleStats
#     user_id (PK & FK → User)
#     avg_cycle_length_days (DECIMAL(5,2))
#     avg_period_length_days (DECIMAL(5,2))
#     streak_days_logged (int)
#     updated_at
#   UserPrediction
#     user_id (FK)
#     predicted_next_period_start_date (DATE)
#     confidence (0–1)
#     method (string, e.g., 'moving_average')
#     generated_at
