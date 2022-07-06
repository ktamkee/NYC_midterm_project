from google_nearby_search import gPlaceSearch

def googleEnrich(df=nyc, radius=1000, query='restaurant'):
    """
    Takes a dataframe and returns an enriched copy of the df

    df (dataframe): must include columns 'latitude' AND 'longitude' AND an 'id' column
    radius (int): distance in meters to query for
    query (string): query string

    returns a dictionary sorted by neighborhood id:
    query_review_counts = [] - review counts per venue
    query_ratings = [] - ratings per venue
    price_levels = [] - price level per venue, some missing values
    query_counts = [] - venue counts per page
    """
    google_dict = {}

    # go through every row
    for row in df.itertuples():
        print(row.id)
        # get data from API
        response = gPlaceSearch(str(row.latitude), str(row.longitude), radius, query)

        # parse data and assign data to temporary lists
        query_counts = [len(page['results']) for page in response]

        query_review_counts = []
        query_ratings = []
        price_levels = []

        for page in response:
            for result in page['results']:
                query_review_counts.append(result['user_ratings_total'])
                query_ratings.append(result['rating'])

                # price_levels have null values, check and replace
                try:
                   price_levels.append(result['price_level'])
                except KeyError:
                   price_levels.append('?')

        # store lists into dict
        google_dict[row.id] = {
            query + '_counts': query_counts,
            query + '_review_counts': query_review_counts,
            query + '_ratings': query_ratings,
            query + '_price_levels': price_levels
        }
    return google_dict