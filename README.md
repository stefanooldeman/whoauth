This is a POC for oAuth2.0. For now it covers the following grant flows:
- password (ongoing)

For the token_type the bearer token will be used. Becuase this is now a standard draft.
http://tools.ietf.org/html/draft-ietf-oauth-v2-bearer-22


getting started and run these on cli:

     pip install -r requirements.txt

 then
 
     python run.py

 and test it with cURL

     curl -X POST http://0.0.0.0:5000/auth/access_token -d grant_type=password\&username=stefano\&password=foo\&scope\



Goals and mindset

This is from a provider stand point and I follow the spec from version 31 which will expire February 1, 2013.
It can be found here: http://tools.ietf.org/html/draft-ietf-oauth-v2-31

I will for now only implement what is needed and be pragmatic in writing down my code.
Therefore i'm useing whatever libraries available. So hereby I can onestly say I don't care about:
- creating dependecies and beeing library agnostic
- maintainable code
- tests

I wan't to get this working before someone else has eaten my lunch!


For help (copy pasting)
    https://github.com/idan/oauthlib
    https://developers.google.com/oauthplayground/
    https://github.com/andymccurdy/redis-py
    http://tools.ietf.org/html/draft-ietf-oauth-v2-31
    http://docs.python.org/2/library/index.html
