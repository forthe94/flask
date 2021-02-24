from flask import Flask, request, render_template, Markup

app = Flask(__name__)


@app.route('/')
def index():
    # links = []
    # links.append(Markup('<iframe width="560" height="315" src="https://www.youtube.com/embed/5qap5aO4i9A" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'))
    # links.append(Markup('<iframe src="https://player.vimeo.com/video/39880101" width="560" height="315" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe>'))
    return render_template('index2.html')



if __name__ == '__main__':
    app.run(debug=True)
