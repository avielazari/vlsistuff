Desc = cellDescClass("EDFFX2")
Desc.properties["cell_footprint"] = "edff"
Desc.properties["area"] = "89.812800"
Desc.properties["cell_leakage_power"] = "2306.199600"
Desc.pinOrder = ['CK', 'D', 'E', 'IQ', 'IQN', 'Q', 'QN', 'next']
Desc.add_arc("CK","D","setup_rising")
Desc.add_arc("CK","D","hold_rising")
Desc.add_arc("CK","E","setup_rising")
Desc.add_arc("CK","E","hold_rising")
Desc.add_arc("CK","Q","rising_edge")
Desc.add_arc("CK","QN","rising_edge")
Desc.add_param("area",89.812800);
Desc.add_pin("D","input")
Desc.set_pin_job("CK","clock")
Desc.add_pin("CK","input")
Desc.add_pin("E","input")
Desc.add_pin("Q","output")
Desc.add_pin_func("Q","unknown")
Desc.add_pin("QN","output")
Desc.add_pin_func("QN","unknown")
Desc.add_pin("IQ","output")
Desc.add_pin_func("IQ","unknown")
Desc.add_pin("IQN","output")
Desc.add_pin_func("IQN","unknown")
Desc.add_pin("next","output")
Desc.add_pin_func("next","unknown")
Desc.set_job("flipflop")
CellLib["EDFFX2"]=Desc
