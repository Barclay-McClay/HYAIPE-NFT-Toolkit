# First we import some python libraries we are going to use
from graphqlclient import GraphQLClient     # This one allows us to get data from stargaze's GraphQL API
import requests # This one lets us request json metadata from stargaze
import json     # This one lets us deal with json data in python
import re       # This one lets us deal with regEx in python
import csv      # This one lets us deal with .csv files
from datetime import datetime # This lets us get the date and time. so we can put a 'timestamp' on the data we output for our records.

# Define the API endpoints we want to use
graphClient = GraphQLClient('https://constellations-api.mainnet.stargaze-apis.com/graphql')
stargaze_ipfs_endpoint = 'https://ipfs-gw.stargaze-apis.com/ipfs/'

# Define the address of the collections we're looking at:
collection_gems = 'stars1cy07wza4phppn7nmrsspps3ugpqa9enlgqz85v6edqxs9p6sukpshjp6ln'
# We need to collect ipfs metadata about the Space Terminators if we want to learn their gemstone trait
# So we'll store both the collection address and the ipfs path in this variable
# We'll need the same data for new collections also,
# So we'll put them in all an array that we'll iterate through:
collection_spaceTerminators = [
    # Original 'Space Terminators' collection
    {'name': 'Original Space Terminators collection', 'addr': 'stars14n286kjtlwht3myguwrztmmp2fgzksamw96na42k76kceu7xvhqqkzz64z', 'ipfs': 'QmSdfAyqAqCk8GK9FGiBwLoCNeEq7nHttgF66s9MmYo2K1'},
    # Space Terminators PT1
    {'name': 'Space Terminators PT1', 'addr': 'stars1vq8r4hp5wusj83ssmuev82zlpve0rtk5fqked6y2rk0ph7hsrj3qe0u6mg', 'ipfs': 'QmU6DVwWmbunYFTw5zPaYZLPi6Ze9LAwVAkQt1DDZD7Fyx'},
    # Alterations V1
    {'name': 'Alterations V1', 'addr': 'stars1ekcst4xkv09y7zfpd55vmcfsnlc3d989vnvchn6m6a863fp8uulqxw44xy', 'ipfs': 'QmTcLMR7NWSEuEGeM7eTPG4ixW4kRihQEiPkePMSXddjm1'}
    # As more collections are released, they need to be added to this array in the same format as the others, and *in order*.
]

# Define the fuctions we are going to use to access the API

# This one is a GraphQL query that collects some token data we'll need
def get_tokensByCollection(collectionAddr):
    # Results are paginated, so we'll iterate through the pages to build our list
    limit = 100 # set the maximum number of results per page
    offset = 0 # start at the first page
    all_tokens = [] # create a list to store all the results
    while True: # We don't want this to accidently loop forever
        try: # Since we're risking a 'while true', we'll wrap our stuff in a try/except as a failsafe
            # construct the query with pagination arguments
            query = f'''
            query Tokens {{
                tokens(collectionAddr: "{collectionAddr}", limit: {limit}, offset: {offset}) {{
                    tokens {{
                        collectionAddr
                        tokenId
                        name
                        mintedAt
                        ownerAddr
                    }}
                }}
            }}
            '''
            # make the request
            response = json.loads(graphClient.execute(query))['data']['tokens']['tokens']
            # add the results to the list
            all_tokens.extend(response)
            print(f"{str(len(all_tokens))} tokens found...")
            # if the number of results returned is less than the limit,
            # we have reached the end of the results and can stop paginating
            if len(response) < limit:
                break # Break the 'while true' loop
            # or, if we're still going, increment the offset to request the next page
            offset += limit
        except: # If anything goes wrong
            print(f'Something went wrong while querying {collectionAddr}')
            break # break the 'while true' loop
    return all_tokens

# The previous function `get_tokensByCollection` retrieves (among other things) the 'tokenId' of tokens in a collection.
# We'll use the tokenId in this function to retrieve the ipfs metadata of a token from stargaze, and return it as a json dictionary
def get_tokenMetadata(collection,tokenID):
    response = requests.get(stargaze_ipfs_endpoint+collection['ipfs']+'/'+str(tokenID)+'.json')
    if response.status_code == 200:
        return response.json()
    else:
        print("Error retrieving data from API")

# Using `get_tokensByCollection` and `get_tokenMetadata`, with the collection adresses we defined earlier;
# We can trawl through all the Space Terminator collections and build a *current* list of all the Space Terminators, who owns them, etc.
def newSpaceTerminatorData():
    global s_t
    s_t = []
    for collection in collection_spaceTerminators: # Iterate through all our collections
        graphData = get_tokensByCollection(collection['addr'])
        print(f"{str(len(graphData))} tokens to parse in {collection['name']}...")
        # Now we'll iterate through each Space Terminator token in the collection
        for token in graphData:
            print(token['name'])
            token['collectionName'] = collection['name']
            if token['name'] is not None:
            # Get each token's metadata
                meta = get_tokenMetadata(collection,token['tokenId'])
                # Update the token object to include the metadata we want (we mainly want the gemstone attribute)
                for attribute in meta['attributes']:
                    token[attribute['trait_type']] = attribute['value']
                # Check if token with same tokenId exists in SPACE_TERMINATORS
                existing_token = next((t for t in s_t if t['Name'] == token['Name']), None)
                if existing_token:
                    # Override the existing token with the newer one
                    s_t[s_t.index(existing_token)] = token
                else:
                    # If its not in the list already, add it
                    s_t.append(token)
    # Now that we've iterated throuh all these collections, we'll dump all this data into a log file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"SpaceTerminator_Log_{timestamp}.json", "w") as outfile:
        json.dump(s_t, outfile)
    #...And finally, we'll pass the data back to the variable that called this function
    return s_t

# We've got some pre-defined limits to our gemstone supply.
# Let's make a dictionary of gemstones as a record to help us
# This will also help make sure we do the gemstones in the proper order
gem_data = [
        ('Amazonite', 1, 72),
        ('Amethyst', 73, 360),
        ('Black Opal', 361, 516),
        ('Blackberry Diamond', 517, 540),
        ('Blueberry Diamond', 541, 624),
        ('Cotton Candy Quartz', 625, 912),
        ('Emerald', 913, 1488),
        ('Energy', 1489, 2316),
        ('Kyanite', 2317, 2412),
        ('Lavender Rose Quartz', 2413, 2568),
        ('Merlinite', 2569, 2616),
        ('Obsidian', 2617, 2784),
        ('Peridot', 2785, 2832),
        ('Quartz', 2833, 2916),
        ('Rose Quartz', 2917, 3024),
        ('Ruby', 3025, 3252),
        ('Sapphire', 3253, 3924),
        ('Spider Web Jasper', 3925, 4056),
        ('Synthetic Amethyst', 4057, 4068),
        ('Synthetic Emerald', 4069, 4104),
        ('Synthetic Sapphire', 4105, 4224),
        ('Unknown', 4225, 5124),
        ('Watermelon Diamond', 5125, 5136),
        ('Yellow Diamond', 5137, 5388),
        ('Piemontite', 5389, 5588),
        ('Nagamani', 5589, 6020),
        ('Hope Diamond', 6021, 6308),
        ('Synthetic Ruby', 6309, 6824),
        ('Earth', 6825, 7556)
    ]
GEM_DICT = [{'name': d[0], 'firstId': str(d[1]), 'lastId': str(d[2])} for d in gem_data]

################################################################################################
# Ok so now we've defined some important variables and some functions to use in our script.
# But we haven't actually *done* anything. Only defined some instuction sets for what we *want* to do.
# Let's actually start doing the things:
print("Gathering Space Terminator collection and generating log...")
SPACE_TERMINATORS = newSpaceTerminatorData()

print("Gathering Gemstone collection...")
GEMSTONE_TOKENS = get_tokensByCollection(collection_gems)

# It takes a few minutes to query all the space terminator data.
# So I've got this code-scrap that lets us "skip" that step and go off of old log data.
"""
filename = "SpaceTerminator_Log_XXXXXXXX_XXXXXX.json"
with open(filename, "r") as infile:
    SPACE_TERMINATORS = json.load(infile)

filename = "GemstoneTokenDumpXXXXXXXX_XXXXXX.json"
with open(filename, "r") as infile:
    GEMSTONE_TOKENS = json.load(infile)
"""

LEDGER = [] # We're going to populate this `LEDGER` array
# Let's organise the Space Terminators by their 'Gemstone' trait
GEM_TRAITS = {}
highestGemTokenId = {}
for gem in GEM_DICT:
    GEM_TRAITS[gem['name']] = []
    for ST in SPACE_TERMINATORS:
        if ST['Gemstone'] == gem['name']:
            GEM_TRAITS[gem['name']].append(ST)
    highestGemTokenId[gem['name']] = int(gem['firstId']) # This is where gemstone id #s 'begin' for each gemstone
# Iterate through the gemstone tokens, and find the 'last' tokenId that has been airdropped
for gem in GEMSTONE_TOKENS:
    # First we gotta do a bit of janky stuff to get the gemstone's name
    gemName = re.search(r"'(.+?)'", gem['name']).group(1) # Extract the gem's name from the token's name, which will be something like "💎 01 'Amazonite' DNA Altering Gemstone 💎"
    # Some of the gemstones' names dont match exactly with Space Terminators' Gemstone property. Gotta rectify that manually:
    if gemName == 'Blackberry':
        gemName = 'Blackberry Diamond'
    elif gemName == 'Blueberry':
        gemName = 'Blueberry Diamond'
    elif gemName == 'Watermelon':
        gemName = 'Watermelon Diamond'
    elif gemName == 'Cotton Candy':
        gemName = 'Cotton Candy Quartz'
    if int(gem['tokenId']) > highestGemTokenId[gemName]: # if the tokenId of the gem we are looking at is larger than the id we currently have in the list- then replace it.
        highestGemTokenId[gemName] = int(gem['tokenId'])
# Now let's build that ledger
for gem in GEM_DICT:    # Iterate through our Gem dictionary, in order
    gemName = gem['name'] # Get the name of the gem we are looking at
    activeId=int(highestGemTokenId[gemName])+1 # We've found the tokenId of the *last* gem that was airdropped... so let's start with the *next* token
    gemsRemain = int(gem['lastId'])-int(highestGemTokenId[gemName]) # Let's quickly check if we've got enough tokens of a particular gemstone
    print(f"{str(gemsRemain)} {gemName} remaining in supply...")
    print(f"{str(len(GEM_TRAITS[gemName]))} Gems to distribute. Starting at {str(activeId)}...")
    if len(GEM_TRAITS[gemName]) > gemsRemain:
        print(f"NOT ENOUGH {gemName} TOKENS TO DISTRIBUTE")
    else: # We've got enough gems? Great. Let's fill out the ledger now
        for ST in GEM_TRAITS[gemName]:
            print(f"{gemName} {str(activeId)} for {ST['Name']} from {ST['collectionName']}")
            LEDGER.append({'gemstone': gemName, 'tokenId': str(activeId), 'address': ST['ownerAddr'], 'terminator': ST['Name'], 'collection': ST['collectionName']})
            activeId+=1

# Write to CSV
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
with open(f'LEDGER_{timestamp}.csv', 'w', newline='') as csvfile:
    fieldnames = ['gemstone','tokenId', 'address','terminator','collection']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    # Write header row
    writer.writeheader()
    # Write data rows
    for row in LEDGER:
        writer.writerow(row)
        