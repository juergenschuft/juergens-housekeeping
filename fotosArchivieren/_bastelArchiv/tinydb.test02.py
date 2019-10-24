from tinydb import TinyDB, Query

db = TinyDB("picimport.log.json")

db.insert({'sourceFolder': 'GalaxyA5Manja', 'sourceFile': 'img001.jpg', 'targetFile': '2019-10-15'})

File = Query()
file = db.search((File.sourceFolder == 'GalaxyA5Manja') & (File.sourceFile == 'img001.jpg'))

print(file.count)

count = db.count((File.sourceFolder == 'GalaxyA5Manja') & (File.sourceFile == 'img001.jpg'))

print(count)
