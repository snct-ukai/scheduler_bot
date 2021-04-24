import sys,pymysql.cursors,discord,re,calendar,keys #keys.pyにdiscordのtokenとSQLデータベースの情報を保存

flag=0

conn=pymysql.connect(
    user = keys.USER, #str
    passwd = keys.PW, #str
    host = keys.HOST, #str
    db = keys.DB, #str
    port = keys.PORT, #int
)

cursor = conn.cursor()

def p_exit():
    conn.close()
    sys.exit()

print('successful')

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.author.bot:
        return
    global flag
    if message.content.startswith("s_exit"):
        await message.channel.send("終了します")
        p_exit()
    
    if flag == 0:
        if message.content.startswith("s_add"):
            await message.channel.send("`yy.mm.dd.予定`の形式で予定を送信してください")
            flag = 1
            return
        #if message.content.startswith("s_list"):

    
    if flag == 1:
        ms_list = message.content.split('.',3)

        if ((len(ms_list) != 4) or (ms_list[2] > 12)):
            await message.channel.send("もう一度入力してください")
            return
        if (ms_list[2] == 1 or ms_list[2] == 3 or ms_list[2] == 5 or ms_list[2] == 7 or ms_list[2] == 8 or ms_list[2] == 9 or ms_list[2] == 12) and (ms_list[3] > 31):
            await message.channel.send("もう一度入力してください")
            return
        if (ms_list[2] == 4 or ms_list[2] == 6 or ms_list[2] == 9 or ms_list[2] == 11) and (ms_list[3] > 30):
            await message.channel.send("もう一度入力してください")
            return
        if (calendar.isleap(ms_list[1])):
            if(ms_list[2] == 2) and (ms_list > 29):
                await message.channel.send("もう一度入力してください")
                return
        if (ms_list[2] == 2) and (ms_list > 28):
            await message.channel.send("もう一度入力してください")
            return
        
        channel_id = int(message.channel.id)
        year = int("20" + ms_list[0])
        month = int(ms_list[1])
        day = int(ms_list[2])
        content = ms_list[3]

        sql = "INSERT INTO schedule(id,year,month,day,content)VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql,(channel_id,year,month,day,content))
        conn.commit()
        sort = "select * from schedule order by year,month,day"
        cursor.execute(sort)
        conn.commit()
        await message.channel.send(str(year) + "年" + str(month) + "月" + str(day) + "日" + content + "を追加しました")
        flag = 0
        return

client.run(keys.TK)