local mp = require( "msgpack" )

local tbl = { a=123, b="Emoji 表情测试\xF0\x9F\x98\x81", c={"中文测试", "日本語テスト",1,2,3} }
local packed = mp.pack(tbl)
local len,ret = mp.unpack(packed)
dump(ret)