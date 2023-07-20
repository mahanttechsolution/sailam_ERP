from .models import Message

formatstr='{0}: for {1} - {2} {3} is {4} by {5}- {6}'
inventory='{0}: Diamond with StockId {1} is {2} by {3}'
parcel='{0}: {0} With Id:{1} is {2} by {3} '


def saveMessage(type,user,*args,**kwargs):
    if type=='memo':
     mess=formatstr.format(*args)
     if 'changes' in kwargs:
      changes=kwargs.get("changes")
      Message.objects.create(Sender=user,Message=mess,Changes=changes)
     else:
      Message.objects.create(Sender=user,Message=mess)

    elif type=='inventory':
     mess=inventory.format(*args)
     if 'changes' in kwargs:
      changes=kwargs.get("changes")
      Message.objects.create(Sender=user,Message=mess,Changes=changes)
     else:
      Message.objects.create(Sender=user,Message=mess)

    elif type=='parcel':
     mess=parcel.format(*args)
     if 'changes' in kwargs:
      changes=kwargs.get("changes")
      Message.objects.create(Sender=user,Message=mess,Changes=changes)
     else:
      Message.objects.create(Sender=user,Message=mess)