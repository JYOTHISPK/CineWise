region_map = {

    "kerala"            : ["malayalam"],
    "tamil nadu"        : ["tamil"],
    "karnataka"         : ["kannada","konkani","tulu"],
    "andhra pradesh"    : ["telugu"],
    "telangana"         : ["telugu"],
    "maharashtra"       : ["hindi","marathi"],
    "west bengal"       : ["bengali","nepali"],
    "punjab"            : ["punjabi","hindi"],
    "gujarat"           : ["hindi","gujarati"],
    "rajasthan"         : ["rajasthani","hindi"],
    "uttar pradesh"     : ["hindi","bhojpuri"],
    "madhya pradesh"    : ["hindi"],
    "bihar"             : ["hindi","bhojpuri"],
    "delhi"             : ["hindi"],
    "odisha"            : ["odia","hindi"],
    "north east"        : ["assamese","bengali","hindi","nepali"],
    "jammu and kashmir" : ["kashmiri","urdu"],
    "north india"       : ["hindi","sanskrit"],
    "south india"       : ["malayalam","tamil","telugu","kannada","tulu","konkani"]
}


age_map = {

    "teen" : ["comedy","animation","fantasy","sport","adventure","musical"],

    "young_adult" : ["comedy","action","thriller","musical","mystery","war","sport","romance","crime","adventure","horror","sci-fi"],

    "adult" : ["comedy","drama","family","history","biography","news","crime"],

    "senior" : ["comedy","documentary","history","family","drama","music"]
    
}


movie_era_map = {

    "teen" : {

        "after_2000"  : 5,
        "1990_2000"   : 2,
        "1980_1990"   : 0,
        "before_1980" : 0
    },

    "young_adult" : {

        "after_2000"  : 5,
        "1990_2000"   : 5,
        "1980_1990"   : 2,
        "before_1980" : 0
    },

    "adult" : {

        "1990_2000"   : 5,
        "1980_1990"   : 4,
        "after_2000"  : 3,
        "before_1980" : 2
    },

    "senior" : {

        "1980_1990"   : 5,
        "before_1980" : 4,
        "1990_2000"   : 3,
        "after_2000"  : 1
    }

}