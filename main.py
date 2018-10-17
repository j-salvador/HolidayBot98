import random
from discord.ext.commands import Bot

BOT_PREFIX = ("?", "!")
TOKEN = 'NTAyMDAxNjYwMDI2MDI4MDUz.DqhlYg.OnTEBxq9p6HigbXNAKyYO15MwvQ'
client = Bot(command_prefix=BOT_PREFIX)

action = ""
city = ""
country = ""
character = ""
specific_location = ""


def random_line(filename):
    file = open(filename, "r")
    line = next(file)
    for num, aline in enumerate(file):
        if random.randrange(num + 2): continue
        line = aline
    return line


def get_country_from_code(code):
    data = open("fixed-countries.txt")

    for line in data:
        if code in line:
            return line.split('\t')[1][:-1]  # remove \n character by slicing

    return "Incorrect code; cannot find country"


def generate_scenario():
    location = random_line("fixed-cities.txt")
    location = location.split('\t')
    print(location)

    country_code = location[0]
    city = location[1][:-1]  # remove \n char at end by slicing
    print("Country code:", country_code)
    print("City:", city)

    # Find country by country code
    country = get_country_from_code(country_code)
    print("Country:", country)

    # Get action
    action = random_line("Verbs.txt")[:-1]
    print("Action:", action)

    # Get character
    character = random_line("Personas.txt")[:-1]

    # Get specific location
    specific_location = random_line("specific-locations.txt")[:-1]

    print("\n\nCollated output:")
    return action + " in " + specific_location + ' ' + city + ", " + country + " with " + character


@client.command(name='holiday',
                description="Generates a holiday with a random activity, location and accomplice",
                aliases=['Holiday', 'hol', 'Hol'])
async def holiday():
    await client.say(generate_scenario())


@client.command(name='submit',
                description="Accepts a submission to a specified category")
async def submit():
    pass



client.run(TOKEN)