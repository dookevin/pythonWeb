#utf-8
import diskctl

if diskctl.checkrdinfo() == 100:
    r1=diskctl.getlastrdinfo()
    list=r1.get('subset')
    os.system("mount /dev/%s /mnt/%s"%(diskctl.getdiskname(list[0].get('disk').get('sn')),r1.get('label')))
    input=open("/run/mininas/tmpdiskinfo","w")
    input.write("1")
    input.close()
else:
    input=open("/run/mininas/tmpdiskinfo","w")
    input.write("0")
    input.close()