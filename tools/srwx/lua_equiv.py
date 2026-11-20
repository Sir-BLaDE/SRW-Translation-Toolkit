import sys
from lupa import LuaRuntime
SER='''
local function ser(v, seen)
  local t=type(v)
  if t=="function" then return "fn" end
  if t~="table" then return tostring(v) end
  local keys={}
  for k in pairs(v) do keys[#keys+1]=k end
  table.sort(keys,function(a,b) return tostring(a)<tostring(b) end)
  local o={}
  for _,k in ipairs(keys) do o[#o+1]=tostring(k).."="..ser(v[k]) end
  return "{"..table.concat(o,",").."}"
end
return function(src)
  local env=setmetatable({},{__index=function(_,k) return k end})
  local f=assert(load(src,"x","t",env))
  f()
  local keys={}
  for k in pairs(env) do keys[#keys+1]=k end
  table.sort(keys)
  local o={}
  for _,k in ipairs(keys) do o[#o+1]=k.."="..ser(env[k]) end
  return table.concat(o,"\\n")
end
'''
lua=LuaRuntime()
run=lua.execute(SER)
def dump(b): return run(b.decode('utf-8'))
if __name__=='__main__':
    a=open(sys.argv[1],'rb').read(); b=open(sys.argv[2],'rb').read()
    print('IGUALES' if dump(a)==dump(b) else 'DISTINTOS')
