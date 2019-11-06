try:
    import fortnitepy
    from fortnitepy.errors import Forbidden
    import BenBotAsync, asyncio, datetime, json, livejson, aiohttp, time, logging, sys, random
    import getpass
    from colorama import init
    init(autoreset=True)
    from colorama import Fore, Back, Style
    from time import sleep
    import warnings
except ModuleNotFoundError:
    print('\u001b[31m' + f'[FORTNITEPY] [N/A] [ERROR] Failed to import 1 or more modules, run "INSTALL PACKAGES.bat".')
    exit()

time = datetime.datetime.now().strftime('%H:%M:%S')
print('\033[1m' + f'[FORTNITEPY] [{time}] fortnitepy-bot made by xMistt. credit to Terbau for creating the library.')
print('\033[1m' + f'[FORTNITEPY] [{time}] Thanks to the contributors: Alexa, TheClassic36 & Wishinn.')

warnings.filterwarnings("ignore", category=DeprecationWarning) 
def debugOn():
    logger = logging.getLogger('fortnitepy.xmpp')
    logger.setLevel(level=logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

with open('config.json') as f:
    print(f'[FORTNITEPY] [{time}] Loading config.')
    data = json.load(f)[0]
    print(f'[FORTNITEPY] [{time}] Config loaded.')
    
if data['debug'] == True:
    print(f'[FORTNITEPY] [{time}] Debug logging is on, prepare for a shitstorm.')
    debugOn()
    
else:
    print(f'[FORTNITEPY] [{time}] Debug logging is off.')
try:
    client = fortnitepy.Client(
        email=data['email'],
        password=data['password'],
        status=data['status'],
        platform=fortnitepy.Platform(data['platform'])
    )
except ValueError:
    print(f"[FORTNITEPY] [{time}] Found issue with initial settings, resetting status and platform")
    plat = "WIN"
    status = None
    client = fortnitepy.Client(
        email=data['email'],
        password=data['password'],
        status=status,
        platform=plat
    )

@client.event
async def event_ready():
    print("",end=None,flush=True)
    print(Fore.GREEN + '[FORTNITEPY] [' + time + '] Client ready as {0.user.display_name}. '.format(client))

@client.event
async def event_party_invite(invite):
    await invite.accept()
    print(f'[FORTNITEPY] [{time}] Accepted party invite from {invite.author.display_name}.')

@client.event
async def event_friend_request(request):
    print(f"[FORTNITEPY] [{time}] Recieved friend request from: {request.display_name}.")

    if data['friendaccept'].lower() == True:
        await request.accept()
        print(f"[FORTNITEPY] [{time}] Accepted friend request from: {request.display_name}.")
    if data['friendaccept'].lower() == False:
        await request.decline()
        print(f"[FORTNITEPY] [{time}] Declined friend request from: {request.display_name}.")

@client.event
async def event_party_member_join(member):
    variants = client.user.party.me.create_variants(**{data['variants-type']: data['variants']})
    if member.id == client.user.id:
        try:
            skin = await BenBotAsync.getSkinId(data["cid"])
            print(f"[FORTNITEPY] [{time}] Selected skin as {skin}")
        except KeyError:
            skin = None
        try:
            emote = await BenBotAsync.getEmoteId(data["eid"])
        except KeyError:
            emote = None
        try:
            backbling = await BenBotAsync.getBackpackId(data["bid"])
        except KeyError:
            backbling = None
        try:
           pickaxe = await BenBotAsync.getPickaxeId(data["pid"])
        except KeyError:
            pickaxe = None
        await client.user.party.me.set_outfit(asset=skin, variants=variants)
        await asyncio.sleep(0.1)
        await client.user.party.me.set_backpack(asset=backbling)
        await asyncio.sleep(0.1)
        await client.user.party.me.set_pickaxe(asset=pickaxe)
        await asyncio.sleep(0.1)
        await client.user.party.me.set_banner(data['banner'], data['banner_colour'], data['level'])
        await asyncio.sleep(0.5)
        await client.user.party.me.set_emote(asset=emote)
        await asyncio.sleep(0.1)
        await client.user.party.me.set_battlepass_info(has_purchased=True, level=data['bp_tier'], self_boost_xp='0', friend_boost_xp='0')
    
    if client.user.display_name != member.display_name:
        print(f"[FORTNITEPY] [{time}] {member.display_name} has joined the lobby.")

@client.event
async def event_friend_message(message):
    contetaaa = message.content
    args = message.content.split()
    contet = contetaaa.replace(args[0] + " ", "")
    print('[FORTNITEPY] [' + time + '] {0.author.display_name}: {0.content}'.format(message))

    if "!skin" in args[0].lower():
        id = await BenBotAsync.getSkinId(contet)
        if id == None:
            await message.reply(f"Couldn't find a skin with the name: {contet}")
        else:
            await client.user.party.me.set_outfit(asset=id)
            await message.reply('Skin set to ' + id)
            print(f"[FORTNITEPY] [{time}] Set Skin to: " + id)
        
    if "!backpack" in args[0].lower():
        id = await BenBotAsync.getBackpackId(contet)
        if id == None:
            await message.reply(f"Couldn't find a backpack with the name: {contet}")
        else:
            await client.user.party.me.set_backpack(asset=id)
            await message.reply('Backpack set to ' + id)
            print(f"[FORTNITEPY] [{time}] Set Backpack to: " + id)

    if "!emote" in args[0].lower():
        await client.user.party.me.clear_emote()
        id = await BenBotAsync.getEmoteId(contet)
        if id == None:
            await message.reply(f"Couldn't find an emote with the name: {contet}")
        else:
            await client.user.party.me.set_emote(asset=id)
            await message.reply('Skin set to ' + id)
            print(f"[FORTNITEPY] [{time}] Set Emote: " + id)

    if "!pickaxe" in args[0].lower():
        id = await BenBotAsync.getPickaxeId(contet)
        if id == None:
            await message.reply(f"Couldn't find a pickaxe with the name: {contet}")
        else:
            await client.user.party.me.set_pickaxe(asset=id)
            await message.reply('Pickaxe set to ' + id)
            print(f"[FORTNITEPY] [{time}] Set Pickaxe to: " + id)

    if "!pet" in args[0].lower():
        id = await BenBotAsync.getPetId(contet)
        await client.user.party.me.set_backpack(
                asset="/Game/Athena/Items/Cosmetics/PetCarriers/" + id + "." + id
        )

        await message.reply('Pet set to ' + id)
        print(f"[FORTNITEPY] [{time}] Client's PetCarrier set to: " + id)

    if "!emoji" in args[0].lower():
        id = await BenBotAsync.getEmoteId(contet)
        await client.user.party.me.clear_emote()
        await client.user.party.me.set_emote(
                asset="/Game/Athena/Items/Cosmetics/Dances/Emoji/" + id + "." + id
        )

        await message.reply('Emoji set to ' + id)
        print(f"[FORTNITEPY] [{time}] Client's Emoji set to " + id)

    if "!purpleskull" in args[0].lower():
        variants = client.user.party.me.create_variants(
           clothing_color=1
        )

        await client.user.party.me.set_outfit(
            asset='CID_030_Athena_Commando_M_Halloween',
            variants=variants
        )

        await message.reply('Skin set to Purple Skull Trooper!')

    if "!pinkghoul" in args[0].lower():
        variants = client.user.party.me.create_variants(
           material=3
        )

        await client.user.party.me.set_outfit(
            asset='CID_029_Athena_Commando_F_Halloween',
            variants=variants
        )

        await message.reply('Skin set to Pink Ghoul Trooper!')

    if "!brainiacghoul" in args[0].lower():
        variants = client.user.party.me.create_variants(
           material=2
        )

        await client.user.party.me.set_outfit(
            asset='CID_029_Athena_Commando_F_Halloween',
            variants=variants
        )

        await message.reply('Skin set to Brainiac Ghoul Trooper!')

    if "!purpleportal" in args[0].lower():
        variants = client.user.party.me.create_variants(
            item='AthenaBackpack',
            particle_config='Particle',
            particle=1
        )

        await client.user.party.me.set_backpack(
            asset='BID_105_GhostPortal',
            variants=variants
        )

        await message.reply('Backpack set to Purple Ghost Portal!')

    if "!banner" in args[0].lower():
        if len(args) == 1:
            await message.reply('You need to specify which banner, color & level you want to set the banner as.')
        if len(args) == 2:
            await client.user.party.me.set_banner(icon=args[1], color=data['banner_colour'], season_level=data['level'])
        if len(args) == 3:
            await client.user.party.me.set_banner(icon=args[1], color=args[2], season_level=data['level'])
        if len(args) == 4:
            await client.user.party.me.set_banner(icon=args[1], color=args[2], season_level=args[3])

        await message.reply(f'Banner set to; {args[1]} {args[2]} {args[3]}')
        print(f"[FORTNITEPY] [{time}] Banner set to; {args[1]} {args[2]} {args[3]}")

    if "CID_" in args[0]:
        await client.user.party.me.set_outfit(
            asset=args[0]
        )

        await message.reply(f'Skin set to {args[0]}')
        await print(f'[FORTNITEPY] [{time}] Skin set to ' + args[0])

    if "!variants" in args[0]:
        args3 = int(args[3])

        if 'CID' in args[1]:
            variants = client.user.party.me.create_variants(**{args[2]: args3})
            await client.user.party.me.set_outfit(
                asset=args[1],
                variants=variants
            )
        elif 'BID' in args[1]:
            variants = client.user.party.me.create_variants(item='AthenaBackpack', **{args[2]: args3})
            await client.user.party.me.set_backpack(
                asset=args[1],
                variants=variants
            )
        elif 'PICKAXE_ID' in args[1]:
            variants = client.user.party.me.create_variants(item='AthenaPickaxe', **{args[2]: args3})
            await client.user.party.me.set_pickaxe(
                asset=args[1],
                variants=variants
            )

        await message.reply(f'Set variants of {args[1]} to {args[2]} {args[3]}.')
        print(f'[FORTNITEPY] [{time}] Set variants of {args[1]} to {args[2]} {args[3]}.')

    if "!checkeredrenegade" in args[0].lower():
        variants = client.user.party.me.create_variants(
           material=2
        )

        await client.user.party.me.set_outfit(
            asset='CID_028_Athena_Commando_F',
            variants=variants
        )

        await message.reply('Skin set to Checkered Renegade!')

    if "EID_" in args[0]:
        await client.user.party.me.clear_emote()
        await client.user.party.me.set_emote(
            asset=args[0]
        )
        await message.reply('Emote set to ' + args[0] + '!')
        
    if "!stop" in args[0].lower():
        await client.user.party.me.clear_emote()
        await message.reply('Stopped emoting.')

    if "BID_" in args[0]:
        await client.user.party.me.set_backpack(
            asset=args[0]
        )

        await message.reply('Backbling set to ' + message.content + '!')

    if "!help" in args[0].lower():
        await message.reply('For a list of commands, goto: https://github.com/xMistt/fortnitepy-bot/blob/master/README.md')

    if "PICKAXE_ID_" in args[0].lower():
        await client.user.party.me.set_pickaxe(
                asset=args[0]
        )

        await message.reply('Pickaxe set to ' + args[0] + '!')

    if "PetCarrier_" in args[0]:
        await client.user.party.me.set_backpack(
                asset="/Game/Athena/Items/Cosmetics/PetCarriers/" + args[0] + "." + args[0]
        )

    if "Emoji_" in args[0]:
        await client.user.party.me.set_emote(asset='EID_ClearEmote')
        await client.user.party.me.set_emote(
                asset="/Game/Athena/Items/Cosmetics/Dances/Emoji/" + args[0] + "." + args[0]
        )

    if "!legacypickaxe" in args[0].lower():
        await client.user.party.me.set_pickaxe(
                asset=args[1]
        )

        await message.reply('Pickaxe set to ' + args[1] + '!')

    if "!ready" in args[0].lower():
        await client.user.party.me.set_ready(True)
        await message.reply('Ready!')

    if ("!unready" in args[0].lower()) or ("!sitin" in args[0].lower()):
        await client.user.party.me.set_ready(False)
        await message.reply('Unready!')

    if "!sitout" in args[0].lower():
        await client.user.party.me.set_ready(None)
        await message.reply('Sitting Out!')

    if "!bp" in args[0].lower():
        await client.user.party.me.set_battlepass_info(has_purchased=True, level=args[1], self_boost_xp='0', friend_boost_xp='0')

    if "!level" in args[0].lower():
        await client.user.party.me.set_banner(icon=client.user.party.me.banner[0], color=client.user.party.me.banner[1], season_level=args[1])

    if "!echo" in args[0].lower():
        await client.user.party.send(contet)

    if "!status" in args[0].lower():
        await client.set_status(contet)

        await message.reply(f'Status set to {contet}')
        print(f'[FORTNITEPY] [{time}] Status set to {contet}.')

    if "!leave" in args[0].lower():
        await client.user.party.me.set_emote('EID_Wave')
        await asyncio.sleep(2)
        await client.user.party.me.leave()
        await message.reply('Bye!')
        print(f'[FORTNITEPY] [{time}] Left the party as requested by {message.author.display_name}.')

    if "!crash" in args[0].lower():
        await message.reply('Bye!')
        await client.user.party.me.set_emote('EID_Wave')
        await asyncio.sleep(2)
        await client.user.party.me.set_outfit('/Game/Athena/Items/Cosmetics/Characters//./')

    if "!kick" in args[0].lower():
        user = await client.fetch_profile(contet)
        member = client.user.party.members.get(user.id)
        if member is None:
            await message.reply("Couldn't find that user, are you sure they're in the party?")
        else:
            try:
                await member.kick()
                await message.reply(f"Kicked user: {member.display_name}.")
                print(f"[FORTNITEPY] [{time}] Kicked user: {member.display_name}")
            except Forbidden:
                await message.reply(f"Couldn't kick {member.display_name}, as the bot is not party leader.")
                print(Fore.RED + f"[FORTNITEPY] [{time}] [ERROR] Failed to kick member as the bot doesn't have the required permissions." + Fore.WHITE)

    if "!promote" in args[0].lower():
        if len(args) != 1:
            user = await client.fetch_profile(contet)
            member = client.user.party.members.get(user.id)
        if len(args) == 1:
            user = await client.fetch_profile(message.author.display_name)
            user = await client.user.party.members.get(user.id)

        if member is None:
            await message.reply("Couldn't find that user, are you sure they're in the party?")
        else:
            try:
                await member.promote()
                await message.reply(f"Promoted user: {member.display_name}.")
                print(f"[FORTNITEPY] [{time}] Promoted user: {member.display_name}")
            except Forbidden:
                await message.reply(f"Couldn't promote {member.display_name}, as I'm not party leader.")
                print(Fore.RED + f"[FORTNITEPY] [{time}] [ERROR] Failed to promote member as I don't have the required permissions." + Fore.WHITE)

    if "!join" in args[0]:
        try:
            _friend = await client.fetch_profile_by_display_name(args[1])
            fid = _friend.id
            friend = client.get_friend(fid)
            if friend != None:
                await client.join_to_party(friend.party_id)
            await message.reply(f"Joining {message.author.display_name}'s party...")
        except Exception as e:
            await message.reply(f"""Failed to join to {message.author.display_name}'s party \n 
            error code: {e}""")

    if "Playlist_" in args[0]:
        try:
            await client.user.party.set_playlist(playlist=args[0])
        except Forbidden:
                await message.reply(f"Couldn't set gamemode to {args[1]}, as I'm not party leader.")
                print(Fore.RED + f"[FORTNITEPY] [{time}] [ERROR] Failed to set gamemode as I don't have the required permissions." + Fore.WHITE)

    if "!platform" in args[0]:
        await message.reply('Setting platform to ' + args[1] + '.')
        party_id = client.user.party.id
        await client.user.party.me.leave()
        client.platform = fortnitepy.Platform(args[1])
        await message.reply('Platform set to ' + str(client.platform) + '.')
        try:
            await client.join_to_party(party_id, check_private=True)
        except fortnitepy.Forbidden:
            await message.reply('Failed to join back as party is set to private.')

if data['email'] != "" and data['password'] != "":
    client.run()
else:
    print(Fore.RED + f"[FORTNITEPY] [{time}] [ERROR] Couldn't find email & password in config." + Fore.WHITE)
    data['email'] = input('Email: ')
    data['password'] = getpass.getpass()
    exit()

