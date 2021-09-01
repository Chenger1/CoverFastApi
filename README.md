Try to use FastApi to implement MVC instead of REST API. 

Major handlers return an **html template** using **Jinja2**

But, there are some difficulties with handling form data.
FastApi has **Form** object, but it is not integrated into **Pydantic** validation.

So, we can either do job using common REST API handler. And send data from client using JavaScript, 
or implement pydantic and forms manually - there are examples on github. 
I chose first variant because it seems clearly for me.
