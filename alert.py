import sys,pymysql.cursors,discord,re,datetime,pytz,time,keys,asyncio

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    
    while(True):
        t = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
        wt = (24-t.hour+1)*3600 + t.minute*60
        await asyncio.sleep(wt)
        conn=pymysql.connect(
            user = keys.USER,
            passwd = keys.PW,
            host = keys.HOST,
            db = keys.DB,
            port = keys.PORT,
        )
        cursor = conn.cursor()
        print('successful')
        now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
        sql = "select * from schedule where (year = " + str(now.year) + " and month =" + str(now.month) + " and day =" + str(now.day) + ")"
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            s = str(row).strip("(")
            sche = s.strip(")")
            schedule = sche.split(",",5)
            channel = client.get_channel(int(schedule[0]))
            content = schedule[4].split("'",10)
            await channel.send(content[1])
            d = "delete from schedule where (id =" + str(schedule[0]) + " and year =" + str(schedule[1]) + " and month =" + str(schedule[2]) + " and day =" + str(schedule[3]) + " and content =" + schedule[4] +")"
            cursor.execute(d)
            conn.commit()

        conn.close()

client.run(keys.TK)