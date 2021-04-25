import sys,pymysql.cursors,discord,re,calendar,datetime,keys #keys.pyにdiscordのtokenとSQLデータベースの情報を保存

flag=0
ms = ""

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
    global ms

    ms = ""
    if message.content.startswith("s_exit"):
        await message.channel.send("終了します")
        p_exit()
    
    if flag == 0:
        if message.content.startswith("s_add"):
            await message.channel.send("`yy.mm.dd.予定`の形式で予定を送信してください")
            flag = 1
            return
        if message.content.startswith("s_list"):
            select = "select * from schedule where id =" + str(message.channel.id)
            cursor.execute(select)
            rows = cursor.fetchall()

            if (len(rows) == 0):
                await message.channel.send("予定はありません")
                return
            
            for row in rows:
                s = str(row).strip("(")
                sche = s.strip(")")
                schedule = sche.split(",",4)
                content = schedule[4].split("'",10)
                ms = ms + str(schedule[1]) + "年" + str(schedule[2]) + "月" + str(schedule[3]) + "日：" + str(content[1]) + "\n"
            await message.channel.send("```" + ms + "```")
    
    if flag == 1:
        ms_list = message.content.split('.',3)

        year = int("20" + ms_list[0])
        month = int(ms_list[1])
        day = int(ms_list[2])
        content = ms_list[3]

        try:
            newDataStr="%04d/%02d/%02d"%(year,month,day)
            datetime.datetime.strptime(newDataStr,"%Y/%m/%d")
        except ValueError:
            await message.channel.send("もう一度入力してください")
            return

        if (len(ms_list) != 4):
            await message.channel.send("もう一度入力してください")
            return
        
        channel_id = int(message.channel.id)

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