# whosThat API

This is a POC for oAuth2.0. For now it covers the following grant flows:
- password (ongoing)

For the `token_type` the bearer token will be used. Becuase this is now a standard draft.
http://tools.ietf.org/html/draft-ietf-oauth-v2-bearer-22


## getting started and run these on cli:

installing

     pip install -r requirements.txt

runiing
 
     python run.py

a request  with cURL

     curl -X POST http://0.0.0.0:5000/auth/access_token -d grant_type=password\&username=stefano\&password=foo\&scope\


### Goals and mindset

This is from a provider stand point and I follow the spec from version 31 which will expire February 1, 2013.
It can be found here: http://tools.ietf.org/html/draft-ietf-oauth-v2-31

I will for now only implement what is needed and be pragmatic in writing down my code.
Therefore i'm useing whatever libraries available. So hereby I can onestly say I don't care about:
* creating dependecies and beeing library agnostic
* maintainable code
* tests

bottom line: 
> I wan't to get this working before someone else has eaten my lunch!


---
### Retrospecive on 1 january 2013:

Writing the code has been really trivial and productive. I started out with one file and added creating users and validating their credentials based on oauth protocol.
I've spend around 2 hours a day, which was enough to make big steps. The last 2 times i've worked on this I refactored the file into a different architecture.
This leads to reviewing my previous statement about _maintainable code_. At first I've wrote down everything roughfly and it worked. Mission accomplished. Then later I moved around some code. This means to me: I haven't wasted any time designing, rather I identified the parts in code that can be abstracted and moved it accordingly where necessarily.
What i learned and accomplished:
* Now i've learned how to work with OO python and modules
* scoping in python
* the code seems more decoupled and could in theory be tested as units

New goals:
* wrap up the _"password credentials grant flow"_
* test the flow with a client, after this consider 2 outcomes:
* 1. stick with this flow, which is discouraged by the *Oauth working group* unless you have a trusted relation with the clients. (which could be if I don't make the api public)
* 2. add more grant flows (which would be really nice to accomplish)


For help (copy pasting)
    https://github.com/idan/oauthlib
    https://developers.google.com/oauthplayground/
    https://github.com/andymccurdy/redis-py
    http://tools.ietf.org/html/draft-ietf-oauth-v2-31
    http://docs.python.org/2/library/index.html
