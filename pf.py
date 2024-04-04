import secrets
import hmac
import hashlib

def getLimboOutcome(server, client, nonce):
    server = server.encode()
    client = client.encode()
    nonce = str(nonce).encode()
    round = 0
    hash = hmac.new(
        server, 
        client + b':' + nonce + b':' + str(round).encode('utf-8'), 
        hashlib.sha256
    ).digest()
    
    first4 = hash[:4]
    x = 1
    total = 0
    for byt in first4:
        total += int(byt) / (256 ** x)
        x += 1

    total *= 16777216
    outcome = 16777216 / (total + 1) * (1 - 0.01)
    return outcome


server = "1"
client = "1"
nonce = 2
outcome = getLimboOutcome(server, client, nonce)
print(f"server: {server}\nclient: {client}\nnonce: {nonce}\nlimbo outcome: {outcome:.2f}x")