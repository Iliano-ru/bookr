def average_rating(rating_list):
    if not rating_list:
        return None
    return round(sum(rating_list)/len(rating_list))