
from flask import Flask, jsonify, abort, request, make_response, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return """
<!DOCTYPE html>
<head>
   <title>Flask Rest API by Eduardo Migueis</title>
   <style>
   @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP&family=Roboto&display=swap');
   body{
       overflow: hidden;
       font-family: 'Roboto', sans-serif;
   }
   .background{
       position: absolute;
       top: 0;
       left: 0;
       width: 100%;
       z-index: -2;
   }
   .background img{
       object-fit: contain;
       min-height: 100%;
       max-width: 110%;
   }
   .content{
       display: flex;
       flex-wrap: wrap;
       align-items: center;
       justify-content: center;
       margin: 100px auto;
       max-width: 450px;
   }
   .content h1{
       width: 100%;
       text-align: center;
       font-size: 2.5rem;
       color: #1d1d1d;
       margin-bottom: 50px;
   }
td {
    padding: 5px;
    color: #495057;
    background-color: #fefefe;
    padding: .75rem;
    vertical-align: top;
    border-top: 1px solid #dee2e6;
}
th{

    color: #fff;
    background-color: #212529;
    border-color: #32383e;
    padding: .75rem;
    vertical-align: top;
}
table {
    border-collapse: collapse;
    border-spacing: 0px;
}
@media only screen and (max-width: 700px){
    .background img{
       object-fit: contain;
       height: 100%;
   }
}
   </style>
</head>

<body style="width: 880px; margin: auto;">  
    <div class="content">
<h1>Simple Flask Rest API</h1>
    <table>
  <colgroup>
    <col class="column1">
    <col class="columns2plus3" span="2">
  </colgroup>
  <tr>
    <th>Index</th>
    <th>Route</th>
    <th>Method</th>
    <th>Description</th>
  </tr>
  <tr>
  <td>1</td>
    <td>/api/tasks</td>
    <td>GET</td>
    <td>Get all tasks</td>
  </tr>
  <tr>
  <td>2</td>
    <td>/api/task/:code</td>
    <td>GET</td>
    <td>Get one task</td>
  </tr>
  <tr>
  <td>3</td>
    <td>/api/task</td>
    <td>POST</td>
    <td>Add one task</td>
  </tr>
  <tr>
  <td>4</td>
    <td>/api/task/:code</td>
    <td>PUT</td>
    <td>Edit one task</td>
  </tr>
  <tr>
  <td>5</td>
    <td>/api/task/:code</td>
    <td>DELETE</td>
    <td>Delete one task</td>
  </tr>
</table>
    </div>
    <div class="background">
        <img src="https://s3.eu-central-1.wasabisys.com/devonilx7/2020/04/swirls-abstract-4k-hd-wallpaper-scaled.jpg" />
    </div>
</body>
"""


tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    },
    {
        'id': 3,
        'title': u'Hey, go medidate',
        'description': u'Need to find a great meditation app',
        'done': False
    }
]


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})


@app.route('/api/task/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})


@app.route('/api/task', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201


@app.route('/api/task/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != str:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not str:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get(
        'description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})


@app.route('/api/task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})


if __name__ == '__main__':
    app.run(debug=True)
