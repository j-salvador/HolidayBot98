import random
from discord import Game
from discord.ext.commands import Bot

BOT_PREFIX = ("?", "!")
TOKEN = 'NTAyMDAxNjYwMDI2MDI4MDUz.DqhlYg.OnTEBxq9p6HigbXNAKyYO15MwvQ'
client = Bot(command_prefix=BOT_PREFIX)


def random_line(filename):
    """
        Randomly selects a line within a specified file.

        Parameters
        ----------
        filename : str
            Path of the desired file you want to retrieve the random line from.

        Returns
        -------
        line : str
            A random line within the specified file, in string format.
    """
    file = open(filename, "r")
    line = next(file)
    for num, aline in enumerate(file):
        if random.randrange(num + 2): continue
        line = aline
    return line


def get_country_from_code(code):
    """
        Retrieves the name of the country based off what code is passed in.

        Parameters
        ----------
        code : str
            A 2-letter FIPS country code uniquely identifying a country.

        Returns
        -------
            The country that matches the FIPS code if successful, otherwise an error message.
    """
    try:
        data = open("fixed-countries.txt")

        for line in data:
            if code in line:
                return line.split('\t')[1][:-1]  # remove \n character by slicing

        return "Incorrect code; cannot find country"
    finally:
        data.close()


def generate_scenario():
    """
        Main function that generates each individual component making up the holiday, or scenario.
        Calls other functions to generate the city, country, action, and character.

        Returns
        -------
            The total string made up of all the components to create the holiday, or scenario.
    """
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

    return action + " in " + specific_location + ' ' + city + ", " + country + " with " + character


# TODO: Currently not needed in program. Will look into removing altogether
# @client.command(name='holiday',
#                 description="Generates a holiday with a random activity, location and accomplice",
#                 aliases=['Holiday', 'hol', 'Hol'])
# async def holiday():
#     await client.say(generate_scenario())


# @client.command(name='submit_person',
#                 description="Accepts a submission to the list of personas",
#                 aliases=['submitperson', 'submitPerson', 'Submitperson', 'SubmitPerson'])
# async def submit_person(value):
def submit_suggestion(filename, value):
    """
        Iterates through file, checks if submitted suggestion is present already. Writes to specified file,
        updating list.

        Parameters
        ----------
        filename : str
            Path of the desired file you want to update.
        value : str
            The user's input of the value to be saved out to file. Whatever new content they want to add to the existing
            database.

        Returns
        -------
            True if successfully written out to the file.
    """
    try:
        file = open(filename, "r")

        for line in file:
            if value not in line:
                if value is not None:
                    print("Value:", value)
                    write_to_file(filename, value)
                    return True
    finally:
        file.close()


def write_to_file(filename, value):
    """
        Saves desired value to specified file, adding onto it's existing contents.

        Parameters
        ----------
        filename : str
            Path of the desired file you want to write to.
        value : str
            The user's input of the value you want to save out to.
    """
    try:
        file = open(filename, 'a+')
        file.write(value + "\n")
        return True
    # except Exception as e:
    #     print(e)
    #     # TODO CHECK if does anything or works
    #     return False
    finally:
        file.close()


@client.event
async def on_message(message):
    """
        Asynchronous function that checks multiple conditional statements to see if a user's message begins with any
        keywords. These keywords invoke functions to generate a scenario or to submit content based off what the user's
        message is.

        Parameters
        ----------
        message : str
            User's message that is compared to 6 keywords to see if any action should be performed.

        Returns
        -------
            The message that will be posted in the chat box the user originally typed in. Posting either a holiday
            scenario or a message verifying the submission of content.
    """
    if message.content.upper().startswith("!HOLIDAY") or message.content.upper().startswith("!HOL"):
        await client.send_message(message.channel, generate_scenario())

    if message.content.upper().startswith("!SUBMITACTION") or message.content.upper().startswith("!SA"):
        content = message.content.split(" ")
        content = " ".join(content[1:])
        submit_suggestion("Verbs.txt", content)
        await client.send_message(message.channel, "Submission successfully accepted")

    if message.content.upper().startswith("!SUBMITPERSON") or message.content.upper().startswith("!SP"):
        print("message content:", message.content)
        content = message.content.split(" ")
        content = " ".join(content[1:])
        submit_suggestion("Personas.txt", content.title())
        await client.send_message(message.channel, "Submission successfully accepted")


@client.event
async def on_ready():
    """
        Sets the discord client to change it's presence (displayed game in discord client).
        Also prints the client's username when it has loaded.
    """
    await client.change_presence(game=Game(name="on holiday"))
    print("Logged in as " + client.user.name)


client.run(TOKEN)
