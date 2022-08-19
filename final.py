
#RC4 

def key(a): #function to convert alphabets into numbers(ASCII code)
    y=[]
    for i in a: #iterating over all letters
        x=ord(i) #finding ASCII code
        y.append(x) #appending into new list
    return(y)

def findt(a): #function makes the an array t with lenght of 256 , using which we can encode 256 bytes of data
    y=key(a)
    t=[]
    j=0
    for i in range(256):
        j=j+1
        t.append(y[i%len(y)]) #repeating elements in list y in order until 256th element.
    return t

def key_schedule(a): #function to perform key_scheduling 
    k=findt(a)
    s=list(range(256)) #making a list s which contains(0,1,2,3,...255)
    j=0
    for i in range(256):
        j=(j+s[i]+k[i%256])%256 #find new value for j over ever iteration 
        x=s[i]
        s[i]=s[j]
        s[j]=x   #swapping elements in s.
    return(s)

def pseudorandom(a,t): #fucntion to perform pseudorandam process
    s=key_schedule(a) #getting s from key_schedule.
    fz=[]
    j=0
    for i in range(len(t)): #iterating over length of the plain text.
        j=(j+s[i])%256  #find new value for j over ever iteration 
        x=s[i]
        s[i]=s[j]
        s[j]=x  #swapping s
        z=s[(s[i] + s[j])%256]
        fz.append(z) #making fz from s which is of length of plain text.
    return(fz)

def encryptor(t,k): #encryption function
    tnum=[] #to store ASCII code
    final=[] #to store encrypted values
    import numpy as np
    for i in range(len(t)): #iterating over t 
        tnum.append(ord(t[i]))#coverting alphabets to numbers (ASCII code)
        num=np.bitwise_xor(tnum[i],k[i]) #encrypting data using key from pseudorandom and performing bitwise xor
        final.append(num) #storing encrypted values
    return(final)

def decryptor(t,k): #decryption function 
    final=[] #to store decrypted msg
    msg=''
    import numpy as np
    for i in range(len(t)):
        num=np.bitwise_xor(t[i],k[i])
        msg=msg+chr(num)
    return msg


    

#Affine ciper

def gcd(a, b): #function to find GCD of numbers
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
    gcd = b
    return gcd, x, y

def modinv(a, m): #funciton to find modular inverse 
    egcd, x, y = gcd(a, m)
    if egcd != 1:
        return None # modular inverse does not exist
    else:
        return x % m 


def affine_encrypt(text, key):# affine cipher encryption function
    x=''
    for t in text:
        x=x+chr((( key[0]*ord(t) + key[1] ) % 300)) #encrypting data with linear function 
    return x



def affine_decrypt(cipher, key):# affine cipher decryption function
    x=''
    for c in cipher:
        x=x+chr((( modinv(key[0],300)*(ord(c) - key[1]))% 300)) #decrypting data using key to find inverse of the function 
    return x
#connecting RC4 and affineciper

def link1(k,key): #link 1 between affine cipher and RC4
    x=''
    for i in k:
        x=x+chr(i)
    e_key=affine_encrypt(x,key) #encrypting RC4 key using affine cipher
    return e_key
def link2(k,key): #link 2 between affine cipher and RC4
    e=affine_decrypt(k,key) #decrypting RC4 key using affine cipher
    d_key=[]
    for i in e:
        d_key.append(ord(i))
    return d_key
    

class messenger: #class to demonstrate the encryption algorithm
    msg=''
    keyr=''
    keya=[]
    def send():
        global msg
        msg=input("Enter Message:")
    def set_RC4key():
        global keyr
        keyr=input("Enter Key:")
    def set_affinekey():
        global keya
        l=[]
        ak=input("Enter key:")
        for i in ak.split(" "):
            l.append(int(i))
        keya=l
    def encrypt():
        global msg
        global keyr
        global keya
        fk=link1(pseudorandom(keyr,msg),keya)
        df=link2(fk,keya)
        code=encryptor(msg,df) 
        print(code)
    def decrypt():
        global msg
        global keyr
        global keya
        fk=link1(pseudorandom(keyr,msg),keya)
        df=link2(fk,keya)
        code=encryptor(msg,df) 
        print(decryptor(code,df))
    def RC4_encryptkey():
        global msg
        global keyr
        print(pseudorandom(keyr,msg))
        
