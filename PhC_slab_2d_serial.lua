-- Bottom pane of Fig. 12 in
-- Shanhui Fan and J. D. Joannopoulos,
-- "Analysis of guided resonances in photonic crystal slabs",
-- Phys. Rev. B, Vol. 65, 235112

local start = os.clock()

S4 = S4
S = S4.NewSimulation()
S:SetLattice({1,0}, {0,1})
S:SetNumG(70)
S:AddMaterial("Silicon", {12,0}) -- real and imag parts
S:AddMaterial("Vacuum", {1,0})

S:AddLayer('AirAbove', 0 , 'Vacuum')
S:AddLayer('Slab', 0.5, 'Silicon')
S:SetLayerPatternCircle('Slab', 'Vacuum', {0,0}, 0.1)
S:AddLayerCopy('AirBelow', 0, 'AirAbove')

S:SetExcitationPlanewave(
	{0,0}, -- incidence angles
	{1,0}, -- s-polarization amplitude and phase (in degrees)
	{0,0}) -- p-polarization amplitude and phase

S:UsePolarizationDecomposition()

File = io.open('PhC_T_lua.txt','w')
File:write('Wavelength (um)\tT\n')
for freq=0.25,0.601,0.001 do
	S:SetFrequency(freq)
	local forward1,backward1 = S:GetPoyntingFlux('AirAbove', 0)
	local forward2 = S:GetPoyntingFlux('AirBelow', 0)
    T = math.abs(forward2/forward1)
	-- print (string.format("%.3f",freq) .. '\t' .. string.format("%.6f",T))
    File:write(string.format("%.3f",freq) .. '\t' .. string.format("%.6f",T) .. '\n')
	io.stdout:flush()
end

print(string.format("Elapsed time for serial is %.4f seconds.", (os.clock() - start)))
File:close()