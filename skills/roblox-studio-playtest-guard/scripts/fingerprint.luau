--!strict
-- Prints one line per script: full name, byte length, FNV-1a 32-bit hash.
-- CRLF is read as LF so the output matches fingerprint.py.
-- Run it in each datamodel you check (Edit, Server, Client).

local ROOTS = {
	"Workspace",
	"ReplicatedFirst",
	"ReplicatedStorage",
	"ServerScriptService",
	"ServerStorage",
	"StarterGui",
	"StarterPack",
	"StarterPlayer",
	"Players",
}

local function fnv1a(s: string): number
	local h = 2166136261
	for i = 1, #s do
		h = bit32.bxor(h, string.byte(s, i))
		-- 16777619 = 2^24 + 403; split so the product stays exact in a double.
		h = (bit32.lshift(h, 24) + h * 403) % 4294967296
	end
	return h
end

local lines = {}
for _, serviceName in ROOTS do
	local okService, service = pcall(game.GetService, game, serviceName)
	if okService and service then
		local okList, descendants = pcall(service.GetDescendants, service)
		if okList then
			for _, inst in descendants do
				if inst:IsA("LuaSourceContainer") then
					local okSource, source = pcall(function()
						return (inst :: any).Source :: string
					end)
					if okSource and type(source) == "string" then
						source = string.gsub(source, "\r\n", "\n")
						table.insert(lines, string.format("%s\t%d\t%08x", inst:GetFullName(), #source, fnv1a(source)))
					end
				end
			end
		end
	end
end

table.sort(lines)
local report = table.concat(lines, "\n")
print(report)
return report
