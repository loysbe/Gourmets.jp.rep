"""

"""

def getAddresses(file_name):
    if file_name == None:
        file_name = './orders_list_YMT.txt'
    f = open(file_name, 'r',encoding='utf-8')
    address = f.readlines()
    f.close()
    return address

user_glogin = 'GourmetsJP'
mdp = 'xxxxxx'
user_yahoo = 'loys_belleguie@yahoo.co.jp'
mdp2 = "xxxxx"

charcuteries_fine_conserves = ['pate-le-delice-25-foie-gras',\
    'coffret-mousse-de-foie-gras-3',\
    'coffret-mousse-de-foie-gras-5',\
    'coffret-mousse-foie-gras-5-promo',\
    'coffret-charcuterie-au-foie-gras',\
    'mousse-de-foie-gras-de-canard-50',\
    'pate-le-delice-25-foie-gras',\
    'rillettes-fg-canard-wake-sale',\
    'rillettes-de-canard-2',\
    'rillettes-de-canard',\
    'kinoko-borde-morilles-25g-vc',\
    'mousse-foie-gras-canard-promo',\
    'rillettes-fg-de-canardx3',\
]

YMT_60 = [    'B085H8J8D4',\
    'coffret-de-3-rillettes-de-canard',\
    'foie-gras-canard-set-1',\
    'kanso-kinoko-borde-otoku-cp',\
    'rillettes-au-foie-gras-de-canard',\
    'kanso-kinoko-borde-cepes-100g',\
    'pate-mousse-rillettes-foie-gras'
    ]

surgeles = ['espn-escalope-foie-gras-4pc',\
    'espn-foie-gras-1er-choix',\
    'espn-escalope-foie-gras-40pc',\
    'espn-escalope-foie-gras-20pc',\
    'espn-cnd-magret',\
    'espn-foie-gras-extra'
    ]