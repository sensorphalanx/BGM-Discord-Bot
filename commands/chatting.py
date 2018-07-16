import discord
import datetime
import os
import random
from bs4 import BeautifulSoup
import sys 
import aiohttp
import asyncio
import requests 

from send import Command

'''
봇의 간단한 문답 기능을 수록합니다.
단, 간단하게 채팅으로 가능한 명령어는 이곳에 수록합니다. 
{100줄 이상 명령어 또는 특수 기능(게임 등)은 제외}
'''

# def restart_bot():
#     python = sys.executable
#     os.execl(python, python, * sys.argv)

def htmltotext(html):
    soup = BeautifulSoup(html)
    text_parts = soup.findAll(text=True)
    return ''.join(text_parts)

def right_check(a):
    try:
        if a is None or a == "":
            return "정보가 없습니다."

        else:
            return a

    except:
        return "정보를 찾을 수 없습니다."


def lxml_string(soup, tag):
    try:    
        find = soup.find(tag).string
        if find is None or find == "":
            return "정보가 존재하지 않음."
        else:
            return find
    except:
        return "정보 없음."

class chatting(Command):
    
    def __init__(self, *args, **kwargs):
        Command.__init__(self, *args, **kwargs)
        self.bot_start_time = datetime.datetime.now()
        
    async def on_message(self, message):

        if message.content.startswith("봇 온도"):
            try:
                a = os.popen("vcgencmd measure_temp").read()
                a = a.replace("temp=","")
                a = a.replace("'C", "")
                a = a.replace("\n","")
                a = float(a)
                if a < 45:
                    embed=discord.Embed(title="✅ 서버 온도", description="현재 서버 온도는 %s°C 입니다." %(str(a)),color=0x1dc73a )
                    embed.set_footer(text="온도가 좋습니다.")

                if 45 <= a and a<50:
                    embed=discord.Embed(title="⚠ 서버 온도", description="현재 서버 온도는 %s°C 입니다." %(str(a)),color=0xd8ef56)
                    embed.set_footer(text="온도가 보통입니다.")
                if 50 <= a:
                    embed=discord.Embed(title="❌ 서버 온도", description="현재 서버 온도는 %s°C 입니다." %(str(a)),color=0xff0909)
                    embed.set_footer(text="온도가 높습니다.")
                await message.channel.send(embed=embed)
            except:
                embed=discord.Embed(title="⚠ 오류", description="시스템에서 온도를 불러오는데에 실패했습니다.",color=0xff0909)
                await message.channel.send(embed=embed)

        if message.content.startswith("봇 따라해"): 
            if "@everyone" in message.content or "@here" in message.content :
                embed=discord.Embed(title="⚠ 경고", description="`@everyone`이나 `@here`은 다른 사용자에게 피해를 줄 수 있습니다.\n사용이 제한됩니다." ,color=0xff0909 )
                embed.set_footer(text=message.author)
                await message.channel.send(embed=embed)
            else:
                try:
                    await message.delete()
                except:
                    pass
                await message.channel.send(message.content[6:])

        if message.content.startswith("봇 거꾸로"):
            try:
                await message.delete()
            except:
                pass
            
            a = message.content[6:]
            a = ''.join(reversed(a))
            if "@everyone" in a or "@here" in a:
                embed=discord.Embed(title="⚠ 경고", description="`@everyone`이나 `@here`은 다른 사용자에게 피해를 줄 수 있습니다.\n사용이 제한됩니다." ,color=0xff0909 )
                embed.set_footer(text=message.author)
                await message.channel.send(embed=embed)
            else:
                await message.channel.send(a)

        if message.content.startswith("봇 서버랭"):
            rank = {}
            allguild = self.client.guilds
            for i in allguild:
                rank[i] = int(i.member_count)
            rank = sorted(rank, key=lambda k : rank[k], reverse=True)
            number = 0
            totalserver = str(len(allguild))
            totalperson = 0
            embed=discord.Embed(title="서버 랭크", description="서버 이름 / 인원수" , color=0x237ccd)

            for i in rank:
                number += 1
                totalperson += int(i.member_count)
                embed.add_field(name=str(number)+"위", value="%s / %s명" %(i.name, i.member_count),inline=False)

                if number == 10:
                    break                                       
            await message.channel.send(embed=embed)

        if message.content.startswith("봇 업타임"):
            uptime = datetime.datetime.now() - self.bot_start_time
            # days = uptime.day
            # hours = uptime.hour
            # minitues = uptime.minute
            # seconds = uptime.second
            day = uptime.days
            day = str(day)

            uptime = str(uptime)
            uptime = uptime.split(":")

            hours = uptime[0]

            hours = hours.replace(" days,","일")
            hours = hours.replace(" day,","일")

            minitues = uptime[1]

            seconds = uptime[2]
            seconds = seconds.split(".")
            seconds = seconds[0]

            embed=discord.Embed(title="봇 업타임", description="봇이 동작한 시간은  %s시간 %s분 %s초 입니다." %(hours,minitues,seconds) , color=0x237ccd)

            await message.channel.send(embed=embed)


        if message.content.startswith('봇 도움'):
            a = message.content
            a = a[5:]
            if a == "":
                embed=discord.Embed(title=" ", description="봇의 사용을 도와줄 도움말입니다. 다음 명령어 그룹들을 참고하세요.", color=0x237ccd)
                embed.add_field(name="봇 도움 기타", value="기타 도움말입니다. 자세한 명령어는 '봇 도움 기타'을 참고하세요.", inline=False)
                embed.add_field(name="봇 도움 게임", value="봇에 있는 게임 기능에 관련된 도움말입니다. 자세한 명령어는 '봇 도움 게임'을 참고하세요.", inline=True)
                embed.add_field(name="봇 도움 기능", value="봇에 있는 기능에 대해 알려드립니다.", inline=True)
                embed.add_field(name="봇 도움 어드민", value="어드민이 서버 관리를 위해 사용 가능한 기능입니다. 자세한 명령어는 '봇 도움 어드민'을 참고하세요.", inline=True)

                
                embed.set_footer(text="도움 명령어에 없는 명령어가 있을 수 있습니다.")
                try:
                    await message.author.send(embed=embed)
                    await message.channel.send("DM으로 메시지를 보냈습니다. 확인하세요.")
                except:
                    embed=discord.Embed(title="⚠ 주의", description="DM 보내기에 실패하였습니다. 계정에서 DM 설정을 확인해주세요.",color=0xd8ef56)
                    await message.channel.send(embed=embed)
            elif a == "게임":
                embed=discord.Embed(title=" ", description="봇에 있는 채팅 기능을 설명합니다.", color=0x237ccd)
                embed.add_field(name="봇 끝말잇기", value="봇과 끝말잇기를 할 수 있습니다. 제한시간은 10초입니다.", inline=False)
                embed.add_field(name="봇 숫자게임", value="1~10까지 중 랜덤으로 뽑은 숫자에서, 봇보다 숫자가 크면 승리입니다.", inline=True)
                embed.add_field(name="봇 카드게임", value="A ~ K 까지의 카드에서 높은 숫자가 나오면 승리합니다.", inline=True)
                embed.add_field(name="봇 컵게임", value="3개의 컵중에 동전이 들어간 컵을 찾는 게임입니다.", inline=True)
                embed.add_field(name="봇 도박 컵 <배팅금액> <배수>", value="컵게임과 같은 방식입니다. 단, 배수가 늘어날수록 컵의 개수도 그만큼 늘어납니다.", inline=True)

                embed.set_footer(text="도움 명령어에 없는 명령어가 있을 수 있습니다.")
                try:
                    await message.author.send(embed=embed)
                except:
                    embed=discord.Embed(title="⚠ 주의", description="DM 보내기에 실패하였습니다. 계정에서 DM 설정을 확인해주세요.",color=0xd8ef56)
                    await message.channel.send(embed=embed)

            elif a == "기능":
                embed=discord.Embed(title=" ", description="봇에 있는 편리한 기능을 설명합니다.", color=0x237ccd)
                embed.add_field(name="봇 프사 @상대", value="멘션한 상대의 프로필 사진을 가져옵니다. 상대를 지정하지 않으면 자신의 프로필 사진을 가져옵니다.", inline=False)
                embed.add_field(name="봇 백과사전 <검색어>", value="백과사전에서 검색어를 검색해줍니다.", inline=False)
                embed.add_field(name="봇 도서검색 <검색어>", value="도서를 검색해줍니다.", inline=False)
                embed.add_field(name="봇 afk <사유>", value="잠수를 선언합니다. 다시 돌아오면 환영해드립니다.", inline=False)
                embed.add_field(name="봇 한글영어번역(영어한글번역, 일어한글번역, 한글일어번역) <번역할 문장>", value="선택한 언어에서 선택한 언어로 번역해줍니다.", inline=False)
                embed.add_field(name="봇 죽창 <개수>", value="죽창을 표시합니다. 60개가 최대입니다.",inline=False)
                embed.add_field(name="봇 지진", value="지진 정보를 표시합니다.", inline=False)
                embed.add_field(name="봇 별명변경 <바꿀별명>", value="입력한 별명으로 별명을 변경합니다.", inline=False)
                embed.add_field(name="봇 조의 표해", value="봇이 조의를 표해줍니다.", inline=False)
                embed.add_field(name="봇 냥이", value="랜덤으로 고양이짤을 보여준다냐!", inline=False)
                embed.add_field(name="봇 강아지", value="랜덤으로 강아지짤을 보야준다멍.", inline=False)
                embed.add_field(name="봇 원주율 구해", value="원주율을 1997자리 까지 구합니다.", inline=False)
                embed.add_field(name="봇 리마인더 <시간(초)> <사유(선택)>", value="선택한 초 있다가 알려드려요.", inline=False)
            
                embed.add_field(name="봇 기상특보", value="기상특보 정보를 표시합니다.", inline=False)
                embed.add_field(name="봇 미세먼지", value="미세먼지 정보를 표시합니다.", inline=False)
                # embed.add_field(name="봇 11번가 검색 <검색어>", value="11번가에서 검색해, 정보를 불러옵니다.", inline=False)
                embed.add_field(name="봇 명언은?", value="명언을 표시합니다. (명언인지 확인안됨)", inline=False)
                embed.add_field(name="봇 서버 인원은?", value="채팅한 서버의 인원을 표시합니다.", inline=False)

                embed.set_footer(text="도움 명령어에 없는 명령어가 있을 수 있습니다.")
                try:
                    await message.author.send(embed=embed)
                except:
                    embed=discord.Embed(title="⚠ 주의", description="DM 보내기에 실패하였습니다. 계정에서 DM 설정을 확인해주세요.",color=0xd8ef56)
                    await message.channel.send(embed=embed)
            elif a == "어드민":
                embed=discord.Embed(title=" ", description="봇에 있는 서버의 관리자가 사용할때 유용한 기능입니다.", color=0x237ccd)
                embed.add_field(name="봇 킥 @유저", value="선택한 유저를 킥합니다.", inline=False)
                embed.add_field(name="봇 밴 @유저", value="선택한 유저를 밴합니다.", inline=False)
                embed.add_field(name="봇 언밴 @유저 또는 유저 ID ", value="선택한 유저를 언밴합니다. 유저 ID는 데스크톱 버전에서 오른쪽키 > ID복사로 얻으실 수 있습니다.", inline=False)
                embed.add_field(name="봇 뮤트 @유저", value="유저를 해당 채널에서 뮤트시킵니다.", inline=False)
                embed.add_field(name="봇 전체뮤트", value="명령어를 사용한 채널을 관리자 제외 모든 유저가 사용할 수 없도록 합니다.", inline=False)
                embed.add_field(name="봇 언뮤트 @유저", value="유저를 해당 채널에서 언뮤트시킵니다.", inline=False)
                embed.add_field(name="봇 전체언뮤트", value="전체뮤트를 해제합니다.", inline=False)
                embed.add_field(name="봇 커스텀 추가 <명령어>|<봇의 대답>", value="해당 서버만 사용되는 커스텀 명령어를 추가합니다. 명령어와 봇의 대답 구분에는 꼭 |가 필요합니다.", inline=False)
                embed.add_field(name="봇 커스텀 보기", value="해당 서버의 모든 커스텀 명령어를 출력합니다.", inline=False)
                embed.add_field(name="봇 커스텀 삭제 [삭제할 커스텀 명령어]", value="해당 서버의 커스텀 명령어중 입력한 명령어를 삭제합니다.", inline=False)

                embed.set_footer(text="도움 명령어에 없는 명령어가 있을 수 있습니다.")

                try:
                    await message.author.send(embed=embed)
                except:
                    embed=discord.Embed(title="⚠ 주의", description="DM 보내기에 실패하였습니다. 계정에서 DM 설정을 확인해주세요.",color=0xd8ef56)
                    await message.channel.send(embed=embed)
            elif a == "기타":
                embed=discord.Embed(title=" ", description="봇에 있는 다른 잡다한 기능들을 소개합니다.", color=0x237ccd)
                embed.add_field(name="봇 철컹철컹", value="??? : 철컹", inline=False)
                try:
                    await message.author.send(embed=embed)
                except:
                    embed=discord.Embed(title="⚠ 주의", description="DM 보내기에 실패하였습니다. 계정에서 DM 설정을 확인해주세요.",color=0xd8ef56)
                    await message.channel.send(embed=embed)
            
            else:
                embed=discord.Embed(title="⚠ 주의", description="해당 도움 그룹이 없습니다. 존재하는 도움 그룹은 \n```기타, 게임, 기능, 어드민``` 입니다.",color=0xd8ef56)
                await message.channel.send(embed=embed)

        if message.content.startswith('봇 안녕') or message.content.startswith('봇 안냥') or message.content.startswith("봇 ㅎㅇ") or message.content.startswith("봇 gd") or message.content.startswith("봇 hello"):
            a = self.client.user.id
            bot_profile = self.client.get_user(a).avatar_url

            embed = discord.Embed(title="👋 안녕하세요!", description="**봇을 사용해 주셔서 감사합니다!**\n봇 / BOT은 BGM#0970이 개발중인 디스코드 봇입니다.\n\n자세한 내용은 `봇 도움` 명령어를 사용해주세요." ,color=0x237ccd)
            embed.set_thumbnail(url=bot_profile)
            await message.channel.send(embed=embed)


        if message.content.startswith('봇 별명변경'):
            try:
                a = message.content
                a = a[6:]
                b = a.lstrip()
                memberid = message.author.id
                member = message.guild.get_member(memberid)

                await member.edit(nick=b)
                embed=discord.Embed(title="✅ 별명 변경", description="별명 변경에 성공하였습니다.",color=0x1dc73a )

                await message.channel.send(embed=embed)
            except:
                embed=discord.Embed(title="❌ 오류 발생", description="봇의 권한이 부족하거나 사용자의 권한이 봇보다 높습니다.",color=0xff0909)
                await message.channel.send(embed=embed)

        if message.content.startswith('봇 별명 초기화'):
            try:
                memberid = message.author.id
                member = message.guild.get_member(memberid)
                await member.edit(nick=None)
                embed=discord.Embed(title="✅ 별명 변경", description="별명 초기화에 성공하였습니다.",color=0x1dc73a )

                await message.channel.send(embed=embed)
            except:
                embed=discord.Embed(title="❌ 오류 발생", description="봇의 권한이 부족하거나 사용자의 권한이 봇보다 높습니다.",color=0xff0909)
                await message.channel.send(embed=embed)


        if message.content.startswith("봇 시간계산"):
            try:
                if not message.content[6:] == "":
                    answer = message.content[6:].lstrip()
                else:
                    embed=discord.Embed(title="봇 시간계산", description="yyyy-mm-dd 형식으로 입력해주세요.",color=0x237ccd)
                    await message.channel.send(embed=embed)
                    def usercheck(a):
                        return a.author == message.author

                    answer = await self.client.wait_for('message', check=usercheck)
                    answer = answer.content
                now = datetime.datetime.now()
                answer = datetime.datetime.strptime(answer, "%Y-%m-%d")
                dap = answer - now
                print(dap)
                days = dap.days
                hours, remainder = divmod(dap.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                # 초 (실험)
                seconds += dap.microseconds / 1e6      
                embed=discord.Embed(title="⏲ 시간 계산", description=str(days) + "일 " + str(hours) + "시간 " + str(minutes) + "분 " + str(int(round(seconds,0))) + "초 남았습니다.",color=0x237ccd)
                embed.set_footer(text="과거 시간은 계산값이 정확하지 않습니다.")
        
                await message.channel.send(embed=embed )
            except Exception as error:
                embed=discord.Embed(title="❌ 오류 발생", description="형식을 제대로 입력하셨는지 학인하시거나, 값 한도를 초과했는지 확인해주세요.. \n\n0001-01-01 ~ 9999-12-31 %s" %(error),color=0xff0909 )
                await message.channel.send(embed=embed)



        if message.content.startswith("봇 핑"):
            nowasdf = datetime.datetime.now()
            await message.channel.trigger_typing()
            latertime = datetime.datetime.now()            
            ping = latertime - nowasdf

            asdf = str(int(ping.microseconds) / 1000)
            asdf = asdf.split(".")
            asdf = asdf[0]
            embed=discord.Embed(title="🏓 퐁! " + asdf+"ms", description=str(ping.microseconds) + "μs", color=0x237ccd)
            embed.set_footer(text="이 수치는 봇이 메시지에 반응하는 속도입니다.")
            await  message.channel.send(embed=embed)
            
        if message.content.startswith("봇 퐁"):
            nowasdf = datetime.datetime.now()
            await message.channel.trigger_typing()
            latertime = datetime.datetime.now()            
            ping = latertime - nowasdf

            asdf = str(int(ping.microseconds) / 1000)
            asdf = asdf.split(".")
            asdf = asdf[0]
            embed=discord.Embed(title="🏓 핑! " + asdf+"ms", description=str(ping.microseconds) + "μs", color=0x237ccd)
            embed.set_footer(text="이 수치는 봇이 메시지에 반응하는 속도입니다.")
            await message.channel.send(embed=embed)
            
        if message.content.startswith("봇 리마인더"):
            a = message.content[6:]
            a = a.lstrip()
            a = a.split()
            try:
                set_time = int(a[0])
                try:  
                    del a[0]
                    reason = ""
                    for i in a:
                        reason = reason + i + " "
                    if not reason == "":
                        embed=discord.Embed(title="✅ 리마인더", description="리마인더에 기록 완료했어요! %s초 있다가 `%s`하라고 알려드릴께요!" %(str(set_time), reason),color=0x1dc73a )
                    else:
                        embed=discord.Embed(title="✅ 리마인더", description="리마인더에 기록 완료했어요! %s초 있다가 알려드릴께요!" %(str(set_time)),color=0x1dc73a )
            
                except IndexError as error:
                    await message.channel.send(error)
                embed.set_footer(text="봇이 꺼지면 초기화됩니다. 유의하여 주십시오.")
                await message.channel.send(embed=embed)
                await asyncio.sleep(set_time)
                await message.channel.send(message.author.mention)
                embed=discord.Embed(title="⏰ 알림", description="시간이 다 되었어요!" ,color=0x1dc73a )
                if not reason == "":
                    embed.add_field(name="내용", value=reason)
                await message.channel.send(embed=embed)

                
            except Exception as error:
                embed=discord.Embed(title="⚠ 오류 발생", description="봇 리마인더 <시간(초)> <사유(선택)> 형식으로 사용해주세요. \n```%s```     "%(error) ,color=0xff0909)    
                await message.channel.send(embed=embed)


        if message.content.startswith('봇 히오스는?'): 
            choice = ["hos.PNG", "hosjongnews.PNG", "hosmang.PNG", "wehatehos.PNG"]
            await message.channel.send(file=discord.File(random.choice(choice)))

        if message.content == ("봇 시공"):
            response = ["**싫음**","너나 해 이 악마야","`봇 시공은?` 계속 쳐봐!","시공이 재밌냐?","싫음.","시 공 시 렁"]
            response = random.choice(response)
            await message.channel.send(response)

        if message.content == ("봇 시공은?"):
            response = ["**싫음**","너나 해 이 악마야","`봇 히오스는?` 계속 쳐봐!","시공이 재밌냐?","싫음.","시 공 시 렁"]
            response = random.choice(response)
            await message.channel.send(response)

        if message.content.endswith("봇 조의 표해"):
            await message.add_reaction("❌")
            await message.add_reaction("✖")
            await message.add_reaction("🇽")
            await message.add_reaction("🇯")
            await message.add_reaction("🇴")
            await message.add_reaction("🇾")

        if message.content == ("봇 지진"):
            async with aiohttp.ClientSession() as session:
                async with session.get("http://m.kma.go.kr/m/risk/risk_03.jsp#") as r:

                    c = await r.text()
                    soup = BeautifulSoup(c,"html.parser")
                    all = soup.find_all("div",{"id":"div_0"})
                    a = right_check(all[0].find_all("td",{"class":"tal pad2"})[0].text)
                    b = right_check(all[0].find_all("td",{"class":"tal pad2"})[1].text)
                    c = right_check(all[0].find_all("td",{"class":"tal pad2"})[2].text)
                    d = right_check(all[0].find_all("td",{"class":"tal pad2"})[3].text)
                    e = right_check(all[0].find_all("td",{"class":"tal pad2"})[4].text)
                    f = right_check(all[0].find_all("td",{"class":"tal pad2"})[5].text)
                
                    embed=discord.Embed(title="지진 정보", description=a,color=0x62bf42)
                    try:
                        img = all[0].find_all("img")[0]['src']
                        img = "http://m.kma.go.kr" + img
                        if img is None: pass
                        else: embed.set_image(url=img)



                    except:
                        pass

                    embed.add_field(name="규모", value=b, inline=True)
                    embed.add_field(name="발생위치", value=c, inline=True)
                    embed.add_field(name="발생깊이", value=d, inline=True)
                    embed.add_field(name="진도", value=e, inline=True)
                    embed.add_field(name="참고사항", value=f, inline=True)
                    embed.set_footer(text="기상청")


                    await message.channel.send(embed=embed)

        if message.content.startswith("봇 골라"):
            if "@everyone" in message.content or "@here" in message.content:
                embed=discord.Embed(title="⚠ 경고", description="`@everyone`이나 `@here`은 다른 사용자에게 피해를 줄 수 있습니다.\n사용이 제한됩니다." ,color=0xff0909 )
                embed.set_footer(text=message.author)
                await message.channdddel.send(embed=embed)
            else:
                a = message.content
                a = a[4:]
                a = a.lstrip().split(",")
                a = random.choice(a)
                embed=discord.Embed(title="❔봇의 선택", description=a,color=0x1dc73a )
                await message.channel.send(embed=embed)

        if message.content.startswith("봇 기상특보"):
            async with aiohttp.ClientSession() as session:
                async with session.get('http://newsky2.kma.go.kr/service/WetherSpcnwsInfoService/WeatherWarningItem?serviceKey=wRI0WBBRTbujkmovOf%2FhZ%2F2gYfki7qlPzuGkLogwp04bnPPE1CU9kGTf3VjnA%2FdGT8Q66Dv8f9eP7zpatOLsyQ%3D%3D') as r:
                    c = await r.text()
                    soup = BeautifulSoup(c,"lxml-xml")
                    title = lxml_string(soup, "t1")
                    area = lxml_string(soup, "t2")
                    content = lxml_string(soup, "t4")
                    now = lxml_string(soup, "t6")
                    will = lxml_string(soup, "t7")
                    cham = lxml_string(soup, "other")

                    embed=discord.Embed(title="🌥 기상특보", description="현재 기준 기상특보 입니다.",color=0x62bf42)
                    
                    embed.add_field(name="현재 특보 제목", value=title)
                    embed.add_field(name="발효 지역", value=area)
                    embed.add_field(name="내용", value=content)
                    embed.add_field(name="특보 현황 내용", value=now)


                    embed.add_field(name="예비특보", value=will)
                    embed.set_footer(text="기상청")

                    await message.channel.send(embed=embed)


        if message.content.startswith("봇 뽑기"):

            embed=discord.Embed(title="🔄 유저 불러오는 중", description="온라인 유저를 불러옵니다.",color=0x1dc73a )
            await message.channel.send(embed=embed)
            online = []
            for i in message.guild.members:
                if i.status == discord.Status.offline:
                    pass
                else:
                    online.append(i.id)

            embed=discord.Embed(title="✅ 뽑기 성공", description="<@%s>님 당첨!" %(str(random.choice(online))),color=0x1dc73a )

            await message.channel.send(embed=embed)


#💨

        if message.content.startswith("봇 미세먼지"):
            async with aiohttp.ClientSession() as session:
                async with session.get('http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnMesureLIst?serviceKey=wRI0WBBRTbujkmovOf%2FhZ%2F2gYfki7qlPzuGkLogwp04bnPPE1CU9kGTf3VjnA%2FdGT8Q66Dv8f9eP7zpatOLsyQ%3D%3D&numOfRows=1&pageSize=1&pageNo=1&startPage=1&itemCode=PM10&dataGubun=HOUR') as r:
                    c = await r.text()
                    
                    soup = BeautifulSoup(c,"lxml-xml")
                    datatime = lxml_string(soup, "dataTime")
                    seoul = lxml_string(soup, "seoul")
                    busan = lxml_string(soup, "busan")
                    daegu = lxml_string(soup, "daegu")
                    incheon = lxml_string(soup, "incheon")
                    gwangju = lxml_string(soup, "gwangju")
                    daejon = lxml_string(soup, "daejeon")
                    ulsan = lxml_string(soup, "ulsan")
                    gyeonggi = lxml_string(soup, "gyeonggi")
                    gangwon = lxml_string(soup, "gangwon")
                    chungbuk = lxml_string(soup, "chungbuk")
                    chungnam = lxml_string(soup, "chungnam")
                    jeonbuk = lxml_string(soup, "jeonbuk")
                    jeonnam = lxml_string(soup, "jeonnam")
                    gyeongbuk = lxml_string(soup, "gyeongbuk")
                    gyeongnam = lxml_string(soup, "gyeongnam")
                    jeju = lxml_string(soup, "jeju")
                    sejong = lxml_string(soup, "sejong")
                    sido = {"서울" : seoul, "부산" : busan, "대구":daegu, "인천":incheon, "광주":gwangju, "대전":daejon, "울산":ulsan, "경기":gyeonggi, "강원": gangwon, "충북": chungbuk, "충남":chungnam, "전북":jeonbuk, "전남" : jeonnam, "경북" : gyeongbuk, "경남" : gyeongnam, "제주":jeju, "세종": sejong}
                    embed=discord.Embed(title="💨 PM10 미세먼지 농도", description=datatime + " 기준", color=0x1dc73a )
                    embed.set_footer(text="에어코리아")
                    name = message.content[6:].lstrip()
                    if name == "":
                        for i in sido.keys():
                            embed.add_field(name=i, value=str(sido[i]), inline=True)
                        await message.channel.send(embed=embed)
                    else:
                        if name in sido.keys():
                            embed.add_field(name=name, value=str(sido[name]), inline=True)
                            await message.channel.send(embed=embed)
                        else:
                            embed=discord.Embed(title="⚠ 주의", description="지역 이름이 없습니다. 광역자치단체 기준으로 불러오며, 도는 줄인 이름으로, 광역시는 `광역시` 글자를 제거해주세요.\n\n```ex) 경북, 경기, 서울, 광주...```",color=0xd8ef56)
                            await message.channel.send(embed=embed)

        if message.content.startswith("봇 초미세먼지"):
            async with aiohttp.ClientSession() as session:
                async with session.get('http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnMesureLIst?serviceKey=wRI0WBBRTbujkmovOf%2FhZ%2F2gYfki7qlPzuGkLogwp04bnPPE1CU9kGTf3VjnA%2FdGT8Q66Dv8f9eP7zpatOLsyQ%3D%3D&numOfRows=1&pageSize=1&pageNo=1&startPage=1&itemCode=PM25&dataGubun=HOUR') as r:
                    c = await r.text()
                    
                    soup = BeautifulSoup(c,"lxml-xml")
                    datatime = lxml_string(soup, "dataTime")
                    seoul = lxml_string(soup, "seoul")
                    busan = lxml_string(soup, "busan")
                    daegu = lxml_string(soup, "daegu")
                    incheon = lxml_string(soup, "incheon")
                    gwangju = lxml_string(soup, "gwangju")
                    daejon = lxml_string(soup, "daejeon")
                    ulsan = lxml_string(soup, "ulsan")
                    gyeonggi = lxml_string(soup, "gyeonggi")
                    gangwon = lxml_string(soup, "gangwon")
                    chungbuk = lxml_string(soup, "chungbuk")
                    chungnam = lxml_string(soup, "chungnam")
                    jeonbuk = lxml_string(soup, "jeonbuk")
                    jeonnam = lxml_string(soup, "jeonnam")
                    gyeongbuk = lxml_string(soup, "gyeongbuk")
                    gyeongnam = lxml_string(soup, "gyeongnam")
                    jeju = lxml_string(soup, "jeju")
                    sejong = lxml_string(soup, "sejong")
                    sido = {"서울" : seoul, "부산" : busan, "대구":daegu, "인천":incheon, "광주":gwangju, "대전":daejon, "울산":ulsan, "경기":gyeonggi, "강원": gangwon, "충북": chungbuk, "충남":chungnam, "전북":jeonbuk, "전남" : jeonnam, "경북" : gyeongbuk, "경남" : gyeongnam, "제주":jeju, "세종": sejong}
                    embed=discord.Embed(title="💨 PM2.5 초미세먼지 농도", description=datatime + " 기준", color=0x1dc73a )
                    embed.set_footer(text="에어코리아")
                    name = message.content[7:].lstrip()
                    if name == "":
                        for i in sido.keys():
                            embed.add_field(name=i, value=str(sido[i]), inline=True)
                        await message.channel.send(embed=embed)
                    else:
                        if name in sido.keys():
                            embed.add_field(name=name, value=str(sido[name]), inline=True)
                            await message.channel.send(embed=embed)
                        else:
                            embed=discord.Embed(title="⚠ 주의", description="지역 이름이 없습니다. 광역자치단체 기준으로 불러오며, 도는 줄인 이름으로, 광역시는 `광역시` 글자를 제거해주세요.\n\n```ex) 경북, 경기, 서울, 광주...```",color=0xd8ef56)
                            await message.channel.send(embed=embed)


        # if message.content.startswith('봇 재시작'):
        #     if message.author.id == 289729741387202560:

        #         try:
        #             embed=discord.Embed(title="봇 재시작", description="봇이 재시작 합니다.",color=0x237ccd )
        #             await message.channel.send(embed=embed)
        #             restart_bot()
        #         except Exception as error :
        #             embed=discord.Embed(title="❌ 경고", description="재시작 중 오류가 발생하였습니다. %s" %(error),color=0xff0909)
        #             await message.channel.send(embed=embed)
        #     else:
        #         embed=discord.Embed(title="⚠ 주의", description="봇 오너만 사용 가능한 명령어입니다.",color=0xd8ef56)
        #         await message.channel.send(embed=embed)


        