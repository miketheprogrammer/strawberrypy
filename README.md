Strawberry Py
---------------

Strawberry Py is a lightweight REST Full API Server. It is fast, efficient, and simple. Thats all.

This version of Strawberry Py also includes my MongoDB Relational Mapper and schema versioner called Mongitude

While both StrawberryPy and Mongitude are far from finished they sport some interesting functionality.





The Request
-----------
Example GET Request

- `http://localhost:8007/users/` GETS all users

	The Response ( this reponse is truncated because it was way too long. Also it has debug enabled so it prints the query data)
	------------
	- `
QUERY :{"_revision_id": "5100489086a955305e447047"}
Params :{"_revision_id": "5100489086a955305e447047"}
 PATH :"/users"



[{"username": "user0", "_revision_id": "5100489086a955305e447047", "name": "surname0, first0", "age": 0, "_id": "5100489386a95530739473bc", "likes": [{"username": "user0", "item": "item0", "is_liked": 1, "_id": "5100489386a95530739473bd", "_revision_id": "5100489086a955305e447048"}, {"username": "user0", "item": "item1", "is_liked": 0, "_id": "5100489386a95530739473be", "_revision_id": "5100489086a955305e447048"}, {"username": "user0", "item": "item2", "is_liked": 0, "_id": "5100489386a95530739473bf", "_revision_id": "5100489086a955305e447048"}, {"username": "user0", "item": "item3", "is_liked": 0, "_id": "5100489386a95530739473c0", "_revision_id": "5100489086a955305e447048"}, {"username": "user0", "item": "item4", "is_liked": 1, "_id": "5100489386a95530739473c1", "_revision_id": "5100489086a955305e447048"}, {"username": "user0", "item": "item5", "is_liked": 0, "_id": "5100489386a95530739473c2", "_revision_id": "5100489086a955305e447048"}, {"username": "user0", "item": "item6", "is_liked": 1, "_id": "5100489386a95530739473c3", "_revision_id": "5100489086a955305e447048"}, {"username": "user0", "item": "item7", "is_liked": 1, "_id": "5100489386a95530739473c4", "_revision_id": "5100489086a955305e447048"}, {"username": "user0", "item": "item8", "is_liked": 1, "_id": "5100489386a95530739473c5", "_revision_id": "5100489086a955305e447048"}, {"username": "user0", "item": "item9", "is_liked": 1, "_id": "5100489386a95530739473c6", "_revision_id": "5100489086a955305e447048"}, {"username": "user0", "item": "item10", "is_liked": 0, "_id": "5100489386a95530739473c7", "_revision_id": "5100489086a955305e447048"}, {"username": "user0", "item": "item11", "is_liked": 1, "_id": "5100489386a95530739473c8", "_revision_id": "5100489086a955305e447048"}, {"username": "user0", "item": "item12", "is_liked": 0, "_id": "5100489386a95530739473c9", "_revision_id": "5100489086a955305e447048"}, {"username": "user0", "item": "item13", "is_liked": 0, "_id": "5100489386a95530739473ca", "_revision_id": "5100489086a955305e447048"}, {"username": "user0", "item": "item14", "is_liked": 0, "_id": "5100489386a95530739473cb", "_revision_id": "5100489086a955305e447048"}, {"username": "user0", "item": "item15", "is_liked": 1, "_id": "5100489386a95530739473cc", "_revision_id": "5100489086a955305e447048"}, {"username": "user0", "item": "item16", "is_liked": 0, "_id": "5100489386a95530739473cd", "_revision_id": "5100489086a955305e447048"}, {"username": "user0", "item": "item17", "is_liked": 1, "_id": "5100489386a95530739473ce", "_revision_id": "5100489086a955305e447048"}, {"username": "user0", "item": "item18", "is_liked": 1, "_id": "5100489386a95530739473cf", "_revision_id": "5100489086a955305e447048"}, {"username": "user0", "item": "item19", "is_liked": 1, "_id": "5100489386a95530739473d0", "_revision_id": "5100489086a955305e447048"}, {"username": "user0", "item": "item20", "is_liked": 1, "_id": "5100489386a95530739473d1", "_revision_id": "5100489086a955305e447048"}, {"username": "user0", "item": "item21", "is_liked": 0, "_id": "5100489386a95530739473d2", "_revision_id": "5100489086a955305e447048"}, {"username": "user0", "item": "item22", "is_liked": 0, "_id": "5100489386a95530739473d3", "_revision_id": "5100489086a955305e447048"}, {"username": "user0", "item": "item23", "is_liked": 0, "_id": "5100489386a95530739473d4", "_revision_id": `

