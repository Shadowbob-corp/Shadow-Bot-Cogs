
from typing import Literal
import discord
import random
# Red
from redbot.core import  commands



author = "Jay_"
version = "0.0.5"

#12/7/2022 - v 0.0.5L: Fixed gay, added "The great gay " to the final line





class Fire(commands.Cog):

    def __init__(self, bot):
        self.bot = bot 
        self.fire_letters = {
            'a':'<a:A_:1033717912596385822>',
            'b':'<a:B_:1033717917478563970>',
            'c':'<a:C_:1033717922629165066>',
            'd':'<a:D_:1033717928824148038>',
            'e':'<a:E_:1033717935384047666>',
            'f':'<a:F_:1033717940912140359>',
            'g':'<a:G_:1033717945207111751>',
            'h':'<a:H_:1033717951146246155>',
            'i':'<a:I_:1033717955655118879>',
            'j':'<a:J_:1033717961736867871>',
            'k':'<a:K_:1033717968267391097>',
            'l':'<a:L_:1033717974009401404>',
            'm':'<a:M_:1033717979357130815>',
            'n':'<a:N_:1033717984251875380>',
            'o':'<a:O_:1033717992007147621>',
            'p':'<a:5132_Alphabet_P:1033717997153566761>',
            'q':'<a:5043_Alphabet_Q:1033718006414573598>',
            'r':'<a:1620_Alphabet_R:1033718024030650368>',
            's':'<a:1844_Alphabet_S:1033718029873328198>',
            't':'<a:6956_Alphabet_T:1033718037620195358>',
            'u':'<a:7484_Alphabet_U:1033718044192673803>',
            'v':'<a:4124_Alphabet_V:1033718048873529414>',
            'w':'<a:4253_Alphabet_W:1033718053596311643>',
            'x':'<a:7288_Alphabet_X:1033718058679812196>',
            'y':'<a:8187_Alphabet_Y:1033718064413417523>',
            'z':'<a:2635_Alphabet_Z:1033718069228478515>',
            '0':'<a:0_:1044940344833347584>',
            '1':'<a:1_:1044940347014397974>',
            '2':'<a:2_:1044940349077991434>',
            '3':'<a:3_:1044940350772490382>',
            '4':'<a:4_:1044940353188417586>',
            '5':'<a:5_:1044940354874511411>',
            '6':'<a:6_:1044940356707422248>',
            '7':'<a:7_:1044940358523572296>',
            '8':'<a:8_:1044940360662659092>',
            '9':'<a:9_:1044940362390704148>',
            ' ':'  ',
            '\'': '',
            '.': '',
            '"':'',
            '?':'',
            '!':'',
            '@':'',
            '#':'',
            '$':'',
            '%':'',
            '^':'',
            '&':'',
            '*':'',
            '(':'',
            ')':'',
            '-':'',
            '_':'',
            '+':'',
            '=':'',
            ',':',',
            ';':'',
            ':':'',
            '/':'',
            '\\':'',
            '|':'',
            '`':'',
            '~':''

        }

        self.fire2_letters = {
            'a':'<a:rflx_a:1044940364454301736>',
            'b':'<a:rflx_b:1044940366849257522>',
            'c':'<a:rflx_c:1044940368887681104>',
            'd':'<a:rflx_d:1044940371236499497>',
            'e':'<a:rflx_e:1044940373593686127>',
            'f':'<a:rflx_f:1044940375846043658>',
            'g':'<a:rflx_g:1044940378178068570>',
            'h':'<a:rflx_h:1044940380124229642>',
            'i':'<a:rflx_i:1044940381831315528>',
            'j':'<a:rflx_j:1044940384121393152>',
            'k':'<a:rflx_k:1044940386495373322>',
            'l':'<a:rflx_l:1044940388684791859>',
            'm':'<a:rflx_m:1044940391146864700>',
            'n':'<a:rflx_n:1044940393768300544>',
            'o':'<a:rflx_o:1044940396440068146>',
            'p':'<a:rflx_p:1044940398520438784>',
            'q':'<a:rflx_q:1044940400898617385>',
            'r':'<a:rflx_r:1044940403335512106>',
            's':'<a:rflx_s:1044940405352955925>',
            't':'<a:rflx_t:1044940407336861716>',
            'u':'<a:rflx_u:1044940409475969065>',
            'v':'<a:rflx_v:1044940411254341692>',
            'w':'<a:rflx_w:1044940413477343242>',
            'x':'<a:rflx_x:1044940415637405828>',
            'y':'<a:rflx_y:1044940417881342062>',
            'z':'<a:rflx_z:1044940420104343664>',
            '0':'<a:0_:1044940344833347584>',
            '1':'<a:1_:1044940347014397974>',
            '2':'<a:2_:1044940349077991434>',
            '3':'<a:3_:1044940350772490382>',
            '4':'<a:4_:1044940353188417586>',
            '5':'<a:5_:1044940354874511411>',
            '6':'<a:6_:1044940356707422248>',
            '7':'<a:7_:1044940358523572296>',
            '8':'<a:8_:1044940360662659092>',
            '9':'<a:9_:1044940362390704148>',
            ',':',',
            ' ':'  ',
            '\'': '',
            '.': '',
            '"':'',
            '?':'',
            '!':'',
            '@':'',
            '#':'',
            '$':'',
            '%':'',
            '^':'',
            '&':'',
            '*':'',
            '(':'',
            ')':'',
            '-':'',
            '_':'',
            '+':'',
            '=':'',
            ',':',',
            ';':'',
            ':':'',
            '/':'',
            '\\':'',
            '|':'',
            '`':'',
            '~':''
        }

        self.moist_letters = {
            'a':'<a:1720lettera:1044907909458444368>',
            'b':'<a:8076letterb:1044907910934835290>',
            'c':'<a:3909letterc:1044907916819447899>',
            'd':'<a:3119letterd:1044907922687279164>',
            'e':'<a:3445lettere:1044907918664945726>',
            'f':'<a:6078letterf:1044907915057823795>',
            'g':'<a:9787letterg:1044907913774379029>',
            'h':'<a:4474letterh:1044907931243642911>',
            'i':'<a:6685letteri:1044907929150689342>',
            'j':'<a:4474letterj:1044907912507686942>',
            'k':'<a:3031letterk:1044907920699162634>',
            'l':'<a:8792letterl:1044907923970719765>',
            'm':'<a:5109letterm:1044907927561052210>',
            'n':'<a:9516lettern:1044907925879136277>',
            'o':'<:SRCpentacleblack:1032658301143498813>',
            'p':'<a:7866letterp:1044907932514517012>',
            'q':'<a:2542letterq:1044907933948981319>',
            'r':'<a:8033letterr:1044907935995797555>',
            's':'<a:1964letters:1044907941322555412>',
            't':'<a:7857lettert:1044907939439329330>',
            'u':'<a:5693letteru:1044907937870659625>',
            'v':'<a:9199letterv:1044907943012880424>',
            'w':'<a:5293letterw:1044907944388595853>',
            'x':'<a:5293letterx:1044907947043598438>',
            'y':'<a:9019lettery:1044907945491709963>',
            'z':'<a:5842letterz:1044907948939411466>',
            '0':'<a:0_:1044940344833347584>',
            '1':'<a:1_:1044940347014397974>',
            '2':'<a:2_:1044940349077991434>',
            '3':'<a:3_:1044940350772490382>',
            '4':'<a:4_:1044940353188417586>',
            '5':'<a:5_:1044940354874511411>',
            '6':'<a:6_:1044940356707422248>',
            '7':'<a:7_:1044940358523572296>',
            '8':'<a:8_:1044940360662659092>',
            '9':'<a:9_:1044940362390704148>',
            ' ':'  ',
            '\'': '',
            '.': '',
            '"':'',
            '?':'',
            '!':'',
            '@':'',
            '#':'',
            '$':'',
            '%':'',
            '^':'',
            '&':'',
            '*':'',
            '(':'',
            ')':'',
            '-':'',
            '_':'',
            '+':'',
            '=':'',
            ',':',',
            ';':'',
            ':':'',
            '/':'',
            '\\':'',
            '|':'',
            '`':'',
            '~':''
        }

        self.moist_letters = {
            'a':'<a:1720lettera:1044907909458444368>',
            'b':'<a:8076letterb:1044907910934835290>',
            'c':'<a:3909letterc:1044907916819447899>',
            'd':'<a:3119letterd:1044907922687279164>',
            'e':'<a:3445lettere:1044907918664945726>',
            'f':'<a:6078letterf:1044907915057823795>',
            'g':'<a:9787letterg:1044907913774379029>',
            'h':'<a:4474letterh:1044907931243642911>',
            'i':'<a:6685letteri:1044907929150689342>',
            'j':'<a:4474letterj:1044907912507686942>',
            'k':'<a:3031letterk:1044907920699162634>',
            'l':'<a:8792letterl:1044907923970719765>',
            'm':'<a:5109letterm:1044907927561052210>',
            'n':'<a:9516lettern:1044907925879136277>',
            'o':'<:SRCpentacleblack:1032658301143498813>',
            'p':'<a:7866letterp:1044907932514517012>',
            'q':'<a:2542letterq:1044907933948981319>',
            'r':'<a:8033letterr:1044907935995797555>',
            's':'<a:1964letters:1044907941322555412>',
            't':'<a:7857lettert:1044907939439329330>',
            'u':'<a:5693letteru:1044907937870659625>',
            'v':'<a:9199letterv:1044907943012880424>',
            'w':'<a:5293letterw:1044907944388595853>',
            'x':'<a:5293letterx:1044907947043598438>',
            'y':'<a:9019lettery:1044907945491709963>',
            'z':'<a:5842letterz:1044907948939411466>',
            '0':'<a:0_:1044940344833347584>',
            '1':'<a:1_:1044940347014397974>',
            '2':'<a:2_:1044940349077991434>',
            '3':'<a:3_:1044940350772490382>',
            '4':'<a:4_:1044940353188417586>',
            '5':'<a:5_:1044940354874511411>',
            '6':'<a:6_:1044940356707422248>',
            '7':'<a:7_:1044940358523572296>',
            '8':'<a:8_:1044940360662659092>',
            '9':'<a:9_:1044940362390704148>',
            ' ':'  ',
            '\'': '',
            '.': '',
            '"':'',
            '?':'',
            '!':'',
            '@':'',
            '#':'',
            '$':'',
            '%':'',
            '^':'',
            '&':'',
            '*':'',
            '(':'',
            ')':'',
            '-':'',
            '_':'',
            '+':'',
            '=':'',
            ',':',',
            ';':'',
            ':':'',
            '/':'',
            '\\':'',
            '|':'',
            '`':'',
            '~':''
        }

        self.rainbow_letters = {
            'a':'<a:aa:1047788998480904295>',
            'b':'<a:bb:1047789060636282890>',
            'c':'<a:cc:1047789063131901993>',
            'd':'<a:dd:1047789421228990524>',
            'e':'<a:ee:1047789423217098814>',
            'f':'<a:ff:1047789425893064784>',
            'g':'<a:gg:1047789428174757908>',
            'h':'<a:hh:1047789430368391179>',
            'i':'<a:ii:1047789434487193610>',
            'j':'<a:jj:1047789436664029214>',
            'k':'<a:kk:1047789439268696095>',
            'l':'<a:ll:1047789450199060480>',
            'm':'<a:mm:1047789452556259368>',
            'n':'<a:nn:1047789455152521277>',
            'o':'<a:oo:1047789457312600084>',
            'p':'<a:pp:1047789459216810014>',
            'q':'<a:qq:1047789461511094292>' ,
            'r':'<a:rr:1047789463755038730>' ,
            's':'<a:ss:1047789466019962880>' ,
            't':'<a:tt:1047789468708524082>',
            'u':'<a:uu:1047789471497715712>',
            'v':' <a:9199letterv:1044907943012880424> ',
            'w':' <a:5293letterw:1044907944388595853> ',
            'x':' <a:5293letterx:1044907947043598438> ',
            'y':' <a:9019lettery:1044907945491709963> ',
            'z':' <a:5842letterz:1044907948939411466> ',
            '0':'<a:0_:1044940344833347584>',
            '1':'<a:1_:1044940347014397974>',
            '2':'<a:2_:1044940349077991434>',
            '3':'<a:3_:1044940350772490382>',
            '4':'<a:4_:1044940353188417586>',
            '5':'<a:5_:1044940354874511411>',
            '6':'<a:6_:1044940356707422248>',
            '7':'<a:7_:1044940358523572296>',
            '8':'<a:8_:1044940360662659092>',
            '9':'<a:9_:1044940362390704148>',
            ' ':'  ',
            '\'': '',
            '.': '',
            '"':'',
            '?':'',
            '!':'',
            '@':'',
            '#':'',
            '$':'',
            '%':'',
            '^':'',
            '&':'',
            '*':'',
            '(':'',
            ')':'',
            '-':'',
            '_':'',
            '+':'',
            '=':'',
            ',':',',
            ';':'',
            ':':'',
            '/':'',
            '\\':'',
            '|':'',
            '`':'',
            '~':''
        }


    async def emojify(self, ctx, emoji: str):
        
        
     
        if emoji[0] == ":" and emoji[-1] == ":":
            name = emoji.strip(":")
            print(name + ' 1')
            return discord.utils.get(ctx.guild.emojis, name=name) 
        elif emoji[0:2] == '<a:':
            name = emoji.split(':')[1].strip(':')
            print(name + ' 2')
            return discord.utils.get(ctx.guild.emojis, name=name)       

    @commands.command()
    async def cum(self, ctx):
        await ctx.send('''⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡖⠋⠉⠉⠙⢲⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⡿⠀⠀⠀⠀⠀⠀⠃⠀⣤⡄⠀⠠⣤⠀⠀⢤⡄⡠⠤⣤⡀⡠⠤⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⣿⠀⠀⢸⡏⠀⠀⢸⡇⠀⠀⢹⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣄⠀⠀⠀⠀⢀⠄⠀⢿⡇⠀⢀⣿⡀⠀⢸⡇⠀⠀⢸⡇⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠓⠒⠒⠊⠁⠀⠀⠈⠛⠒⠁⠛⠃⠐⠚⠛⠂⠐⠚⠓⠂⠐⠛⠓⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀''')

    @commands.command()
    async def rand(self, ctx: commands.Context, *message):
        rand_list = [self.rainbow_letters, self.moist_letters, self.fire_letters, self.fire2_letters]        
        t_str = ""
        m_str = ""
        rand_num = random.randint(0,len(rand_list)-1)
        
        if len(message) >1:
            for m in message:
                m_str = m_str +"  " +  m  
                m_str = m_str
        else:
            print(message)
            m_str = str(message[0])

        for a in m_str:
            if a is None:
                continue
            try:                    
                t_str += str(rand_list[random.randint(0,len(rand_list) - 1)][a.lower()])
            except Exception as isnt:

                await ctx.send(f'Invalid character in string: {a}')
                continue
        await ctx.send(t_str + '\n' + '- ' + ctx.author.mention)
        


    @commands.command()
    async def gay(self, ctx: commands.Context, *message):
        t_str = ""
        m_str = ""
        
        if len(message) >1:
            for m in message:
                m_str = m_str +"  " +  m  
                m_str = m_str
        else:
            m_str = str(message[0])
        for a in m_str:
            try:
                t_str = t_str + str(self.rainbow_letters[a.lower()])
            except:
                await ctx.send(f'Invalid character in string: {a}')
                continue
        await ctx.send(t_str + '\n' + '- The great gay ' + ctx.author.mention)


    @commands.command()
    async def rainbow(self, ctx: commands.Context, *message):
        t_str = ""
        m_str = ""
        
        if len(message) > 1:
            for m in message:
                m_str = m_str + "  " +  m  
                m_str = m_str
        else:
            m_str = str(message[0])
        for a in m_str:
            try:
                t_str = t_str + str(self.rainbow_letters[a.lower()])
            except:
                await ctx.send(f'Invalid character in string: {a}')
                continue
        await ctx.send(t_str + '\n' + '- ' + ctx.author.mention)


    @commands.command()
    async def moist(self, ctx: commands.Context, *message):
        t_str = ""
        m_str = ""
        
        if len(message) >1:
            for m in message:
                m_str = m_str + "  " + m 
                m_str = m_str
        else:
            m_str = str(message[0])
        for a in m_str:
            try:
                t_str = t_str + str(self.moist_letters[a.lower()])
            except:
                await ctx.send(f'Invalid character in string: {a}')
                continue
        await ctx.send(t_str + '\n' + '- ' + ctx.author.mention)

    @commands.command()
    async def fire(self, ctx: commands.Context, *message):
        t_str = ""
        m_str = ""
        
        if len(message) >1:
            for m in message:
                m_str = m_str + "  " + m 
                m_str = m_str
        else:
            m_str = str(message[0])
        for a in m_str:
            try:
                t_str = t_str + str(self.fire_letters[a.lower()])
            except:
                await ctx.send(f'Invalid character in string: {a}')
                continue
        await ctx.send(t_str[:3999] + '\n' + '- ' + ctx.author.mention)

    @commands.command()
    async def fire2(self, ctx: commands.Context, *message):
        t_str = ""
        m_str = ""
        
        if len(message) >1:
            for m in message:
                m_str = m_str + "  " + m 
                m_str = m_str
        else:
            m_str = str(message[0])
        for a in m_str:
            try:
                t_str = t_str + str(self.fire2_letters[a.lower()])
            except:
                #emoji = await self.emojify(ctx, a)
                
               # t_str = t_str + str(emoji)
                await ctx.send("Jay_ is trying to fix this but it prolly doesnt work. Don't be hatin, check this dumb character you tried to enter: {a}")
                continue
        await ctx.send(t_str + '\n' + '- ' + ctx.author.mention)