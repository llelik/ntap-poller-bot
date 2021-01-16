from hurry.filesize import size
import telebot
from netapp_ontap import config, HostConnection, NetAppRestError
from netapp_ontap.resources import Volume,Cluster

bot = telebot.TeleBot("TOKEN")

@bot.message_handler(commands=["help"])
def print_help(message): 
    bot.send_message(message.chat.id, '/copycat - copies yr message as it was'+'\n'+'/debug - prints yr message in debug JSON output'+'\n'+'/vol_show - prints volume name,size,status from a given SVM'+'\n'+'/vol_perf - prints RW latency of all volumes in a given SVM')

@bot.message_handler(commands=["copycat"])
def repeat_all_messages(message): 
    bot.send_message(message.chat.id, message.text)

@bot.message_handler(commands=["debug"])
def print_debug(message): 
    bot.send_message(message.chat.id, 'Full output was:')
    bot.send_message(message.chat.id, message.text.split()[-1])


@bot.message_handler(commands=["vol_show"])
def print_vols(message):
    try:
        config.CONNECTION = HostConnection('*.*.*.*', username='admin', password='secret', verify=False)
    except NetAppRestError as err:
        bot.send_message(message.chat.id, "Couldn't connect to the appliance. Error was: %s" % err)

    try:
        for volume in Volume.get_collection(**{"svm.name": message.text.split()[-1]}):
            volume.get()
            t = "Name: "+volume.name+ '\n' +"Size: "+size(volume.size)+'\n'+"Status: "+volume.state
            bot.send_message(message.chat.id, t)        

    except NetAppRestError as err:
         bot.send_message(message.chat.id, "Error: Volume list  was not created for SVM %s" % message.text.split()[-1])
        
@bot.message_handler(commands=["vol_perf"])
def print_vol_perf(message):
    try:
        config.CONNECTION = HostConnection('*.*.*.*', username='admin', password='secret', verify=False)
    except NetAppRestError as err:
        bot.send_message(message.chat.id, "Couldn't connect to the appliance. Error was: %s" % err)

    try:
        for volume in Volume.get_collection(**{"svm.name": message.text.split()[-1]}):
            volume.get()
            t = "Name: "+volume.name+ '\n' +"Latency: "+'\n'+"Read: "+str(volume.metric.latency.read)+'\n'+"Write: "+str(volume.metric.latency.write)
            #print(volume.metric.latency.read)

            bot.send_message(message.chat.id, t)        

    except NetAppRestError as err:
         bot.send_message(message.chat.id, "Error: Volume list  was not created for SVM %s" % message.text.split()[-1])

@bot.message_handler(commands=["connect"])
def connect_ntap(message):
    try:
        config.CONNECTION = HostConnection(message.text.split()[-3], username=message.text.split()[-2], password=message.text.split()[-1], verify=False)
        cluster = Cluster()
        cluster.get()
        bot.send_message(message.chat.id, cluster.name)

    except NetAppRestError as err:
        bot.send_message(message.chat.id, "Couldn't connect to the appliance. Error was: %s" % err)

@bot.message_handler(commands=["test_conn"])
def connect_ntap(message):
    try:
        if cluster != None:
           bot.send_message(message.chat.id, cluster.name)
        else:
           bot.send_message(message.chat.id, 'You are not connected to a cluster!') 

    except NetAppRestError as err:
        bot.send_message(message.chat.id, "Couldn't connect to the appliance. Error was: %s" % err)



if __name__ == '__main__':
     bot.infinity_polling()