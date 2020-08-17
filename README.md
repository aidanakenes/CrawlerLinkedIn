# LinkedIn Profile Crawler
###Structure
 ![alt](https://github.com/aidanakenes/CrawlerLinkedIn/blob/dev/data/project_scheme.png) <br/>
###**API Endpoints:**

####1. GET: ``/linkedin/profile``
Query parameters:<br/>
 **user_id**: _*required_ (linkedin.com/in/**any-user-id**/)<br/>

 **Sample request:** ``GET /linkedin/profile?user_id=anakin-skywalker-4339961b1``<br/>
 **Sample response:** 
 ```
{
    "data": {
        "user_id": "anakin-skywalker-4339961b1",
        "fullname": "Anakin Skywalker",
        "user_url": "https://www.linkedin.com/in/anakin-skywalker-4339961b1",
        "profile_pic_url": "https://media-exp1.licdn.com/dms/image/C4E03AQFTXENc5s8EDw/profile-displayphoto-shrink_800_800/0?e=1603324800&v=beta&t=CxzbjjtXRbDRrDzyWnho_Hv6o0WRDOv29qhDaDmm-cY",
        "location": "United States",
        "heading": "a.k.a Darth Vader:  Welcome to the Dark Side, honey 🖤\n(If you want more power, hate Resistance and love Naboo Senators you are in the right place!)",
        "education": [
            {
                "school": "ALFA FLYING SCHOOL",
                "degree": "Bachelor's degree",
                "start": 2012,
                "end": 2014
            }
        ],
        "experience": [
            {
                "company": "Galactic Republic",
                "position": "Jedi",
                "start": 2015,
                "end": 2016
            },
            {
                "company": "Galaxy",
                "position": "Emperor",
                "start": 2017,
                "end": null
            }
        ],
        "skill": [
            "Costume Design",
            "Political Consulting",
            "Parent Education",
            " Race",
            "Aerospace"
        ]
    }
}
```

####2. GET: ``/linkedin/search``
Query parameters:<br/>
 **fullname**: _*required_ (at least two words)<br/>

 **Sample request:** ``GET /linkedin/search?fullname=anakin%20skywalker``<br/>
 **Sample response:** 
 ```
    "total": 36,
    "data": [
       {
         "user_id": "anakin-skywalker-4339961b1",
         "fullname": "Anakin Skywalker",
          ...
       },
       {
         "user_id": ...,
         "fullname": "Anakin Skywalker",
          ...
       },
       ...
    ]   
```
 
