MessageCrypte=""
lg=len(MessageCrypte)
MessageClair=""
cle=14 

for i in range(lg):
    if MessageCrypte[i]==' ':
        MessageClair+=' '
    else:
        asc=ord(MessageCrypte[i])-cle
        MessageClair+=chr(asc+26*((asc<65)-(asc>90)))

print(MessageClair)
