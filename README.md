# Chesski

Anki style application for practicing and memorizing Chess positions/puzzles.

## Running Application
```
export FLASK_APP=chesski.py  
flask db init 
flask db migrate -m "first migration" 
flask db upgrade 
flask run 
```

## Roadmap
* Add full support for spaced repetition of Chess puzzles
* Add support for multiple users/ability to share positions
* Add support for running application in production environment
* Add fully featured frontend using modern front-end framework.

## Run from Docker
```
docker run -p 8080:8080 image_name/hash
```

# TODO
* Support non-auto queening to support puzzles where promoting to a Queen is incorrect
* Refactor JS
* Add more attractive front end
* Associate puzzles with users/courses
* Fix tests now login is required