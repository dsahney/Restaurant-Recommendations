"""
A restaurant recommendation system.

Here are some example dictionaries.  These correspond to the information in
restaurants_small.txt.

Restaurant name to rating:
# dict of {str: int}
{'Georgie Porgie': 87,
 'Queen St. Cafe': 82,
 'Dumplings R Us': 71,
 'Mexican Grill': 85,
 'Deep Fried Everything': 52}

Price to list of restaurant names:
# dict of {str, list of str}
{'$': ['Queen St. Cafe', 'Dumplings R Us', 'Deep Fried Everything'],
 '$$': ['Mexican Grill'],
 '$$$': ['Georgie Porgie'],
 '$$$$': []}

Cuisine to list of restaurant names:
# dict of {str, list of str}
{'Canadian': ['Georgie Porgie'],
 'Pub Food': ['Georgie Porgie', 'Deep Fried Everything'],
 'Malaysian': ['Queen St. Cafe'],
 'Thai': ['Queen St. Cafe'],
 'Chinese': ['Dumplings R Us'],
 'Mexican': ['Mexican Grill']}

With this data, for a price of '$' and cuisines of ['Chinese', 'Thai'], we
would produce this list:

    [[82, 'Queen St. Cafe'], [71, 'Dumplings R Us']]
"""

# The file containing the restaurant data.
FILENAME = 'restaurants_small.txt'

def recommend(file, price, cuisines_list):
    """(file open for reading, str, list of str) -> list of [int, str] list 
    
    Find restaurants in file that are priced according to price and that are
    tagged with any of the items in cuisines_list.  Return a list of lists of
    the form [rating%, restaurant name], sorted by rating%.
    """
    
    # Read the file and build the data structures.
    # - a dict of {restaurant name: rating%}
    # - a dict of {price: list of restaurant names}
    # - a dict of {cusine: list of restaurant names}
    name_to_rating, price_to_names, cuisine_to_names = read_restaurants(file)
    
    # Look for price or cuisines first?
    # Price: look up the list of restaurant names for the requested price.
    names_matching_price = price_to_names[price]
    
    # Now we have a list of restaurants in the right price range.
    # Need a new list of restaurants that serve one of the cuisines.
    names_final = filter_by_cuisine(names_matching_price, cuisine_to_names, cuisines_list)

    # Now we have a list of restaurants that are in the right price range and serve the requested cuisine.
    # Need to look at ratings and sort this list.
    result = build_rating_list(name_to_rating, names_final)

    return result


def build_rating_list(name_to_rating, names_final):
    """ (dict of {str: int}, list of str) -> list of list of [int, str]
    Return a list of [rating%, restaurant name], sorted by rating% 

    >>> name_to_rating = {'Georgie Porgie': 87,
     'Queen St. Cafe': 82,
     'Dumplings R Us': 71,
     'Mexican Grill': 85,
     'Deep Fried Everything': 52}
    >>> names = ['Queen St. Cafe', 'Dumplings R Us']
    [[82, 'Queen St. Cafe'], [71, 'Dumplings R Us']]
    """
  
    new_list = []
    for z in names_final:
        if z in name_to_rating:
            new_list.append([int(name_to_rating[z]), z])
    sorted(new_list, reverse=True)
    return new_list


def filter_by_cuisine(names_matching_price, cuisine_to_names, cuisines_list):
    """ (list of str, dict of {str: list of str}, list of str) -> list of str 
    >>> names = ['Queen St. Cafe', 'Dumplings R Us', 'Deep Fried Everything']
    >>> cuis = 'Canadian': ['Georgie Porgie'],
     'Pub Food': ['Georgie Porgie', 'Deep Fried Everything'],
     'Malaysian': ['Queen St. Cafe'],
     'Thai': ['Queen St. Cafe'],
     'Chinese': ['Dumplings R Us'],
     'Mexican': ['Mexican Grill']}
    >>> cuisines = ['Chinese', 'Thai']
    >>> filter_by_cuisine(names, cuis, cuisines)
    ['Queen St. Cafe', 'Dumplings R Us']
    """
  
    list_accumulator = []
    for cuisine in cuisines_list:
        if cuisine in cuisine_to_names:
            for name in cuisine_to_names[cuisine]:
                if not name in list_accumulator: # or if name not in list_accumulator:
                    list_accumulator.append(name)
            
    names_final = []
    for x in names_matching_price:
        if x in list_accumulator:
            names_final.append(x)

    return names_final

    
def read_restaurants(file):
    """ (file) -> (dict, dict, dict)
    Return a tuple of three dictionaries based on the information in the file:
    - a dict of {restaurant name: rating%}
    - a dict of {price: list of restaurant names}
    - a dict of {cusine: list of restaurant names}
    """
# read the file line by line and accumulate info about the restaurants.
    name_to_rating = {}
    price_to_names = {'$': [], '$$': [], '$$$': [], '$$$$': []}
    cuisine_to_names = {}
    first_list = []
    file = open(FILENAME, 'r')
    for line in file:
        if line == '\n':
            name_to_rating[first_list[0]] = first_list[1]
            price_to_names[first_list[2]].append(first_list[0])

            for b in first_list[3].split(','):
                if b not in cuisine_to_names:
                    cuisine_to_names[b] = [first_list[0]]
                else:
                    cuisine_to_names[b].append(first_list[0])
            first_list = []
        else:
            first_list.append(line.rstrip('%\n'))
    name_to_rating[first_list[0]] = first_list[1]
    price_to_names[first_list[2]].append(first_list[0])
    for c in first_list[3].split(","):
        if c not in cuisine_to_names:
            cuisine_to_names[c] = [first_list[0]]
        else:
            cuisine_to_names[c].append(first_list[0])
    
    file.close()
    return name_to_rating, price_to_names, cuisine_to_names
