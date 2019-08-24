# Deployment

Yes, yes, deploying Python app is not as easy as let's j. 

So let me introduce to you **Propel**

I created 



## Deploy to Production

Now your application is ready, it is time to deploy in production.

While there many other options, I'm more familiar with [Propel](deploy.md) and Gunicorn.


- With [Propel](deploy.md)

        propel -w

- On Gunicorn

        gunicorn app_www:app