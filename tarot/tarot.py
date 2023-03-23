from redbot.core import commands
from redbot.core.bot import Red
import discord 
import random
_author_ = "GeeterSkeeter#8008"
class Tarot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.image_list = {
    "https://imgur.com/6InvUMk": 'If you are experiencing health issues The Hierophant Tarot card indicates that conventional medicine may be the best route for you at the moment.',
    "https://imgur.com/fLJyhSd": 'The Emperor represents a powerful leader who demands respect and authority. Status, power, and recognition are essential to you.',
    "https://imgur.com/2Aq2Jj9": 'The Hanged Man reminds you that sometimes you have to put everything on hold before you can take the next step, or the Universe will do it on your behalf',
    "https://imgur.com/wpSC04a": 'The Justice card represents justice, fairness, truth and the law. You are being called to account for your actions and will be judged accordingly. If you have acted in alignment with your Higher Self and for the greater good of others, you have nothing to worry about.',
    "https://imgur.com/FlWWVll": 'The Sun card represents happiness, joy, success, and abundance. It is a card of optimism and good fortune, and it is a reminder that you are on the right path. The Sun  It can represent the end of a relationship, a job, a phase of life, or even a way of thinking. It can also represent the end of a cycle and the beginning of a new one.',
    "https://imgur.com/GPJTZVt": 'The Death card represents endings and new beginnings. It is a card of transformation and change, and it is a reminder that nothing lasts forever. The Death  It can represent the end of a relationship, a job, a phase of life, or even a way of thinking.',
    "https://imgur.com/hgWk1HG": 'The Judgment card advises that you allow yourself to grow, transform, and release hidden potentials within yourself. Divest yourself of fruitless endeavors without neglecting your duties. At the same time, invest your energies in new growth.',
    "https://imgur.com/h0ARvwe": 'The World card may be giving you permission to do whatever you want. Presently, your motivation is close to the will of the divine. Even if you commit an error, it will be turned to the greater good. Stay active and just keep moving forward. It is unnecessary to keep checking or interrupting your spontaneity with calculation.',
    "https://imgur.com/fIfbvPV": 'The Devil card advises that you show some spunk. There may be nothing to be gained by trying to be subtle or strategic in this situation. Assert your agenda, express yourself honestly, and let the chips fall where they may. Your best bet could be to express your true emotions, possibly even including anger. Acknowledge that you have whatever feelings you have.',
    "https://imgur.com/6Dt1exH": 'The Hermit advises that you think things through carefully. The demands on you have been high, giving you scant time for reflection. While you have a gift for understanding the larger implications involved, you need some private time to consider the steps to take in the future.',
    "https://imgur.com/wV1ZJDt": 'Have faith in your innate creativity. The Magician advises you give your questioning nature and free-associating mind plenty of room to explore the subject at hand. Behave just as if you were an open-minded and curious scientist.',
    "https://imgur.com/LDm6xw1": 'The High Priestess advises you to adhere to your chosen spiritual practice on a more regular basis. If you want the benefits of evolution, youll have to cooperate with spirit. We all have distractions, demands, a whole life full of reasons why we cannot find the time to retreat into our inner sanctum.',
    "https://imgur.com/YdSWV2f": 'The Lovers card advises that you study your options and make the wisest choice. Carefully consider your long-term interests. There is no judgment on what you choose to keep from the array of possibilities before you.',
    "https://imgur.com/PGVH9XS": 'With the Tower card, think of yourself as an agent of transformation. This self-sacrificing role is likely to create stressful situations. Your vision shows you that a radical change has already been unleashed by forces much larger than mere mortals, and therefore you are no longer resisting.',
    "https://imgur.com/IZWSqEN": 'The Wheel of Fortune advises you follow the flow of events. Physical moves, spiritual awakenings, or dramatically changing social patterns could arise now. Accept these transformations',
    "https://imgur.com/HAm9OgK": 'The Empress advises you to trust in the good sense you have shown up to this point. Recognize your good intentions in carrying out your responsibilities as a compassionate human. You are capable of demonstrating the finest aspects of your personality.',
    "https://imgur.com/hpWmol3": 'The Chariot advises that you be prepared for changes that might include a move or an opportunity to travel. The Charioteer travels light and stays open to fresh experiences that change with every valley or mountain pass.',
    "https://imgur.com/FmS6Sug": 'The Temperance card advises you to identify and seek the missing ingredients in your life. Marshal your known skills and abilities and do what needs to be done to complete your mission.',
    "https://imgur.com/Q94Zr4s": 'The Star card reversed suggests that you are temporarily alienated from your brilliance and usefulness. You may feel clumsy, unskilled, at odds within your true nature.',
    "https://imgur.com/HmQws6j": 'The Moon card advises that you trust your instincts and intuitions. Your intuitive body, which is connected to all living things, is sharper and quicker than the cultivated, civilized self. The everyday mind may not be prepared for strange oceanic circumstances',
    "https://imgur.com/cm7PTAP": 'The Strength card advises that you assertively discipline yourself and separate self interest from enlightened wisdom. Deliberately identify with your intuition, even if it works against the desires of your willful ego.',
    "https://imgur.com/gallery/hhVp0GG": 'The Fool advises that you lighten up. Let yourself be spontaneous enough to stretch beyond the realm of logic. There is no advantage to be gained by thinking you possess the knowledge, power, or control to direct reality. Open and receive without question, instead of trying to manage whats happening right now',
        }
#this is the list of image urls and their tarot card names and readings
        self.client = discord.Client()

    @commands.command()
    async def tarot(self,ctx: commands.Context):

            #this just listens for the event of tarot being called

           #this is the randomizer for w random tarot card and reading to be pulled from the list above
        key = random.choice(list(self.image_list.keys()))
        image_url = key
        message = self.image_list[image_url]

            #this is send the image and reading to the channel 
        await ctx.send(image_url)
        await ctx.send(message)

        