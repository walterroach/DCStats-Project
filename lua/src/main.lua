
json = require "json"
dofile("config.lua")


stats_path = paths["stats"]
save_path = paths["savedir"]

dofile(stats_path)

JSON = assert(loadfile "JSON.lua")() -- one-time load of the routines

local stats_json = JSON:encode_pretty(stats) -- "pretty printed" version for human readability

local currentLocalTime= os.date('%Y-%m-%d-%H%M%S')


local filename= "" .. save_path .. "stats_" .. currentLocalTime .. ".json"

file = io.open(filename,"w")
io.output(file)
io.write(stats_json)
io.close(file)
print("Saved SLMod file as JSON at ...")
print(filename)