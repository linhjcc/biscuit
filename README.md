# Biscuit

## Introduction

This project is primarily designed for extending the functionality of Feishu Bitable.
Different extension scripts are developed for different scenarios to provide
more convenient and flexible features for the use of Bitable.    

Our project starts with the Flask framework and the pure frontend development template provided in
[Docs on Multi-dimensional Table Extension Script Development](https://bytedance.feishu.cn/docx/HazFdSHH9ofRGKx8424cwzLlnZc).
With these foundations, we design interactive pages to gather necessary information, including
`personalBaseToken`, `appToken`, `table_id`, and so on, which are further fed to the Flask backend.

Additionally, based on the scaffold provided in
[BaseOpenSDK (Python) Official Documentation](https://bytedance.feishu.cn/wiki/E95iw3QohiOOolkjmXwcVsC5nae),
we develop backend scripts to realize various table manipulation utilities.

## File Hierarchy

- [app.py](./app.py): Flask entrypoint
- [templates/](./templates/): Flask HTML templates
- [static/](./static/): Static resources, including JS scripts, CSS files, icon files, etc.
- [functions/](./functions/): Flask blueprints for extensible utilities

## Get Started with A Line Plot Example

With the line plot extension, we will be able to select two fields from a table for X and Y axes,
draw a line plot using `matplotlib`, and finally upload the result image to the table
as an attachment.

### Resolve Dependencies

TBA

### Run Flask

```bash
FLASK_APP=app.py
flask --debug run --port 8080
```

### Add Extension to a Bitable

The URL will be `http://localhost:8080/insert_picture`.
For more information, please refer to https://bytedance.feishu.cn/docx/HazFdSHH9ofRGKx8424cwzLlnZc.

### Play with the Extension

Run the extension and we will be able to see the embedded page, fill in necessary information,
trigger a draw, and finally witness an image being uploaded.

For more information on attaining information like `personalBaseToken`, please refer to
https://bytedance.feishu.cn/docx/QpMLdHkoporxOHxya5mcxhxln6f.

> [!WARNING]
> An "Attachment" field must exist, which is hard-coded currently.
