# project1
## introduction
In this project, you can select two columns as x-axis and y-axis, and then it will insert a 
line char picture in Attachment.  
## Setup
1. clone the project and run it 
```
git clone https://github.com/linhjcc/biscuit.git/project1
```

2. run the project
```
cd project1
set FLASK_APP=app.py
flask run --host localhost --port 8080
```

3. add scripts to your bitable as extentions according [Docs on Multi-dimensional Table Extension Script Development](https://bytedance.feishu.cn/docx/HazFdSHH9ofRGKx8424cwzLlnZc).  
![example](./static/img_1.png)      

4. enter information needed
* personalBaseToken and appToken according [the page](https://bytedance.feishu.cn/docx/QpMLdHkoporxOHxya5mcxhxln6f)  
* select a table and two columns
* note that there must be a column named Attachment in selected table
