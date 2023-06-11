from level import *
from cmu_112_graphics import *
import time

def redrawAll(app, canvas):
  canvas.create_text(270, 680, font="Arial 10", text="click on bar to set time at which traffic lights change color "+str(app.level.passedCar() - app.level.penalty))
  app.level.drawCrossroad(canvas)
  canvas.create_text(100, 50, font="Arial 15", text="passed: "+str(app.level.passedCar() - app.level.penalty))
  canvas.create_text(100, 80, font="Arial 15", text="best: "+str(app.level.highestPassed - app.level.penalty))
  if app.level.startSimulation:
    curTime = time.time() - app.startTime
    if curTime > app.level.duration:
      app.level.startSimulation = False
      app.level.clearCars()
      app.level.penalty = 0
      return None
    else:
      for key in app.level.allCars:
        for car in app.level.allCars[key]:
          car.drawCar(canvas)
  
      for key in app.level.trafficLights:
        light = app.level.trafficLights[key]
        light.updateLight(curTime)
        light.drawLight(canvas)
  # pre simulation setup
  else:
    for key in app.level.trafficLights:
      app.level.trafficLights[key].drawLight(canvas)

def mousePressed(app, event):
  if app.level.startSimulation:
    pass
  else:
    app.level.mousePressed(event)

def appStarted(app):
  app.level = level(100, 40)
  app.timerDelay = 10
  app.addCarInterval = app.level.addCarInterval
  app.timeCount = 0

def keyPressed(app, event):
  if event.key == "s":
    app.level.startSimulation = True
    app.startTime = time.time()

def timerFired(app):
  if app.level.startSimulation:
    app.level.checkCars()
    app.timeCount += 2
    if app.timeCount == app.level.addCarInterval:
      app.level.addCar()
      app.timeCount = 0
    for carListKey in app.level.allCars:
      for car in app.level.allCars[carListKey]:
        car.move()
      
runApp(width = 500, height = 700)


