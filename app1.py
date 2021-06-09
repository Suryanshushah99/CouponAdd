from flask import Flask,jsonify,request

app=Flask(__name__)

stores=[
{
    "name":"ram",
    "items":[{
        "name":"item",
        "price":12
    }]
}
]

@app.route("/")
def home():
	return "hello"

@app.route("/store")
def get_stores():
	return jsonify({'stores': stores})

@app.route('/store',methods=['POST'])
def create_store():
    request_data=request.get_json()
    new_store={
        "name":request_data["name"],
        "items":[]
    }
    stores.append(new_store)
    return jsonify({'stores': stores})



@app.route("/store/<name>", methods=['DELETE'])
def delete_store(name):
	for store in stores:
		if store["name"]==name:
			del store
			return "done"
	return "error"

@app.route("/store/<name>", methods=['PUT'])
def put_store(name):
	request_data=request.get_json()
	for store in stores:
		if store["name"]==name:
			store.update({"name":request_data["name"]})
			return "done"
	return "Error"


	


app.run(port=5000)