# Week 2

## Software Design Patterns

Definition from Wikipedia [Design Patterns](https://en.wikipedia.org/wiki/Software_design_pattern) article (my own emphasis added):

> In software engineering, a software design pattern is a ***general reusable solution*** to a ***commonly occurring problem*** within a ***given context*** in software design. It is ***not a finished design*** that can be transformed directly into source or machine code. It is a ***description or template*** for how to solve a problem that can be used in many different situations. Design patterns are ***formalized best practices*** that the programmer can use to solve common problems when designing an application or system.

As you can see in the Wikipedia article, design patterns can be categorized based on the types of problems they solve.

Let's take a look at a few:
- [Builder](https://en.wikipedia.org/wiki/Builder_pattern)
- [Singleton](https://en.wikipedia.org/wiki/Singleton_pattern)
- [Adapter](https://en.wikipedia.org/wiki/Adapter_pattern)
- [Strategy](https://en.wikipedia.org/wiki/Strategy_pattern)
- [Template](https://en.wikipedia.org/wiki/Template_method_pattern)

Remember that these descriptions are formal definitions, not actual solutions. When you work on code in real life, you will find that you have to tweak the patterns to fit your needs.

Let's take a look at a real life example in which I created a program that blends both the Strategy and Template patterns.
- [daoism](https://github.com/gri-is/daoism): This code is used to insert hyperlinks to digitized materials into Finding Aids for the GRI's Special Collections.
- It takes two inputs: The Finding Aid (EAD in XML format) and a CSV file that gives me the links to the digital objects and some element to match against in the Finding Aid.
- But each collection was catalogued differently. Sometimes I can match on a unique ID, sometimes I can match on title. But a single matching algorithm will not work for all collections.
- So I created a method does all of the work of processing the CSV and inserting the links.
- The only piece it does not do is find the matching element in the XML file. For that step, it uses a special method that gets passed to it.
- I created several finder methods. Some are specific to a collection. Some are more generic for collections that have unique IDs in a certain place.
- Thus I have a library of different matching strategies, but they are just methods, not subclasses.
- And I insert those strategies into the bigger template algorithms of processing the list and inserting the links.

## Software Architecture Patterns

OK, now let's look at some higher level concepts. When desiging entire software systems, as opposed to a single program or script, you will find that, again, for similar problems, you will use similar solutions.

Let's take a look at a few common patterns found in web development:
- [Client-Server](https://en.wikipedia.org/wiki/Client%E2%80%93server_model)
- [Multitier](https://en.wikipedia.org/wiki/Multitier_architecture)
- Service Oriented & [Microservices](https://en.wikipedia.org/wiki/Microservices)
- [Model-View-Controller](https://en.wikipedia.org/wiki/Model-View-Controller) & [Model-View-Presenter](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93presenter)

The Model-View-Controller pattern and its variations are the dominating pattern found in most web development frameworks, such as Django (Python), Rails (Ruby), CodeIgniter (PHP), and Angular (JavaScript).

We will spend the next few weeks learning how to use DJango's implementation of the MVC pattern.

## MVC Model Layer

### Object Relational Mapping

Before we dive into Django, we need to discuss [Object-Relational Mapping (ORM)](https://en.wikipedia.org/wiki/Object-relational_mapping). An ORM provides data from a relational database in the format of an OOP object. This enables easier data manipulation by abstracting away SQL commands and providing the data in a format that is consistent with the other types of data structures being used by the programmer.

Python has several ORMs to choose from. The most popular are [SQLAlchemy](https://www.sqlalchemy.org/) and Django's built-in ORM. However, there are some lighter weight Python ORMs that can also be useful for smaller jobs, such as [peewee](docs.peewee-orm.com/) and [PonyORM](https://ponyorm.com/).

### Django Models

OK, let's take a look at the Django ORM. But first, we need to start a project!

How to start a project in Django? Look at [part 1 of the tutorial](https://docs.djangoproject.com/en/1.10/intro/tutorial01/).

#### Django Models Core Topics
- [Basics](https://docs.djangoproject.com/en/1.11/topics/db/models/)
- [Fields](https://docs.djangoproject.com/en/1.11/topics/db/models/#fields)
    - [Relationships](https://docs.djangoproject.com/en/1.11/topics/db/models/#relationships)
    - [Field Options](https://docs.djangoproject.com/en/1.11/ref/models/fields/#field-options)
    - [Field Types](https://docs.djangoproject.com/en/1.11/ref/models/fields/#field-types)
- [Meta options](https://docs.djangoproject.com/en/1.11/topics/db/models/#meta-options)
    - [more details](https://docs.djangoproject.com/en/1.11/ref/models/options/)
- [Model Methods](https://docs.djangoproject.com/en/1.11/topics/db/models/#model-methods)
- [Making Queries](https://docs.djangoproject.com/en/1.11/topics/db/queries/)
- [Migrations](https://docs.djangoproject.com/en/1.11/topics/migrations/)

#### Example Project - Digital Projects Database

Code repo: ([DPDB](https://github.com/gri-is/dpdb))
This is a small Django app for the Digital Services Department at the GRI. I built it based on "back of the napkin" requirements, which have subsequently changed. Therefore I will work on rebuilding it throughout the class as an example.