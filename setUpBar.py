class setUpBar(object):
  x = 30
  length = 400
  height = 20
  t = None

  def __init__(self, y):
    self.y = y
  
  def mousePressed(self, event):
    if self.x < event.x < self.x + self.length and self.y < event.y < self.y + self.height:
      return (event.x - self.x) / self.length
    else:
      return None
  
  def drawBar(self, canvas, points, duration, initColor, dir):
    canvas.create_text(self.x + self.length + 15 ,self.y + self.height / 2, text=dir, font="Arial 18", fill="blue")
    canvas.create_rectangle(self.x, self.y, self.x +
     self.length, self.y + self.height, fill = 'blue')

    lastPoint = self.x
    for point in points:
      pointX = (point / duration) * self.length + self.x
      canvas.create_rectangle(lastPoint, self.y, pointX, self.y + self.height, fill = initColor)
      canvas.create_rectangle(pointX - 5, self.y, pointX + 
      5, self.y + self.height, fill = 'white')
      lastPoint = pointX + 5
      if initColor == "red":
        initColor = "green"
      else:
        initColor = "red"
    canvas.create_rectangle(lastPoint, self.y, self.x + self.length, self.y + self.height, fill = initColor)

    if self.t is not None:
      timeX = (self.t / duration) * self.length + self.x
      canvas.create_rectangle(timeX - 2, self.y, timeX + 5, self.y + self.height, fill = "blue")

    